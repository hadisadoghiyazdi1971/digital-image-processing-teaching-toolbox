from __future__ import annotations
import numpy as np
from PIL import Image
from skimage import data, color, exposure

STANDARD = ['camera','moon','coins','page','text','clock','checkerboard','zone_plate','ramp','low_contrast_camera','salt_pepper_camera']

def _gray(x):
    a=np.asarray(x)
    if a.ndim==3: a=color.rgb2gray(a[..., :3])
    a=a.astype(float)
    if a.max()>1: a/=255.0
    return np.clip(a,0,1)

def zone_plate(n=512):
    y,x=np.mgrid[-3:3:complex(n),-3:3:complex(n)]
    return 0.5*(1+np.cos(8*(x*x+y*y)))

def ramp(n=512): return np.tile(np.linspace(0,1,n),(n,1))

def load_standard(name):
    name=str(name)
    if name=='camera': return _gray(data.camera())
    if name=='moon': return _gray(data.moon())
    if name=='coins': return _gray(data.coins())
    if name=='page': return _gray(data.page())
    if name=='text': return _gray(data.text())
    if name=='clock': return _gray(data.clock())
    if name=='checkerboard': return _gray(data.checkerboard())
    if name=='zone_plate': return zone_plate()
    if name=='ramp': return ramp()
    if name=='low_contrast_camera': return exposure.rescale_intensity(_gray(data.camera()), out_range=(0.3,0.65))
    if name=='salt_pepper_camera':
        from skimage.util import random_noise
        return random_noise(_gray(data.camera()), mode='s&p', amount=0.08, rng=2026)
    raise KeyError(name)

def load_file(path):
    return _gray(Image.open(path))
