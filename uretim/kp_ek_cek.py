# -*- coding: utf-8 -*-
"""Kelime evrenine eklenen baş kelimeler (veri/kaynak/ek_kelimeler.json) icin Keyword Planner aylik hacim · TR · Eyl 2024 - Agu 2026."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = sys.argv[1] if len(sys.argv) > 1 else "2024-09-01"
CIKTI = "veri/ham/kp_ek_%s_2026-08.json" % DF[:7]
kws = [r["kw"] for r in json.load(open(os.path.join(P, "veri/kaynak/ek_kelimeler.json"), encoding="utf-8"))]
r = dfs.post("/v3/keywords_data/google_ads/search_volume/live", [{"location_code": 2792, "language_code": "tr", "date_from": DF, "date_to": "2026-08-31", "keywords": kws, "search_partners": False}])
t = r["tasks"][0]; print(t["status_message"], t.get("cost"))
out = {res["keyword"]: {"hacim": res.get("search_volume"), "cpc": res.get("cpc"), "rekabet": res.get("competition"),
       "seri": {"%04d-%02d" % (m["year"], m["month"]): m["search_volume"] for m in (res.get("monthly_searches") or [])}} for res in t.get("result") or []}
json.dump({"kaynak": "Google Ads Keyword Planner (DataForSEO) · TR 2792 · tr · %s - 2026-08 · cekim 04.10.2026" % DF[:7], "kelimeler": out},
          open(os.path.join(P, CIKTI), "w", encoding="utf-8"), ensure_ascii=False)
for k in kws: print(k, (out.get(k) or {}).get("hacim"))
