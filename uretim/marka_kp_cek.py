# -*- coding: utf-8 -*-
"""Marka aramaları için Keyword Planner aylık hacim (DataForSEO Google Ads search_volume) · TR · Eyl 2022 - Ağu 2026.
Kullanım: python3 marka_kp_cek.py <ad> <kelime_dosyasi.txt>   -> veri/ham/marka_kelime/<ad>.json (1000'lik paketler, var olan kelimeler atlanır)"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ad, dosya = sys.argv[1], sys.argv[2]
CIKTI = os.path.join(P, "veri/ham/marka_kelime/%s.json" % ad)
kws = list(dict.fromkeys(l.strip().lower() for l in open(dosya, encoding="utf-8") if l.strip()))
kws = [k for k in kws if len(k) <= 80 and len(k.split()) <= 10]
eski = json.load(open(CIKTI, encoding="utf-8"))["kelimeler"] if os.path.exists(CIKTI) else {}
kalan = [k for k in kws if k not in eski]
print(ad, "toplam", len(kws), "çekilecek", len(kalan))
for i in range(0, len(kalan), 1000):
    paket = kalan[i:i + 1000]
    r = dfs.post("/v3/keywords_data/google_ads/search_volume/live", [{"location_code": 2792, "language_code": "tr", "date_from": "2022-09-01", "date_to": "2026-08-31", "keywords": paket, "search_partners": False}])
    t = r["tasks"][0]; print(i, t["status_code"], t["status_message"], t.get("cost"))
    for res in t.get("result") or []:
        eski[res["keyword"]] = {"hacim": res.get("search_volume"), "seri": {"%04d-%02d" % (m["year"], m["month"]): m["search_volume"] for m in (res.get("monthly_searches") or [])}}
    for k in paket: eski.setdefault(k, {"hacim": None, "seri": {}})
    json.dump({"kaynak": "Google Ads Keyword Planner · TR · tr · 2022-09 - 2026-08 · çekim 04.10.2026", "kelimeler": eski}, open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False)
    time.sleep(1)
dolu = sum(1 for k in kws if (eski.get(k) or {}).get("hacim"))
print("hacmi olan", dolu, "/", len(kws))
