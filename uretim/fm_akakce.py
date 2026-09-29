# -*- coding: utf-8 -*-
"""Akakce: kategori kelimeleri (arama/kategori listesi ilk sayfa, curl + tarayici UA) ve VitrA urun sayfalari (JSON-LD AggregateOffer)."""
import json, re, subprocess, sys, html, time, urllib.parse
from fm_ortak import *
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
def getir(url):
    for deneme in range(6):
        kod,son,h = _getir(url)
        if kod != 429: return kod,son,h
        time.sleep(180*(deneme+1))   # 429: geri cekil
    return kod,son,h
def _getir(url):
    r = subprocess.run(["curl","-s","-L","-m","40","-A",UA,"-H","Accept-Language: tr-TR,tr;q=0.9","-w","\n__KOD__%{http_code}|%{url_effective}",url],capture_output=True)
    s = r.stdout.decode("utf-8","replace"); i = s.rfind("\n__KOD__"); kod,son = s[i+8:].split("|",1)
    return int(kod or 0), son, s[:i]
def fiyat_say(tl):  # "6.750" -> 6750
    return float(tl.replace(".","")) if tl else None
def liste_ayikla(h):
    out=[]
    for blok in h.split('<li data-pr=')[1:]:
        m_id=re.match(r'"(\d+)" data-mk="([^"]*)"',blok)
        t=re.search(r'title="([^"]*)" class="iC"',blok); href=re.search(r'href="([^"]*)" title="[^"]*" class="iC"',blok)
        p=re.search(r'pt_v9">\s*([\d\.]+)<i>,(\d+) TL',blok); n=re.search(r'\+(\d+) F',blok)
        if not (m_id and t and p): continue
        out.append({"id":m_id.group(1),"marka":m_id.group(2),"urun":html.unescape(t.group(1)),"en_dusuk_fiyat":fiyat_say(p.group(1))+int(p.group(2))/100,
                    "ek_fiyat_sayisi":int(n.group(1)) if n else 0,"url":"https://www.akakce.com"+href.group(1) if href else None})
    return out
def urun_sayfasi(h):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try: d=json.loads(m.group(1))
        except Exception: continue
        if isinstance(d,dict) and d.get("@type")=="Product":
            o=d.get("offers",{}); ofs=o.get("offers",[]) if isinstance(o,dict) else []
            sat=[]
            for x in ofs:
                ad=x.get("seller",{}).get("name","")
                sat.append({"satici":ad.split("/")[0],"fiyat":float(x["price"]) if x.get("price") else None})
            return {"ad":d.get("name"),"marka":(d.get("brand") or {}).get("name"),"teklif_sayisi":int(o.get("offerCount",0) or 0),
                    "en_dusuk":float(o["lowPrice"]) if o.get("lowPrice") else None,"en_yuksek":float(o["highPrice"]) if o.get("highPrice") else None,"saticilar":sat}
    return None
if __name__=="__main__":
    cikti=KOK+"_akakce_ham.json"
    try: veri=json.load(open(cikti))
    except Exception: veri={"kategori":{},"vitra":{}}
    log=open(KOK+"akakce.log","a")
    def yaz(s): log.write(s+"\n"); log.flush(); print(s,flush=True)
    for k in KATEGORILER:
        if veri["kategori"].get(k,{}).get("kod")==200: continue
        kod,son,h=getir("https://www.akakce.com/arama/?q="+urllib.parse.quote(k)); bekle(7,11)
        it=liste_ayikla(h) if kod==200 else []
        toplam=re.search(r'"numberOfItems":(\d+)',h); 
        detay=[]
        for u in it[:3]:
            if not u["url"]: continue
            kod2,_,h2=getir(u["url"]); bekle(7,11)
            detay.append({"urun":u["urun"],"marka":u["marka"],"sayfa":urun_sayfasi(h2) if kod2==200 else None,"kod":kod2,"url":u["url"]})
        veri["kategori"][k]={"kod":kod,"son_url":son,"toplam":int(toplam.group(1)) if toplam else None,"liste":it,"detay":detay}
        yaz("kategori %s kod=%s liste=%d detay=%d toplam=%s son=%s"%(k,kod,len(it),len(detay),toplam.group(1) if toplam else None,son))
        json.dump(veri,open(cikti,"w"),ensure_ascii=False)
    for k in VITRA_URUNLER:
        if veri["vitra"].get(k,{}).get("kod")==200: continue
        kod,son,h=getir("https://www.akakce.com/arama/?q="+urllib.parse.quote(k)); bekle(7,11)
        it=liste_ayikla(h) if kod==200 else []
        anah=[w for w in k.split() if w not in ("vitra","artema","asma","klozet","lavabo","bataryası","dolabı","banyo","kapağı")]
        secili=[u for u in it if any(a in u["urun"].lower() for a in anah) and u["marka"] in ("VitrA","Artema")][:3] or [u for u in it if u["marka"] in ("VitrA","Artema")][:2]
        detay=[]
        for u in secili:
            kod2,_,h2=getir(u["url"]); bekle(7,11)
            detay.append({"urun":u["urun"],"marka":u["marka"],"sayfa":urun_sayfasi(h2) if kod2==200 else None,"kod":kod2,"url":u["url"]})
        veri["vitra"][k]={"kod":kod,"liste_sayisi":len(it),"liste":it[:12],"detay":detay}
        yaz("vitra %s kod=%s liste=%d detay=%d"%(k,kod,len(it),len(detay)))
        json.dump(veri,open(cikti,"w"),ensure_ascii=False)
    yaz("BITTI")
