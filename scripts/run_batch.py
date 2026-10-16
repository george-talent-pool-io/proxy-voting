"""Immutable run manifests, resumable failures and exact-input reproduction."""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import time
import uuid
import tarfile
from importlib.metadata import version
from pathlib import Path
import numpy as np
import psutil
from apps.api.store import connect,initialise,dumps,now
from classifier.laya_classifier import LayaClassifier,load_config,config_version,prepare_config
from classifier.preprocessing import normalise,source_hash

def run_batch(path=None,config=None,reproduce=None,resume=None,limit=None,classifier_factory=LayaClassifier):
    initialise(path)
    cfg=config or load_config()
    with connect(path) as c:
        if reproduce:
            old=c.execute('SELECT * FROM runs WHERE id=?',(reproduce,)).fetchone()
            if not old:raise ValueError('Unknown reproduction run')
            cfg=prepare_config(json.loads(old['config']))
            rows=c.execute('SELECT n.* FROM notices n JOIN run_inputs i ON i.record_id=n.id WHERE i.run_id=? ORDER BY n.id',(reproduce,)).fetchall()
        elif resume:
            old=c.execute('SELECT * FROM runs WHERE id=?',(resume,)).fetchone()
            if not old:raise ValueError('Unknown resume run')
            cfg=prepare_config(json.loads(old['config']))
            rows=c.execute('SELECT n.* FROM notices n JOIN run_inputs i ON i.record_id=n.id WHERE i.run_id=? ORDER BY n.id',(resume,)).fetchall()
        else:
            rows=c.execute('SELECT * FROM notices ORDER BY id').fetchall()
            if limit:rows=rows[:limit]
        if not rows:raise ValueError('No imported notices')
        inputs=[{'id':r['id'],'source_hash':r['source_hash']} for r in rows]
        dataset_hash=hashlib.sha256(dumps(inputs).encode()).hexdigest()
        run_id=resume or str(uuid.uuid4())
        manifest={'inputs':len(inputs),'reproduces':reproduce,'python':platform.python_version(),'platform':platform.platform(),
            'code_revision':subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
            'code_dirty':bool(subprocess.run(['git','status','--porcelain'],capture_output=True,text=True).stdout.strip()),
            'source_fingerprint':source_fingerprint(),'package_versions':{k:version(k) for k in ['laya','torch','transformers','numpy']},'hardware':platform.machine(),'timing':'amortised inference batch time; not online request latency'}
        if not resume:
            c.execute('INSERT INTO runs(id,created_at,status,model,model_version,config,config_version,dataset_hash,manifest) VALUES (?,?,?,?,?,?,?,?,?)',
                (run_id,now(),'RUNNING',f'{cfg["checkpoint"]}/{cfg["subfolder"]}',cfg['checkpoint_revision'],json.dumps(cfg,ensure_ascii=False,allow_nan=False),config_version(cfg),dataset_hash,dumps(manifest)))
            c.executemany('INSERT INTO run_inputs VALUES (?,?,?)',[(run_id,r['id'],r['source_hash']) for r in rows])
        else:
            c.execute("UPDATE runs SET status='RUNNING' WHERE id=?",(run_id,))
        done={r['record_id'] for r in c.execute('SELECT record_id FROM predictions WHERE run_id=?',(run_id,))}
    if not resume:
        folder=Path('data/run_sources');folder.mkdir(exist_ok=True,parents=True)
        with tarfile.open(folder/(run_id+'.tar.gz'),'w:gz') as archive:
            for root in ['apps/api','classifier','training','evaluation','scripts']:
                for p in sorted(Path(root).glob('*.py')):archive.add(p)
            for p in ['uv.lock','pyproject.toml','classifier/config.json']:archive.add(p)
    print(f'RUN {run_id} / {len(rows)} source rows / {len(done)} already persisted',flush=True)
    start=time.perf_counter(); latencies=[]; batches=[]; peak=psutil.Process().memory_info().rss; failures=0; cached=0
    cache={}
    try:
        model=classifier_factory(cfg)
        pending=[r for r in rows if r['id'] not in done]
        # Classify each unique normalised source once; preserve a prediction for every input row.
        groups={}
        for r in pending:groups.setdefault(source_hash(normalise(r['text'])),[]).append(r)
        unique=list(groups.items())
        for offset in range(0,len(unique),cfg['batch_size']):
            chunk=unique[offset:offset+cfg['batch_size']]
            batch_start=time.perf_counter()
            try:
                results=model.classify_batch([g[0]['text'] for h,g in chunk])
                if len(results)!=len(chunk):raise ValueError('Batch output count mismatch')
                errors=[None]*len(chunk)
            except Exception as exc:
                # Isolate record failures, never silently switch model or fabricate a decision.
                results=[]; errors=[]
                for h,g in chunk:
                    try: results.append(model.classify(g[0]['text'])); errors.append(None)
                    except Exception as inner: results.append(None);errors.append(f'{type(inner).__name__}: {inner}')
            batches.append((time.perf_counter()-batch_start)*1000)
            with connect(path) as c:
                for (h,records),result,error in zip(chunk,results,errors):
                    if result:latencies.append(result.processing_time_ms)
                    for j,r in enumerate(records):
                        value=result.model_dump(mode='json') if result else None
                        if value:value.update(cache_hit=j>0,inference_source_record=records[0]['id'])
                        cached+=int(j>0);failures+=int(error is not None)
                        c.execute('INSERT INTO predictions VALUES (?,?,?,?,?,?)',(run_id,r['id'],r['source_hash'],dumps(value) if value else None,error,now()))
            peak=max(peak,psutil.Process().memory_info().rss)
            if offset % 40==0:print(f'{offset+len(chunk)}/{len(unique)} unique texts, {failures} failed rows',flush=True)
        elapsed=time.perf_counter()-start
        with connect(path) as c:
            count=c.execute('SELECT count(*) FROM predictions WHERE run_id=?',(run_id,)).fetchone()[0]
            failed=c.execute('SELECT count(*) FROM predictions WHERE run_id=? AND error IS NOT NULL',(run_id,)).fetchone()[0]
            benchmark={'source_rows':len(rows),'output_rows':count,'failed_rows':failed,'cached_rows_this_session':cached,'unique_inferences_this_session':len(latencies),
                'total_wall_seconds_this_session':elapsed,'model_load_ms':model.load_time_ms,'source_rows_per_second_this_session':len(pending)/elapsed,
                'unique_texts_per_second_this_session':len(latencies)/elapsed,
                'median_amortised_inference_ms':float(np.median(latencies)) if latencies else None,
                'p95_amortised_inference_ms':float(np.percentile(latencies,95)) if latencies else None,
                'p95_batch_wall_ms':float(np.percentile(batches,95)) if batches else None,'peak_sampled_process_rss_mb':peak/1024**2,
                'device':str(getattr(getattr(model,'agent',None),'device','unknown')),
                'model_manifest':getattr(model,'model_manifest',None),
                'timing_limitations':'Deduplicated inference; row throughput includes cache reuse. RSS excludes device allocations. Resume reports this session only.'}
            if count!=len(rows):raise RuntimeError('Output count mismatch')
            c.execute('UPDATE runs SET status=?,completed_at=?,benchmark=? WHERE id=?',('COMPLETED_WITH_ERRORS' if failed else 'COMPLETED',now(),dumps(benchmark),run_id))
        print(dumps(benchmark),flush=True)
    except BaseException:
        with connect(path) as c:c.execute("UPDATE runs SET status='INTERRUPTED' WHERE id=?",(run_id,))
        raise
    return run_id

def source_fingerprint():
    h=hashlib.sha256()
    for root in ['apps/api','classifier','training','evaluation','scripts']:
        for p in sorted(Path(root).glob('*.py')):h.update(str(p).encode()+p.read_bytes())
    return h.hexdigest()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config');p.add_argument('--reproduce');p.add_argument('--resume');p.add_argument('--limit',type=int);a=p.parse_args()
    run_batch(config=load_config(a.config) if a.config else None,reproduce=a.reproduce,resume=a.resume,limit=a.limit)
