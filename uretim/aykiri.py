# -*- coding: utf-8 -*-
"""Arama hacmi serilerinde konu disi olaylardan ya da olcum sapmasindan kaynaklanan aykiri aylar.
1) "wc" kelimesi FIFA Dunya Kupasi 2026 (11 Haziran - 19 Temmuz) doneminde futbol aramalariyla karismis;
   Haziran ve Temmuz 2026 hacmi (165K, 201K) normal seviyenin (27-60K) 3-6 kati. Bu iki ay, bir onceki
   yilin ayni ayinin degeriyle degistirilir.
2) "lavabo" kelimesinde Keyword Planner Haziran 2025 - Mayis 2026 arasinda 60-135K gostermektedir (onceki
   ve sonraki aylar 27-40K). Google Trends (Turkiye, 04.10.2026 cekimi) ayni donemde yalnizca ~%30'luk bir
   artis gostermektedir. Bu aylar, sapma oncesi donemin (Eyl 2024 - May 2025) Keyword Planner / Trends
   oraniyla Trends degerinden yeniden olceklenir; Keyword Planner degeri bu degerin altindaysa dokunulmaz."""
import json, os, collections
DUZELT = {"wc": ("2026-06", "2026-07")}
TRENDS_DUZELT = {"lavabo": (("2024-09", "2025-05"), ("2025-06", "2026-05"))}
_TR_DOSYA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "veri", "ham", "trends", "banyo_trends_2026-10-04.json")
_TRA = None
def _trends(kw):
    global _TRA
    if _TRA is None:
        d = json.load(open(_TR_DOSYA, encoding="utf-8")); _TRA = {}
        for i, k in enumerate(d["keywords"]):
            ay = collections.defaultdict(list)
            for h in d["data"]:
                if h["v"][i] is not None: ay[h["hafta"][:7]].append(h["v"][i])
            _TRA[k] = {m: sum(v) / len(v) for m, v in ay.items()}
    return _TRA.get(kw)

def seri(kw, s):
    """s: {"YYYY-MM": hacim} sozlugu; duzeltilmis kopya doner."""
    k = (kw or "").strip().lower()
    if not isinstance(s, dict) or (k not in DUZELT and k not in TRENDS_DUZELT):
        return s
    s = dict(s)
    for a in DUZELT.get(k, ()):
        onceki = "%d-%s" % (int(a[:4]) - 1, a[5:])
        if s.get(onceki) is not None:
            s[a] = s[onceki]
    if k in TRENDS_DUZELT:
        (t0, t1), (d0, d1) = TRENDS_DUZELT[k]; T = _trends(k)
        taban = [m for m in s if t0 <= m <= t1 and s[m] and T.get(m)]
        oran = sum(s[m] for m in taban) / sum(T[m] for m in taban)
        for m in list(s):
            if d0 <= m <= d1 and s[m] and T.get(m):
                yeni = int(round(oran * T[m], -2))
                if s[m] > yeni: s[m] = yeni
    return s
