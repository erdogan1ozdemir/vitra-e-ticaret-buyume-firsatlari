# -*- coding: utf-8 -*-
"""Arama hacmi serilerinde konu disi olaylardan kaynaklanan aykiri aylar.
"wc" kelimesi FIFA Dunya Kupasi 2026 (11 Haziran - 19 Temmuz) doneminde futbol aramalariyla karismis;
Haziran ve Temmuz 2026 hacmi (165K, 201K) normal seviyenin (27-60K) 3-6 kati. Bu iki ay, bir onceki
yilin ayni ayinin degeriyle degistirilir."""
DUZELT = {"wc": ("2026-06", "2026-07")}

def seri(kw, s):
    """s: {"YYYY-MM": hacim} sozlugu; duzeltilmis kopya doner."""
    aylar = DUZELT.get((kw or "").strip().lower())
    if not aylar or not isinstance(s, dict):
        return s
    s = dict(s)
    for a in aylar:
        onceki = "%d-%s" % (int(a[:4]) - 1, a[5:])
        if s.get(onceki) is not None:
            s[a] = s[onceki]
    return s
