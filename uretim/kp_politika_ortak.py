# -*- coding: utf-8 -*-
"""Kanal politikalari arastirmasi ortak yardimcilari: curl ile sayfa cekme (tarayici UA), onbellek, metne indirgeme."""
import hashlib, html, os, random, re, subprocess, time, json
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "veri", "ham", "derin", "kanal_politikalari"))
SAYFA = os.path.join(KOK, "sayfalar")
os.makedirs(SAYFA, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
TARIH = time.strftime("%Y-%m-%d")

def yol(url):
    return os.path.join(SAYFA, hashlib.md5(url.encode()).hexdigest()[:12] + ".html")

def cek(url, yeniden=False, bekle=True):
    """(durum_kodu, html) doner; onbellekten okur."""
    y = yol(url)
    if os.path.exists(y) and not yeniden:
        d = open(y, encoding="utf-8", errors="replace").read()
        m = re.match(r"<!--HTTP (\d+)-->\n", d)
        return (int(m.group(1)) if m else 200), d[m.end():] if m else d
    if bekle:
        time.sleep(random.uniform(3, 6))
    r = subprocess.run(["curl", "-s", "-L", "-m", "40", "-A", UA, "-H", "Accept-Language: tr-TR,tr;q=0.9",
                        "-H", "Accept: text/html,application/xhtml+xml", "-w", "\n%{http_code}", url],
                       capture_output=True)
    out = r.stdout.decode("utf-8", errors="replace")
    govde, _, kod = out.rpartition("\n")
    kod = int(kod) if kod.strip().isdigit() else 0
    open(y, "w", encoding="utf-8").write("<!--HTTP %d-->\n" % kod + govde)
    return kod, govde

def metin(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|section|article)>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t\xa0]+", " ", h)
    h = re.sub(r"\n\s*\n+", "\n", h)
    return h.strip()

def bul(t, kaliplar, pencere=160, azami=6):
    """Metinde anahtar kalip gecen cevreyi dondurur."""
    sonuc = []
    for k in kaliplar:
        for m in re.finditer(k, t, flags=re.I):
            a = max(0, m.start() - pencere); b = min(len(t), m.end() + pencere)
            s = re.sub(r"\s+", " ", t[a:b]).strip()
            if s not in sonuc:
                sonuc.append(s)
            if len(sonuc) >= azami:
                return sonuc
    return sonuc
