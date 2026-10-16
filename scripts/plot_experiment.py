"""Standalone figures use only measured experiment artifacts."""
import json
from pathlib import Path
from training.synthetic_protocol import ROOT

def main():
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
 p=json.loads((ROOT/'learning-curve.json').read_text());points=p['points']
 fig,ax=plt.subplots(figsize=(8,4.5))
 for key,label in [('exact_match','All-field exact match'),('macro_f1','Mean field macro F1'),('votable_recall','Votable recall'),('restriction_recall','Restriction recall')]:
  ax.plot([r['n'] for r in points],[r[key] for r in points],marker='o',label=label)
 ax.set(xlabel='Supplied labelled training rows (includes duplicate texts)',ylabel='Score on supplied 100-row validation set',ylim=(0,1.04),title='Laya decision-head learning curve · 4 epochs, seed 42');ax.legend(loc='lower right');ax.grid(alpha=.2)
 fig.text(.1,.01,'AI-authored synthetic labels; known train/validation duplicates. Not independent customer accuracy.',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(ROOT/'learning-curve.png',dpi=180);fig.savefig(ROOT/'learning-curve.svg');plt.close(fig)
 data=json.loads((ROOT/'automation-analysis.json').read_text());fig,axes=plt.subplots(1,2,figsize=(10,4))
 for name,rows in data['models'].items():
  valid=[r for r in rows if r['accuracy'] is not None]
  axes[0].plot([r['threshold'] for r in valid],[r['coverage'] for r in valid],marker='.',label=name)
  axes[1].plot([r['threshold'] for r in valid],[r['accuracy'] for r in valid],marker='.',label=name)
 for ax in axes:ax.set(xlabel='Minimum winning factor probability',ylim=(0,1.04));ax.legend();ax.grid(alpha=.2)
 axes[0].set_ylabel('Hypothetical coverage');axes[1].set_ylabel('Observed all-field accuracy');fig.suptitle('Synthetic diagnostic only · automation disabled')
 fig.tight_layout();fig.savefig(ROOT/'automation-curve.png',dpi=180);fig.savefig(ROOT/'automation-curve.svg');plt.close(fig)
 losses={}
 for name in ['head-4ep','encoder-4ep']:
  m=json.loads((Path('data/models/supplied-synthetic-v1')/name/'training-manifest.json').read_text());losses[name]=m['training']['epoch_loss']
 fig,ax=plt.subplots(figsize=(7,4))
 for name,values in losses.items():ax.plot(range(1,len(values)+1),values,marker='o',label=name)
 ax.set(xlabel='Epoch',ylabel='Training soft cross entropy',title='Official Laya SDK training loss');ax.legend();fig.tight_layout();fig.savefig(ROOT/'training-loss.png',dpi=180);plt.close(fig)
if __name__=='__main__':main()
