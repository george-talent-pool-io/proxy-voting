"""Supported per-label denominators, including abstention and asymmetric misses."""
from semantic_pipeline.metrics import field_metrics

def metrics(truth,predicted,field):
    positive='VOTABLE' if field=='votability' else 'PASSED' if field=='deadline_status' else 'YES'
    out=field_metrics(truth,predicted,positive)
    per={}
    for label in sorted(set(truth)|set(predicted)):
        tp=sum(y==p==label for y,p in zip(truth,predicted));fn=sum(y==label and p!=label for y,p in zip(truth,predicted));fp=sum(y!=label and p==label for y,p in zip(truth,predicted));tn=len(truth)-tp-fn-fp
        precision=tp/(tp+fp) if tp+fp else None;recall=tp/(tp+fn) if tp+fn else None
        per[label]={'support':tp+fn,'predicted_support':tp+fp,'precision':precision,'recall':recall,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,'true_positive':tp,'false_positive':fp,'false_negative':fn,'true_negative':tn,'specificity':tn/(tn+fp) if tn+fp else None}
    out['per_class']=per
    out['positive_false_negatives']=per.get(positive,{}).get('false_negative',0);out['positive_false_positives']=per.get(positive,{}).get('false_positive',0)
    neg='NOT_VOTABLE' if field=='votability' else 'OPEN' if field=='deadline_status' else 'NO'
    out['negative_label']=neg;out['negative_precision']=per.get(neg,{}).get('precision');out['negative_recall_specificity']=per.get(neg,{}).get('recall');out['negative_f1']=per.get(neg,{}).get('f1');out['negative_support']=per.get(neg,{}).get('support',0)
    if field=='classification':
        for key in ['positive_label','positive_support','positive_precision','positive_recall','positive_f1','negative_label','negative_precision','negative_recall_specificity','negative_f1','negative_support','positive_false_negatives','positive_false_positives']:out[key]=None
    return out
