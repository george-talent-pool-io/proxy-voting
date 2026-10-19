"""The source handoff contains executable modules, never customer artifacts."""
import tarfile
from scripts.package_learning_source import package, ROOT


def test_source_archive_contains_every_package_and_excludes_operational_data(tmp_path):
    archive=tmp_path/'source.tar.gz'
    package(archive)
    with tarfile.open(archive) as stream:names=set(stream.getnames())
    for folder in ROOT.iterdir():
        if folder.is_dir() and (folder/'__init__.py').exists():
            assert folder.name+'/__init__.py' in names
    assert 'tests/fixtures/prowide-mt564.json' in names
    assert {'.dockerignore','.gitignore'} <= names
    for name in names:
        assert not name.startswith(('artifacts/','data/experiments/','data/qualification-corpora/','data/training-workspace/'))
        assert not name.endswith(('.safetensors','.sqlite','.sqlite3','.pem','.key'))
