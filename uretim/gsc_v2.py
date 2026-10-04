# -*- coding: utf-8 -*-
"""Genisletilmis SERP seti (set_v2.json) icin Search Console ort. sira, click, gosterim · sc-domain:vitra.com.tr · 1 Tem - 30 Eyl 2026 (OAuth)."""
import json, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc_cek.py"), encoding="utf-8").read().split('S, E = "2025-06-01"')[0]
g = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc_cek.py")}; exec(src, g)
import veri
kws = [s["kw"] for s in json.load(open(os.path.join(veri.V, "ham/derin/serp/set_v2.json"), encoding="utf-8"))["kelimeler"]]
S_, E_ = "2026-07-01", "2026-09-30"
q = {r["keys"][0]: r for r in g["sorgu"](["query"], S_, E_, 25000)}
for kw in kws:
    if kw in q: continue
    rr = g["sorgu"](["query"], S_, E_, 10, [{"dimension": "query", "operator": "equals", "expression": kw}])
    if rr: q[kw] = rr[0]
out = {"donem": [S_, E_], "kelime": {kw: ({"tik": q[kw]["clicks"], "gosterim": q[kw]["impressions"], "sira": round(q[kw]["position"], 1)} if kw in q else None) for kw in kws}}
json.dump(out, open(os.path.join(veri.V, "ham/derin/serp/gsc_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("gsc eşleşen", sum(1 for v in out["kelime"].values() if v), "/", len(kws))
