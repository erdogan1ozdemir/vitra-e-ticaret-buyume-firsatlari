# -*- coding: utf-8 -*-
"""Cimri + Akakce verilerini birlestirir -> cimri_akakce.json ; kategori/model karsilastirma tablolari (_karsilastirma.json)."""
import json, re, statistics as st
from fm_ortak import *
from fm_cimri_ayikla import ayikla as cimri_ayikla, sayi
import fm_akakce as AK
SCR="/private/tmp/claude-501/-Users-Erdo-Desktop-Claude-Projects-Vitra/dbdc56cb-c768-473e-95dd-d0ee7d3212ec/scratchpad/"
# ---------- Akakce dogrudan (curl, 200 donen sayfalar) ----------
ad=json.load(open(KOK+"_akakce_ham.json"))
dogrudan={"kategori":{},"vitra":{}}
for k,v in ad["kategori"].items():
    if v["kod"]==200:
        dogrudan["kategori"][k]={"sayfa_url":v["son_url"],"toplam_urun":v["toplam"],"ilk_sayfa_urun_sayisi":len(v["liste"]),
          "ilk_sayfa":[{"marka":u["marka"],"urun":u["urun"],"en_dusuk_fiyat":u["en_dusuk_fiyat"],"ek_fiyat_sayisi":u["ek_fiyat_sayisi"],"url":u["url"]} for u in v["liste"]],
          "urun_sayfalari":[d for d in v["detay"] if d["sayfa"]]}
# erken (ilk 429 oncesi) alinmis VitrA S20 orneği (scratchpad)
try:
    h=open(SCR+"s20srch.html").read(); it=AK.liste_ayikla(h)
    h2=open(SCR+"p1.html").read()
    dogrudan["vitra"]["vitra s20 asma klozet"]={"arama_listesi":[u for u in it if u["marka"]=="VitrA"][:12],"urun_sayfasi":AK.urun_sayfasi(h2)}
except Exception as e: print("s20 ornek yok",e)
# ---------- Akakce SERP ----------
asp=json.load(open(KOK+"_akakce_serp_ham.json"))
def _a(x): return x.lower().replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g").replace("ö","o").replace("ü","u").replace("i̇","i")
def _slug(k): return re.sub(r"\s+","-",_a(k))
def ak_kategori(k):
    sl=_slug(k)
    for tur in ("kategori_liste","kategori_site"):
        for r in asp.get(tur+"|"+k,{}).get("sonuclar",[]):
            a=(r["aciklama"] or "")
            m=re.search(r"([\d\.]+) farklı (?:.*?)seçenek",a) or re.search(r"([\d\.]+) farklı ",a)
            f=re.search(r"([\d\.]+(?:,\d+)?) ?TL'den başlayan",a)
            if m and re.search(r"akakce\.com/[a-z0-9-]+(/[a-z0-9-]+)?\.html$",r["url"]) and (sl in r["url"] or tur=="kategori_liste"):
                return {"url":r["url"],"secenek":int(m.group(1).replace(".","")),"baslangic_fiyat":sayi(f.group(1)) if f else None,"tam_eslesme":r["url"].endswith("/"+sl+".html")}
    return None
AKV=re.compile(r"((?:VitrA|Vitra|Artema)[^;·|]{3,90}?)\s+(?:Çok Renkli\.? )?(?:En [Uu]cuz|En ucuz fiyat)?\s*([\d\.]+,\d{2}) TL\s*(?:\+(\d+) FİYAT|TEK FİYAT|En ucuz fiyat (\d+) satıcı)?")
def ak_vitra(k):
    out={}
    for r in asp.get("vitra|"+k,{}).get("sonuclar",[]):
        metin=(r["baslik"] or "")+" || "+(r["aciklama"] or "")
        for m in AKV.finditer(metin):
            ad=m.group(1).strip(" .,"); 
            if len(ad)<8: continue
            out[ad]={"en_dusuk":sayi(m.group(2)),"fiyat_sayisi":int(m.group(3) or m.group(4) or 1)}
        m=re.search(r"(\d+) satıcı arasındaki en ucuz (.*?) ;? ?fiyatı ([\d\.]+,\d{2}) TL",metin)
        if m: out[m.group(2).strip(" ;")]={"en_dusuk":sayi(m.group(3)),"fiyat_sayisi":int(m.group(1))}
    return out
# ---------- Cimri ----------
cm=json.load(open(KOK+"_cimri_ham.json"))
for v in cm.values(): v["ayiklanan"]=[cimri_ayikla(r) for r in v["sonuclar"]]
def cm_kategori(k):
    adaylar=[]
    for tur in ("kategori_liste","kategori_site"):
        for x in cm.get(tur+"|"+k,{}).get("ayiklanan",[]):
            if x.get("tur")=="kategori" and "?page=" not in x["url"] and not x.get("marka_kategori") and x.get("secenek_sayisi") and "/vitra-" not in x["url"] and "/creavit" not in x["url"]:
                adaylar.append(x)
    # kelimeye en yakin baslik: kelime tokenlarini iceren ve en kisa baslik
    tok=[t for t in re.split(r"\s+",k.lower())]
    def skor(x):
        b=x["baslik"].lower().replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g").replace("ö","o").replace("ü","u")
        tt=[t.replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g").replace("ö","o").replace("ü","u") for t in tok]
        return (-sum(1 for t in tt if t in b), len(b))
    sl=_slug(k)
    def tam(x):
        p=x["url"].split("cimri.com/")[1]
        return 0 if p in (sl,sl+"-fiyatlari","en-ucuz-"+sl,sl+"-modelleri","en-ucuz-"+sl+"-fiyatlari") else 1
    adaylar.sort(key=lambda x:(tam(x),)+skor(x))
    if adaylar: x=adaylar[0]; return {"url":x["url"],"baslik":x["baslik"],"secenek":x["secenek_sayisi"],"baslangic_fiyat":x.get("en_dusuk"),"tam_eslesme":tam(x)==0}
    return None
def cm_marka(k):
    out={}
    for tur in ("kategori_liste","kategori_site"):
        for x in cm.get(tur+"|"+k,{}).get("ayiklanan",[]):
            if x.get("marka_kategori") and "?page=" not in x["url"]:
                mk=x["baslik"].split(" ")[0]; out[mk]={"baslik":x["baslik"],"urun_sayisi":x.get("secenek_sayisi"),"baslangic_fiyat":x.get("en_dusuk"),"url":x["url"]}
            elif x.get("tur")=="kategori" and re.search(r"/vitra-|/creavit|/kale|/artema",x["url"]) and "?page=" not in x["url"]:
                mk=x["baslik"].split(" ")[0]; out.setdefault(mk,{"baslik":x["baslik"],"urun_sayisi":x.get("secenek_sayisi"),"baslangic_fiyat":x.get("en_dusuk"),"url":x["url"]})
    return out
def cm_vitra(k):
    out=[]
    for x in cm.get("vitra|"+k,{}).get("ayiklanan",[]):
        if x.get("tur")=="urun" and x.get("en_dusuk") and re.search(r"vitra|artema",x["baslik"],re.I) and "Sayfa" not in x["baslik"] and "?page" not in x["url"]:
            out.append({"urun":x["baslik"],"en_dusuk":x["en_dusuk"],"satici_sayisi":x.get("satici_sayisi"),"fiyat_tarihi":x.get("fiyat_tarihi"),"url":x["url"]})
    return out
MARKALAR_CM=["vitra","artema","creavit","kale","turkuaz","eca","grohe","serel","bocchi","seramiksan","geberit","duravit","hansgrohe","bien","isvea","franke","blanco","teka"]
marka_sayfalari=[]
for kk,v in cm.items():
    for x in v["ayiklanan"]:
        m=re.search(r"cimri\.com/([a-z0-9-]+)/en-ucuz-([a-z0-9]+)-([a-z0-9-]+)-fiyatlari$",x["url"]) or re.search(r"cimri\.com/([a-z0-9-]+)/([a-z0-9]+)-([a-z0-9-]+)$",x["url"])
        if m and m.group(2) in MARKALAR_CM and x.get("secenek_sayisi") and "?page" not in x["url"]:
            marka_sayfalari.append({"kaynak":"Cimri","kategori":m.group(1),"marka":m.group(2),"urun_sayisi":x["secenek_sayisi"],"baslangic_fiyat":x.get("en_dusuk"),"url":x["url"]})
for kk,v in asp.items():
    for r in v["sonuclar"]:
        m=re.search(r"akakce\.com/([a-z0-9-]+)/([a-z0-9-]+)\.html$",r["url"]); a=r["aciklama"] or ""
        n=re.search(r"([\d\.]+) farklı",a); f=re.search(r"([\d\.]+(?:,\d+)?) ?TL'den başlayan",a)
        if m and m.group(2) in MARKALAR_CM and n:
            marka_sayfalari.append({"kaynak":"Akakçe","kategori":m.group(1),"marka":m.group(2),"urun_sayisi":int(n.group(1).replace(".","")),"baslangic_fiyat":sayi(f.group(1)) if f else None,"url":r["url"]})
_g={}
for x in marka_sayfalari: _g[(x["kaynak"],x["kategori"],x["marka"])]=x
marka_sayfalari=list(_g.values())
kat={}
for k in KATEGORILER:
    kat[k]={"tip":TIP[k],"cimri":cm_kategori(k),"cimri_markalar":cm_marka(k),"akakce_serp":ak_kategori(k),"akakce_dogrudan":{kk:dogrudan["kategori"][k][kk] for kk in ("sayfa_url","toplam_urun")} if k in dogrudan["kategori"] else None}
vt={}
for k in VITRA_URUNLER:
    vt[k]={"cimri":cm_vitra(k),"akakce_serp":ak_vitra(k),"akakce_dogrudan":dogrudan["vitra"].get(k)}
json.dump({"kapsam":"Cimri ve Akakce: 2026-09-29. Akakce: curl (tarayici UA) ile ilk ~15 istek 200, ardindan 429 + Cloudflare challenge (asilmadi). Cimri: dogrudan 403 (curl ve Apify rag-web-browser). Her iki sitenin geri kalani Google SERP ozetlerinden (DataForSEO organic live) okundu.",
  "kategori":kat,"vitra_urunleri":vt,"marka_sayfalari":marka_sayfalari,"akakce_dogrudan":dogrudan,"cimri_serp_ayiklanan":{k:v["ayiklanan"] for k,v in cm.items()},"akakce_serp_ham":{k:v["sonuclar"] for k,v in asp.items()}},
  open(KOK+"cimri_akakce.json","w"),ensure_ascii=False)
json.dump({"kategori":kat,"vitra":vt,"marka_sayfalari":marka_sayfalari},open(KOK+"_karsilastirma.json","w"),ensure_ascii=False,indent=1)
print("kategori cimri",sum(1 for v in kat.values() if v["cimri"]),"akakce",sum(1 for v in kat.values() if v["akakce_serp"]),"/",len(kat))
print("vitra cimri",sum(1 for v in vt.values() if v["cimri"]),"akakce",sum(1 for v in vt.values() if v["akakce_serp"]),"/",len(vt))
for k,v in kat.items(): print(k,"|",v["cimri"] and (v["cimri"]["secenek"],v["cimri"]["baslangic_fiyat"]),"|",v["akakce_serp"] and (v["akakce_serp"]["secenek"],v["akakce_serp"]["baslangic_fiyat"]),"|",list(v["cimri_markalar"].keys())[:6])
for k,v in vt.items(): print(k,"|",[(x["urun"][:30],x["en_dusuk"]) for x in v["cimri"]][:3],"|",list(v["akakce_serp"].items())[:2])
