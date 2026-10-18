"""Known-frequency AI software fixture, NEVER a model/customer calibrator."""
import argparse
import json
from pathlib import Path
from production import confidence
from semantic_pipeline.schema import PREDICATES


def verify(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    records=[]
    for key in (*PREDICATES,'final_decision'):
        for fold,n in [('FIT',500),('EVALUATION',200)]:
            for i in range(n):
                strong=bool(i%2)
                correct=i%10<(8 if strong else 5)
                records.append({'id':fold+str(i),'predicate':key,'role':'CALIBRATION','fold':fold,'group':fold+str(i),
                                'features':{'language':'en','constructed_signal':strong},'correct':correct,'origin':'AI_AUTHORED'})
    identity='SOFTWARE_FIXTURE_NOT_A_MODEL_RELEASE'
    m=confidence.fit(records,identity=identity,population='AI_CONTROLLED_KNOWN_FREQUENCIES',output=out/'calibrator.json')
    loaded=confidence.load(out/'calibrator.json',identity)
    assert len(m['models'])==10 and loaded==m
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    r=m['reports']['final_decision']['evaluation'];fig,ax=plt.subplots(figsize=(5,4))
    ax.plot([0,1],[0,1],color='#8794a3',linestyle='--')
    ax.plot([b['mean_probability'] for b in r['bins']],[b['observed_correctness'] for b in r['bins']],'o-',color='#244d70')
    ax.set(xlim=(0,1),ylim=(0,1),xlabel='Calibrated probability',ylabel='Observed correctness',title='Software fixture only · known frequencies')
    fig.tight_layout();fig.savefig(out/'reliability.svg');plt.close(fig)
    receipt={'scope':'AI_AUTHORED_SOFTWARE_CONTRACT_ONLY_NOT_MODEL_PERFORMANCE','models':len(m['models']),
             'fit_per_field':500,'independent_evaluation_per_field':200,'brier':r['brier'],'ece':r['ece'],
             'reload_identical':True,'real_model_calibration_established':False,'automation_enabled':False}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();verify(a.output)
