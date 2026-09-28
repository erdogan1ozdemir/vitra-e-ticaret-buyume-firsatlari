# -*- coding: utf-8 -*-
"""EVDS serilerini aylik tablolara indirger."""
import json, os
from collections import defaultdict
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); E = os.path.join(P, "veri/ham/evds"); O = os.path.join(P, "veri/islenmis")
def oku(ad): return json.load(open(os.path.join(E, ad + ".json")))["items"]
def f(v):
    try: return float(v)
    except: return None
out = {}
# kart harcama haftalik -> aylik toplam (milyon TL)
ay = defaultdict(lambda: defaultdict(float)); ayn = defaultdict(int)
for it in oku("kart_harcama_haftalik"):
    g, m, y = it["Tarih"].split("-"); k = f"{y}-{m}"
    for c in ("TP_KKHARTUT_KT1","TP_KKHARTUT_KT17","TP_KKHARTUT_KT23","TP_KKHARTUT_KT50","TP_KKHARTUT_KT8","TP_KKHARTUT_KT16"):
        if f(it.get(c)) is not None: ay[k][c] += f(it[c]) / 1000  # bin TL -> milyon TL
    ayn[k] += 1
out["kart_harcama_aylik_mnTL"] = {k: {"toplam": v["TP_KKHARTUT_KT1"], "mobilya_dekorasyon": v["TP_KKHARTUT_KT17"], "yapi_malzemeleri": v["TP_KKHARTUT_KT23"], "internet": v["TP_KKHARTUT_KT50"], "elektronik": v["TP_KKHARTUT_KT8"], "market_avm": v["TP_KKHARTUT_KT16"], "hafta": ayn[k]} for k, v in sorted(ay.items())}
def seri(ad, alanlar):
    r = {}
    for it in oku(ad):
        t = it["Tarih"]; r[t] = {k2: f(it.get(k1)) for k1, k2 in alanlar.items()}
    return r
out["kartli_odeme_endeksi"] = seri("kartli_odeme_endeksi", {"TP_KARTMETRE_D1":"genel_nominal","TP_KARTMETRE_D2":"genel_reel","TP_KARTMETRE_D3":"hane_nominal","TP_KARTMETRE_D4":"hane_reel"})
out["tuketici_egilim"] = seri("tuketici_egilim", {"TP_TG2_Y01":"guven_endeksi","TP_TG2_Y02":"hane_maddi_son12","TP_TG2_Y03":"hane_maddi_gelecek12","TP_TG2_Y05":"genel_ekonomi_gelecek12","TP_TG2_Y08":"dayanikli_mal_uygunluk","TP_TG2_Y09":"dayanikli_harcama_gelecek12","TP_TG2_Y10":"tasarruf_uygunluk","TP_TG2_Y12":"tasarruf_ihtimali","TP_TG2_Y18":"konut_tamirat_harcama_ihtimali","TP_TG2_Y19":"konut_alma_ihtimali"})
out["konut_satis"] = seri("konut_satis", {"TP_AKONUTSAT1_KTRTOPLAM":"toplam","TP_AKONUTSAT3_KTRTOPLAM":"ilk_el","TP_AKONUTSAT4_KTRTOPLAM":"ikinci_el","TP_AKONUTSAT2_KTRTOPLAM":"ipotekli"})
out["konut_fiyat"] = seri("konut_fiyat", {"TP_KFE_TR":"kfe","TP_YKFE_TR":"yeni_konut_kfe"})
out["banka_kredi_egilim"] = seri("banka_kredi_egilim", {"TP_BKEA_S058":"diger_bireysel_standart","TP_BKEA_S094":"diger_bireysel_talep","TP_BKEA_S110":"dayanikli_mal_etkisi","TP_BKEA_S111":"tuketici_guveni_etkisi","TP_BKEA_S119":"diger_bireysel_standart_beklenti","TP_BKEA_S122":"diger_bireysel_talep_beklenti","TP_BKEA_S056":"konut_kredi_standart","TP_BKEA_S092":"konut_kredi_talep"})
out["hanehalki_beklenti"] = seri("hanehalki_beklenti", {"TP_HANEBEK_HAN15E":"dayanikli_fiyat_artti_pay","TP_HANEBEK_HAN16E":"dayanikli_fiyat_artacak_pay","TP_HANEBEK_HAN14A":"enflasyon_beklenti_12ay"})
out["kaynak"] = "TCMB EVDS · 28.09.2026 · kart harcama BKM/TCMB haftalık akım, aylık toplam (milyon TL); tüketici eğilim TÜİK-TCMB; konut satış ve fiyat TÜİK/TCMB; banka kredileri eğilim anketi TCMB (üç aylık, net yüzde)"
json.dump(out, open(os.path.join(O, "evds_tablolar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
k = out["kart_harcama_aylik_mnTL"]
print("Kart harcama · aylık milyon TL · mobilya-dekorasyon / yapı malzemeleri / internet / toplam")
for m in sorted(k):
    if m >= "2024-01": print(m, f"{k[m]['mobilya_dekorasyon']:10.0f} {k[m]['yapi_malzemeleri']:10.0f} {k[m]['internet']:11.0f} {k[m]['toplam']:12.0f}  ({k[m]['hafta']} hafta)")
t = out["tuketici_egilim"]
print("\nTüketici eğilim · güven / dayanıklı mal uygunluk / konut tamiratı harcama ihtimali / konut alma")
for m in sorted(t, key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))[-24:]: print(m, t[m]["guven_endeksi"], t[m]["dayanikli_mal_uygunluk"], t[m]["konut_tamirat_harcama_ihtimali"], t[m]["konut_alma_ihtimali"])
ks = out["konut_satis"]; print("\nKonut satış (son 8 ay)"); [print(m, ks[m]) for m in list(ks)[-8:]]
b = out["banka_kredi_egilim"]; print("\nBanka kredi eğilim (son 6 çeyrek)"); [print(m, b[m]) for m in list(b)[-6:]]
