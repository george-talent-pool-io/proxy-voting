"""Required before freezing a NEW experiment; metadata only, no generation."""
from semantic_pipeline.fallback import OllamaFallback
from semantic_pipeline.experiment import ROOT,write

if __name__=='__main__':
    model=OllamaFallback()
    write(ROOT/'installed-runtime-metadata.json',{'identity':model.identity,
        'show':model.http('/api/show',{'model':model.config['model']})})
    print('Pinned local runtime metadata saved')
