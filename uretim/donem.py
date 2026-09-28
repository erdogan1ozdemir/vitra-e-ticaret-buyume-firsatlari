# -*- coding: utf-8 -*-
"""Google Keyword Planner (DataForSEO) hacimleri ve takvim hizali donem hesaplari.

Kural: karsilastirilan pencereler ayni takvim aylarini kapsar.
- Tam yil YoY: 2024 (Oca-Ara) ile 2025 (Oca-Ara)
- YTD YoY:     2025 (Oca-Tem) ile 2026 (Oca-Tem)
- Uc yillik:   2023 (Oca-Tem) ile 2026 (Oca-Tem)

Temmuz, Keyword Planner'in veri dondurdugu son aydir.

Not: Google Ads benzer kelimeler icin birlesik hacim dondurur. Ayni hacim ve ayni
aylik seriye sahip kelimeler tek grup olarak isaretlenir (GRUP_ESLERI).
"""
import os, json
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
HAM = json.load(open(os.path.join(BASE, "dfs_hacim.json"), encoding="utf-8"))

AYLAR = sorted({a for v in HAM.values() for a in v["aylik"]})
SON_AY = AYLAR[-1]                 # 2026-07
YTD_AY_SAYISI = 7                  # Ocak - Temmuz
YTD_ETIKET = "Oca-Tem"
SON_AY_TR = "Temmuz 2026"

# --- Google Ads'in birlestirdigi kelime gruplari -----------------------------
_g = defaultdict(list)
for k, v in HAM.items():
    _g[(v["hacim"], tuple(sorted(v["aylik"].items())))].append(k)
GRUP_ESLERI = {}
for grup in _g.values():
    if len(grup) > 1:
        for k in grup:
            GRUP_ESLERI[k] = sorted(grup)

def seri(k):
    a = HAM[k]["aylik"]
    return [a.get(ay) for ay in AYLAR]

def _ort(k, aylar):
    v = [HAM[k]["aylik"].get(a) for a in aylar]
    v = [x for x in v if x is not None]
    return sum(v) / len(v) if v else None

def yil(k, y):
    return _ort(k, ["%d-%02d" % (y, m) for m in range(1, 13)])

def ytd(k, y):
    return _ort(k, ["%d-%02d" % (y, m) for m in range(1, YTD_AY_SAYISI + 1)])

def yuzde(once, sonra):
    if not once or sonra is None: return None
    return (sonra / once - 1) * 100

def hesapla(k):
    d = {"hacim": HAM[k]["hacim"], "cpc": HAM[k].get("cpc"),
         "rekabet": HAM[k].get("rekabet"), "rekabet_index": HAM[k].get("rekabet_index"),
         "y2024": yil(k, 2024), "y2025": yil(k, 2025),
         "t2023": ytd(k, 2023), "t2025": ytd(k, 2025), "t2026": ytd(k, 2026),
         "grup": GRUP_ESLERI.get(k)}
    d["yoy_tam"] = yuzde(d["y2024"], d["y2025"])
    d["yoy_ytd"] = yuzde(d["t2025"], d["t2026"])
    d["uc_yil"] = yuzde(d["t2023"], d["t2026"])
    return d

TUM = {k: hesapla(k) for k in HAM}

YONTEM = ("Hacimler Google Keyword Planner kaynaklıdır ve Almanya (DE) ile Almanca dil kırılımıyla "
          "alınmıştır. Karşılaştırılan pencereler aynı takvim aylarını kapsar: tam yıl karşılaştırması "
          "2024 ve 2025 takvim yıllarının 12 aylık ortalamasıdır; 2026 için Keyword Planner Temmuz'a "
          "kadar veri döndürdüğünden bu yıl YTD (Ocak-Temmuz) olarak alınmış, 2025 de aynı yedi ayla "
          "eşlenmiştir. Üç yıllık değişim aynı Ocak-Temmuz penceresiyle 2023'e bağlanmıştır.")

GRUP_NOTU = ("Google Ads, anlamca yakın kelimeler için birleşik hacim döndürür. Aynı hacmi ve aynı aylık "
             "seriyi paylaşan kelimeler bu raporda tek grup olarak gösterilir; grup üyelerinin hacimleri "
             "toplanmaz.")

def pc_tr(v):
    if v is None: return "-"
    return ("%+.1f" % v).replace(".", ",").replace("+", "+%").replace("-", "-%")
def tb(v):
    if v is None: return "-"
    return "{:,.0f}".format(v).replace(",", ".")
