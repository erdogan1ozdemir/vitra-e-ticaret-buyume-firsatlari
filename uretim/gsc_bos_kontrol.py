# -*- coding: utf-8 -*-
"""SERP'te VitrA'nin ilk 20'de gorunmedigi kelimeler icin Search Console (OAuth, sc-domain) dogrulamasi -> veri/ham/derin/serp/gsc_bos_kontrol.json"""
import json, os, re, sys
sys.argv = [sys.argv[0]]
import importlib.util
spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__), "gsc_cek.py"))
src = open(os.path.join(os.path.dirname(__file__), "gsc_cek.py"), encoding="utf-8").read().split('S, E = "2025-06-01"')[0]
g = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc_cek.py")}; exec(src, g)
sorgu = g["sorgu"]
B = re.findall(r'\("([^"]+)", \d+, "[^"]+"\)', open(os.path.join(os.path.dirname(__file__), "b_serp.py"), encoding="utf-8").read().split("BOS = [")[1].split("]\n")[0])
out = {}
for kw in B:
    rows = sorgu(["query", "page"], "2026-06-26", "2026-09-25", 50, [{"dimension": "query", "operator": "equals", "expression": kw}])
    imp = sum(r["impressions"] for r in rows); clk = sum(r["clicks"] for r in rows)
    pos = (sum(r["position"] * r["impressions"] for r in rows) / imp) if imp else None
    top = sorted(rows, key=lambda r: -r["impressions"])[:3]
    out[kw] = {"gosterim": imp, "tik": clk, "ort_sira": pos, "sayfalar": [(r["keys"][1], r["impressions"], round(r["position"], 1)) for r in top]}
    print("%-28s gösterim %6d  tık %4d  sıra %s  %s" % (kw, imp, clk, ("%.1f" % pos) if pos else "-", top[0]["keys"][1] if top else ""))
json.dump(out, open(os.path.join(g["P"], "veri/ham/derin/serp/gsc_bos_kontrol.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
