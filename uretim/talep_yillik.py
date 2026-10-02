# -*- coding: utf-8 -*-
"""Kategori talebi yil yil: 2.420 kelimenin 48 aylik (Eyl 2022 - Agu 2026) hacmi -> ana kategori x yil x ay. Cikti: veri/islenmis/talep_yillik.json"""
import json, os
from collections import defaultdict
import veri
K48 = json.load(open(os.path.join(veri.V, "ham", "kp_sezon_2022-09_2026-08.json"), encoding="utf-8"))["kelimeler"]
import aykiri; K48 = {k_: (dict(v_, seri=aykiri.seri(k_, v_.get("seri"))) if isinstance(v_, dict) else v_) for k_, v_ in K48.items()}   # Dunya Kupasi 2026 'wc' duzeltmesi
Y = defaultdict(lambda: defaultdict(float)); eks = 0
for r in veri.KELIME:
    s = (K48.get(r["kw"]) or {}).get("seri") if isinstance(K48, dict) else None
    if not s: eks += 1; continue
    for m, v in s.items():
        if v is None: continue
        Y[r["k1"]][m] += v; Y["Toplam"][m] += v
out = {"yillar": [2023, 2024, 2025, 2026], "kategori": {}}
for k, d in Y.items():
    out["kategori"][k] = {str(y): [(round(d["%d-%02d" % (y, a)]) if "%d-%02d" % (y, a) in d else None) for a in range(1, 13)] for y in out["yillar"]}
json.dump(out, open(os.path.join(veri.V, "islenmis", "talep_yillik.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("kategori", len(out["kategori"]), "eksik kelime", eks, "Toplam 2025", sum(v for v in out["kategori"]["Toplam"]["2025"] if v))
