# -*- coding: utf-8 -*-
"""Cimri SERP ozetlerinden alan cikarimi (baslik, en dusuk fiyat, satici/urun/secenek sayisi, tur)."""
import json, re
from fm_ortak import *
def sayi(s): return float(s.replace(".","").replace(",","."))
TL=r"([\d\.]+(?:,\d+)?) ?TL"
def ayikla(r):
    a=(r.get("aciklama") or ""); b=r["baslik"] or ""; u=r["url"]
    out={"url":u,"baslik":b,"aciklama":a}
    m=re.search(r"(\d+) satıcı arasındaki en ucuz .*? fiyatı, (\d\d\.\d\d\.\d{4}) tarihinde "+TL,a)
    if m: out.update(tur="urun",satici_sayisi=int(m.group(1)),en_dusuk=sayi(m.group(3)),fiyat_tarihi=m.group(2))
    else:
        m=re.search(r"(\d+) (?:seçenek|ürün) arasında(?:n)? .*?"+TL+"'den başlayan",a)
        if m: out.update(tur="kategori",secenek_sayisi=int(re.search(r"(\d+) (?:seçenek|ürün)",a).group(1)),en_dusuk=sayi(m.group(2)))
        else:
            m=re.search(r"(\d+) (?:seçenek|ürün) arasından en iyi",a)
            m2=re.search(TL+"'den başlayan",a)
            if m: out.update(tur="kategori",secenek_sayisi=int(m.group(1)),en_dusuk=sayi(m2.group(1)) if m2 else None)
            else:
                m=re.search(TL+"'den başlayan",a) or re.search(r"En Ucuz\. "+TL,a)
                if m: out.update(tur="urun",en_dusuk=sayi(m.group(1)))
                else:
                    m=re.search(r"en ucuz .*? "+TL+" ",a)
                    out.update(tur="urun" if "/en-ucuz-" in u else "diger",en_dusuk=sayi(m.group(1)) if m else None)
    if "/en-ucuz-" in u and re.search(r"/[a-z0-9-]+/en-ucuz-[a-z0-9-]+-fiyatlari$",u) and out.get("tur")=="kategori": out["marka_kategori"]=True
    return out
if __name__=="__main__":
    c=json.load(open(KOK+"_cimri_ham.json"))
    for k,v in c.items():
        v["ayiklanan"]=[ayikla(r) for r in v["sonuclar"]]
    json.dump(c,open(KOK+"_cimri_ayiklanan.json","w"),ensure_ascii=False)
    n=sum(len(v["ayiklanan"]) for v in c.values()); ok=sum(1 for v in c.values() for x in v["ayiklanan"] if x.get("en_dusuk"))
    print(len(c),n,ok)
