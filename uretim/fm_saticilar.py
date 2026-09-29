# -*- coding: utf-8 -*-
"""VitrA urunleri: merchant/google/sellers (her urun aramasi icin en iyi 2 eslesen liste)."""
import json, time
from fm_ortak import *
from fm_shopping import gorev_gonder, sonuc_al
ANAH = {"vitra s20 asma klozet":"s20","vitra integra asma klozet":"integra","vitra integra klozet kapağı":"integra","vitra root lavabo dolabı":"root",
 "vitra sento asma klozet":"sento","vitra metropole asma klozet":"metropole","vitra shift asma klozet":"shift","vitra nest trendy asma klozet":"nest",
 "artema solid s lavabo bataryası":"solid","artema minimax s lavabo bataryası":"minimax","artema flo s banyo bataryası":"flo s","vitra sento lavabo dolabı":"sento"}
u = json.load(open(KOK+"_shopping_urun_ham.json"))
secim = []
for k,v in u.items():
    n=0
    for i in v["items"]:
        if i.get("type")!="google_shopping_serp": continue
        b=(i["title"] or "").lower()
        if ANAH[k] in b and ("vitra" in b or "artema" in b) and i["data_docid"]:
            secim.append((k,i)); n+=1
        if n>=2: break
print(len(secim),"liste secildi")
gorevler=[]
for k,i in secim:
    p={"location_code":2792,"language_code":"tr","data_docid":i["data_docid"],"tag":k}
    if i["product_id"]: p["product_id"]=i["product_id"]
    if i["gid"]: p["gid"]=i["gid"]
    tid=gorev_gonder("sellers",p,"sellers:"+k+":"+i["title"][:40]); gorevler.append((k,i,tid)); print(k,tid,flush=True); bekle()
sonuc=[]
for k,i,tid in gorevler:
    r=sonuc_al("sellers",tid) if tid else {"hata":"gorev_yok"}
    print("sonuc",k,r.get("hata",""),len(r.get("items",[])) if isinstance(r,dict) else 0,flush=True)
    sonuc.append({"sorgu":k,"liste_basligi":i["title"],"ilk_fiyat":i["price"],"ilk_satici":i["seller"],"sonuc":r})
json.dump(sonuc,open(KOK+"_sellers_ham.json","w"),ensure_ascii=False)
