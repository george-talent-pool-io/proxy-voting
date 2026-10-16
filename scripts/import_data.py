import argparse
from apps.api.store import initialise,import_normalised
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('file'); a=p.parse_args()
    initialise(); print({'imported':import_normalised(a.file)})
