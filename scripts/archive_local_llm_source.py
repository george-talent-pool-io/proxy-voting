"""Archive executable source/dependency metadata, without copying model weights."""
import argparse,hashlib,json
from importlib.metadata import distributions
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from semantic_pipeline.experiment import ROOT,verify,write,now

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--revision',default='');args=parser.parse_args()
    if args.revision and not args.revision.isalnum():raise ValueError('Alphanumeric archive revision required')
    suffix='-'+args.revision if args.revision else ''
    verify()
    from training.synthetic_protocol import verify_freeze
    verify_freeze()
    for f in ['data/experiments/iso-hybrid-v1/PIPELINE-FREEZE.json','data/experiments/narrow-v1/FREEZE.json']:
        blob=json.loads(Path(f).read_text())
        for p,h in {**blob.get('files',{}),**blob.get('code',{}),**blob.get('model_files',{})}.items():
            assert Path(p).is_file(),p
            assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    paths=[]
    for folder in ['classifier','hybrid','semantic_pipeline','semantic_runtime','training','evaluation','apps','scripts','tests']:
        paths += [p for p in Path(folder).rglob('*') if p.is_file() and p.suffix in ('.py','.js','.css','.html','.json','.txt','.sh') and '__pycache__' not in p.parts]
    paths += [Path(n) for n in ['README.md','pyproject.toml','uv.lock','requirements-hybrid.txt','docker-compose.yml']]
    target=ROOT/('EXECUTABLE-SOURCE'+suffix+'.zip')
    with ZipFile(target,'x',compression=ZIP_DEFLATED) as z:
        for p in sorted(set(paths)):z.write(p,str(p))
    write(ROOT/('SOURCE-ENVIRONMENT'+suffix+'.json'),{'created_at':now(),'source_archive':str(target),
        'archive_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))},
        'installed_python_packages':{d.metadata['Name']:d.version for d in distributions()},
        'weights':'Not duplicated. Pinned paths/SHA-256 values in FREEZE.json and previous model manifests.',
        'historical_dependency_manifests_verified':True,
        'note':'Post-run source snapshot; frozen inference hashes and pre-existing historical manifests are verified, not replaced.'})
    print('Archived',len(paths),'source files')
