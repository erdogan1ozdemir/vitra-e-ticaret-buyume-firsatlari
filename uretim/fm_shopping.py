# -*- coding: utf-8 -*-
"""Google Shopping (DataForSEO merchant API, task tabanli): kategori kelimeleri + VitrA urun adlari -> sellers."""
import json, sys, time
import dfs
from fm_ortak import *
LOG = KOK+"maliyet_dfs.jsonl"
def kayit(ad, cost, ek=""):
    open(LOG,"a").write(json.dumps({"is":ad,"maliyet_usd":cost,"not":ek,"zaman":time.strftime("%Y-%m-%d %H:%M:%S")},ensure_ascii=False)+"\n")
def gorev_gonder(endpoint, payload, ad):
    o = dfs.post("/v3/merchant/google/%s/task_post"%endpoint,[payload])
    t = o["tasks"][0]
    kayit(ad, t.get("cost",0), t["status_message"])
    return t["id"] if t["status_code"]==20100 else None
def sonuc_al(endpoint, tid, bekleme=60):
    for _ in range(bekleme//6+4):
        r = dfs_get("/v3/merchant/google/%s/task_get/advanced/%s"%(endpoint,tid))
        t = r["tasks"][0]
        if t["status_code"]==20000: return t["result"][0]
        if t["status_code"] not in (40602,40601): return {"hata":t["status_code"],"mesaj":t["status_message"]}
        time.sleep(6)
    return {"hata":"zaman_asimi"}
if __name__=="__main__":
    asama = sys.argv[1]
    if asama=="kategori":
        gorevler = {}
        for k in KATEGORILER:
            gorevler[k] = gorev_gonder("products",{"keyword":k,"location_code":2792,"language_code":"tr","depth":120,"tag":k},"products:"+k)
            print(k, gorevler[k], flush=True); bekle()
        json.dump(gorevler,open(KOK+"_gorev_kategori.json","w"),ensure_ascii=False)
        sonuc = {}
        for k,tid in gorevler.items():
            sonuc[k] = sonuc_al("products",tid) if tid else {"hata":"gorev_yok"}
            print("sonuc",k,len(sonuc[k].get("items",[])) if isinstance(sonuc[k],dict) else 0, sonuc[k].get("hata",""), flush=True)
        json.dump(sonuc,open(KOK+"_shopping_kategori_ham.json","w"),ensure_ascii=False)
    elif asama=="urun":
        gorevler = {}
        for k in VITRA_URUNLER:
            gorevler[k] = gorev_gonder("products",{"keyword":k,"location_code":2792,"language_code":"tr","depth":40,"tag":k},"products_urun:"+k)
            print(k, gorevler[k], flush=True); bekle()
        sonuc = {}
        for k,tid in gorevler.items():
            sonuc[k] = sonuc_al("products",tid) if tid else {"hata":"gorev_yok"}
            print("sonuc",k,len(sonuc[k].get("items",[])), sonuc[k].get("hata",""), flush=True)
        json.dump(sonuc,open(KOK+"_shopping_urun_ham.json","w"),ensure_ascii=False)
