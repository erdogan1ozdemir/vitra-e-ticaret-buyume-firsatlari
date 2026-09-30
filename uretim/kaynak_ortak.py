# -*- coding: utf-8 -*-
"""VitrA e-ticaret buyume raporu · kaynak dokumu ortak katmani: satir kaydi, bolum adlari, alan adi cozumleme."""
import os, re, sys, html
from urllib.parse import urlsplit, unquote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kaynakca

KOK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HAM = os.path.join(KOK, "veri", "ham")
DERIN = os.path.join(HAM, "derin")
RAPOR = os.path.join(KOK, "VitrA_E-Ticaret_Buyume_Firsatlari.html")

# ---------------------------------------------------------------- bolumler (rapor HTML'inden)
H = open(RAPOR, encoding="utf-8").read()
BOLUM = {}       # id -> (no, ad)
SIRA = []
for sid, no, govde in re.findall(r'<section id="([^"]+)"><h2><span class="no">(\d+)</span>(.*?)</h2>', H, re.S):
    ad = html.unescape(re.sub(r"<[^>]+>", "", govde)).strip()
    BOLUM[sid] = (int(no), ad); SIRA.append(sid)

def bolum_adi(sid):
    no, ad = BOLUM[sid]
    return "%02d %s" % (no, ad)

# ---------------------------------------------------------------- kaynakca kodu -> bolumler (rapordaki ust simge atiflarindan)
def _kod_bolum():
    lis = re.findall(r'<li id="kay-(\d+)">(.*?)</li>', H, re.S)
    no2kod = {}
    for n, body in lis:
        txt = html.unescape(re.sub(r"<[^>]+>", "", body))
        hit = [c for c, (tr, en, u) in kaynakca.K.items() if tr in txt]
        if len(hit) != 1:
            raise SystemExit("Kaynakca numarasi koda eslenemedi: %s %s" % (n, hit))
        no2kod[int(n)] = hit[0]
    sonuc = {c: [] for c in kaynakca.K}
    for sid, no, body in re.findall(r'<section id="([^"]+)"><h2><span class="no">(\d+)</span>(.*?)</section>', H, re.S):
        if sid in ("kaynakca", "sozluk"):
            continue
        nums = set()
        for m in re.finditer(r'<sup class="ref">(.*?)</sup>', body):
            nums |= set(int(n) for n in re.findall(r'>(\d+)</a>', m.group(1)))
        for n in nums:
            c = no2kod[n]
            if sid not in sonuc[c]:
                sonuc[c].append(sid)
    return sonuc
KOD_BOLUM = _kod_bolum()

# ---------------------------------------------------------------- alan adi
_IKI = {"com", "co", "gov", "org", "net", "edu"}
def host(url):
    return urlsplit(url).netloc.lower().split("@")[-1].split(":")[0]
def alan_adi(url):
    h = host(url)
    p = h.split(".")
    if len(p) >= 3 and p[-2] in _IKI:
        return ".".join(p[-3:])
    if len(p) >= 2:
        return ".".join(p[-2:])
    return h
def anahtar(url):
    """Tekrar denetimi icin normalize adres: sema ve www yok, sonda egik cizgi yok, kucuk harf ana bilgisayar."""
    s = urlsplit(url.strip())
    h = s.netloc.lower()
    if h.startswith("www."):
        h = h[4:]
    yol = s.path.rstrip("/")
    q = ("?" + s.query) if s.query else ""
    return h + yol + q

# ---------------------------------------------------------------- kayit defteri
SATIR = {}   # anahtar -> dict
def ekle(url, amac="", bilgi="", bolum=(), yontem="", tarih="", kod=(), adet=1, href=None, metin=True, tur=None, kodbolum=None):
    """kodbolum: kaynakca kodunun rapordaki atif bolumleri de eklensin mi (varsayilan: yalniz bolum verilmediyse)."""
    k = anahtar(url)
    sec = list(bolum)
    if kodbolum is None:
        kodbolum = not bolum
    for c in kod:
        if c not in kaynakca.K:
            raise SystemExit("Bilinmeyen kaynakca kodu: %s" % c)
        if not kodbolum:
            continue
        for s in KOD_BOLUM[c]:
            if s not in sec:
                sec.append(s)
    for s in sec:
        if s not in BOLUM:
            raise SystemExit("Bilinmeyen bolum: %s" % s)
    r = SATIR.get(k)
    if r is None:
        r = SATIR[k] = {"url": url, "href": href or (url if url.startswith("http") and "{" not in url else None), "amac": [], "bilgi": [], "bolum": [], "yontem": [], "tarih": [], "kod": [], "adet": adet, "tur": tur}
    if metin:
        if amac and amac not in r["amac"]:
            r["amac"].append(amac)
        if bilgi and bilgi not in r["bilgi"]:
            r["bilgi"].append(bilgi)
    for s in sec:
        if s not in r["bolum"]:
            r["bolum"].append(s)
    for y in ([yontem] if isinstance(yontem, str) else yontem):
        if y and y not in r["yontem"]:
            r["yontem"].append(y)
    for t in ([tarih] if isinstance(tarih, str) else tarih):
        if t and t not in r["tarih"]:
            r["tarih"].append(t)
    for c in kod:
        if c not in r["kod"]:
            r["kod"].append(c)
    r["adet"] = max(r["adet"], adet)
    if tur:
        r["tur"] = tur
    return r

def sayi(n):
    """TR binlik ayraci."""
    return "{:,}".format(int(n)).replace(",", ".")
