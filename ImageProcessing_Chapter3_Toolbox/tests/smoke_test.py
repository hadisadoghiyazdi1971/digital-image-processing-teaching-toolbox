import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from image_sources import load_standard
import algorithm_registry as R

def main():
    img=load_standard('camera')[::4,::4]
    ref=load_standard('moon')[::4,::4]
    failed=[]
    for name in R.A:
        try:
            fn=R.load_apply(name); pars={}
            for spec in R.get(name)[2]:
                k,t,d,*e=spec
                if t=='reference': pars[k]=ref
                else: pars[k]=d
            y=np.asarray(fn(img,**pars))
            assert y.ndim==2 and np.isfinite(y).all() and y.size>0
            print('PASS',name,y.shape,float(y.min()),float(y.max()))
        except Exception as e:
            failed.append((name,repr(e))); print('FAIL',name,e)
    if failed:
        raise SystemExit('Failures: '+repr(failed))
    print('ALL PASS:',len(R.A),'algorithms')
if __name__=='__main__': main()
