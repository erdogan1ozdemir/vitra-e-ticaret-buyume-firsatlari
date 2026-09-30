# -*- coding: utf-8 -*-
"""Pazaryeri panel verileri (Trendyol satici paneli, Hepsiburada) -> veri/islenmis/panel.json.
Cikti kisisel veri ve TL ciro tutari icermez; yalnizca adet, pay, oran ve medyan fiyat tasir.
Ham dosyalar: pazaryeri-verileri/ (depoya alinmaz)."""
import os, re, glob, json, zipfile, warnings
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV = os.path.join(KOK, "pazaryeri-verileri"); TY = os.path.join(PV, "trendyol"); HBD = os.path.join(PV, "HB")
OUT = os.path.join(KOK, "veri", "islenmis", "panel.json")
def num(s): return pd.to_numeric(s, errors="coerce")
Q = {"18.41.42": "2025Q4", "18.42.51": "2026Q1", "18.43.21": "2026Q2", "18.43.38": "2026Q3"}
QD = {"18.41.06": "2025Q4", "18.38.43": "2026Q1", "18.39.09": "2026Q2", "18.39.37": "2026Q3"}
CEY = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
R = {}
# ---------------- satis raporu
fr = []
for f in glob.glob(os.path.join(TY, "seller-144409-satış-raporu-*.xlsx")):
    q = [v for k, v in Q.items() if k in f][0]
    d = pd.read_excel(f, sheet_name="urun-bazlı-satış-raporu"); d["q"] = q; fr.append(d)
U = pd.concat(fr)
for c in ["Brüt Satış Adedi", "İptal Adedi", "İade Adedi", "Net Satış Adedi", "Brüt Ciro", "İndirim Tutarı", "Net Ciro", "Toplam Komisyon Tutarı", "Ortalama Satış Fiyatı", "Güncel Satış Fiyatı", "Güncel Stok"]:
    U[c] = num(U[c])
# urun adi yedegi: favori-goruntuleme raporlarindan model kodu -> ad
FV = []
for f in glob.glob(os.path.join(TY, "seller-144409-favori-görüntüleme-raporu-*.xlsx")):
    d = pd.read_excel(f); d["dosya"] = os.path.basename(f); FV.append(d)
ADM = {}
for d in FV:
    for _, r in d.iterrows():
        if isinstance(r.get("Ürün Adı"), str) and r["Ürün Adı"].strip(): ADM.setdefault(str(r["Model Kodu"]).strip(), r["Ürün Adı"].strip())
U["ad"] = U.apply(lambda r: r["Ürün Adı"] if isinstance(r["Ürün Adı"], str) and r["Ürün Adı"].strip() else ADM.get(str(r["Model Kodu"]).strip()), axis=1)
KATM = U.dropna(subset=["Kategori"]).groupby("Model Kodu")["Kategori"].first()
U["Kategori"] = U["Kategori"].fillna(U["Model Kodu"].map(KATM))
MRKM = U.dropna(subset=["Marka"]).groupby("Model Kodu")["Marka"].first().to_dict()
U["Marka"] = U["Marka"].fillna(U["Model Kodu"].map(MRKM))
for d_ in FV:
    for _, r_ in d_.iterrows():
        if isinstance(r_.get("Marka"), str): MRKM.setdefault(r_["Model Kodu"], r_["Marka"])
U["Marka"] = U["Marka"].fillna(U["Model Kodu"].map(MRKM))
cey = []
for q in CEY:
    d = U[U.q == q]
    brut, net = d["Brüt Satış Adedi"].sum(), d["Net Satış Adedi"].sum()
    art = d[d.Marka == "Artema"]["Net Satış Adedi"].sum()
    cey.append({"q": q, "net": int(net), "model": int(d["Model Kodu"].nunique()), "artema_pay": art / net * 100,
                "ort_fiyat": d["Net Ciro"].sum() / net, "indirim": d["İndirim Tutarı"].sum() / d["Brüt Ciro"].sum() * 100,
                "iptal": d["İptal Adedi"].sum() / brut * 100, "iade": d["İade Adedi"].sum() / brut * 100,
                "komisyon": d["Toplam Komisyon Tutarı"].sum() / d["Net Ciro"].sum() * 100})
R["ceyrek"] = cey
# kategori
tc = U["Net Ciro"].sum(); tn = U["Net Satış Adedi"].sum()
RV = pd.concat([pd.read_excel(f) for f in glob.glob(os.path.join(TY, "seller-144409-urun-degerlendirmeleri-*.xlsx"))]).drop_duplicates()
RV["puan"] = num(RV["Değerlendirme Puanı"]); RV["t"] = pd.to_datetime(RV["Değerlendirme Tarihi"], format="%d-%m-%Y %H:%M")
kat = []
for k, d in U.groupby("Kategori"):
    net = d["Net Satış Adedi"].sum()
    if net < 25: continue
    rv = RV[RV.Kategori == k]
    q4 = d[d.q == "2025Q4"]["Net Satış Adedi"].sum(); q3 = d[d.q == "2026Q3"]["Net Satış Adedi"].sum()
    kat.append({"kategori": k, "net": int(net), "adet_pay": net / tn * 100, "ciro_pay": d["Net Ciro"].sum() / tc * 100, "ort_fiyat": d["Net Ciro"].sum() / net,
                "iptal": d["İptal Adedi"].sum() / d["Brüt Satış Adedi"].sum() * 100, "iade": d["İade Adedi"].sum() / d["Brüt Satış Adedi"].sum() * 100,
                "puan": float(rv.puan.mean()) if len(rv) >= 5 else None, "deg": int(len(rv)), "dusuk": float((rv.puan <= 2).mean() * 100) if len(rv) >= 5 else None,
                "q4": int(q4), "q3": int(q3)})
R["kategori"] = sorted(kat, key=lambda r: -r["ciro_pay"])
# urun
P = U.groupby("Model Kodu").agg(ad=("ad", "first"), kat=("Kategori", "first"), marka=("Marka", "first"), net=("Net Satış Adedi", "sum"), brut=("Brüt Satış Adedi", "sum"),
                                 iade=("İade Adedi", "sum"), ciro=("Net Ciro", "sum"), stok=("Güncel Stok", "last"))
P = P[P.net > 0]
P["adet_pay"] = P.net / tn * 100; P["ciro_pay"] = P.ciro / tc * 100; P["ort_fiyat"] = P.ciro / P.net; P["iade_o"] = P.iade / P.brut * 100
q3m = U[U.q == "2026Q3"].groupby("Model Kodu")["Güncel Stok"].last()
top = P.sort_values("net", ascending=False).head(20)
R["urun_adet"] = [{"kod": str(i), "ad": r.ad, "kat": r.kat, "marka": r.marka, "net": int(r.net), "adet_pay": r.adet_pay, "ciro_pay": r.ciro_pay, "ort_fiyat": r.ort_fiyat, "iade": r.iade_o, "stok": (None if pd.isna(r.stok) else int(r.stok))} for i, r in top.iterrows()]
topc = P.sort_values("ciro", ascending=False).head(15)
R["urun_ciro"] = [{"kod": str(i), "ad": r.ad, "kat": r.kat, "marka": r.marka, "net": int(r.net), "adet_pay": r.adet_pay, "ciro_pay": r.ciro_pay, "ort_fiyat": r.ort_fiyat, "iade": r.iade_o, "stok": (None if pd.isna(r.stok) else int(r.stok))} for i, r in topc.iterrows()]
s = P.sort_values("ciro", ascending=False).ciro.cumsum() / tc; s2 = P.sort_values("net", ascending=False).net.cumsum() / tn
R["pareto"] = {"urun": int(len(P)), "ciro50": int((s < .5).sum() + 1), "ciro80": int((s < .8).sum() + 1), "adet50": int((s2 < .5).sum() + 1), "adet80": int((s2 < .8).sum() + 1)}
bands = [(0, 500, "<500"), (500, 1000, "500-1.000"), (1000, 2000, "1.000-2.000"), (2000, 5000, "2.000-5.000"), (5000, 10000, "5.000-10.000"), (10000, 20000, "10.000-20.000"), (20000, 1e12, "20.000+")]
R["fiyat_bandi"] = [{"band": b, "urun": int(((P.ort_fiyat >= lo) & (P.ort_fiyat < hi)).sum()), "adet_pay": P[(P.ort_fiyat >= lo) & (P.ort_fiyat < hi)].net.sum() / tn * 100,
                     "ciro_pay": P[(P.ort_fiyat >= lo) & (P.ort_fiyat < hi)].ciro.sum() / tc * 100} for lo, hi, b in bands]
q3 = U[U.q == "2026Q3"]; z = q3[q3["Güncel Stok"] == 0]
R["stok"] = {"q3_urun": int(q3["Model Kodu"].nunique()), "stok0": int(z["Model Kodu"].nunique()), "adet_pay": z["Net Satış Adedi"].sum() / q3["Net Satış Adedi"].sum() * 100,
             "ciro_pay": z["Net Ciro"].sum() / q3["Net Ciro"].sum() * 100,
             "ornek": [{"ad": ADM.get(str(r["Model Kodu"]).strip(), r["Ürün Adı"]) if not isinstance(r["Ürün Adı"], str) else r["Ürün Adı"], "net": int(r["Net Satış Adedi"])} for _, r in z.sort_values("Net Satış Adedi", ascending=False).head(8).iterrows()]}
q3v = q3[(q3["Güncel Satış Fiyatı"] > 0) & (q3["Ortalama Satış Fiyatı"] > 0)]
R["liste_fark"] = {"medyan": float(((q3v["Ortalama Satış Fiyatı"] / q3v["Güncel Satış Fiyatı"] - 1) * 100).median()), "n": int(len(q3v))}
# iptal iade nedenleri
M = pd.concat([pd.read_excel(f, sheet_name="marka-bazlı-satış-raporu") for f in glob.glob(os.path.join(TY, "seller-144409-satış-raporu-*.xlsx"))])
cols = ["Müşterinin İptal Ettiği", "Trendyol'un İptal Ettiği", "Benim İptal Ettiğim", "Kusurlu Ürün Gönderildi", "Yanlış Ürün Gönderildi", "Vazgeçtim", "Diğer", "Bedeni/Ebatı Küçük Geldi", "Bedeni/Ebatı Büyük Geldi"]
R["neden"] = {c: int(num(M[c]).sum()) for c in cols}
# siparis dagilimi
def dag(sh):
    out = {}
    for f in glob.glob(os.path.join(TY, "seller-144409-sipariş-dağılım-raporu-*.xlsx")):
        q = [v for k, v in QD.items() if k in f][0]; d = pd.read_excel(f, sheet_name=sh)
        out[q] = {str(r.iloc[0]): float(num(r["Sipariş Dağılım%"])) for _, r in d.iterrows()}
    return out
yn = dag("Yeni & Mevcut Müşteri"); pl = dag("Trendyol Plus"); ad_ = dag("Adet Bazlı"); tu = dag("Tutar Bazlı"); cn = dag("Cinsiyet")
prof = []
for q in CEY:
    ust5 = sum(v for k, v in tu[q].items() if k.startswith(("5000", "10000", "25000", "50.000")))
    prof.append({"q": q, "yeni": yn[q]["Yeni Müşteriler"], "plus": pl[q]["Trendyol Plus Müşterileri"], "tek": ad_[q]["1"], "ust5": ust5, "kadin": cn[q]["Kadın"]})
R["profil"] = prof
IL = pd.concat([pd.read_excel(f, sheet_name="İl ve İlçe") for f in glob.glob(os.path.join(TY, "seller-144409-sipariş-dağılım-raporu-*.xlsx"))])
IL["n"] = num(IL["Sipariş Adedi"]); il = IL.groupby("İl").n.sum().sort_values(ascending=False)
R["il"] = [{"il": k, "pay": v / il.sum() * 100} for k, v in il.head(6).items()]; R["il_sayi"] = int(len(il))
GS = pd.concat([pd.read_excel(f, sheet_name="Gün ve Saat") for f in glob.glob(os.path.join(TY, "seller-144409-sipariş-dağılım-raporu-*.xlsx"))])
GS["n"] = num(GS["Sipariş Adedi"]); sa = GS.groupby("Saat Aralığı").n.sum(); gu = GS.groupby("Gün").n.sum()
R["saat"] = {k: v / sa.sum() * 100 for k, v in sa.items()}; R["gun"] = {k.replace("Perșembe", "Perşembe"): v / gu.sum() * 100 for k, v in gu.items()}
# magaza raporu
MG = pd.concat([pd.read_excel(f) for f in glob.glob(os.path.join(TY, "seller-144409-magaza-raporu-*.xlsx"))])
MG["t"] = pd.to_datetime(MG["Tarih"], format="%d-%m-%Y %H:%M")
for c in MG.columns:
    if c not in ("Tarih", "t"): MG[c] = num(MG[c].astype(str).str.replace("+ ", "").str.replace("- ", "-"))
m26 = MG[MG.t >= "2026-01-01"]
R["magaza"] = {"takipci_bas": int(MG.sort_values("t").iloc[0]["Toplam Takipçi Sayısı"]), "takipci_son": int(MG.sort_values("t").iloc[-1]["Toplam Takipçi Sayısı"]),
               "vitrin_siparis_2026": m26["Mağazanın Brüt Sipariş Adedi"].sum() / m26["Toplam Brüt Sipariş Adedi"].sum() * 100,
               "kasim_takipci": int(MG[(MG.t >= "2025-11-01") & (MG.t < "2025-12-01")]["Toplam Takipçi Sayısı - Kazanılan"].sum()),
               "takipci_bas_t": str(MG.sort_values("t").iloc[0]["t"])[:10], "takipci_son_t": str(MG.sort_values("t").iloc[-1]["t"])[:10]}
# operasyon
OP = pd.read_excel(os.path.join(TY, "seller-144409-operasyon-raporu-2026.09.30-18.47.24.xlsx")).set_index("Kalite Metriklerim")
R["operasyon"] = {str(c): {k: float(num(pd.Series([OP.loc[k, c]])).iloc[0]) for k in OP.index} for c in ["2026", "2025", "2024", "2023"]}
# degerlendirme
R["deger"] = {"n": int(len(RV)), "ort": float(RV.puan.mean()), "bes": float((RV.puan == 5).mean() * 100), "dusuk": float((RV.puan <= 2).mean() * 100), "yorumlu": int(RV["Yorum"].notna().sum()),
              "artema": float(RV[RV.Marka == "Artema"].puan.mean()), "vitra": float(RV[RV.Marka == "VitrA"].puan.mean()),
              "bas": str(RV.t.min().date()), "son": str(RV.t.max().date())}
T = {"Kalite ve malzeme": r"kalite|sağlam|saglam|plastik|hafif|malzeme", "Görünüm ve tasarım": r"şık|güzel|guzel|tasarım|görünüm|estetik|renk", "Hediye ve paketleme jesti": r"hediye|teşekkür|tesekkur",
     "Kargo ve teslimat": r"kargo|teslim|geç|hızlı|hizli|erken", "Ambalaj": r"ambalaj|paket|kutu|koli", "Eksik parça ve aksesuar": r"eksik|vida|dübel|aparat|parça|parca|gelmedi",
     "Ölçü ve uyum": r"uyum|uymad|ölçü|olcu|boyut|küçük|büyük", "Kırık ve hasar": r"kırık|kirik|kırıl|çatla|hasar|ezik|zarar", "Montaj": r"montaj|takıl|takil|kurul|usta|tesisat",
     "İade ve değişim": r"iade|değişim|degisim", "Su kaçağı ve işlev": r"kaçır|kacir|sızdır|sizdir|akıt|bozuk|arıza|ariza|damla"}
Y = RV[RV["Yorum"].notna()].copy(); Y["y"] = Y["Yorum"].str.lower()
R["tema"] = []
for k, rx in T.items():
    m = Y[Y.y.str.contains(rx, regex=True)]
    R["tema"].append({"tema": k, "n": int(len(m)), "ort": float(m.puan.mean()), "dusuk": int((m.puan <= 2).sum())})
SV = pd.concat([pd.read_excel(f) for f in glob.glob(os.path.join(TY, "seller-144409-satıcı-değerlendirmeleri-*.xlsx"))]).drop_duplicates(subset=["Teslimat Numarası", "Değerlendirme Tarihi", "Model Kodu"])
SV["puan"] = num(SV["Değerlendirme Puanı"])
sp = pd.to_datetime(SV["Sipariş Tarihi"], format="%d-%m-%Y", errors="coerce"); te = pd.to_datetime(SV["Teslimat Tarihi"], format="%d-%m-%Y", errors="coerce")
R["satici"] = {"n": int(len(SV)), "ort": float(SV.puan.mean()), "bir": int((SV.puan == 1).sum()), "teslim_medyan": float((te - sp).dt.days.median()),
               "etki": SV["Olumsuz Etkiler"].dropna().str.split(", ").explode().value_counts().to_dict()}
QS = pd.read_excel(os.path.join(TY, "UrunSorulariniz_29.09.2026-17_01.xlsx")); QS["s"] = QS["Soru Detayı"].astype(str).str.lower(); QS["c"] = QS["Onaylanan Cevap"].astype(str).str.lower()
T2 = {"Uyumluluk (klozet, lavabo, valf kodu)": r"uyum|uyar|uygun mu|uygun mudur|uygunmu|kodlu|takılır|takılabilir|yerine", "Stok, renk ve varyant": r"stok|var mı|varmı|var mıdır|mevcut mu|rengi|renk|siyah|antrasit",
      "Ölçü ve boyut": r"ölçü|olcu|cm|santim|boyut|genişli|derinli|yüksekli|delik aralığı|vida aralığı", "Yedek parça": r"yedek|parça|parca|menteşe|conta|vida|başlık olarak",
      "Kargo ve teslim süresi": r"kargo|ne zaman|bugün|acil|teslim", "Montaj": r"montaj|monte|kurul|takar|usta|takt", "Kutu içeriği (kapak, rezervuar, hortum dahil mi)": r"dahil|içeri|iceri|set halinde|çıkıyor mu|birlikte mi|hortum",
      "Eksik, hasarlı, arızalı ürün": r"eksik|kırık|kirik|çatlak|arıza|ariza|bozuk|kaçır|kacir|hasar|yanlış|yanlis", "Orijinallik ve marka": r"orjinal|orijinal|artema mı|vitra mı|marka"}
C2 = {"Danışma Hattı / yetkili servise yönlendirme": r"danışma hattı|yetkili servis", "\"İlgili ekibe ilettik, tekrar sorun\"": r"ilgili ekibe sorunuzu ilettik",
      "\"Ürün kodunu paylaşırsanız\"": r"ürün kodunu bizimle paylaşırsanız", "Farklı marka uyumluluğu paylaşılamıyor": r"farklı marka ürünlerle ilgili", "Trendyol kuralı: parça ve bağlantı gönderilemiyor": r"trendyol kuralları gereği"}
R["soru"] = {"n": int(len(QS)), "cevap_medyan_dk": float(num(QS["Cevaplama Süresi (dk.)"]).median()), "tema": [{"tema": k, "n": int(QS.s.str.contains(rx, regex=True).sum())} for k, rx in T2.items()],
             "cevap": [{"kalip": k, "n": int(QS.c.str.contains(rx, regex=True).sum())} for k, rx in C2.items()]}
QO = pd.read_excel(os.path.join(TY, "SiparisSorulariniz_29.09.2026-17_03.xlsx"))
R["siparis_talep"] = QO["Konu"].value_counts().to_dict()
# favori-goruntuleme 2026
f26 = [d for d in FV if "19.29.08" in d.dosya.iloc[0]][0].copy()
for c in f26.columns[6:15]: f26[c] = num(f26[c])
f26["Ürün Kategorisi"] = f26["Ürün Kategorisi"].fillna(f26["Model Kodu"].map(KATM))
fg = f26.groupby("Ürün Kategorisi").agg(gor=("Satıcı Görüntülenme Sayısı", "sum"), sepet=("Sepete Eklenme Sayısı", "sum"), sat=("Brüt Satış Adedi", "sum"), fav=("Aktif Favori Sayısı", "sum"))
tg = fg.gor.sum()
R["donusum"] = {"toplam_gor": int(f26["Toplam Görüntülenme Sayısı"].sum()), "satici_gor": int(tg), "sepet": float(f26["Sepete Eklenme Sayısı"].sum() / tg * 100), "cr": float(f26["Brüt Satış Adedi"].sum() / tg * 100),
                "satissiz_urun": int((f26["Brüt Satış Adedi"].fillna(0) == 0).sum()), "urun": int(len(f26)),
                "satissiz_gor": float(f26[f26["Brüt Satış Adedi"].fillna(0) == 0]["Satıcı Görüntülenme Sayısı"].sum() / tg * 100),
                "kat": [{"kategori": k, "gor_pay": r.gor / tg * 100, "sepet": r.sepet / r.gor * 100, "cr": r.sat / r.gor * 100, "fav": int(r.fav)} for k, r in fg.sort_values("gor", ascending=False).head(14).iterrows()],
                "bakan_cok": [{"ad": r["Ürün Adı"], "kat": r["Ürün Kategorisi"], "gor": int(r["Satıcı Görüntülenme Sayısı"]), "sepet": int(r["Sepete Eklenme Sayısı"] or 0), "sat": int(r["Brüt Satış Adedi"] or 0)}
                              for _, r in f26[(f26["Brüt Satış Adedi"].fillna(0) <= 2) & f26["Ürün Adı"].notna()].sort_values("Satıcı Görüntülenme Sayısı", ascending=False).head(8).iterrows()]}
f25 = [d for d in FV if "19.29.27" in d.dosya.iloc[0]][0].copy()
for c in f25.columns[6:15]: f25[c] = num(f25[c])
R["donusum25"] = {"sepet": float(f25["Sepete Eklenme Sayısı"].sum() / f25["Satıcı Görüntülenme Sayısı"].sum() * 100), "cr": float(f25["Brüt Satış Adedi"].sum() / f25["Satıcı Görüntülenme Sayısı"].sum() * 100)}
# enleri
E = pd.DataFrame([json.loads(l) for f in glob.glob(os.path.join(TY, "enleri_*.jsonl")) for l in open(f, encoding="utf-8") if l.strip()])
E["mn"] = E.marka.fillna("").str.lower(); E["vit"] = E.mn.str.contains("vitra|artema"); E["siz"] = E.sizin_urununuz.fillna(False).astype(bool)
en = []
for k, g in E.groupby("kategori"):
    def l(n): return g[g.liste == n]
    s_, c_, f_, v_ = l("En Çok Satılanlar"), l("En Çok Ciro Getirenler"), l("En Çok Favorilenenler"), l("En Çok Görüntülenenler")
    vv = pd.to_numeric(v_.get("ek_deger"), errors="coerce") if len(v_) else pd.Series(dtype=float)
    lider = s_.sort_values("sira").marka.value_counts().index[0] if len(s_) else None
    en.append({"kategori": k, "sat_siz": int(s_.siz.sum()), "sat_vit": int(s_.vit.sum()), "ciro_siz": int(c_.siz.sum()), "ciro_vit": int(c_.vit.sum()),
               "fav_vit": int(f_.vit.sum()), "gor_vit": int(v_.vit.sum()) if len(v_) else None,
               "gor_pay": float(vv[v_.vit.values].sum() / vv.sum() * 100) if len(v_) and vv.sum() else None, "gor_top": int(vv.sum()) if len(v_) and vv.sum() else None,
               "sat_med": float(s_.ort_fiyat.replace(0, np.nan).median()), "vit_med": float(g[g.vit].ort_fiyat.replace(0, np.nan).median()) if g.vit.any() else None,
               "lider": lider, "lider_n": int((s_.marka == lider).sum()) if lider else 0})
R["enleri"] = en
vr = E[E.vit]; R["enleri_ozet"] = {"satir": int(len(E)), "liste": int(E.groupby(["kategori", "liste"]).ngroups), "vit": int(len(vr)), "vit_3p": int((~vr.siz).sum()), "siz": int(E.siz.sum()),
                                  "bb_fark_siz": float(((vr[vr.siz].buybox_fiyat / vr[vr.siz].ort_fiyat - 1) * 100).median())}
# HB
z = zipfile.ZipFile(glob.glob(os.path.join(HBD, "Urun_performans_*.xlsx"))[0]); xml = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
rows = re.findall(r"<row[^>]*>(.*?)</row>", xml, re.S)
def cells(r):
    o = {}
    for m in re.finditer(r'<c r="([A-Z]+)\d+"[^>]*>(.*?)</c>', r, re.S):
        v = re.search(r"<t[^>]*>(.*?)</t>", m.group(2), re.S) or re.search(r"<v>(.*?)</v>", m.group(2), re.S); o[m.group(1)] = v.group(1) if v else ""
    return o
hdr = cells(rows[0]); ks = sorted(hdr, key=lambda s: (len(s), s))
H = pd.DataFrame([[cells(r).get(k, "") for k in ks] for r in rows[1:]], columns=[hdr[k] for k in ks])
for c in ["Ürün Adedi", "Sipariş tutarı", "Komisyon tutarı", "Kargo Bedeli", "Hizmet bedeli", "Kampanya indirimleri", "Tahsilat Yönetim Bedeli", "Net Hak Ediş"]: H[c] = num(H[c])
sat = H[H["Ürün Adedi"] > 0]; t_ = sat["Sipariş tutarı"].sum()
R["hb"] = {"siparis": int(sat["Sipariş No"].nunique()), "adet": int(sat["Ürün Adedi"].sum()), "sku": int(sat["Ürün No (SKU)"].nunique()),
           "komisyon": -sat["Komisyon tutarı"].sum() / t_ * 100, "kargo": -sat["Kargo Bedeli"].sum() / t_ * 100, "tahsilat": -sat["Tahsilat Yönetim Bedeli"].sum() / t_ * 100,
           "hizmet": -sat["Hizmet bedeli"].sum() / t_ * 100, "kampanya": sat["Kampanya indirimleri"].sum() / t_ * 100, "hak_edis": sat["Net Hak Ediş"].sum() / t_ * 100}
G = pd.read_excel(glob.glob(os.path.join(HBD, "*GoruntulenmeRaporu.xlsx"))[0])
for c in G.columns[1:6]: G[c] = num(G[c])
R["hb"].update({"gor": int(G["Toplam Goruntulenme Sayisi"].sum()), "gor_sku": int(len(G)), "sepet": float(G["Sepete Eklenme Sayisi"].sum() / G["Toplam Goruntulenme Sayisi"].sum() * 100),
                "cr": float(G["Satis Miktari"].sum() / G["Toplam Goruntulenme Sayisi"].sum() * 100), "satissiz_sku": int((G["Satis Miktari"] == 0).sum()),
                "satissiz_gor": float(G[G["Satis Miktari"] == 0]["Toplam Goruntulenme Sayisi"].sum() / G["Toplam Goruntulenme Sayisi"].sum() * 100)})
C = pd.read_excel(glob.glob(os.path.join(HBD, "*cancels.xlsx"))[0]); C["m"] = num(C["Iptal Miktari"])
cs = C.groupby(C["Iptal Sebebi"].fillna("(belirtilmemiş)")).m.sum(); R["hb"]["iptal_neden"] = {k: int(v) for k, v in cs.sort_values(ascending=False).items()}; R["hb"]["iptal_top"] = int(C.m.sum())
D = pd.read_csv(glob.glob(os.path.join(HBD, "UrunDegerlendirmeRaporu.csv"))[0], sep=";", encoding="utf-8-sig")
for c in D.columns[2:7]: D[c] = num(D[c])
R["hb"].update({"deg_sku": int(len(D)), "deg_satici": int(D["Değerlendirme Sayısı"].sum()), "deg_hb": int(D["Hepsiburada Değerlendirme Sayısı"].sum()), "puan": float(D["Hepsiburada Ürün Puanı"].mean())})
json.dump(R, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
print("yazıldı", OUT, round(os.path.getsize(OUT) / 1024), "KB")
