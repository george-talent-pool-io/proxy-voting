"""Explicit local public-notice application smoke; no labels, no training or quality claims."""
import json,urllib.request,urllib.parse,sqlite3
from pathlib import Path

def get(path):
    with urllib.request.urlopen('http://127.0.0.1:8000'+path,timeout=180) as r:return json.load(r)

def main():
    with sqlite3.connect('data/voting.sqlite') as c:
        ident=c.execute('SELECT id FROM notices WHERE length(text) BETWEEN 250 AND 800 ORDER BY length(text),id LIMIT 1').fetchone()[0]
    before=get('/api/notice?'+urllib.parse.urlencode({'id':ident}))
    request=urllib.request.Request('http://127.0.0.1:8000/api/semantic/analyse',data=json.dumps({'record_id':ident}).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=180) as r:execution=json.load(r)
    assert execution['record_id']==ident and execution['text']==before['text']
    assert execution['result']['architecture']=='C' and execution['result']['llm']['invoked'] and execution['result']['llm']['valid']
    assert execution['result']['decision']['manual_review_required'] and not execution['result']['automation_enabled']
    after=get('/api/notice?'+urllib.parse.urlencode({'id':ident}))
    assert after['semantic_execution']==execution and before['prediction']==after['prediction']
    Path('artifacts/local-llm-integrated-notice.json').write_text(json.dumps({'record_id':ident,'execution':execution,'historical_prediction_unchanged':True},indent=2))
    print(ident,execution['run_id'],execution['result']['decision']['classification'])
if __name__=='__main__':main()
