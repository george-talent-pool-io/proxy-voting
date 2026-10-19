"""Persistent local JSONL helper; Java objects never cross this boundary."""
import json,subprocess,threading,select,time
from pathlib import Path
from qwen_domain.protocol import ROOT
from iso_adapter.scanner import scan,QUALIFIERS,NARRATIVE_TAGS
VERSION='prowide-jsonl-v1.1'

def same_payload(left,right):
    # Prowide may normalize FIN CRLFs internally. Offsets/quotes still point to
    # the unchanged original; this comparison is only for ordered alignment.
    def view(s):return s.replace('\r\n','\n').replace('\r','\n').strip().removesuffix('-}').rstrip()
    return view(left)==view(right)
class Prowide:
    def __init__(self):self.process=None;self.lock=threading.RLock();self.load_ms=None
    def start(self):
        if self.process is not None and self.process.poll() is None:return
        jar=ROOT/'tools/prowide/target/prowide-helper-1.0.0.jar'
        if not jar.exists():raise RuntimeError('Prowide helper is not built; run mvn -f tools/prowide/pom.xml package')
        started=time.perf_counter();log=(ROOT/'artifacts/prowide-helper.log').open('ab')
        self.process=subprocess.Popen(['java','-Xms32m','-Xmx256m','-jar',str(jar)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,text=True,encoding='utf-8',bufsize=1);log.close();self.load_ms=(time.perf_counter()-started)*1000
    def close(self):
        if self.process is not None:
            self.process.terminate()
            try:self.process.wait(3)
            except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
            self.process=None
    def parse(self,text):
        with self.lock:
            start=time.perf_counter();self.start();self.process.stdin.write(json.dumps({'text':text},ensure_ascii=False)+'\n');self.process.stdin.flush()
            if not select.select([self.process.stdout],[],[],30)[0]:self.close();raise TimeoutError('Prowide helper did not respond')
            line=self.process.stdout.readline()
            if not line:self.close();raise RuntimeError('Prowide helper exited')
            value=json.loads(line);value['raw_source']=text;value['latency_ms']=(time.perf_counter()-start)*1000
            value['helper_version']=value.get('adapter_version','prowide-jsonl-v1');value['adapter_version']=VERSION
            if value['parse_status']=='FAILED':return value
            recovered=scan(text);refs={};dates={};options=[];narratives=[];unknown=[];event={};security={}
            if len(recovered['fields'])!=len(value['fields']):value['warnings'].append('FIELD_BOUNDARY_DISAGREEMENT: Core and recovery found different field counts; use non-authoritative recovery')
            cursor=-1
            for f in value['fields']:
                import re
                candidate=next((r for r in recovered['fields'] if r['start']>cursor and r['tag']==f['tag'] and same_payload(r['value'],f['value'])),None)
                if candidate:
                    f.update(start=candidate['start'],end=candidate['end'],source_text=text[candidate['start']:candidate['end']],sequence_instance_path=candidate['sequence_instance_path']);cursor=candidate['start']
                else:f['source_span_unavailable']=True
                q=re.match(r':([A-Z0-9]{4})//',f['value']);f['qualifier']=q[1] if q else None
                if f['tag']=='20C' and q:refs.setdefault(q[1],[]).append(f)
                elif f['tag'].startswith('98') and q:dates.setdefault(q[1],[]).append(f)
                elif f['tag']=='22F' and q and q[1]=='CAEV':event.setdefault('caev',[]).append(f)
                elif f['tag']=='22F' and q and q[1]=='CAOP':options.append(f)
                elif f['tag']=='35B':
                    security.setdefault('fields',[]).append(f)
                    c=f.get('components',[])
                    if len(c)>1 and c[0]=='ISIN':security.setdefault('isins',[]).append({'value':c[1],'source_field':f})
                if f['tag'] in NARRATIVE_TAGS and q and q[1] in QUALIFIERS:
                    candidates=[r for r in recovered['narratives'] if r['tag']==f['tag'] and r['qualifier']==q[1] and r['start']==f.get('start')]
                    if candidates:
                        r=candidates[0];narratives.append({**r,'source':'PROWIDE','typed_field':f.get('typed_field'),'components':f.get('components')})
                if f.get('unrecognised') or f.get('component_error'):unknown.append(f)
            value.update(references=refs,security=security,event=event,dates=dates,options=options,narratives=narratives,unknown_fields=unknown)
            return value
