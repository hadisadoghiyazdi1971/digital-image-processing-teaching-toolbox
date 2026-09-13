from pathlib import Path
import matplotlib.pyplot as plt
from image_sources import load_standard
import algorithm_registry as R

out=Path('outputs'); out.mkdir(exist_ok=True)
img=load_standard('camera')
selected=[
('منفی (کتاب 3-3)','Negative'),
('گاما / توانی (کتاب 3-5)','Gamma'),
('همسان‌سازی سراسری','Histogram equalization'),
('گاوسی','Gaussian smoothing'),
('میانه','Median smoothing'),
('لاپلاسین و تیزسازی','Laplacian sharpening'),
('گرادیان Sobel','Sobel magnitude'),
('بالاگذر از پایین‌گذر','Highpass from lowpass'),
('زنجیره ترکیبی فصل 3','Combined enhancement'),
]
fig,axs=plt.subplots(3,3,figsize=(11,10))
for ax,(name,title) in zip(axs.ravel(),selected):
    fn=R.load_apply(name); pars={}
    for spec in R.get(name)[2]:
        k,t,d,*e=spec
        if t=='reference': pars[k]=load_standard('moon')
        else: pars[k]=d
    y=fn(img,**pars); ax.imshow(y,cmap='gray',vmin=0,vmax=1); ax.set_title(title,fontsize=9); ax.axis('off')
plt.tight_layout(); p=out/'demo_contact_sheet.png'; plt.savefig(p,dpi=150); print('Saved',p)
