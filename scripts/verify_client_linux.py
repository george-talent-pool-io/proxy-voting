"""Run INSIDE the Linux image, without network; produces factual JSON receipts.

The tiny random Qwen architecture verifies PEFT learning mechanics only. It is
not a substitute for qualifying the customer's pretrained Qwen checkpoint/GPU.
"""
import argparse
import json
import os
import platform
import shutil
import time
from pathlib import Path


def main(output, learning=False, skip_laya=False):
    import importlib.metadata as metadata
    from training.framework import jobs
    from training.framework.bundle import write
    from iso_adapter.routing import route, _REFERENCE
    from iso_adapter.benchmark import fin
    import torch
    started=time.perf_counter()
    assert torch.version.cuda is None, 'This image is explicitly CPU-qualified'
    raw=fin(':16R:GENL\n:20C::CORP//VERIFY\n:20C::SEME//VERIFY1\n:23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n:16R:ADDINFO\n:70E::ADTX//Registration is required.\n:16S:ADDINFO')
    parsed=route(raw)
    assert parsed['parser']=='PROWIDE' and parsed['raw_source']==raw
    assert parsed['structure']['references']['CORP'][0]['components']==['CORP','VERIFY']
    assert route('Ordinary shareholder notice')['parser']=='NOT_APPLICABLE'
    assert route(':16R:ADDINFO\n:70E::ADTX//POA is required.')['parser']=='LENIENT_RECOVERY'
    _REFERENCE.close()
    receipt={'platform':platform.platform(),'machine':platform.machine(),'uid':os.getuid(),
             'versions':{k:metadata.version(k) for k in ['torch','transformers','peft','laya']},
             'parser':'REAL_PROWIDE_JVM','network':'Docker --network none', 'automation_enabled':False}
    if learning:
        from training.framework.schema import TrainSpec
        from training.framework.runtime import RegisteredModel
        workspace=jobs.WORKSPACE;workspace.mkdir(parents=True,exist_ok=True)
        bundle=jobs.member('bundles','linux-smoke');bundle.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree('/input-bundle',bundle)
        if not skip_laya:
            spec=TrainSpec(backend='LAYA_SDK',family='LAYA',model_path='/srv/voting/models/laya/multilingual',
                           base_model_id='convaiinnovations/laya:multilingual',base_revision='7b928d828b7b0e022f929d9bd2e44165aa270148',
                           epochs=1,learning_rate=.0001,batch_size=1,gradient_accumulation=1,max_length=512,device='cpu')
            job=jobs.member('jobs','linux-laya');plan=jobs.prepare(bundle,spec,job);jobs.execute(job)
            model=RegisteredModel(job)
            try:
                pred=model.analyse('Shareholders may submit votes at this meeting.',use_iso=False)
                assert len(pred['predicates'])>=9
            finally:model.close()
            receipt['laya']={'state':jobs.status(job)['state'],'job_id':plan['job_id'],
                             'result':json.loads((job/'result.json').read_text()) if (job/'result.json').exists() else jobs.status(job)}
        else:
            import laya,gc
            from training.framework.bundle import laya_questions
            agent=laya.load('/srv/voting/models/laya/multilingual',device='cpu')
            predictions=agent.predict_batch(['Shareholders may vote.'],laya_questions(),batch_size=1,max_len=512,head_max_len=256)
            assert len(predictions[0]['answers'])==9
            del agent;gc.collect()
            receipt['laya']={'inference':'REAL_OFFICIAL_SDK_CPU_PASSED','linux_training':'NOT_QUALIFIED_3GB_LIMIT'}
        # Real optimiser and model architecture, intentionally random weights.
        from tokenizers import Tokenizer,models,pre_tokenizers
        from transformers import PreTrainedTokenizerFast,Qwen3_5TextConfig,Qwen3_5ForCausalLM
        vocab={'[UNK]':0,'[PAD]':1,'[EOS]':2}
        pre=pre_tokenizers.Whitespace()
        for name in ['llm-train.jsonl','llm-validation.jsonl']:
            for line in (bundle/name).read_text().splitlines():
                for message in json.loads(line)['messages']:
                    for token,_ in pre.pre_tokenize_str(message['content']):
                        if token not in vocab:vocab[token]=len(vocab)
        tokenizer=Tokenizer(models.WordLevel(vocab,unk_token='[UNK]'));tokenizer.pre_tokenizer=pre
        tok=PreTrainedTokenizerFast(tokenizer_object=tokenizer,unk_token='[UNK]',pad_token='[PAD]',eos_token='[EOS]')
        tok.chat_template="{% for m in messages %}{{ m['role'] + ': ' + m['content'] + '\\n' }}{% endfor %}{% if add_generation_prompt %}{{ 'assistant: ' }}{% endif %}"
        base=workspace/'software-only-random-qwen35';base.mkdir()
        config=Qwen3_5TextConfig(vocab_size=len(tok),hidden_size=32,intermediate_size=64,num_hidden_layers=1,
                   num_attention_heads=4,num_key_value_heads=2,head_dim=8,layer_types=['full_attention'],
                   max_position_embeddings=8192,pad_token_id=1,eos_token_id=2)
        torch.manual_seed(42);random_model=Qwen3_5ForCausalLM(config);random_model.save_pretrained(base);tok.save_pretrained(base)
        del random_model
        spec=TrainSpec(backend='TRANSFORMERS_PEFT',family='QWEN',model_path=str(base),
                       base_model_id='RANDOM_INITIALISATION_QWEN35_TEXT_SOFTWARE_TEST',base_revision='SEED42_CONFIG_RECEIPT',
                       epochs=1,learning_rate=.001,batch_size=1,gradient_accumulation=1,max_length=8192,
                       lora_rank=4,lora_alpha=8,device='cpu',max_steps=2,generation_tokens=32)
        job=jobs.member('jobs','linux-qwen-mechanics');jobs.prepare(bundle,spec,job);jobs.execute(job)
        from safetensors.torch import load_file
        weights=load_file(job/'checkpoint/adapter_model.safetensors')
        changed=any(bool(v.abs().sum()>0) for k,v in weights.items() if 'lora_B' in k)
        assert changed
        model=RegisteredModel(job)
        try:
            pred=model.analyse('Shareholders may vote.',use_iso=False)
            assert pred['decision']['manual_review_required']
        finally:model.close()
        receipt['qwen_peft']={'state':jobs.status(job)['state'],'lora_B_updated':changed,
                             'scope':'Random small Qwen3_5 text architecture; optimiser/checkpoint mechanics, NOT pretrained quality or 27B/CUDA compatibility',
                             'status':jobs.status(job)}
    receipt['elapsed_seconds']=time.perf_counter()-started
    Path(output).parent.mkdir(parents=True,exist_ok=True);write(output,receipt)
    print(json.dumps(receipt,default=str))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--learning',action='store_true');p.add_argument('--skip-laya-training',action='store_true');a=p.parse_args();main(a.output,a.learning,a.skip_laya_training)
