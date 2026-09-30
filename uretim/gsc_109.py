# -*- coding: utf-8 -*-
"""109 SERP kelimesi icin Search Console ort. sira ve tik (26.06-25.09.2026, sc-domain) + YouTube 30 ifadesinin Google hacmi."""
import json, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc_cek.py"), encoding="utf-8").read().split('S, E = "2025-06-01"')[0]
g = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc_cek.py")}; exec(src, g)
import veri, dfs
K = json.load(open(os.path.join(veri.V, "ham/derin/serp/kelime_sonuc.json"), encoding="utf-8"))
kws = [r["kelime"] for r in K]
rows = g["sorgu"](["query"], "2026-06-26", "2026-09-25", 25000)
q = {r["keys"][0]: r for r in rows}
out = {kw: ({"tik": q[kw]["clicks"], "gosterim": q[kw]["impressions"], "sira": round(q[kw]["position"], 1)} if kw in q else None) for kw in kws}
json.dump(out, open(os.path.join(veri.V, "ham/derin/serp/gsc_109.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("gsc eşleşen", sum(1 for v in out.values() if v), "/", len(kws))
A = json.load(open(os.path.join(veri.V, "islenmis", "analiz.json"), encoding="utf-8"))
yq = list(A["yt"].keys())
H = os.path.join(veri.V, "ham", "autocomplete_hacim.json"); hd = json.load(open(H, encoding="utf-8"))
yeni = [k for k in yq if k not in hd["kelime"]]
if yeni:
    r = dfs.post("/v3/keywords_data/google_ads/search_volume/live", [{"keywords": yeni, "location_code": 2792, "language_code": "tr", "date_from": "2025-09-01", "search_partners": False}])
    for it in (r["tasks"][0].get("result") or []):
        ms = it.get("monthly_searches") or []; m26 = [m["search_volume"] for m in ms if m["year"] == 2026 and 1 <= m["month"] <= 8]
        hd["kelime"][it["keyword"]] = {"v12": it.get("search_volume"), "ort2026": (sum(m26) / len(m26) if m26 else None), "ay2026": len(m26), "aylik": [(m["year"], m["month"], m["search_volume"]) for m in ms]}
    json.dump(hd, open(H, "w", encoding="utf-8"), ensure_ascii=False)
print("yt ifade", len(yq), "yeni hacim", len(yeni))
