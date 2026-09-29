# -*- coding: utf-8 -*-
"""Akakce yedek yolu: dogrudan erisim ~15 istek sonrasi Cloudflare challenge verdi (asilmadi, fm_akakce.py durduruldu).
Google SERP ozetleri (DataForSEO organic live) uzerinden akakce.com sonuclari: baslik, en dusuk fiyat, secenek sayisi. Maliyet kaydedilir."""Cimri: akakce.com dogrudan 403 (Cloudflare; curl ve Apify rag-web-browser ikisinde de). Yedek: Google SERP ozetleri (DataForSEO organic live) uzerinden
akakce.com sonuclari: urun/kategori basligi, en dusuk fiyat, satici sayisi. Maliyet kaydedilir."""
import json, time
import dfs
from fm_ortak import *
LOG=KOK+"maliyet_dfs.jsonl"
cikti=KOK+"_akakce_serp_ham.json"
try: veri=json.load(open(cikti))
except Exception: veri={}
def sorgula(q):
    o=dfs.post("/v3/serp/google/organic/live/regular",[{"keyword":q,"location_code":2792,"language_code":"tr","depth":10,"device":"desktop"}])
    t=o["tasks"][0]
    open(LOG,"a").write(json.dumps({"is":"serp_akakce:"+q,"maliyet_usd":t.get("cost",0),"not":t["status_message"],"zaman":time.strftime("%Y-%m-%d %H:%M:%S")},ensure_ascii=False)+"\n")
    items=[]
    for i in (t.get("result") or [{}])[0].get("items",[]) if t.get("result") else []:
        if i["type"]=="organic" and "akakce.com" in (i.get("domain") or ""):
            items.append({"sira":i["rank_absolute"],"url":i["url"],"baslik":i["title"],"aciklama":i.get("description")})
    return items
sorgular=[]
for k in KATEGORILER: sorgular += [("kategori_site",k,"site:akakce.com "+k),("kategori_liste",k,"akakce "+k+" fiyatları")]
for k in VITRA_URUNLER: sorgular.append(("vitra",k,"site:akakce.com "+k))
for tur,k,q in sorgular:
    anahtar=tur+"|"+k
    if anahtar in veri: continue
    veri[anahtar]={"sorgu":q,"sonuclar":sorgula(q)}
    print(anahtar,len(veri[anahtar]["sonuclar"]),flush=True)
    json.dump(veri,open(cikti,"w"),ensure_ascii=False); bekle()
print("BITTI")
