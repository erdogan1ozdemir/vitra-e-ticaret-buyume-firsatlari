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


def k48():
    """48 aylik Keyword Planner serileri (sezon listesi + 04.10.2026 eklenen bas kelimeler)."""
    import json as _j, os as _o
    d = _j.load(open(_o.path.join(V, "ham", "kp_sezon_2022-09_2026-08.json"), encoding="utf-8"))["kelimeler"]
    d.update(_j.load(open(_o.path.join(V, "ham", "kp_ek_2022-09_2026-08.json"), encoding="utf-8"))["kelimeler"])
    return d


def seri_bul(K48, r):
    """Kelimenin 48 aylik serisi: once gorunen ad, bulunamazsa ayni seriyi paylasan varyantlar."""
    for k_ in [r["kw"]] + list(r.get("varyant") or []):
        s_ = (K48.get(k_) or {}).get("seri") if isinstance(K48.get(k_), dict) else None
        if s_: return s_
    return None


def kanonik():
    """Yakin varyant -> evrendeki gorunen ad (ornek: banyo batarya -> banyo bataryası)."""
    return {v_: r["kw"] for r in KELIME for v_ in [r["kw"]] + list(r.get("varyant") or [])}
