"""Host-side real Linux container auth, persistence and deployment checks."""
import argparse
import base64
import json
import os
import socket
import subprocess
import time
import urllib.request
from pathlib import Path
from production.security import password_record


def verify(image, output, docker_config=None):
    root=Path(output).resolve();root.mkdir(parents=True,exist_ok=False)
    secret=root/'users.json';password=os.urandom(20).hex()
    secret.write_text(json.dumps({'qualifier':{'roles':['ADMIN','TRAINER'],'password':password_record(password)}}));secret.chmod(0o644)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    origin=f'http://127.0.0.1:{port}';name='voting-service-check-'+str(port)
    env=os.environ.copy()
    if docker_config:env['DOCKER_CONFIG']=str(Path(docker_config).resolve())
    def docker(*args):return subprocess.check_output(['docker',*args],env=env,text=True).strip()
    auth='Basic '+base64.b64encode(('qualifier:'+password).encode()).decode()
    def request(path,body=None,authenticated=True):
        headers={'Authorization':auth} if authenticated else {}
        if body is not None:headers['Content-Type']='application/json'
        req=urllib.request.Request(origin+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
    volume=name+'-state'
    container=docker('run','-d','--name',name,'--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true',
        '--memory','1g','--tmpfs','/tmp:rw,nosuid,size=128m,uid=10001,gid=10001,mode=0700',
        '-p',f'127.0.0.1:{port}:8000','--mount',f'type=bind,src={secret},dst=/run/secrets/users,readonly',
        '--mount',f'type=volume,src={volume},dst=/srv/voting/state','--tmpfs','/srv/voting/logs:rw,size=32m,uid=10001,gid=10001',
        '-e','VOTING_REQUIRE_WORKER=false','-e','VOTING_USERS_FILE=/run/secrets/users','-e',f'VOTING_PUBLIC_ORIGIN={origin}','-e','VOTING_ALLOW_LOCAL_HTTP=true',image)
    try:
        def wait():
            for _ in range(150):
                try:request('/health/live',authenticated=False);return
                except OSError:time.sleep(.2)
            raise RuntimeError(docker('logs',name))
        wait();status=request('/api/client/status')
        receipt=request('/api/client/imports',{'id':'linux-persistent-corpus','rows':[{'raw':'Shareholders may vote at this meeting.','sender':'AI_TEST','source_type':'STANDARDS_DERIVED_SYNTHETIC','source_reference':'AI_AUTHORED_SOFTWARE_TEST','group_id':'g1','family':'f1','split':'TRAIN','language':'en','population':'AI_FRAMEWORK','declared':{'corp':'c1','seme':'s1','function':'NEWM'}}]})
        assert receipt['accepted']==1
        assert request('/api/client/events')['total']==1
        docker('restart',name);wait()
        assert request('/api/client/events')['total']==1
        assert request('/api/client/ready')['ready']
        info=json.loads(docker('inspect',name))[0]
        assert info['Config']['User']=='10001:10001' and info['HostConfig']['ReadonlyRootfs']
        assert info['HostConfig']['CapDrop']==['ALL']
        noauth=False
        try:request('/api/client/status',authenticated=False)
        except urllib.error.HTTPError as e:noauth=e.code==401
        assert noauth
        result={'image':info['Image'],'platform':'linux/arm64' if 'arm64' in docker('image','inspect',image,'--format','{{.Architecture}}') else 'linux/amd64',
                'named_auth':True,'nonroot':True,'read_only_root':True,'capabilities_dropped':True,'restart_persistence':True,
                'source_imported':1,'ready':True,'automation_enabled':False,'model_execution':False,'volume':volume,
                'test_transport':'Loopback HTTP only; production Compose adds supplied-certificate TLS'}
        (root/'receipt.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
    finally:
        (root/'container.log').write_text(docker('logs',name))
        docker('rm','-f',name);secret.unlink()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('output');p.add_argument('--docker-config');a=p.parse_args();verify(a.image,a.output,a.docker_config)
