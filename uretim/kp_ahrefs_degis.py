# -*- coding: utf-8 -*-
"""Raporda Ahrefs hacmi kullanilan kelimeler icin Google Keyword Planner (DataForSEO) hacmi · TR · Eyl 2024 - Agu 2026.
Kapsam: kategori bas kelimeleri (Bolum 15), marka arama talebi (Bolum 15, SEOmonitor rakipleri dahil), pazaryeri alt kategori en iyi kelimeleri (Bolum 16)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import dfs, veri
AP = json.load(open(os.path.join(veri.V, "ham", "derin", "ahrefs_pazaryeri", "analiz_ozet_tablolar.json"), encoding="utf-8"))
BK = ["banyo dolabı", "duşakabin", "duş başlığı", "klozet", "taharet musluğu", "lavabo", "çamaşır makinesi dolabı", "klozet kapağı", "banyo bataryası",
      "banyo modelleri", "dolap kulpu", "duş seti", "gömme rezervuar", "klozet takımı", "musluk başlığı", "kartuş", "banyo aynası"]
MARKA = ["vitra", "artema", "eca", "bien", "bocchi", "creavit", "grohe", "geberit", "hansgrohe", "turkuaz seramik", "duravit", "visam", "serel", "kale banyo",
         "kale", "banyomarka", "banyomega", "banyoline", "ikea banyo", "bauhaus banyo"]
PZ = sorted({r["top_kw"] for k_ in ("altkat_trendyol", "altkat_hepsiburada") for r in AP[k_]["satirlar"] if r.get("top_kw")})
kws = sorted(set(BK + MARKA + PZ))
r = dfs.post("/v3/keywords_data/google_ads/search_volume/live",
             [{"location_code": 2792, "language_code": "tr", "date_from": "2024-09-01", "date_to": "2026-08-31", "keywords": kws, "search_partners": False}])
t = r["tasks"][0]
print(t["status_message"], t.get("cost"), len(kws))
out = {}
for res in t.get("result") or []:
    ms = res.get("monthly_searches") or []
    seri = {"%04d-%02d" % (m["year"], m["month"]): m["search_volume"] for m in ms}
    son12 = [seri.get(a) for a in sorted(seri)[-12:]]
    out[res["keyword"]] = {"hacim_kp": res.get("search_volume"), "ort12": round(sum(v for v in son12 if v) / 12) if any(son12) else None, "seri": seri}
json.dump({"kaynak": "Google Ads Keyword Planner (DataForSEO) · TR 2792 · tr · 2024-09 - 2026-08 · cekim 03.10.2026", "bas_kelime": BK, "marka": MARKA, "pazaryeri": PZ,
           "kelimeler": out}, open(os.path.join(veri.V, "ham", "kp_ahrefs_degis.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("donmeyen:", [k for k in kws if k not in out or not out[k]["ort12"]])
for k in BK + MARKA: print(k, (out.get(k) or {}).get("ort12"))
