# -*- coding: utf-8 -*-
"""Tablo kaynak logoları: her tablonun "Tabloyu kopyala" düğmesinin soluna, verinin alındığı kaynağın logosu konur.
Logonun üzerine gelindiğinde kaynak adı, kapsamı ve veri dönemi açılır. Tablonun altındaki kaynak notu aynen kalır.

Kural: tablonun bağlı olduğu kaynak notu (aynı alt başlıktaki not, yoksa bölümün notları) aday kaynakları verir.
Tablo metninde (sütun başlığı ve açıklamaları) adı geçen adaylar seçilir; açık araç adları (Keyword Planner, Search Console,
Ahrefs, TCMB vb.) sütun açıklamasında geçiyorsa not dışında da seçilir. Hiçbiri eşleşmezse notun tüm kaynakları kullanılır.
Hover metni notun o kaynağa ait parçasıdır; parçada tarih yoksa kaynağın veri dönemi eklenir."""
import re, html as _h

# anahtar: (logo alan adı, ad tr, ad en, not ve metin regex tr, regex en, varsayılan kapsam tr, en, araç mı)
K = {
 "kp":         ("ads.google.com", "Google Ads Keyword Planner", "Google Ads Keyword Planner", r"Keyword Planner|Google Ads", r"Keyword Planner|Google Ads",
                "aylık arama hacmi, Türkiye, Türkçe · Eyl 2022 - Ağu 2026", "monthly search volume, Türkiye, Turkish · Sep 2022 - Aug 2026", True),
 "gsc":        ("search.google.com", "Google Search Console", "Google Search Console", r"Search Console", r"Search Console",
                "sc-domain:vitra.com.tr · 1 Eki 2025 - 30 Eyl 2026", "sc-domain:vitra.com.tr · 1 Oct 2025 - 30 Sep 2026", True),
 "shopping":   ("shopping.google.com", "Google Shopping", "Google Shopping", r"Shopping", r"Shopping",
                "ürün ve satıcı listeleri, Türkiye · 29.09.2026", "product and seller listings, Türkiye · 29.09.2026", False),
 "google":     ("google.com.tr", "Google arama sonuçları", "Google search results", r"Google TR|Google arama sonuç|Google sonuç|Google gözlem|AI Overview|Autocomplete|otomatik tamamlama|Google Maps|SERP|arama sonuç sayfası",
                r"Google TR|Google search result|Google result|Google observation|AI Overview|Autocomplete|autocomplete|Google Maps|SERP|search results page",
                "Google TR sonuç sayfası gözlemi · 28.09 - 04.10.2026", "Google TR results page observation · 28.09 - 04.10.2026", False),
 "youtube":    ("youtube.com", "YouTube", "YouTube", r"YouTube", r"YouTube",
                "arama sonuçları ve yorumlar, Türkiye · 28-29.09.2026", "search results and comments, Türkiye · 28-29.09.2026", False),
 "ahrefs":     ("ahrefs.com", "Ahrefs", "Ahrefs", r"Ahrefs", r"Ahrefs",
                "Site Explorer ve Keywords Explorer, Türkiye, tahmini trafik · 27-28.09.2026", "Site Explorer and Keywords Explorer, Türkiye, estimated traffic · 27-28.09.2026", True),
 "seomonitor": ("seomonitor.com", "SEOmonitor", "SEOmonitor", r"SEOmonitor", r"SEOmonitor",
                "vitra.com.tr kampanyası, mobil · 03.10.2026", "vitra.com.tr campaign, mobile · 03.10.2026", True),
 "similarweb": ("similarweb.com", "Similarweb", "Similarweb", r"Similarweb", r"Similarweb",
                "site trafiği ve kanal kırılımı · Haz - Ağu 2026", "site traffic and channel split · Jun - Aug 2026", True),
 "tcmb":       ("tcmb.gov.tr", "TCMB EVDS", "CBRT EVDS", r"TCMB|EVDS|BKM", r"CBRT|EVDS|BKM",
                "Merkez Bankası veri sistemi · 28.09.2026 itibarıyla yayımlanan son veriler", "Central Bank data system · latest data published as of 28.09.2026", True),
 "tuik":       ("tuik.gov.tr", "TÜİK", "TurkStat", r"TÜİK", r"TurkStat",
                "ADNKS 2024, konut satış ve yapı izin istatistikleri", "ABPRS 2024, house sales and building permit statistics", True),
 "sikayetvar": ("sikayetvar.com", "Şikayetvar", "Şikayetvar", r"Şikayetvar", r"Şikayetvar",
                "VitrA ve Artema marka sayfaları, şikayet metinleri · Eki 2024 - Eyl 2026", "VitrA and Artema brand pages, complaint texts · Oct 2024 - Sep 2026", False),
 "chatgpt":    ("chatgpt.com", "ChatGPT", "ChatGPT", r"ChatGPT", r"ChatGPT",
                "yapay zeka yanıt takibi, 125 soru · 4 Eyl - 3 Eki 2026", "AI answer tracking, 125 questions · 4 Sep - 3 Oct 2026", False),
 "gemini":     ("gemini.google.com", "Gemini", "Gemini", r"Gemini", r"Gemini",
                "yapay zeka yanıt takibi, 125 soru · 4 Eyl - 3 Eki 2026", "AI answer tracking, 125 questions · 4 Sep - 3 Oct 2026", False),
 "wikipedia":  ("wikipedia.org", "Wikidata ve Wikipedia", "Wikidata and Wikipedia", r"Wikidata|Wikipedia", r"Wikidata|Wikipedia",
                "VitrA maddeleri · 02.10.2026", "VitrA entries · 02.10.2026", False),
 "akakce":     ("akakce.com", "Akakçe", "Akakçe", r"Akakçe", r"Akakçe",
                "arama, ürün ve kategori sayfaları · 30.09.2026", "search, product and category pages · 30.09.2026", False),
 "cimri":      ("cimri.com", "Cimri", "Cimri", r"Cimri", r"Cimri",
                "kategori, marka ve ürün sayfaları · 30.09.2026", "category, brand and product pages · 30.09.2026", False),
 "trendyol":   ("trendyol.com", "Trendyol", "Trendyol", r"Trendyol", r"Trendyol",
                "kategori, arama, çok satan ve ürün sayfaları · 29-30.09.2026", "category, search, best-seller and product pages · 29-30.09.2026", False),
 "hepsiburada": ("hepsiburada.com", "Hepsiburada", "Hepsiburada", r"Hepsiburada", r"Hepsiburada",
                "kategori, arama, çok satan ve ürün sayfaları · 29-30.09.2026", "category, search, best-seller and product pages · 29-30.09.2026", False),
 "koctas":     ("koctas.com.tr", "Koçtaş", "Koçtaş", r"Koçtaş", r"Koçtaş",
                "e-mağaza kategori ve ürün sayfaları · 29-30.09.2026", "online store category and product pages · 29-30.09.2026", False),
 "vitra":      ("vitra.com.tr", "vitra.com.tr", "vitra.com.tr", r"(?<!sc-domain:)vitra\.com\.tr(?! kampanya)", r"(?<!sc-domain:)vitra\.com\.tr(?! campaign)",
                "kategori, ürün, hizmet ve arama sayfaları · 29.09 - 04.10.2026", "category, product, service and search pages · 29.09 - 04.10.2026", False),
 "web":        ("web", "Web siteleri", "Websites", r"web site|yardım|e-mağaza|hizmet ve kampanya|kampanya sayfa|rakip site|kategori sitemap|Seramik Federasyonu|Eczacıbaşı|\bVDS-",
                r"website|help|online store|service and campaign|campaign page|competitor site|category sitemap|Ceramics Federation|Eczacıbaşı|\bVDS-",
                "rakip ve benzer oyuncuların web siteleri, yardım, hizmet ve kampanya sayfaları · 28-30.09.2026", "websites, help, service and campaign pages of competitors and comparable players · 28-30.09.2026", False),
}
# vitra.com.tr yalnız kaynak olduğu bölümlerde kullanılır (diğer bölümlerde ölçülen site olarak konu durumundadır)
VITRA_BOLUM = {"derin", "katalog", "set", "model", "yolculuk", "fiyat", "yeni", "geo", "politika"}
# Karma ve sentez tablolarda açık atama: (bölüm, alt başlığın başı) -> anahtarlar
ATAMA = [
 ("serp", "Kullanıcının Google'da sorduğu sorular", ["google"]),
 ("ihtiyac", "Kategori bazında ihtiyaç", ["kp"]), ("ihtiyac", "", ["kp"]),
 ("marka", "Autocomplete önerilerinin tema oranı", ["google"]), ("marka", "En çok tık getiren sorgular", ["gsc"]),
 ("organik", "Kategori bazında organik trafik", ["gsc", "kp"]), ("organik", "Trafik hangi sayfa türlerine", ["gsc"]), ("organik", "En çok tık alan sayfalar", ["gsc"]),
 ("set", "Rakip ve benzer modeller", ["web"]),
 ("derin", "Aynı model kodunda", ["trendyol", "hepsiburada", "akakce", "cimri", "vitra"]),
 ("yolculuk", "Sepet ve ödeme", ["vitra"]), ("yolculuk", "Dönüşüm fırsatları", ["vitra"]), ("yolculuk", "Site içi arama", ["vitra", "kp"]), ("yolculuk", "Yolculuk adımları", ["google", "vitra"]),
 ("geo", "Ölçüm setleri", ["chatgpt", "gemini", "google", "seomonitor", "gsc"]), ("geo", "Yapay zeka yanıt takibi", ["chatgpt", "gemini", "google"]),
 ("yapayzeka", "Yapay zeka özelliklerinde gösterim", ["gsc"]), ("yapayzeka", "Yapay zeka gösterim payına göre", ["gsc"]), ("yapayzeka", "Yapay zeka özelliklerinde en çok", ["gsc"]), ("yapayzeka", "Sayfa türüne göre yapay zeka", ["gsc"]),
 ("yapayzeka", "AI Overview çıkan ve çıkmayan", ["gsc", "ahrefs"]),
 ("geo", "SEOmonitor takibi", ["seomonitor"]), ("geo", "Rapor hedef kelimeleri", ["google"]), ("geo", "Sitenin hazırlığı", ["gsc"]),
 ("politika", "Ödeme ve taksit", ["web"]), ("politika", "Kargo, teslimat", ["web"]), ("politika", "Garanti, yedek parça", ["web"]),
 ("katalog", "", ["vitra", "kp"]), ("yeni", "", ["kp", "vitra", "web"]), ("makro", "Yıllık banyo yenileme", ["tuik", "web"]), ("rakip", "Site trafiği", ["similarweb"]),
 ("adimlar", "", []), ("marka", "Marka adıyla", ["kp"]), ("marka", "Marka + kategori", ["kp"]), ("marka", "\"vitra\" +", ["kp"]), ("marka", "\"vitra\" ile birlikte", ["kp"]),
]
# Resmi mağaza paneli: aynı logo, farklı kapsam
PANEL = {
 "trendyol": ("Trendyol satıcı paneli (VitrA resmi mağazası)", "Trendyol seller panel (VitrA official store)",
              "dışa aktarım · satış 2025 Q4 - 2026 Q3, görüntülenme 2025 ve Oca - Eyl 2026, listeler Eylül 2026", "export · sales 2025 Q4 - 2026 Q3, views 2025 and Jan - Sep 2026, lists September 2026"),
 "hepsiburada": ("Hepsiburada satıcı paneli (VitrA resmi mağazası)", "Hepsiburada seller panel (VitrA official store)",
                 "dışa aktarım · son 12 ay (29-30.09.2026 itibarıyla)", "export · last 12 months (as of 29-30.09.2026)"),
}
SIRA = list(K)
_TARIH = re.compile(r"\d{2}\.\d{2}\.\d{4}|\b\d{1,2}[.-]\d{1,2}\.\d{2}\.\d{4}|\b(?:Oca|Şub|Mar|Nis|May|Haz|Tem|Ağu|Eyl|Eki|Kas|Ara|Jan|Feb|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zçğıöşü]*\.? \d{4}|\b20\d\d Q\d|\bson 12 ay|\blast 12 months|\b20\d\d-\d{2}|\b20\d\d\b")


def _duz(t):
    return " ".join(_h.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"\[\[ref:[^\]]*\]\]", "", t))).split())


def _parcala(metin, en=False):
    """Kaynak notunu kaynak bazlı parçalara böler: {anahtar: 'parça · parça'}."""
    metin = re.sub(r"^(Kaynak|Source):\s*", "", metin)
    out, son, genel = {}, None, []
    for p in [p.strip() for p in re.split(r"\s·\s", metin) if p.strip()]:
        if re.fullmatch(r"[\d.\s,-]+", p) and _TARIH.search(p):   # yalnız tarihten oluşan parça notun tamamına aittir
            genel.append(p); continue
        bulunan = [k for k in SIRA if re.search(K[k][4 if en else 3], p)]
        # Google yüzeyleri ile Shopping / Search Console / Keyword Planner çakışmasın
        if any(k in bulunan for k in ("shopping", "gsc", "kp")) and "google" in bulunan and not re.search(r"AI Overview|SERP|Google TR|Autocomplete|otomatik tamamlama|Maps", p): bulunan.remove("google")
        if bulunan:
            for k in bulunan: out.setdefault(k, []).append(p)
            son = bulunan[-1]
        elif son:
            out[son].append(p)
    sonuc = {}
    for k, v in out.items():
        t = " · ".join(v)
        if genel and not _TARIH.search(t): t += " · " + " · ".join(genel)
        sonuc[k] = t
    return sonuc


def _metin_anahtarlari(t, sadece_arac=False):
    return [k for k in SIRA if (K[k][7] or not sadece_arac) and re.search(K[k][3], t)]


_FIG = re.compile(r'''<figure class="fig[^"]*"(?:\s+[a-z-]+=(?:"[^"]*"|'[^']*'))*\s*>''')
_TAB = re.compile(r'<div class="tw(?: [^"]*)?"[^>]*>.*?</table></div>', re.S)


def uygula(govde, EK, x):
    """govde: bölüm HTML'i ([[ref]] çözülmeden önce); EK: TR -> EN çeviri sözlüğü; x: kayıt fonksiyonu.
    Tablolarda logolar "Tabloyu kopyala" çubuğuna (JS), grafiklerde başlık satırının sağına yerleşir."""
    rapor = []
    def ikonlar(sid, ic, pos, metin, tur):
        notlar = []   # (konum, {k: parça_tr}, {k: parça_en})
        for n in re.finditer(r'<p class="src">(.*?)</p>', ic, re.S):
            tr = _duz(n.group(1)); en = EK.get(tr, "")
            notlar.append((n.start(), _parcala(tr), _parcala(en, True) if en else {}))
        basliklar = [h.start() for h in re.finditer(r"<h3", ic)]
        onc = [b for b in basliklar if b < pos]; son = [b for b in basliklar if b > pos]
        a, b = (onc[-1] if onc else 0, son[0] if son else len(ic))
        ilgili = [nn for nn in notlar if a < nn[0] < b and nn[0] > pos] or [nn for nn in notlar if a < nn[0] < b] or \
                 [nn for nn in notlar if nn[0] > pos][:1] or notlar[-1:]
        aday_tr, aday_en = {}, {}
        for _, ptr, pen in ilgili:
            for k_, v_ in ptr.items(): aday_tr.setdefault(k_, v_)
            for k_, v_ in pen.items(): aday_en.setdefault(k_, v_)
        if sid not in VITRA_BOLUM: aday_tr.pop("vitra", None); aday_en.pop("vitra", None)
        secim = [k_ for k_ in SIRA if k_ in aday_tr and re.search(K[k_][3], metin)]
        secim += [k_ for k_ in _metin_anahtarlari(metin, True) if k_ not in secim]
        if not secim: secim = [k_ for k_ in SIRA if k_ in aday_tr]
        h3 = re.search(r"<h3[^>]*>(.*?)</h3>", ic[a:b], re.S)
        h3t = _duz(h3.group(1)) if h3 else ""
        atama = next((L_ for s_, b_, L_ in ATAMA if s_ == sid and (h3t.startswith(b_) if b_ else not h3t)), None)
        if atama is not None: secim = atama
        ikon = []
        for k_ in [k_ for k_ in SIRA if k_ in secim]:
            ad_tr, ad_en, kap_tr, kap_en = K[k_][1], K[k_][2], aday_tr.get(k_, ""), aday_en.get(k_, "")
            if sid == "panel" and k_ in PANEL:
                ad_tr, ad_en, kap_tr, kap_en = PANEL[k_]
            elif not kap_tr or not kap_en:
                kap_tr, kap_en = K[k_][5], K[k_][6]
            elif not _TARIH.search(kap_tr):
                kap_tr, kap_en = kap_tr + " · " + K[k_][5], kap_en + " · " + K[k_][6]
            kap_tr = re.sub(r"^" + re.escape(ad_tr) + r"\s*[·:]\s*", "", kap_tr) or K[k_][5]
            kap_en = re.sub(r"^" + re.escape(ad_en) + r"\s*[·:]\s*", "", kap_en) or K[k_][6]
            x(kap_tr, kap_en); x(ad_tr, ad_en)
            ikon.append('<span class="tk" tabindex="0" role="img" aria-label="%s" data-t="%s"><i class="lg lg-%s"></i></span>'
                        % (_h.escape(ad_tr, quote=True), _h.escape(kap_tr, quote=True), K[k_][0].replace(".", "_")))
        rapor.append((sid, tur, h3t, secim))
        return "".join(ikon)
    def bolum(m):
        sid, ic = m.group(1), m.group(2)
        if sid == "ek": return m.group(0)
        # 1) grafikler: logolar başlık satırının sağına (başlık yoksa grafiğin üstüne ayrı satır)
        parcalar = []; konum = 0
        for f in _FIG.finditer(ic):
            cap = re.match(r'<figcaption class="figcap">(.*?)</figcaption>', ic[f.end():], re.S)
            metin = _duz(cap.group(1)) if cap else ""
            ik = ikonlar(sid, ic, f.start(), metin, "grafik")
            parcalar.append(ic[konum:f.end()])
            if ik and cap:
                parcalar.append('<figcaption class="figcap"><span class="tkay fkay">%s</span>%s</figcaption>' % (ik, cap.group(1))); konum = f.end() + cap.end()
            else:
                parcalar.append('<div class="tkay fkay fk-satir">%s</div>' % ik if ik else ""); konum = f.end()
        parcalar.append(ic[konum:]); ic = "".join(parcalar)
        # 2) tablolar: logolar tablodan önce; JS "Tabloyu kopyala" çubuğuna taşır
        parcalar = []; konum = 0
        for t in _TAB.finditer(ic):
            metin = " ".join(_h.unescape(v) for v in re.findall(r'data-t="([^"]*)"', t.group(0))) + " " + _duz(" ".join(re.findall(r"<th[^>]*>(.*?)</th>", t.group(0), re.S)))
            ik = ikonlar(sid, ic, t.start(), metin, "tablo")
            parcalar.append(ic[konum:t.start()]); parcalar.append('<div class="tkay">%s</div>' % ik if ik else ""); parcalar.append(t.group(0)); konum = t.end()
        parcalar.append(ic[konum:])
        return '<section id="%s">%s</section>' % (sid, "".join(parcalar))
    govde = re.sub(r'<section id="([^"]+)">(.*?)</section>', bolum, govde, flags=re.S)
    return govde, rapor
