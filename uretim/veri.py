# -*- coding: utf-8 -*-
"""Islenmis veri erisimi."""
import os, json
BASE = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(BASE)
V = os.path.join(KOK, "veri")
def J(*p): return json.load(open(os.path.join(V, *p), encoding="utf-8"))
AYLAR = ["%d-%02d" % (y, m) for y in (2024, 2025, 2026) for m in range(1, 13)][8:32]   # 2024-09 .. 2026-08
KELIME = J("islenmis", "kelime_seti.json")
GSC = J("islenmis", "gsc_kategori.json")
EVDS = J("islenmis", "evds_tablolar.json")
AY = J("ham", "autocomplete_youtube.json")
AHREFS = J("ham", "ahrefs_rakip_ozet.json")
TARIH = "28.09.2026"
