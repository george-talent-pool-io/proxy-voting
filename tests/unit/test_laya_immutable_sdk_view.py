import json
from pathlib import Path
from types import SimpleNamespace
from training.framework.trainers import isolate_laya_base, snapshot


def test_actual_sdk_tokenizer_compatibility_rewrite_cannot_touch_frozen_source(tmp_path):
    from laya.agent import _fix_tokenizer_config
    source=tmp_path/'foundation';(source/'tokenizer').mkdir(parents=True)
    (source/'model.safetensors').write_bytes(b'OPAQUE_SOFTWARE_FIXTURE_NOT_WEIGHTS')
    (source/'tokenizer/tokenizer_config.json').write_text(json.dumps({'tokenizer_class':'TokenizersBackend','backend':'tokenizers','is_local':True}))
    before=snapshot(source);view=tmp_path/'view';isolate_laya_base(source,view)
    _fix_tokenizer_config(str(view))  # Executes the installed SDK's real rewrite.
    assert snapshot(source)==before and snapshot(view)!=before
    assert json.loads((view/'tokenizer/tokenizer_config.json').read_text())['tokenizer_class']=='PreTrainedTokenizerFast'
    assert (source/'model.safetensors').stat().st_ino!=(view/'model.safetensors').stat().st_ino


def test_serving_uses_private_sdk_view_and_cleans_up(tmp_path,monkeypatch):
    import laya
    from laya.agent import _fix_tokenizer_config
    from training.framework.runtime import RegisteredModel
    source=tmp_path/'foundation';(source/'tokenizer').mkdir(parents=True)
    (source/'tokenizer/tokenizer_config.json').write_text('{"tokenizer_class":"TokenizersBackend"}')
    bundle=tmp_path/'bundle';bundle.mkdir();(bundle/'laya-questions.json').write_text('{}')
    loaded=[]
    def load(path,**kw):loaded.append(Path(path));_fix_tokenizer_config(path);return object()
    monkeypatch.setattr(laya,'load',load)
    model=RegisteredModel.__new__(RegisteredModel);model.root=tmp_path/'jobs'/'fixture'
    model.spec=SimpleNamespace(backend='LAYA_SDK',device='cpu');model.checkpoint_path=source
    model.plan={'bundle':str(bundle)};before=snapshot(source)
    model._load_backend();assert loaded[0]!=source and loaded[0].exists() and snapshot(source)==before
    model.close();assert not loaded[0].exists()
