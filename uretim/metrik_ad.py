# -*- coding: utf-8 -*-
"""Metrik adlarının rapor genelinde tekilleştirilmesi: Türkçe metinde GA4, Search Console ve SEO araçlarının metrikleri İngilizce adıyla yazılır
(oturum -> session, gösterim -> impression, tıklama -> click, gelir / ciro -> revenue, ortalama sıra -> average position, arama hacmi -> search volume,
ziyaret -> visit, trafik -> traffic, görüntülenme -> view, dönüşüm oranı -> conversion rate, etkileşim oranı -> engagement rate,
ortalama sipariş tutarı -> AOV, satın alma (metrik olarak) -> purchase). Türkçe ekler kesme işaretiyle ve İngilizce okunuşa uygun ünlüyle eklenir.

Dönüşüm çeviri katmanından hemen önce, Türkçe HTML'in metin düğümlerine, açıklama niteliklerine ve grafik verisine uygulanır; aynı fonksiyon
çeviri sözlüğünün anahtarlarına da uygulandığı için İngilizce karşılıklar eşleşmeye devam eder. Kaynak dosyalardaki veri anahtarları (ör. "oturum")
etkilenmez. Metrik dışı anlamlar korunur: satış hacmi, ıslak hacim, mağaza ziyareti, küvet dönüşümü, etkileşim modeli, "sayfasını görüntüle" bağlantısı,
fiil olarak "gelir" (gelir mi, ... ile gelir)."""
import re, json
from collections import Counter

DEGISIM = Counter()
_H = "A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ"
_ON = r"(?<![%s'’\-/_])" % _H          # solunda harf, kesme, tire, eğik çizgi yok


def _buyuk(ilk, en):
    return en[:1].upper() + en[1:] if ilk[:1].isupper() else en


def _kural(desen, harita, en, on_dislama=None, sonra_dislama=None):
    """desen: (baş harf grubu)(gövde)(ek); harita: ek -> İngilizce ek ("" -> ek yok). Haritada olmayan ek dönüştürülmez."""
    rx = re.compile(_ON + desen + r"(?![%s])" % _H)
    def f(m):
        ek = m.group("ek") or ""
        if ek not in harita: return m.group(0)
        if on_dislama and re.search(r"\b" + on_dislama + r"\s*$", m.string[max(0, m.start() - 24):m.start()], re.I): return m.group(0)
        if sonra_dislama and re.match(sonra_dislama, m.string[m.end():m.end() + 24], re.I): return m.group(0)
        yeni = _buyuk(m.group(0), en) + harita[ek]
        DEGISIM[(m.group(0), yeni)] += 1
        return yeni
    return rx, f


# ---- ek haritaları (İngilizce kelimenin okunuşuna göre: session / impression / position -> ı-a; click / visit / traffic -> i-e; volume -> u-a)
def _ses(ekler_tr, donustur):
    return {e: donustur(e) for e in ekler_tr}

_OTURUM = {"": "", "u": "'ı", "un": "'ın", "a": "'a", "da": "'da", "dan": "'dan", "daki": "'daki", "la": "'la", "lar": "'lar", "ları": "'ları", "ların": "'ların",
           "larda": "'larda", "lardan": "'lardan", "lara": "'lara", "larının": "'larının", "larına": "'larına", "larını": "'larını", "lardaki": "'lardaki",
           "larla": "'larla", "unda": "'ında", "unu": "'ını", "una": "'ına", "unun": "'ının", "lardır": "'lardır", "dur": "'dur", "larıdır": "'larıdır"}
_GOSTERIM = {"": "", "i": "'ı", "in": "'ın", "e": "'a", "de": "'da", "den": "'dan", "deki": "'daki", "le": "'la", "ler": "'lar", "leri": "'ları", "lerin": "'ların",
             "lerde": "'larda", "lerinin": "'larının", "ine": "'ına", "inin": "'ının", "indeki": "'ındaki", "ini": "'ını", "dir": "'dır", "iyle": "'ıyla", "inde": "'ında",
             "lerden": "'lardan", "lere": "'lara"}
_TIKLAMA = {"": "", "sı": "'i", "ları": "'leri", "sının": "'inin", "ya": "'e", "yı": "'i", "lar": "'ler", "ların": "'lerin", "nın": "'in", "da": "'de", "dan": "'den",
            "sına": "'ine", "sını": "'ini", "larının": "'lerinin", "larını": "'lerini", "larına": "'lerine"}
_GELIR = {"": "", "i": "'su", "inin": "'sunun", "in": "'nun", "indeki": "'sundaki", "ini": "'sunu", "e": "'ya", "den": "'dan", "deki": "'daki", "de": "'da",
          "idir": "'sudur", "ine": "'suna", "inde": "'sunda", "iyle": "'suyla", "ler": "'lar", "leri": "'ları", "lerin": "'ların"}
_CIRO = {"": "", "nun": "'nun", "ya": "'ya", "sunda": "'sunda", "sunun": "'sunun", "da": "'da", "su": "'su", "dan": "'dan", "yu": "'yu", "sunu": "'sunu", "suna": "'suna"}
_SIRA = {"": "", "sı": "'ı", "sını": "'ını", "sında": "'ında", "da": "'da", "ya": "'a", "nın": "'ın", "sının": "'ının", "sıdır": "'ıdır", "sıyla": "'ıyla", "lar": "'lar"}
_ORAN = {"": "", "ı": "", "ının": "'inin", "ında": "'inde", "ından": "'inden", "ına": "'ine", "ıdır": "'idir", "ını": "'ini", "ları": "'leri", "lar": "'ler"}
_HACIM = {"": "", "i": "", "ine": "'a", "inin": "'un", "indeki": "'daki", "idir": "'dur", "iyle": "'la", "ini": "'u", "in": "'un", "e": "'a", "dir": "'dur",
          "den": "'dan", "leri": "'ları", "ler": "'lar", "lerin": "'ların", "li": "'lu", "de": "'da"}
_ZIYARET = {"": "", "i": "'i", "in": "'in", "e": "'e", "le": "'le", "ler": "'ler", "leri": "'leri", "lerin": "'lerin", "lerinin": "'lerinin", "ini": "'ini",
            "lerini": "'lerini", "lerde": "'lerde", "ten": "'ten", "te": "'te", "ine": "'ine", "lere": "'lere", "lerine": "'lerine"}
_TRAFIK = {"k": "", "ği": "'i", "kli": "'li", "ğinin": "'inin", "ğini": "'ini", "ğin": "'in", "kte": "'te", "kleri": "'leri", "ğe": "'e", "ktir": "'tir",
           "kle": "'le", "ğinden": "'inden", "kler": "'ler", "klerin": "'lerin", "ğine": "'ine", "kten": "'ten", "ğinde": "'inde", "ğiyle": "'iyle"}
_VIEW = {"": "", "si": "'ı", "nin": "'ın", "den": "'dan", "lerin": "'ların", "de": "'da", "ye": "'a", "siyle": "'ıyla", "sine": "'ına", "sinin": "'ının",
         "yle": "'la", "ler": "'lar", "leri": "'ları"}
_AOV = {"": "", "ı": "", "ının": "'nin", "ına": "'ye", "ında": "'de", "ından": "'den", "ıdır": "'dir"}

KURALLAR = [
    # çok kelimeli metrikler önce
    _kural(r"(?P<b>[Tt]ıklama oran)(?P<ek>[a-zçğıöşü]*)", {"": "", "ı": "", "ının": "'ın", "ından": "'dan", "ıdır": "'dır", "ına": "'a", "ında": "'da", "ını": "'ı"}, "CTR"),
    _kural(r"(?P<b>[Dd]önüşüm oran)(?P<ek>[a-zçğıöşü]*)", _ORAN, "conversion rate"),
    _kural(r"(?P<b>[Ee]tkileşim oran)(?P<ek>[a-zçğıöşü]*)", _ORAN, "engagement rate"),
    _kural(r"(?P<b>[Ee]tkileşimli oturum)(?P<ek>[a-zçğıöşü]*)", _OTURUM, "engaged session"),
    _kural(r"(?P<b>[Oo]rt\. sipariş tutar)(?P<ek>[a-zçğıöşü]*)", _AOV, "AOV"),
    _kural(r"(?P<b>[Oo]rtalama sipariş tutar)(?P<ek>[a-zçğıöşü]*)", _AOV, "AOV"),
    _kural(r"(?P<b>[Oo]rt\. sıra)(?P<ek>[a-zçğıöşü]*)", _SIRA, "avg. position"),
    _kural(r"(?P<b>[Oo]rtalama sıra)(?P<ek>[a-zçğıöşü]*)", _SIRA, "average position"),
    _kural(r"(?P<b>[Aa]rama hacm)(?P<ek>[a-zçğıöşü]*)", {"i": "", "ine": "'a", "inin": "'un", "indeki": "'daki", "idir": "'dur", "iyle": "'la", "ini": "'u", "in": "'un", "inde": "'da"}, "search volume"),
    _kural(r"(?P<b>[Aa]ranma hacm)(?P<ek>[a-zçğıöşü]*)", {"i": "", "ine": "'a", "inin": "'un", "indeki": "'daki", "ini": "'u"}, "search volume"),
    _kural(r"(?P<b>[Aa]rama hacim)(?P<ek>[a-zçğıöşü]*)", {"": "", "leri": "'ları", "ler": "'lar", "lerin": "'ların", "li": "'lu", "de": "'da", "den": "'dan", "dir": "'dur"}, "search volume"),
    # tek kelimeli metrikler
    _kural(r"(?P<b>[Oo]turum)(?P<ek>[a-zçğıöşü]*)", _OTURUM, "session"),
    _kural(r"(?P<b>[Gg]österim)(?P<ek>[a-zçğıöşü]*)", _GOSTERIM, "impression", on_dislama=r"(?:fiyat|stok|net fiyat|ürün|indirim|kampanya)"),
    _kural(r"(?P<b>[Tt]ıklama)(?P<ek>[a-zçğıöşü]*)", _TIKLAMA, "click"),
    _kural(r"(?P<b>[Gg]elir)(?P<ek>[a-zçğıöşü]*)", _GELIR, "revenue"),
    _kural(r"(?P<b>[Cc]iro)(?P<ek>[a-zçğıöşü]*)", _CIRO, "revenue"),
    _kural(r"(?P<b>[Hh]acm)(?P<ek>[a-zçğıöşü]*)", {"e": "'a", "i": "", "ine": "'a", "inin": "'un", "indeki": "'daki", "idir": "'dur", "iyle": "'la", "ini": "'u", "in": "'un", "inde": "'da"}, "search volume",
           on_dislama=r"(?:satış|ıslak|islak|depo|su|hazne|rezervuar|tank)"),
    _kural(r"(?P<b>[Hh]acim)(?P<ek>[a-zçğıöşü]*)", {"": "", "leri": "'ları", "ler": "'lar", "lerin": "'ların", "li": "'lu", "de": "'da", "den": "'dan", "dir": "'dur"}, "search volume",
           on_dislama=r"(?:satış|ıslak|islak|depo|su|hazne|rezervuar|tank|büyük|küçük)", sonra_dislama=r"\s+(?:ürün|ve ölçüye|paket|kargo|mobilya)"),
    _kural(r"(?P<b>[Zz]iyaret)(?P<ek>[a-zçğıöşü]*)", _ZIYARET, "visit", on_dislama=r"(?:mağaza|mağazayı|showroom|bayi|ev|servis)"),
    _kural(r"(?P<b>[Tt]rafi)(?P<ek>[kğ][a-zçğıöşü]*)", _TRAFIK, "traffic"),
    _kural(r"(?P<b>[Gg]örüntülenme)(?P<ek>[a-zçğıöşü]*)", _VIEW, "view"),
    _kural(r"(?P<b>[Ii]zlenme)(?P<ek>[a-zçğıöşü]*)", {"": "", "si": "'ı", "ye": "'a", "nin": "'ın", "ler": "'lar", "leri": "'ları", "lerin": "'ların", "de": "'da", "den": "'dan", "sine": "'ına"}, "view"),
    _kural(r"(?P<b>[Tt]ık)(?P<ek>[a-zçğıöşü]*)", {"": "", "lar": "'ler", "ları": "'leri", "ların": "'lerin", "larının": "'lerinin", "ı": "'i", "ın": "'in", "a": "'e", "ta": "'te",
                                                  "tan": "'ten", "lara": "'lere", "larını": "'lerini", "larına": "'lerine", "la": "'le", "lardaki": "'lerdeki"}, "click"),
    _kural(r"(?P<b>[Gg]örüntüleme)(?P<ek> / click)", {" / click": " / click"}, "view"),
]
# "gelir" fiil olarak (geldiği anlamında) kullanıldığında korunur: ardından soru eki ya da "ile ... gelir" kalıbı
_GELIR_FIIL = re.compile(r"\b(?:ile|birlikte|beraber|öne|ortaya|sırayla|önce|sonra|ilk sırada|üstte|başta)\s+gelir\b|\bgelir\s+mi\b|\b[Oo]turum aç\w*|\b[Oo]turum kapat\w*", re.I)   # fiil "gelir" ve oturum açma (giriş yapma) korunur
# satın alma yalnız metrik olarak: başlık / etiket ("Satın alma", "Satın alma 2025"), sayıyla ("2.473 satın alma"), "satın alma sayısı / oranı"
_SATIN = [
    (re.compile(r"^Satın alma(?=$| \d{4}$| /)"), "Purchase"),
    (re.compile(r"\b(session|revenue|Session|Revenue)(,| ve) satın alma\b(?![a-zçğıöşü])"), r"\1\2 purchase"),
    (re.compile(r"\b([Ss])atın alma (ve|,) (revenue|session)\b"), lambda m: ("P" if m.group(1) == "S" else "p") + "urchase " + m.group(2) + " " + m.group(3)),
    (re.compile(r"\bsatın alma (?=\((?:çizgi|çubuk)\))"), "purchase "),
    (re.compile(r"(?<![\w.,])(\d[\d.,]*[KM]?) satın almanın"), r"\1 purchase'ın"),
    (re.compile(r"\bsatın almanın (?=kaynak)"), "purchase'ın "),
    (re.compile(r"\b([Ss])atın alma (?=revenue|olay)"), lambda m: ("P" if m.group(1) == "S" else "p") + "urchase "),
    (re.compile(r"\bdüşen satın alma\b(?![a-zçğıöşü])"), "düşen purchase"),
    (re.compile(r"\bsatın alması (?=\d)"), "purchase'ı "),
    (re.compile(r"\bya da satın alma atanma"), "ya da purchase atanma"),
    (re.compile(r"(?<![\w.,])(\d[\d.,]*[KM]?) satın alma(?![a-zçğıöşü])(?! ve montaj)(?! sorus)"), r"\1 purchase"),
    (re.compile(r"\b([Ss])atın alma sayısı"), lambda m: ("P" if m.group(1) == "S" else "p") + "urchase sayısı"),
    (re.compile(r"\b([Ss])atın alma oranı(?=$|[^a-zçğıöşü])"), lambda m: ("P" if m.group(1) == "S" else "p") + "urchase rate"),
    (re.compile(r"\b([Ss])atın alma oranının"), lambda m: ("P" if m.group(1) == "S" else "p") + "urchase rate'inin"),
    (re.compile(r"^E-ticaret satın alma"), "E-ticaret purchase"),
    (re.compile(r"^Görüntülenen ürün$"), "Items viewed"),
    (re.compile(r"^Satın alınan ürün$"), "Items purchased"),
    (re.compile(r"^Görüntüleme$"), "View"),
    (re.compile(r"^Hemen çıkma$"), "Bounce rate"),
    (re.compile(r"\b([Hh])emen çıkma oranı"), lambda m: ("B" if m.group(1) == "H" else "b") + "ounce rate"),
    (re.compile(r"\b([Oo])lay sayısı \(Event count\)"), lambda m: ("E" if m.group(1) == "O" else "e") + "vent count"),
    (re.compile(r"\b([Oo])lay sayısı(?![a-zçğıöşü])"), lambda m: ("E" if m.group(1) == "O" else "e") + "vent count"),
    (re.compile(r"\b([Oo])lay sayıları"), lambda m: ("E" if m.group(1) == "O" else "e") + "vent count'ları"),
    (re.compile(r"\b([Oo])rt\. süre\b"), lambda m: ("A" if m.group(1) == "O" else "a") + "vg. duration"),
    (re.compile(r"\b([Oo])rtalama süre\b"), lambda m: ("A" if m.group(1) == "O" else "a") + "verage duration"),
    (re.compile(r"^Aylık arama$"), "Aylık search volume"),
    (re.compile(r"\b([Aa])ylık arama (?=·)"), lambda m: m.group(1) + "ylık search volume "),
    (re.compile(r"\baylık arama sayısı"), "aylık search volume"),
]


def donustur(s):
    if not s or not isinstance(s, str): return s
    if not re.search(r"[Oo]turum|[Gg]österim|[Tt]ık|[Ii]zlenme|[Hh]emen çıkma|[Oo]lay sayı|süre|[Aa]ylık arama|[Gg]örüntülenen ürün|[Ss]atın alınan ürün|[Gg]elir|[Cc]iro|[Ss]ıra|[Hh]ac[im]|[Zz]iyaret|[Tt]rafi|[Gg]örüntüle|[Dd]önüşüm|[Ee]tkileşim|sipariş tutar|[Ss]atın alma", s):
        return s
    korunan = []
    def koru(m):
        korunan.append(m.group(0)); return "\x00%d\x00" % (len(korunan) - 1)
    s2 = _GELIR_FIIL.sub(koru, s)
    for rx, f in KURALLAR:
        s2 = rx.sub(f, s2)
    for rx, yeni in _SATIN:
        onc = s2
        s2 = rx.sub(yeni, s2)
        if s2 != onc: DEGISIM[("satın alma", rx.pattern[:30])] += 1
    for i, k in enumerate(korunan):
        s2 = s2.replace("\x00%d\x00" % i, k)
    return s2


def json_donustur(v):
    if isinstance(v, str): return donustur(v)
    if isinstance(v, list): return [json_donustur(x) for x in v]
    if isinstance(v, dict): return {k: json_donustur(x) for k, x in v.items()}
    return v


ATLA_SINIF = {"kw", "de", "src-url", "hn-a"}   # hn-a: huni adım adları (GA4 olayları) Türkçe kalır
ATLA_ETIKET = {"script", "style", "code"}


def html_donustur(doc):
    """Türkçe HTML: metin düğümleri, açıklama nitelikleri ve grafik verisi. Anahtar kelime, Almanca ifade ve bağlantı adresleri değişmez."""
    from bs4 import BeautifulSoup, Comment
    c = BeautifulSoup(doc, "html.parser")
    for d in list(c.find_all(string=True)):
        if isinstance(d, Comment) or d.parent is None: continue
        if any(a.name in ATLA_ETIKET or (set(a.get("class") or []) & ATLA_SINIF) for a in d.parents if getattr(a, "name", None)): continue
        y = donustur(str(d))
        if y != str(d): d.replace_with(y)
    for e in c.find_all(True):
        for ad in ("data-t", "title", "aria-label", "alt", "data-term"):
            v = e.get(ad)
            if v and isinstance(v, str):
                y = donustur(v)
                if y != v: e[ad] = y
        g = e.get("data-grafik")
        if g:
            try:
                e["data-grafik"] = json.dumps(json_donustur(json.loads(g)), ensure_ascii=False, separators=(",", ":"))
            except Exception:
                pass
    return str(c)


EN_DUZELT = {"Aylık search volume": "Monthly search volume"}   # iki Türkçe ifade aynı metriğe indiğinde İngilizce karşılık tekilleşir


def sozluk_donustur(d):
    """Çeviri sözlüğü: anahtarlar aynı dönüşümden geçer; çakışmada ilk karşılık korunur."""
    yeni, cakisma = {}, []
    for k, v in d.items():
        k2 = donustur(k)
        if k2 in yeni and yeni[k2] != v and k2 != k: cakisma.append((k2, yeni[k2], v)); continue
        if k2 not in yeni or k2 == k: yeni[k2] = v
    for k, v in EN_DUZELT.items():
        if k in yeni: yeni[k] = v
    for k, v in d.items(): yeni.setdefault(k, v)   # dönüşümden muaf tutulan düğümler (huni adım adları) özgün anahtarla eşleşir
    return yeni, cakisma
