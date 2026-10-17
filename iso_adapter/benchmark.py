"""CPU-only parser comparison. Never loads or calls a semantic model."""
import json,re,time,statistics,subprocess
from collections import Counter
from pathlib import Path
import psutil
from qwen_domain.protocol import ROOT,sha,read,rows,write,append,now
from iso_adapter.prowide import Prowide
from iso_adapter.scanner import scan
from iso_adapter.routing import route
from iso_adapter.facts import project
from hybrid.parser import parse as legacy

OUT=ROOT/'data/experiments/prowide-v1'

def fin(body,mt='564'):
    return f'{{1:F01TESTBIC0AXXX0000000000}}{{2:I{mt}TESTBIC1XXXXN}}{{4:\n'+body+'\n-}'

def summary(values):
    values=sorted(values)
    return {'n':len(values),'median_ms':statistics.median(values),'p95_ms':values[min(len(values)-1,int(len(values)*.95))],'records_per_second':len(values)/(sum(values)/1000)} if values else None

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'SUMMARY.json').exists():raise ValueError('Completed benchmark is immutable; create a new experiment')
    sources=rows(ROOT/'data/iso15022_corpus/sources.jsonl')+rows(ROOT/'data/iso15022_corpus/prowide_reference/sources.jsonl');helper=Prowide();timings={k:[] for k in ['PROWIDE','CUSTOM','SCANNER','ROUTER']};counts=Counter();disagreements=[];field_assertions=Counter();cold=[];peak=0
    first=read(ROOT/'data/iso15022_corpus/standards_derived/chain-000-0.json')
    for _ in range(5):
        h=Prowide();t=time.perf_counter();h.parse(fin(first['raw'][first['raw'].find(':16R:'):].removesuffix('-}')));cold.append((time.perf_counter()-t)*1000);h.close()
    for meta in sources:
        item=read(ROOT/'data/iso15022_corpus'/meta['path']);assert sha(ROOT/'data/iso15022_corpus'/meta['path'])==meta['sha256'];text=item['raw'];result={}
        for name,fn in [('CUSTOM',legacy),('SCANNER',scan),('PROWIDE',helper.parse),('ROUTER',lambda s:route(s,helper))]:
            t=time.perf_counter()
            try:result[name]=fn(text)
            except Exception as e:result[name]={'exception':f'{type(e).__name__}: {e}'};counts[name+'_crash']+=1
            timings[name].append((time.perf_counter()-t)*1000)
        counts[meta['source_type']]+=1;counts['route_'+result['ROUTER']['input_type']]+=1
        counts['prowide_'+result['PROWIDE']['parse_status']]+=1
        # Existing fixtures are explicitly PARTIAL. Prowide is also measured with a
        # synthetic envelope, separately, without pretending the result is official.
        wrapped=None
        if meta['source_type']=='STANDARDS_DERIVED_SYNTHETIC':
            body=text[text.find(':16R:'):].removesuffix('-}').rstrip();wrapped=helper.parse(fin(body,item['message_type'][2:]));counts['synthetic_envelope_'+wrapped['parse_status']]+=1
            pf=project(wrapped) if wrapped['parse_status']!='FAILED' else []
            lf=result['CUSTOM'].get('facts',[])
            for key,truth in item.get('expected',{}).items():
                if key in ('kind','unknown_preserved'):continue
                if key=='narrative':
                    outputs={'CUSTOM':[f['value'] for f in lf if f['name']=='narrative'],'SCANNER':[n['text'].rstrip('\r\n') for n in result['SCANNER']['narratives']], 'PROWIDE_WRAPPED':[n['text'].rstrip('\r\n') for n in wrapped.get('narratives',[])]}
                else:outputs={'CUSTOM':[f['value'] for f in lf if f['name']==key],'PROWIDE_WRAPPED':[f['value'] for f in pf if f['name']==key]}
                for name,values in outputs.items():
                    field_assertions[name+'_n']+=1;field_assertions[name+'_correct']+=int(truth in values)
                    if truth not in values:disagreements.append({'id':item['id'],'field':key,'truth':truth,'parser':name,'values':values,'source_type':item['source_type']})
        if helper.process:peak=max(peak,psutil.Process(helper.process.pid).memory_info().rss)
        append(OUT/'comparison.jsonl',{'id':item['id'],'source_hash':sha(ROOT/'data/iso15022_corpus'/meta['path']),'source_type':item['source_type'],'results':result,'synthetic_envelope_prowide':wrapped})
    public=ROOT/'data/normalised/public-lsh-v1.jsonl';public_counts=Counter();public_hints=[];start=time.perf_counter()
    for row in rows(public):
        r=route(row['text'],helper);public_counts[r['input_type']]+=1
        if r['input_type'] not in ('UNSTRUCTURED_NOTICE','UNRECOGNISED'):public_hints.append({'id':row['id'],'result':r})
    public_ms=(time.perf_counter()-start)*1000
    # Forced reference-parser controls: stratified lengths + genuine tag-pattern hits.
    # Avoid asserting that a detector-only bypass proves a negative.
    data=rows(public);sample=sorted(data,key=lambda r:len(r['text']))[::max(1,len(data)//80)]
    controls=[]
    for row in sample:
        r=helper.parse(row['text']);controls.append({'id':row['id'],'parse_status':r['parse_status'],'error':r.get('error'),'message_type':r.get('message_type')})
    helper.close()
    result={'created_at':now(),'dependency':'com.prowidesoftware:pw-swift-core:SRU2025-10.3.20','standards_release':'SRU2025','adapter':'prowide-jsonl-v1','java':subprocess.run(['java','-version'],capture_output=True,text=True).stderr.strip(),
        'helper_sha256':sha(ROOT/'tools/prowide/target/prowide-helper-1.0.0.jar'),'source_manifest_sha256':sha(ROOT/'data/iso15022_corpus/sources.jsonl'),'corpus_counts':dict(counts),'expected_assertions':dict(field_assertions),'disagreements':disagreements,
        'timing':{k:summary(v) for k,v in timings.items()},'cold_parse_ms':cold,'cold':summary(cold),'peak_sampled_java_rss_bytes':peak,'java_heap_cap_bytes':256*1024**2,
        'public':{'n':len(data),'source_sha256':sha(public),'counts':dict(public_counts),'total_routing_ms':public_ms,'iso_like_records':public_hints,'forced_prowide_controls':controls},
        'scope':'Parseability/component extraction, not SWIFT network/business validation. Wrapped partial examples are synthetic, not official messages. No Qwen run was active during these measurements.'}
    write(OUT/'SUMMARY.json',result);print(json.dumps({k:result[k] for k in ['corpus_counts','expected_assertions','timing','cold','peak_sampled_java_rss_bytes']},indent=2));print('Public',dict(public_counts))
if __name__=='__main__':run()
