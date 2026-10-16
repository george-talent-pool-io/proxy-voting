"""Download one pre-verified Ollama library quantisation; no notice data sent."""
import json,time,urllib.request,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('data/experiments/cascade-v2')
name='qwen3.8:27b-q4_K_M';manifest=json.loads((ROOT/'ollama_manifest.json').read_text())
preflight={'verified_before_download_at':datetime.now(timezone.utc).isoformat(),'publisher':'Qwen','upstream':'Qwen/Qwen3.8-27B','upstream_revision':'1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0','hf_total_parameters_including_vision':27781427952,'ollama_language_parameters_approx':27300000000,'quantisation':'Q4_K_M','model':name,'digest':hashlib.sha256((ROOT/'ollama_manifest.json').read_bytes()).hexdigest(),'download_bytes':sum(x['size'] for x in manifest['layers'])+manifest['config']['size'],'expected_unified_memory_bytes_range':[21_000_000_000,28_000_000_000],'memory_estimate_not_measurement':True,'licence':'Apache-2.0','runtime':'Ollama 0.34.3; qwen35 architecture already supported; thinking true/false available, exact controls checked after pull','sources':['https://huggingface.co/Qwen/Qwen3.8-27B','https://ollama.com/library/qwen3.8:27b-q4_K_M','https://docs.ollama.com/capabilities/thinking'],'notices_transmitted':0}
with (ROOT/'QWEN-PREFLIGHT.json').open('x') as f:json.dump(preflight,f,indent=2)
req=urllib.request.Request('http://127.0.0.1:11434/api/pull',data=json.dumps({'model':name,'stream':True}).encode(),headers={'Content-Type':'application/json'})
last=None;started=time.time()
with urllib.request.urlopen(req,timeout=3600) as response:
 for line in response:
  item=json.loads(line);status=item.get('status','')
  if item.get('error'):raise RuntimeError(item['error'])
  bucket=(status,round(10*item.get('completed',0)/item.get('total',1)))
  if bucket!=last:print(json.dumps({'elapsed_s':round(time.time()-started),'status':status,'completed':item.get('completed'),'total':item.get('total')}),flush=True);last=bucket
print('Pull finished',round(time.time()-started),flush=True)
