"""Actual Compose TLS/local-network acceptance, with disposable test identities."""
import argparse
import base64
import json
import os
import socket
import ssl
import subprocess
import urllib.request
from pathlib import Path
from production.security import password_record


def verify(output,docker_config):
    root=Path(output).resolve();root.mkdir(parents=True,exist_ok=False)
    password=os.urandom(20).hex();secret=root/'users.json';tls=root/'tls';tls.mkdir()
    secret.write_text(json.dumps({'tls-test':{'roles':['ADMIN','TRAINER'],'password':password_record(password)}}));secret.chmod(0o644)
    subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(tls/'server.key'),'-out',str(tls/'server.crt'),
                    '-days','1','-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost,IP:127.0.0.1'],check=True,capture_output=True)
    (tls/'server.key').chmod(0o644) # Disposable test key only; production uses root:10001 mode 0640.
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    origin=f'https://127.0.0.1:{port}'
    env={**os.environ,'DOCKER_CONFIG':str(Path(docker_config).resolve()),'VOTING_IMAGE_TAG':'qualification-final',
         'VOTING_USERS_SECRET':str(secret),'VOTING_TLS_DIRECTORY':str(tls),'VOTING_MODEL_DIRECTORY':str(Path('data/models').resolve()),
         'VOTING_PUBLIC_ORIGIN':origin,'VOTING_PORT':str(port),'VOTING_MEMORY_LIMIT':'1g','TRAINING_EXECUTION_ENABLED':'false'}
    command=['docker','compose','-p','voting-client-acceptance','-f','deploy/compose.yml']
    def compose(*a):
        r=subprocess.run(command+list(a),env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if r.returncode:
            (root/'last-error.log').write_text(r.stdout)
            raise RuntimeError(r.stdout)
        return r.stdout
    auth='Basic '+base64.b64encode(('tls-test:'+password).encode()).decode()
    context=ssl.create_default_context(cafile=str(tls/'server.crt'))
    try:
        (root/'startup.log').write_text(compose('up','-d','--no-build','--wait','--wait-timeout','90'))
        def request(path,body=None):
            req=urllib.request.Request(origin+path,data=json.dumps(body).encode() if body is not None else None,
                        headers={'Authorization':auth,'Content-Type':'application/json','Origin':origin})
            with urllib.request.urlopen(req,context=context,timeout=30) as r:return json.load(r)
        assert request('/api/client/ready')['ready']
        from iso_adapter.benchmark import fin
        raw=fin(':16R:GENL\n:20C::CORP//CLIENTTEST\n:20C::SEME//CLIENTTEST1\n:23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n:16R:ADDINFO\n:70E::ADTX//Registration is required.\n:16S:ADDINFO')
        r=request('/api/client/imports',{'id':'tls-fin-import','rows':[{'raw':raw,'sender':'AI_TEST','source_type':'STANDARDS_DERIVED_SYNTHETIC',
                  'source_reference':'AI_AUTHORED_COMPOSE_ACCEPTANCE','group_id':'g1','family':'f1','split':'TRAIN','language':'en','population':'AI_FRAMEWORK'}]})
        assert r['accepted']==1,r
        event=request('/api/client/events/'+r['rows'][0]['event_id'])
        assert event['messages'][0]['payload']['parser']=='PROWIDE' and event['messages'][0]['raw_source']==raw
        code="import socket; s=socket.socket();s.settimeout(2)\ntry:s.connect(('1.1.1.1',443)); print('EXTERNAL_CONNECTION_SUCCEEDED')\nexcept OSError:print('EGRESS_BLOCKED')"
        egress=compose('exec','-T','api','python','-c',code)
        assert 'EGRESS_BLOCKED' in egress,egress
        status=request('/api/client/status');assert not status['automation_switch']
        receipt={'https_certificate_verified':True,'named_auth':True,'real_prowide_import':True,'raw_source_identical':True,
                 'egress_blocked':True,'automation_enabled':False,'training_enabled':False,
                 'scope':'Real Linux Compose integration with AI_AUTHORED source; no model/customer-accuracy claim'}
        (root/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
    finally:
        try:(root/'service.log').write_text(compose('logs','--no-color'))
        finally:compose('down')
        secret.unlink(missing_ok=True);(tls/'server.key').unlink(missing_ok=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--docker-config',required=True);a=p.parse_args();verify(a.output,a.docker_config)
