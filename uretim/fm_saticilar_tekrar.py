# -*- coding: utf-8 -*-
"""fm_saticilar.py'de zaman asimina ugrayan sellers gorevlerini yeniden dener."""
import json
from fm_ortak import *
from fm_shopping import gorev_gonder, sonuc_al
ANAH = {"vitra s20 asma klozet":"s20","vitra integra asma klozet":"integra","vitra integra klozet kapağı":"integra","vitra root lavabo dolabı":"root",
 "vitra sento asma klozet":"sento","vitra metropole asma klozet":"metropole","vitra shift asma klozet":"shift","vitra nest trendy asma klozet":"nest",
 "artema solid s lavabo bataryası":"solid","artema minimax s lavabo bataryası":"minimax","artema flo s banyo bataryası":"flo s","vitra sento lavabo dolabı":"sento"}
u=json.load(open(KOK+"_shopping_urun_ham.json")); eski=json.load(open(KOK+"_sellers_ham.json"))
idx={}
for k,v in u.items():
    n=0
    for i in v["items"]:
        if i.get("type")!="google_shopping_serp": continue
        b=(i["title"] or "").lower()
        if ANAH[k] in b and ("vitra" in b or "artema" in b) and i["data_docid"]:
            idx.setdefault(k,[]).append(i); n+=1
        if n>=2: break
sayac={}
for e in eski:
    k=e["sorgu"]; j=sayac.get(k,0); sayac[k]=j+1
    if "hata" in e["sonuc"]:
        i=idx[k][j]; p={"location_code":2792,"language_code":"tr","data_docid":i["data_docid"],"tag":k}
        if i["product_id"]: p["product_id"]=i["product_id"]
        if i["gid"]: p["gid"]=i["gid"]
        tid=gorev_gonder("sellers",p,"sellers_tekrar:"+k); bekle()
        e["sonuc"]=sonuc_al("sellers",tid,bekleme=180); print(k,e["sonuc"].get("hata",""),len(e["sonuc"].get("items",[])),flush=True)
json.dump(eski,open(KOK+"_sellers_ham.json","w"),ensure_ascii=False)
