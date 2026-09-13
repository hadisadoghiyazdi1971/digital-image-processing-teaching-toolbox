from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

from image_sources import STANDARD, load_standard, load_file
import algorithm_registry as registry

class Toolbox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Chapter 3 Toolbox — Intensity Transformations & Spatial Filtering')
        self.geometry('1180x760')
        self.minsize(980,650)
        self.source=load_standard('camera'); self.result=self.source.copy(); self.reference=load_standard('moon')
        self.source_name='camera'; self.param_widgets={}
        self._build(); self._refresh_images(); self._on_category()

    def _build(self):
        top=ttk.Frame(self,padding=8); top.pack(fill='x')
        ttk.Label(top,text='تصویر ورودی:').pack(side='left')
        self.sample=tk.StringVar(value='camera'); cb=ttk.Combobox(top,textvariable=self.sample,values=STANDARD,state='readonly',width=22); cb.pack(side='left',padx=4); cb.bind('<<ComboboxSelected>>',lambda e:self._load_sample())
        ttk.Button(top,text='Browse تصویر...',command=self._browse).pack(side='left',padx=4)
        ttk.Button(top,text='Browse مرجع...',command=self._browse_ref).pack(side='left',padx=4)
        ttk.Button(top,text='ذخیره خروجی',command=self._save).pack(side='right',padx=4)
        ttk.Button(top,text='هیستوگرام',command=self._hist).pack(side='right',padx=4)

        main=ttk.Panedwindow(self,orient='horizontal'); main.pack(fill='both',expand=True,padx=8,pady=4)
        left=ttk.Frame(main,padding=8); right=ttk.Frame(main,padding=8); main.add(left,weight=1); main.add(right,weight=3)

        ttk.Label(left,text='گروه الگوریتم').pack(anchor='w')
        self.cat=tk.StringVar(value=registry.categories()[0]); self.catcb=ttk.Combobox(left,textvariable=self.cat,values=registry.categories(),state='readonly'); self.catcb.pack(fill='x',pady=(2,8)); self.catcb.bind('<<ComboboxSelected>>',lambda e:self._on_category())
        ttk.Label(left,text='الگوریتم').pack(anchor='w')
        self.alg=tk.StringVar(); self.algcb=ttk.Combobox(left,textvariable=self.alg,state='readonly'); self.algcb.pack(fill='x',pady=(2,8)); self.algcb.bind('<<ComboboxSelected>>',lambda e:self._build_params())
        ttk.Separator(left).pack(fill='x',pady=6)
        ttk.Label(left,text='پارامترها').pack(anchor='w')
        self.params=ttk.Frame(left); self.params.pack(fill='x',pady=4)
        ttk.Button(left,text='اجرا',command=self._run).pack(fill='x',pady=8)
        ttk.Button(left,text='بازگردانی ورودی',command=self._reset).pack(fill='x')
        ttk.Label(left,text='نکته: بیشتر الگوریتم‌های فصل ۳ روی شدت خاکستری اجرا می‌شوند.\nبرای توضیح هر گزینه، OPTIONS_GUIDE_FA.md را ببینید.',wraplength=240,justify='right').pack(fill='x',pady=16)

        views=ttk.Frame(right); views.pack(fill='both',expand=True)
        self.in_label=ttk.Label(views,anchor='center'); self.in_label.grid(row=0,column=0,sticky='nsew',padx=4,pady=4)
        self.out_label=ttk.Label(views,anchor='center'); self.out_label.grid(row=0,column=1,sticky='nsew',padx=4,pady=4)
        views.columnconfigure(0,weight=1); views.columnconfigure(1,weight=1); views.rowconfigure(0,weight=1)
        ttk.Label(right,text='چپ: ورودی     |     راست: خروجی',anchor='center').pack(fill='x')
        self.status=tk.StringVar(value='آماده'); ttk.Label(self,textvariable=self.status,relief='sunken',anchor='w').pack(fill='x',side='bottom')
        self.bind('<Configure>',lambda e:self.after_idle(self._refresh_images))

    def _on_category(self):
        vals=registry.algorithms_for(self.cat.get()); self.algcb['values']=vals
        if vals: self.alg.set(vals[0]); self._build_params()

    def _build_params(self):
        for w in self.params.winfo_children(): w.destroy()
        self.param_widgets={}
        if not self.alg.get(): return
        _,_,pars=registry.get(self.alg.get())
        for spec in pars:
            name,typ,default,*extra=spec
            row=ttk.Frame(self.params); row.pack(fill='x',pady=2)
            ttk.Label(row,text=name,width=18).pack(side='left')
            var=tk.StringVar(value=str(default) if default is not None else '')
            if typ=='bool':
                bv=tk.BooleanVar(value=bool(default)); w=ttk.Checkbutton(row,variable=bv); self.param_widgets[name]=(typ,bv)
            elif typ=='enum':
                vals=extra[0]; w=ttk.Combobox(row,textvariable=var,values=vals,state='readonly',width=15); self.param_widgets[name]=(typ,var)
            elif typ=='reference':
                ttk.Label(row,text='از تصویر مرجع Browse/پیش‌فرض moon').pack(side='left'); self.param_widgets[name]=(typ,None); continue
            else:
                w=ttk.Entry(row,textvariable=var,width=18); self.param_widgets[name]=(typ,var)
            w.pack(side='right',fill='x',expand=True)

    def _get_params(self):
        d={}
        for k,(typ,var) in self.param_widgets.items():
            if typ=='reference': d[k]=self.reference
            elif typ=='bool': d[k]=bool(var.get())
            else:
                v=var.get()
                if typ=='int': v=int(float(v))
                elif typ=='float': v=float(v)
                elif typ=='enum' and k=='connectivity': v=int(v)
                d[k]=v
        return d

    def _load_sample(self): self.source=load_standard(self.sample.get()); self.source_name=self.sample.get(); self.result=self.source.copy(); self._refresh_images()
    def _browse(self):
        p=filedialog.askopenfilename(filetypes=[('Images','*.png *.jpg *.jpeg *.bmp *.tif *.tiff'),('All','*.*')]);
        if p: self.source=load_file(p); self.source_name=Path(p).name; self.result=self.source.copy(); self._refresh_images()
    def _browse_ref(self):
        p=filedialog.askopenfilename(filetypes=[('Images','*.png *.jpg *.jpeg *.bmp *.tif *.tiff'),('All','*.*')]);
        if p: self.reference=load_file(p); self.status.set('تصویر مرجع: '+Path(p).name)
    def _run(self):
        try:
            fn=registry.load_apply(self.alg.get()); pars=self._get_params(); self.result=np.asarray(fn(self.source,**pars),dtype=float); self._refresh_images(); self.status.set('اجرا شد: '+self.alg.get())
        except Exception as e: messagebox.showerror('خطا',str(e))
    def _reset(self): self.result=self.source.copy(); self._refresh_images(); self.status.set('خروجی بازنشانی شد')
    def _save(self):
        p=filedialog.asksaveasfilename(defaultextension='.png',filetypes=[('PNG','*.png'),('JPEG','*.jpg')]);
        if p:
            a=np.clip(self.result,0,1); Image.fromarray((a*255+0.5).astype(np.uint8)).save(p); self.status.set('ذخیره شد: '+p)
    def _hist(self):
        plt.figure('Histograms'); plt.clf(); plt.hist(self.source.ravel(),256,[0,1],alpha=.55,label='input'); plt.hist(np.clip(self.result,0,1).ravel(),256,[0,1],alpha=.55,label='output'); plt.legend(); plt.xlabel('Intensity'); plt.ylabel('Count'); plt.tight_layout(); plt.show()
    def _to_photo(self,a):
        a=np.clip(np.asarray(a),0,1); im=Image.fromarray((a*255+0.5).astype(np.uint8),'L')
        maxw=max(300,(self.winfo_width()-340)//2-20); maxh=max(300,self.winfo_height()-180); im.thumbnail((maxw,maxh),Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(im)
    def _refresh_images(self):
        try:
            self._pi=self._to_photo(self.source); self._po=self._to_photo(self.result); self.in_label.configure(image=self._pi); self.out_label.configure(image=self._po)
        except Exception: pass

if __name__=='__main__': Toolbox().mainloop()
