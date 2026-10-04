# -*- coding: utf-8 -*-
"""Marka karsilastirma aramalari: Google otomatik tamamlama onerileri (TR, tr, mobil) -> veri/ham/derin/serp/karsilastirma_oneri.json"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import dfs, veri
TOHUM = ["vitra mı", "vitra mi", "vitra veya", "vitra ile", "kale mi vitra", "creavit mi vitra", "geberit mi vitra", "grohe mu vitra", "eca mı vitra", "serel mi vitra", "artema mı",
         "vitra artema", "vitra kale", "vitra creavit", "en iyi klozet markası", "en iyi banyo dolabı markası", "en iyi batarya markası", "en iyi gömme rezervuar markası",
         "en iyi vitrifiye markası", "hangi klozet", "hangi batarya", "hangi marka klozet", "klozet markaları", "batarya markaları", "banyo dolabı markaları", "vitrifiye markaları"]
out = {}
for t in TOHUM:
    r = dfs.post("/v3/serp/google/autocomplete/live/advanced", [{"keyword": t, "location_code": 2792, "language_code": "tr", "client": "chrome"}])
    tk = r["tasks"][0]; res = (tk.get("result") or [{}])[0] or {}
    out[t] = [i.get("suggestion") for i in (res.get("items") or []) if i.get("suggestion")]
    time.sleep(0.3)
json.dump(out, open(os.path.join(veri.V, "ham", "derin", "serp", "karsilastirma_oneri.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t, L in out.items(): print(t, "->", L[:8])
