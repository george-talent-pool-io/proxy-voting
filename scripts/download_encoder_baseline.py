"""Download public baseline weights only; never uploads notice text."""
import hashlib,json
from pathlib import Path
from huggingface_hub import HfApi,hf_hub_download

def main():
 repo='sentence-transformers/all-MiniLM-L6-v2';rev=HfApi().model_info(repo).sha
 root=Path('data/models/minilm');root.mkdir(parents=True,exist_ok=True)
 files={}
 for name in ['config.json','model.safetensors','tokenizer.json','tokenizer_config.json','special_tokens_map.json','vocab.txt']:
  p=Path(hf_hub_download(repo,name,revision=rev,local_dir=root));files[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 (root/'baseline-manifest.json').write_text(json.dumps({'repository':repo,'revision':rev,'files':files,'source':'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2','pooling':'attention-mask mean pooling then L2 normalise; max256 tokens'},indent=2))
 print({'repository':repo,'revision':rev})
if __name__=='__main__':main()
