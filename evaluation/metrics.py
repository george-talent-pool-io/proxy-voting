"""Model-independent metrics. Operational status confidence is explicitly a policy score."""
import math
import numpy as np
from sklearn.metrics import accuracy_score,balanced_accuracy_score,classification_report,confusion_matrix,f1_score
from classifier.schema import Status

LABELS=[s.value for s in Status]

def wilson_lower(correct,n,z=1.96):
    if not n:return None
    p=correct/n
    return (p+z*z/(2*n)-z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n)

def automation_curve(rows):
    """One sorted sweep; avoids quadratic work on large fully reviewed corpora."""
    thresholds=sorted(set([0,.5,.6,.7,.8,.9,.95,.98,.99,1]+[r['confidence'] for r in rows]),reverse=True)
    candidates=sorted((r for r in rows if r['eligible']),key=lambda r:r['confidence'],reverse=True)
    factors=['votable','share_blocking','poa_required','other_restriction','deadline_status']
    groups={};group_correct=0;correct=0;count=0;curve=[]
    for threshold in thresholds:
        while count<len(candidates) and candidates[count]['confidence']>=threshold:
            r=candidates[count]
            ok=all(r['true_decision'][k]==r['decision'][k] for k in factors) if 'true_decision' in r else r['correct']
            correct+=int(ok)
            group=r.get('group_id',r['id'])
            if group not in groups:
                groups[group]=bool(ok);group_correct+=int(ok)
            elif groups[group] and not ok:
                groups[group]=False;group_correct-=1
            count+=1
        curve.append(dict(independent_groups=len(groups),threshold=threshold,auto_processed=count,
            manual_review=len(rows)-count,wrong_auto_processed=count-correct,
            coverage=count/len(rows) if rows else 0,accuracy=correct/count if count else None,
            precision_lower_95=wilson_lower(group_correct,len(groups)),precision_lower_95_rows=wilson_lower(correct,count)))
    return list(reversed(curve))

def select_threshold(rows,target=.98,min_examples=100):
    # Validation-only caller. A confidence bound, not the model's raw confidence, supports the policy.
    options=[p for p in automation_curve(rows) if p['independent_groups']>=min_examples and (p['precision_lower_95'] or 0)>=target]
    return max(options,key=lambda p:p['coverage']) if options else None

def compute_metrics(rows):
    if not rows:return {'n':0,'accuracy':None,'macro_f1':None,'message':'No independently verified records in this split','curve':[]}
    y=[r['true'] for r in rows]; p=[r['predicted'] for r in rows]
    correct=np.array([a==b for a,b in zip(y,p)],dtype=float)
    conf=np.array([r['confidence'] for r in rows])
    bins=[]
    for lo in np.arange(0,1,.1):
        mask=(conf>=lo)&(conf<lo+.1 if lo<.9 else conf<=1)
        if mask.any(): bins.append(dict(low=float(lo),n=int(mask.sum()),mean_confidence=float(conf[mask].mean()),accuracy=float(correct[mask].mean())))
    # Calibration for minimum factor confidence vs status correctness is a diagnostic only.
    ece=sum(b['n']/len(rows)*abs(b['mean_confidence']-b['accuracy']) for b in bins)
    actionable=[r for r in rows if r.get('true_votable')=='YES']
    auto=[r for r in rows if r.get('action')=='AUTO_CLASSIFY']
    factors={}
    for key in ['votable','share_blocking','poa_required','other_restriction','deadline_status']:
        truth=[str(r['true_decision'][key]) for r in rows]; pred=[str(r['decision'][key]) for r in rows]
        factors[key]={'accuracy':accuracy_score(truth,pred),'report':classification_report(truth,pred,output_dict=True,zero_division=0)}
    return dict(n=len(rows),accuracy=accuracy_score(y,p),balanced_accuracy=balanced_accuracy_score(y,p),
        macro_f1=f1_score(y,p,labels=LABELS,average='macro',zero_division=0),weighted_f1=f1_score(y,p,average='weighted',zero_division=0),
        per_category=classification_report(y,p,labels=LABELS,output_dict=True,zero_division=0),
        labels=LABELS,confusion_matrix=confusion_matrix(y,p,labels=LABELS).tolist(),
        actionable_voting_recall=sum(r.get('predicted_votable')=='YES' for r in actionable)/len(actionable) if actionable else None,
        all_factor_exact_match=sum(all(r['true_decision'][k]==r['decision'][k] for k in ['votable','share_blocking','poa_required','other_restriction','deadline_status']) for r in rows)/len(rows),
        factor_metrics=factors,confidence_bins=bins,status_score_ece=ece,
        calibration_note='Status score is minimum factor probability, not a calibrated joint probability. Factor Brier/log loss use native option probabilities.',
        factor_calibration=factor_calibration(rows),curve=automation_curve(rows),
        auto_processed=len(auto),manual_review=len(rows)-len(auto),wrong_auto_processed=sum(any(r['true_decision'][k]!=r['decision'][k] for k in ['votable','share_blocking','poa_required','other_restriction','deadline_status']) for r in auto),
        false_positives=[r['id'] for r in rows if r.get('predicted_votable')=='YES' and r.get('true_votable')!='YES'],
        false_negatives=[r['id'] for r in rows if r.get('true_votable')=='YES' and r.get('predicted_votable')!='YES'])

def factor_calibration(rows):
    result={}
    for key in ['votable','share_blocking','poa_required','other_restriction','deadline_status']:
        losses=[]; briers=[]; bins=[]; truths=[]; confidences=[]; correctness=[]
        for r in rows:
            scores=r['scores'][key]
            value=r['true_decision'][key]
            truth=('UNKNOWN' if value is None else 'YES' if value is True else 'NO' if value is False else value)
            losses.append(-math.log(max(scores.get(truth,0),1e-15)))
            briers.append(sum((v-int(label==truth))**2 for label,v in scores.items()))
            win=max(scores,key=scores.get); confidences.append(scores[win]); correctness.append(win==truth)
        for i in range(10):
            idx=[j for j,c in enumerate(confidences) if i/10<=c<(i+1)/10 or (i==9 and c==1)]
            if idx:bins.append({'n':len(idx),'confidence':float(np.mean([confidences[j] for j in idx])),'accuracy':float(np.mean([correctness[j] for j in idx]))})
        result[key]={'brier':float(np.mean(briers)),'log_loss':float(np.mean(losses)), 'ece':sum(b['n']/len(rows)*abs(b['confidence']-b['accuracy']) for b in bins),'bins':bins}
    return result
