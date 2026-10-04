# -*- coding: utf-8 -*-
"""Search Console ortak dönemleri ve 12 aylık sayfa toplamları (2. çekim, 04.10.2026).
12 ay: 1 Eki 2025 - 30 Eyl 2026 · sayfa türü ve kategori: 1 Oca - 30 Eyl 2026 (Aralık 2025 adres birleşmesi nedeniyle)."""
import json, os, re
from collections import defaultdict
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D12 = ("1 Eki 2025 - 30 Eyl 2026", "1 Oct 2025 - 30 Sep 2026")
D12U = ("1 Ekim 2025 - 30 Eylül 2026", "1 October 2025 - 30 September 2026")
D26 = ("1 Oca - 30 Eyl 2026", "1 Jan - 30 Sep 2026")
D26U = ("1 Ocak - 30 Eylül 2026", "1 January - 30 September 2026")
DHE = ("1 Haz - 29 Eyl", "1 Jun - 29 Sep")   # yapay zeka özellikleri karşılaştırma penceresi (2025 ve 2026)
Y12 = ["2025-%02d" % m for m in (10, 11, 12)] + ["2026-%02d" % m for m in range(1, 10)]
_SA = json.load(open(os.path.join(P, "veri/ham/gsc2/sayfa_aylik.json"), encoding="utf-8"))
def yol(u): return re.sub(r"^https?://[^/]+", "", u).split("#")[0].split("?")[0].rstrip("/").lower() or "/"
SAYFA12 = defaultdict(lambda: [0, 0, 0.0])
for _m in Y12:
    for _r in _SA[_m]:
        _a = SAYFA12[yol(_r["keys"][0])]; _a[0] += _r["clicks"]; _a[1] += _r["impressions"]; _a[2] += _r["position"] * _r["impressions"]
def sayfa(p):
    """Tek sayfa (adres yolu) için 12 ay [tık, gösterim, ortalama sıra]."""
    c, i, ps = SAYFA12.get(p.rstrip("/").lower() or "/", [0, 0, 0.0]); return [c, i, round(ps / i, 1) if i else None]
