# -*- coding: utf-8 -*-
"""HTML rapor - kabuk, stil, grafik yardimcilari."""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veri

BASE = veri.BASE
VITRA = open(os.path.join(BASE, "logo_0.txt")).read().strip()
INBOUND = open(os.path.join(BASE, "logo_1.txt")).read().strip()

GLOSSARY = {
 "CTR": "Click-through rate; gösterimin tıklamaya dönüşme oranı.",
 "Impression": "Gösterim; sitenin arama sonuçlarında görüntülendiği sayı.",
 "Click": "Tıklama; arama sonucundan siteye gelen ziyaret.",
 "Position": "Ortalama sıra; sitenin arama sonuçlarında ortalama olarak yer aldığı konum.",
 "DR": "Domain Rating; Ahrefs'in alan adı bağlantı gücü puanı, 0-100 ölçeğinde.",
 "Organik trafik": "Ahrefs'in sıralanan kelimelerden tahmin ettiği aylık ücretsiz arama ziyareti.",
 "Paid trafik": "Ahrefs'in Google Ads reklamlarından tahmin ettiği aylık ziyaret.",
 "Long-tail": "Düşük hacimli ancak niyeti belirgin uzun arama ifadeleri.",
 "Autocomplete": "Google arama kutusunda yazarken önerilen tamamlama ifadeleri; gerçek kullanıcı aramalarından türetilir.",
 "Bundle": "Birden fazla ürünün tek fiyatla birlikte satıldığı set.",
 "AOV": "Average Order Value; sipariş başına ortalama sepet tutarı.",
 "Conversion rate": "Ziyaretin satın almaya dönüşme oranı.",
 "Pureplayer": "Fiziksel mağazası olmayan, yalnızca çevrimiçi satış yapan perakendeci.",
 "Marketplace": "Üçüncü taraf satıcılara yer açan pazaryeri platformu.",
 "Retargeting": "Siteyi ziyaret etmiş kullanıcıya sonradan gösterilen hatırlatıcı reklam.",
 "Kartlı Ödeme Endeksi": "TCMB'nin banka ve kredi kartı harcamalarından türettiği endeks; reel seri enflasyondan arındırılmıştır.",
 "Net yüzde": "Anketlerde olumlu yanıt payından olumsuz yanıt payının çıkarılmasıyla elde edilen gösterge.",
 "SSG": "Seramik sağlık gereçleri; klozet, lavabo, bide, pisuvar ve rezervuar gibi vitrifiye ürünler.",
 "BM": "Banyo mobilyası; lavabo dolabı, boy dolabı, aynalı dolap, ayna, tezgah ve tamamlayıcılar.",
 "3P": "Üçüncü taraf satıcı; başka bir satıcının ürününün marka sitesinde listelenip satıldığı model.",
 "GA4": "Google Analytics 4; sitenin ziyaret, dönüşüm ve ürün performansını ölçen analitik aracı.",
 "GSC": "Google Search Console; Google'ın siteye gönderdiği arama trafiğini gösterim, tık ve sıra düzeyinde raporlayan araç.",
 "SERP": "Search Engine Results Page; bir arama için Google'ın döndürdüğü sonuç sayfası.",
 "KD": "Keyword Difficulty; Ahrefs'in bir kelimede ilk 10'a girmenin zorluğunu 0-100 arası puanlayan göstergesi.",
 "TP": "Traffic Potential; bir kelimede 1. sıradaki sayfanın tüm kelimelerinden aldığı tahmini aylık trafik (Ahrefs).",
 "PAA": "People Also Ask; arama sonuç sayfasındaki \"Diğer sorular\" kutusu.",
 "AI Overview": "Google'ın arama sonuçlarının üstünde gösterdiği yapay zeka üretimi özet; kaynak gösterdiği sitelere bağlantı verir.",
 "YoY": "Year over year; bir dönemin bir önceki yılın aynı dönemine göre değişimi.",
 "TCMB": "Türkiye Cumhuriyet Merkez Bankası.",
 "EVDS": "TCMB Elektronik Veri Dağıtım Sistemi; makro ve finansal serilerin yayımlandığı veri tabanı.",
 "BKM": "Bankalararası Kart Merkezi; kartlı ödeme istatistiklerinin kaynağı.",
 "CPC": "Cost per click; Google Ads'te tıklama başına ortalama maliyet.",
 "Buybox": "Pazaryerinde aynı ürünü satan satıcılar arasında \"sepete ekle\" düğmesini kazanan satıcı.",
 "PVC": "Polivinil klorür; suya dayanıklı plastik gövde malzemesi.",
 "MDF": "Orta yoğunluklu lif levha; banyo mobilyasında yaygın gövde malzemesi.",
}

def T(t):
    """Glossary terimini span'a alir."""
    return '<span class="term" data-term="%s">%s</span>' % (GLOSSARY[t].replace('"', "&quot;"), t)

def cizgi(seriler, yukseklik=250, genislik=880, y_etiket="Aylık arama hacmi", aylar=None, x_etiket=None, kalin=None, notlar=None, bagla=False):
    """seriler: [(ad, renk, [degerler])] - aylar listesiyle hizali."""
    aylar = aylar if aylar is not None else veri.AYLAR
    sol, sag, ust, alt = 58, 14, (30 if notlar else 16), 34
    iw = genislik - sol - sag; ih = yukseklik - ust - alt
    tum = [v for _, _, s in seriler for v in s if v is not None]
    ymax = max(tum) * 1.08; ymin = 0
    n = len(aylar)
    def X(i): return sol + iw * i / (n - 1)
    def Y(v): return ust + ih - ih * (v - ymin) / (ymax - ymin)
    p = ['<svg class="chart" viewBox="0 0 %d %d" role="img" preserveAspectRatio="xMidYMid meet">' % (genislik, yukseklik)]
    adim = 10 ** int(math.log10(ymax)) / 2
    while ymax / adim > 6: adim *= 2
    g = 0
    while g <= ymax:
        p.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (sol, Y(g), genislik - sag, Y(g)))
        p.append('<text class="ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 8, Y(g) + 4, f"{int(g):,}".replace(",", ".")))
        g += adim
    for i, ay in enumerate(aylar):
        if x_etiket:
            p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (X(i), yukseklik - 12, x_etiket[i]))
            continue
        if ay.endswith("-01"):
            p.append('<line class="grid yr" x1="%.1f" y1="%d" x2="%.1f" y2="%.1f"/>' % (X(i), ust, X(i), ust + ih))
            p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (X(i), yukseklik - 12, ay[:4]))
    for sk, (ad, renk, s) in enumerate(seriler):
        d = []
        for i, v in enumerate(s):
            if v is None: continue
            d.append(("M" if not d else "L") + "%.1f %.1f" % (X(i), Y(v)))
        p.append('<path class="sr" data-k="%d" d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (sk, " ".join(d), renk, (kalin or {}).get(sk, 2.2)))
        if bagla and sk > 0:
            i0 = next((i for i, v in enumerate(s) if v is not None), None)
            onc = seriler[sk - 1][2]
            if i0 and onc[i0 - 1] is not None:
                p.append('<path class="sr" data-k="%d" d="M%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="%s" stroke-dasharray="3 3"/>' % (sk, X(i0 - 1), Y(onc[i0 - 1]), X(i0), Y(s[i0]), renk, (kalin or {}).get(sk, 2.2)))
    # peak / base notlari: (seri, indeks, metin, 'ust'|'alt')
    for sk, i, metin, yer in (notlar or []):
        v = seriler[sk][2][i]; renk = seriler[sk][1]
        yy = Y(v) - 9 if yer == "ust" else Y(v) + 17
        p.append('<g class="an" data-k="%d"><circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/><text class="anl" x="%.1f" y="%.1f" text-anchor="%s" fill="%s">%s</text></g>' % (sk, X(i), Y(v), renk, X(i) + (-4 if i == 0 else (4 if i == n - 1 else 0)), yy, "start" if i == 0 else ("end" if i == n - 1 else "middle"), renk, metin))
    # imlec cizgisi ve nokta isaretleri (JS ile konumlanir)
    p.append('<line class="hx" x1="0" y1="%d" x2="0" y2="%.1f" style="display:none"/>' % (ust, ust + ih))
    for _ in seriler:
        p.append('<circle class="hp" r="3.6" style="display:none"/>')
    # hover bantlari: her ay icin gorunmez dikdortgen
    bw = iw / (n - 1)
    for i in range(n):
        p.append('<rect class="hz" data-i="%d" x="%.1f" y="%d" width="%.1f" height="%.1f"/>'
                 % (i, X(i) - bw / 2, ust, bw, ih))
    p.append('</svg>')
    lej = '<div class="legend">' + "".join(
        '<span class="lg-t" data-k="%d" role="button" tabindex="0" aria-pressed="true"><i style="background:%s"></i>%s</span>' % (k_, r, a) for k_, (a, r, _) in enumerate(seriler)) + '</div>'
    veri_js = json.dumps({
        "aylar": aylar,
        "px": [round(X(i), 1) for i in range(n)],
        "seriler": [{"ad": a, "renk": r, "deger": s,
                     "py": [(round(Y(v), 1) if v is not None else None) for v in s]}
                    for a, r, s in seriler],
    }, ensure_ascii=False).replace("'", "&#39;")
    return ('<figure class="fig" data-grafik=\'%s\'><figcaption class="figcap">%s</figcaption>'
            '%s<div class="tip" hidden></div>%s</figure>') % (veri_js, y_etiket, "".join(p), lej)

def barlar(veriler, yukseklik=None, genislik=880, olcu="YoY değişim"):
    """veriler: [(etiket, deger, renk)] yatay bar."""
    n = len(veriler); bh = 26; ara = 9
    yukseklik = yukseklik or (n * (bh + ara) + 14)
    sol = 250; sag = 66
    iw = genislik - sol - sag
    vmax = max(abs(v) for _, v, _ in veriler) or 1
    p = ['<svg class="chart" viewBox="0 0 %d %d" role="img" preserveAspectRatio="xMidYMid meet">' % (genislik, yukseklik)]
    for i, (et, v, renk) in enumerate(veriler):
        y = 7 + i * (bh + ara)
        w = iw * abs(v) / vmax
        p.append('<text class="bl" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 12, y + bh * 0.68, et))
        p.append('<rect x="%d" y="%.1f" width="%.1f" height="%d" rx="3" fill="%s"/>' % (sol, y, w, bh, renk))
        _bv = ("%+.1f" % v).replace(".", ",").replace("+", "+%").replace("-", "-%")
        p.append('<text class="bv" x="%.1f" y="%.1f">%s</text>' % (sol + w + 8, y + bh * 0.68, _bv))
        p.append('<rect class="hz" data-i="%d" x="%d" y="%.1f" width="%.1f" height="%d"/>'
                 % (i, sol, y, iw, bh))
    p.append('</svg>')
    veri_js = json.dumps({
        "tip": "bar", "olcu": olcu,
        "satirlar": [{"ad": e, "deger": round(v, 1), "renk": r} for e, v, r in veriler],
    }, ensure_ascii=False).replace("'", "&#39;")
    return '<figure class="fig" data-grafik=\'%s\'>%s<div class="tip" hidden></div></figure>' % (veri_js, "".join(p))
