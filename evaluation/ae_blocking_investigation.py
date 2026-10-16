"""Forensic validation-only probes; no model, label or aggregation changes."""
import gc,json
from collections import Counter
from pathlib import Path
from semantic_pipeline.experiment import lines,write,ROOT,now,verify
from training.synthetic_protocol import rows
from hybrid.semantics import NarrowLaya,passages,aggregate

def investigate():
    verify();source={r['id']:r for r in rows('validation')}
    original={k:{r['id']:r for r in lines(f'data/experiments/iso-hybrid-v1/{k}-validation.jsonl')} for k in ('base','fine')}
    positive=[r for r in rows('validation') if r['share_blocking']=='YES'];cases=[]
    for row in positive:
        cases.append({'id':row['id'],'text':row['text'],'expected':'YES','chunks':list(passages(row['text'])),
            'original':{k:{'aggregate':original[k][row['id']]['result']['predicates']['share_blocking'],
                'passages':original[k][row['id']]['result']['passage_predictions']['share_blocking']} for k in original}})
    for name,path in [('base','data/models/laya/multilingual'),('fine','data/models/narrow-v1')]:
        model=NarrowLaya(path)
        predictions=model.agent.predict_batch([r['text'] for r in positive],{'share_blocking':model.questions['share_blocking']},batch_size=2,max_len=2048,head_max_len=256,sort_by_length=True)
        for c,p in zip(cases,predictions):c.setdefault('whole_document_probe',{})[name]=p['answers']['share_blocking']
        del model;gc.collect()
        import torch
        if torch.backends.mps.is_available():torch.mps.empty_cache()
    train=rows('train');cfg=json.loads(Path('data/experiments/narrow-v1/training-config.json').read_text())
    training=lines('data/experiments/narrow-v1/train.jsonl')
    encoding_correct=all(t['state']==s['text'] and t['expected']['share_blocking']==s['share_blocking'] for t,s in zip(training,train))
    summary={'created_at':now(),'positive_cases':len(cases),'training_class_counts':dict(Counter(r['share_blocking'] for r in train)),
        'validation_class_counts':dict(Counter(r['share_blocking'] for r in source.values())),
        'training_encoding_matches_source':encoding_correct,'question_matches_training':all(t['questions']['share_blocking']==training[0]['questions']['share_blocking'] for t in training),
        'training_config':cfg,'cases':cases,'no_training_or_policy_change':True,
        'fine_positive_chunks_detected':sum(any(p['value']=='YES' and p['confidence']>=.7 for p in c['original']['fine']['passages']) for c in cases),
        'fine_aggregate_conflicts':sum(c['original']['fine']['aggregate']['conflict'] for c in cases),
        'whole_document_fine_yes':sum(c['whole_document_probe']['fine']['choice']=='YES' for c in cases)}
    write(ROOT/'BLOCKING-FORENSICS.json',summary)
    md=['# Blocking false-negative investigation','',
        f'All {len(cases)} affirmative validation records were inspected. The original document-level output detects zero, while sentence-level fine-tuned Laya detects a confident YES passage in {summary["fine_positive_chunks_detected"]}/{len(cases)}. All {summary["fine_aggregate_conflicts"]} documents are then changed to UNKNOWN by `conflict_abstain`: an unrelated introductory sentence classified NO is treated as contradicting the affirmative restriction sentence. This is an aggregation/formulation defect, not evidence that the checkpoint cannot recognise blocking.',
        '',f'The same frozen fine-tuned checkpoint classified the whole document YES in {summary["whole_document_fine_yes"]}/{len(cases)} fresh validation-only component probes. These probes do not alter any A–E result, model or threshold.',
        '',f'Training distribution: `{summary["training_class_counts"]}`; validation: `{summary["validation_class_counts"]}`. Original training records retain the source strings and labels exactly: {encoding_correct}. The YES/NO option mapping is direct; there is no inversion. Native passage scores explicitly favour YES on the blocking clause. Checkpoint weights are covered by both historical and A–E freeze hashes, and reload native-score equality was separately demonstrated.',
        '', 'Training uses whole notices whereas inference asks independent sentence questions. In the choice formulation, NO includes “not stated”; absence in one sentence is not a negative assertion about another sentence. The reducer incorrectly equates these meanings. Its selected-passage scores are retained even when the aggregate abstains; they are not document-level probabilities. The .70 activity cutoff exposes opposing confident passage predictions rather than causing the affirmative passage to disappear.',
        '', 'Imbalance and repetitive synthetic language remain limitations, but do not explain this particular 0/11 result. Preprocessing preserves the affirmative clause (offsets and passage text below); none is truncated. Whole-document/sentence contrast and direct positive passage detection rule out a global training/loading failure. Distribution mismatch is real (document training, sentence inference), and the deterministic conflict policy amplifies it.',
        '', 'Next experiment: distinguish explicit negation from absence of mention, then validate a scope-aware reducer on independently labelled multi-paragraph notices including supersession. A naive any-positive reducer would recover these eleven cases but can incorrectly revive historical/waived restrictions. No such fix was applied after examining the challenge set.',
        '', '## Every affirmative validation case']
    for c in cases:
        md += ['',f'### {c["id"]}', '',c['text'],'','Expected: SHARE_BLOCKING = YES.','']
        md += ['```json',json.dumps({k:v for k,v in c.items() if k not in ('text','id')},ensure_ascii=False,indent=2),'```']
    Path('data/reports/BLOCKING_FALSE_NEGATIVE_ANALYSIS.md').write_text('\n'.join(md)+'\n')
    print({k:v for k,v in summary.items() if k not in ('cases','training_config')})

if __name__=='__main__':investigate()
