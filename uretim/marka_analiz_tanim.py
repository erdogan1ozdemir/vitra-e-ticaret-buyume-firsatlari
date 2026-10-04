# -*- coding: utf-8 -*-
"""Marka araştırmasının ortak tanımları: marka adları, marka adının kelimede bulunması ve kök ifadenin çıkarılması, banyo dışı konu süzgeci."""
import re
MARKA = [("vitra", "VitrA"), ("artema", "Artema"), ("kale", "Kale"), ("creavit", "Creavit"), ("eca", "E.C.A."), ("serel", "Serel"), ("turkuaz", "Turkuaz"),
         ("duravit", "Duravit"), ("ideal standard", "Ideal Standard"), ("isvea", "Isvea"), ("geberit", "Geberit"), ("grohe", "Grohe"), ("hansgrohe", "Hansgrohe"),
         ("bocchi", "Bocchi"), ("visam", "Visam"), ("newarc", "Newarc"), ("roca", "Roca"), ("orka", "Orka"), ("idevit", "Idevit"), ("durul", "Durul"),
         ("kalebodur", "Kalebodur"), ("seranit", "Seranit"), ("ege seramik", "Ege Seramik"), ("çanakkale seramik", "Çanakkale Seramik"), ("yurtbay", "Yurtbay"), ("kütahya seramik", "Kütahya Seramik")]
# yazım biçimleri: e.c.a, kutahya seramik, canakkale seramik
_YAZIM = {"e.c.a": "eca", "e.c.a.": "eca", "kutahya seramik": "kütahya seramik", "canakkale seramik": "çanakkale seramik", "ng kütahya seramik": "kütahya seramik"}
PAZAR = {"trendyol.com", "hepsiburada.com", "koctas.com.tr"}
# banyo dışı konular: ısıtma ve klima (E.C.A.), kilit ve kapı (Kale Kilit), borsa, gıda, giyim
DISI = re.compile(r"kombi|petek|radyat|şofben|sofben|termosifon|ısıtıcı|isitici|klima|kazan|doğalgaz|dogalgaz|kilit|kapı|kapi|çelik|alarm|kasa\b|hisse|borsa|temettü|"
                  r"halka arz|termostatik vana|ofis|tahin|helva|kolye|yüzük|küpe|elbise|gömlek|ceket|pantolon|oyuncak|kalem|telefon|ayakkabı|çanta|tişört|parfüm|boya\b|mutfak dolab")
_DESEN = [(re.compile(r"(?<![\wçğıöşü])" + re.escape(t) + r"(?![\wçğıöşü])"), t, ad) for t, ad in sorted(MARKA, key=lambda m: -len(m[0]))]
def normal(kw):
    k = " ".join(kw.lower().split())
    for a, b in _YAZIM.items(): k = re.sub(r"(?<![\wçğıöşü])" + re.escape(a) + r"(?![\wçğıöşü])", b, k)
    return k
def marka_bul(kw):
    """Kelimedeki marka adını döndürür; birden fazla marka geçen (karşılaştırma) kelimeler alınmaz. "kale" kalebodur'dan ayrıdır."""
    k = normal(kw); bul = []
    for d, t, ad in _DESEN:
        if d.search(k) and not any(t in b_ for b_ in bul): bul.append(t)
    if "hansgrohe" in bul and "grohe" in bul: bul.remove("grohe")
    return dict(MARKA)[bul[0]] if len(bul) == 1 else None
def kok_cikar(kw, ad):
    t = {v: k for k, v in MARKA}[ad]; k = normal(kw)
    return " ".join(re.sub(r"(?<![\wçğıöşü])" + re.escape(t) + r"(?![\wçğıöşü])", " ", k).split())
