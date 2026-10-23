"""The source handoff contains executable modules, never customer artifacts."""
import tarfile
from scripts.package_learning_source import package, ROOT


def test_source_archive_contains_every_package_and_excludes_operational_data(tmp_path):
    archive=tmp_path/'source.tar.gz'
    package(archive)
    with tarfile.open(archive) as stream:names=set(stream.getnames())
    with tarfile.open(archive) as stream:
        for notice in ['LICENSE', 'NOTICE', 'COMMERCIAL-LICENSE']:
            assert stream.extractfile(notice).read() == (ROOT / notice).read_bytes()
    for folder in ROOT.iterdir():
        if folder.is_dir() and (folder/'__init__.py').exists():
            assert folder.name+'/__init__.py' in names
    assert 'tests/fixtures/prowide-mt564.json' in names
    assert {'.dockerignore','.gitignore'} <= names
    parser_examples = {n for n in names if n.startswith('data/iso15022_corpus/')}
    assert len(parser_examples) == 7
    assert 'data/iso15022_corpus/official_examples/clearstream-dscl-excerpt.json' in parser_examples
    for name in names:
        assert not name.startswith('training/reliability/')
        assert not name.startswith(('artifacts/','data/experiments/','data/qualification-corpora/','data/training-workspace/'))
        assert not name.endswith(('.safetensors','.sqlite','.sqlite3','.pem','.key'))


def test_extracted_delivery_retains_provenance_without_inheriting_parent_repository(tmp_path, monkeypatch):
    import hashlib
    import json
    import subprocess
    from scripts import package_learning_source as source
    data={'app.py':b'customer source'}
    original={'git_commit':'frozen-upstream','workspace_dirty':True,
              'files':{'app.py':hashlib.sha256(data['app.py']).hexdigest()}}
    (tmp_path/'SOURCE-MANIFEST.json').write_text(json.dumps(original))
    monkeypatch.setattr(source,'ROOT',tmp_path)
    monkeypatch.setattr(source.subprocess,'run',lambda *a,**kw:subprocess.CompletedProcess(a,0,'/some/parent/repository\n',''))
    assert source.provenance(data)['provenance_source']=='ARCHIVE_MANIFEST'
    assert not source.provenance(data)['workspace_dirty']
    assert source.provenance({'app.py':b'changed'})['workspace_dirty']
    def no_git(*a,**kw):raise FileNotFoundError('git not installed')
    monkeypatch.setattr(source.subprocess,'run',no_git)
    assert source.provenance(data)['git_commit']=='frozen-upstream'
