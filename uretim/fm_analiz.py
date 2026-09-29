# -*- coding: utf-8 -*-
"""Fiyat manzarasi analizi: Shopping + sellers + Akakce + Cimri -> shopping.json, cimri_akakce.json, fiyat_matrisi.csv, vitra_saticilar.csv, _ozet_sayilar.json"""
import json, csv, re, collections, statistics as st, os
from fm_ortak import *
OFIS = "VitrA Online (vitra.com.tr)"
KANAL_KURAL = [("Trendyol",["trendyol"]),("Hepsiburada",["hepsiburada"]),("Amazon TR",["amazon"]),("Çiçeksepeti",["ciceksepeti","çiçeksepeti"]),
 ("Koçtaş",["koçtaş","koctas"]),("Bauhaus",["bauhaus"]),("IKEA",["ikea"]),("Tekzen",["tekzen"]),("Evidea",["evidea"]),
 (OFIS,["vitra online","vitra.com.tr"]),
 ("Diğer resmi marka mağazası",["creavit","e.c.a satış","eca satış","kale seramik","turkuaz"]),
 ("Diğer pazaryeri / genel perakende",["n11","pttavm","pazarama","idefix","a101","vivense","mediamarkt","teknosa","carrefour","migros","gittigidiyor"])]
def kanal(ad, domain=None):
    b=((ad or "")+" "+(domain or "")).lower()
    if "banyomarka" in b: return "Banyomarka (uzman e-ticaret)"
    for k,anah in KANAL_KURAL:
        if any(a in b for a in anah): return k
    return "Bağımsız banyo & yapı mağazası"
def medyan(x): return round(st.median(x),2) if x else None
def q(x,p):
    if not x: return None
    x=sorted(x); k=(len(x)-1)*p; f=int(k); c=min(f+1,len(x)-1); return round(x[f]+(x[c]-x[f])*(k-f),2)
# ------------- Shopping kategori -------------
ham=json.load(open(KOK+"_shopping_kategori_ham.json"))
satirlar=[]  # tum urunler
kw_ozet={}
for k,v in ham.items():
    if not v.get("items"): continue
    for i in v["items"]:
        if i["type"]!="google_shopping_serp" or not i.get("price"): continue
        satirlar.append({"kelime":k,"tip":TIP[k],"sira":i["rank_absolute"],"baslik":i["title"],"marka":marka_bul(i["title"]),"satici":i["seller"],
            "mecra":kanal(i["seller"]),"fiyat":float(i["price"]),"eski_fiyat":i.get("old_price"),"puan":i.get("product_rating"),"degerlendirme":i.get("reviews_count"),
            "product_id":i.get("product_id"),"data_docid":i.get("data_docid")})
# kelime bazli aykiri deger temizligi (kelime medyaninin 0.2x-5x disi = aksesuar/paket gurultusu)
temiz=[]; atilan=0
med_kw={k:st.median([s["fiyat"] for s in satirlar if s["kelime"]==k]) for k in set(s["kelime"] for s in satirlar)}
for s in satirlar:
    m=med_kw[s["kelime"]]
    if 0.2*m<=s["fiyat"]<=5*m: temiz.append(s)
    else: atilan+=1
# ayni tip icinde mukerrer (kelimeler arasi ortusme) temizligi
gor=set(); tekil=[]
for s in temiz:
    a=(s["tip"],s["satici"],s["baslik"],s["fiyat"])
    if a in gor: continue
    gor.add(a); tekil.append(s)
print("ham",len(satirlar),"aykiri atilan",atilan,"tekil",len(tekil))
# ------------- matris: tip x mecra -------------
MECRA_SIRA=["Trendyol","Hepsiburada","Amazon TR","Çiçeksepeti","Koçtaş","Bauhaus","IKEA",OFIS,"Diğer resmi marka mağazası","Banyomarka (uzman e-ticaret)","Diğer pazaryeri / genel perakende","Bağımsız banyo & yapı mağazası"]
matris=[]
tipler=sorted(set(s["tip"] for s in tekil))
for t in tipler:
    rows=[s for s in tekil if s["tip"]==t]
    tum=[s["fiyat"] for s in rows]
    resmi_vitra=[s["fiyat"] for s in rows if s["mecra"]==OFIS and s["marka"] in ("VitrA","Artema")]
    resmi_med=medyan(resmi_vitra)
    for m in MECRA_SIRA+["TÜM MECRALAR"]:
        f=[s["fiyat"] for s in rows if (m=="TÜM MECRALAR" or s["mecra"]==m)]
        if not f: continue
        vf=[s["fiyat"] for s in rows if (m=="TÜM MECRALAR" or s["mecra"]==m) and s["marka"] in ("VitrA","Artema")]
        matris.append({"urun_tipi":t,"mecra":m,"urun_adedi":len(f),"min":round(min(f),2),"p25":q(f,.25),"medyan":medyan(f),"p75":q(f,.75),"maks":round(max(f),2),
            "vitra_artema_adedi":len(vf),"vitra_artema_medyan":medyan(vf),
            "vitra_online_medyanina_fark_yuzde":round((medyan(vf)/resmi_med-1)*100,1) if (vf and resmi_med and m not in (OFIS,)) else None,
            "vitra_online_medyan":resmi_med})
with open(KOK+"fiyat_matrisi.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(matris[0].keys())); w.writeheader(); w.writerows(matris)
matris_v=[]
for t in tipler:
    rows=[s for s in tekil if s["tip"]==t and s["marka"] in ("VitrA","Artema")]
    ofr=[s["fiyat"] for s in rows if s["mecra"]==OFIS]
    for m in MECRA_SIRA+["TÜM MECRALAR"]:
        f=[s["fiyat"] for s in rows if (m=="TÜM MECRALAR" or s["mecra"]==m)]
        if not f: continue
        matris_v.append({"urun_tipi":t,"mecra":m,"marka_kapsami":"VitrA + Artema","urun_adedi":len(f),"min":round(min(f),2),"medyan":medyan(f),"maks":round(max(f),2),
            "vitra_online_medyan":medyan(ofr),"vitra_online_adet":len(ofr),
            "vitra_online_medyanina_fark_yuzde":round((medyan(f)/medyan(ofr)-1)*100,1) if (len(ofr)>=2 and m not in (OFIS,"TÜM MECRALAR")) else None})
with open(KOK+"fiyat_matrisi_vitra_artema.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(matris_v[0].keys())); w.writeheader(); w.writerows(matris_v)
# en ucuz mecra (medyan, n>=5) her tip
en_ucuz={}
for t in tipler:
    adaylar=[r for r in matris if r["urun_tipi"]==t and r["mecra"] not in ("TÜM MECRALAR",OFIS,"Diğer resmi marka mağazası") and r["urun_adedi"]>=5]
    tum=[r for r in matris if r["urun_tipi"]==t and r["mecra"]=="TÜM MECRALAR"][0]
    if adaylar:
        a=sorted(adaylar,key=lambda r:r["medyan"])
        en_ucuz[t]={"en_ucuz_mecra":a[0]["mecra"],"medyan":a[0]["medyan"],"en_pahali_mecra":a[-1]["mecra"],"en_pahali_medyan":a[-1]["medyan"],"tum_medyan":tum["medyan"],"tum_adet":tum["urun_adedi"]}
# ------------- marka ve magaza payi -------------
def pay(rows,alan):
    c=collections.Counter(s[alan] for s in rows); n=sum(c.values()); return [(k,v,round(v/n*100,1)) for k,v in c.most_common()]
kw_ham=[s for s in satirlar]  # payda: ham tum listeleme
marka_pay=pay(kw_ham,"marka"); satici_pay=pay(kw_ham,"satici"); mecra_pay=pay(kw_ham,"mecra")
ilk10=[s for s in kw_ham if s["sira"]<=10]
marka_pay10=pay(ilk10,"marka"); mecra_pay10=pay(ilk10,"mecra")
# marka bazli medyan fiyat (tip icinde en az 5 ilan)
marka_fiyat=[]
for t in tipler:
    rows=[s for s in tekil if s["tip"]==t]
    for mk in ("VitrA","Artema","Kale","Creavit","Turkuaz","ECA","Grohe","Serel","Seramiksan","Bocchi","Güral","Duravit","Hansgrohe","Geberit","Newarc","Franke","Blanco","Teka"):
        f=[s["fiyat"] for s in rows if s["marka"]==mk]
        if len(f)>=3: marka_fiyat.append({"tip":t,"marka":mk,"adet":len(f),"min":min(f),"medyan":medyan(f),"maks":max(f)})
# vitra.com.tr magazasi gorunurlugu
vo=[s for s in kw_ham if s["mecra"]==OFIS]
vo_kw=sorted(set(s["kelime"] for s in vo)); vo_urun=sorted(set(s["baslik"] for s in vo))
vo_ilk10=[s for s in vo if s["sira"]<=10]
vitra_marka_ilan=[s for s in kw_ham if s["marka"] in ("VitrA","Artema")]
vitra_marka_kanal=pay(vitra_marka_ilan,"mecra")
# ------------- sellers -------------
sel=json.load(open(KOK+"_sellers_ham.json"))
vs_satir=[]; vs_ozet=[]
for e in sel:
    its=e["sonuc"].get("items",[]) if isinstance(e["sonuc"],dict) else []
    if not its: continue
    rows=[]
    for i in its:
        fy=i.get("total_price") or i.get("base_price")
        if not fy: continue
        rows.append({"satici":i["title"],"domain":i["domain"],"mecra":kanal(i["title"],i["domain"]),"fiyat":float(fy),"baz_fiyat":i.get("base_price"),"kargo":i.get("shipping_price"),"stok":i.get("product_availability")})
    rows.sort(key=lambda r:r["fiyat"])
    ofr=[r for r in rows if r["mecra"]==OFIS]
    for n,r in enumerate(rows,1):
        vs_satir.append({"urun_sorgusu":e["sorgu"],"liste_basligi":e["sonuc"].get("title") or e["liste_basligi"],"fiyat_sirasi":n,"satici":r["satici"],"alan_adi":r["domain"],"mecra":r["mecra"],
            "fiyat_try":r["fiyat"],"kargo_try":r["kargo"],"stok":r["stok"],"en_ucuz":"Evet" if n==1 else "","vitra_online_fark_yuzde":round((r["fiyat"]/ofr[0]["fiyat"]-1)*100,1) if ofr and r["mecra"]!=OFIS else ""})
    f=[r["fiyat"] for r in rows]
    vs_ozet.append({"urun_sorgusu":e["sorgu"],"liste_basligi":e["sonuc"].get("title") or e["liste_basligi"],"satici_sayisi":len(rows),"en_ucuz_satici":rows[0]["satici"],"en_ucuz_mecra":rows[0]["mecra"],
        "en_dusuk":min(f),"medyan":medyan(f),"en_yuksek":max(f),"yayilim_yuzde":round((max(f)/min(f)-1)*100,1),
        "vitra_online_var":bool(ofr),"vitra_online_fiyat":ofr[0]["fiyat"] if ofr else None,"vitra_online_sira":[n for n,r in enumerate(rows,1) if r["mecra"]==OFIS][0] if ofr else None,
        "vitra_online_en_dusuge_fark_yuzde":round((ofr[0]["fiyat"]/min(f)-1)*100,1) if ofr else None})
with open(KOK+"vitra_saticilar.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(vs_satir[0].keys())); w.writeheader(); w.writerows(vs_satir)
kanal_ozet=[]
for m in MECRA_SIRA:
    listeler=collections.defaultdict(list)
    for r in vs_satir:
        listeler[(r["urun_sorgusu"],r["liste_basligi"])].append(r)
    var=0; ucuz=0; oranlar=[]
    for kx,rs in listeler.items():
        mn=min(r["fiyat_try"] for r in rs)
        mm=[r for r in rs if r["mecra"]==m]
        if mm:
            var+=1; oranlar.append(min(r["fiyat_try"] for r in mm)/mn-1)
            if rs[0]["mecra"]==m: ucuz+=1
    if var: kanal_ozet.append({"mecra":m,"listede_gorulme":var,"liste_toplam":len(listeler),"en_ucuz_sayisi":ucuz,"en_dusuk_fiyata_medyan_fark_yuzde":round(st.median(oranlar)*100,1)})
# ------------- json ciktilar -------------
json.dump({"kapsam":"Google Shopping Turkiye (location 2792, tr), 2026-09-29, DataForSEO merchant/google/products (depth 120) + sellers","kategori_kelimeleri":KATEGORILER,
    "ilanlar":satirlar,"vitra_urun_listeleri":[{"sorgu":k,"liste":[{"sira":i["rank_absolute"],"baslik":i["title"],"satici":i["seller"],"fiyat":i["price"]} for i in v.get("items",[]) if i["type"]=="google_shopping_serp"]} for k,v in json.load(open(KOK+"_shopping_urun_ham.json")).items()],
    "vitra_saticilar":vs_ozet},open(KOK+"shopping.json","w"),ensure_ascii=False,indent=0)
ozet={"ilan_ham":len(satirlar),"aykiri":atilan,"ilan_tekil":len(tekil),"kelime":len([k for k,v in ham.items() if v.get("items")]),
 "matris":matris,"en_ucuz":en_ucuz,"marka_pay":marka_pay,"marka_pay10":marka_pay10,"satici_pay":satici_pay[:25],"mecra_pay":mecra_pay,"mecra_pay10":mecra_pay10,"marka_fiyat":marka_fiyat,
 "vitra_online":{"ilan":len(vo),"kelime":len(vo_kw),"kelimeler":vo_kw,"tekil_urun":len(vo_urun),"ilk10_ilan":len(vo_ilk10),"toplam_ilan":len(kw_ham)},
 "vitra_marka_ilan":len(vitra_marka_ilan),"vitra_marka_kanal":vitra_marka_kanal,"vs_ozet":vs_ozet,"kanal_ozet":kanal_ozet,"matris_vitra":matris_v}
json.dump(ozet,open(KOK+"_ozet_sayilar.json","w"),ensure_ascii=False,indent=1)
print("ok")
