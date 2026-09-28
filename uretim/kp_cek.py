# -*- coding: utf-8 -*-
"""Sezon reposundaki 2.420 kelime icin Keyword Planner aylik hacim · TR · Eyl 2024 - Agu 2026."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(P, "veri/kaynak/sezon_dashboard.js"), encoding="utf-8").read()
d = json.loads(s[s.index("{"):s.rindex("}") + 1])
kws = sorted({k["kw"].strip().lower() for k in d["keywords"] if k.get("kw")})
print("kelime", len(kws))
out = {}
for i in range(0, len(kws), 1000):
    parca = kws[i:i + 1000]
    r = dfs.post("/v3/keywords_data/google_ads/search_volume/live",
                 [{"location_code": 2792, "language_code": "tr", "date_from": "2024-09-01", "date_to": "2026-08-31",
                   "keywords": parca, "search_partners": False}])
    t = r["tasks"][0]
    print(i, t["status_message"], t.get("cost"))
    for res in t.get("result") or []:
        ms = res.get("monthly_searches") or []
        out[res["keyword"]] = {"hacim": res.get("search_volume"), "cpc": res.get("cpc"), "rekabet": res.get("competition"),
                               "seri": {"%04d-%02d" % (m["year"], m["month"]): m["search_volume"] for m in ms}}
json.dump({"kaynak": "Google Ads Keyword Planner (DataForSEO) · TR 2792 · tr · 2024-09 - 2026-08 · cekim 28.09.2026",
           "kelimeler": out}, open(os.path.join(P, "veri/ham/kp_sezon_2024-09_2026-08.json"), "w", encoding="utf-8"), ensure_ascii=False)
donmeyen = [k for k in kws if k not in out or not out[k]["hacim"]]
print("kayit", len(out), "hacim donmeyen", len(donmeyen))
