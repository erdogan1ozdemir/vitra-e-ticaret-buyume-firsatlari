# -*- coding: utf-8 -*-
"""VitrA e-ticaret buyume raporu · kaynak siteler ve sayfalar dokumu (Excel).
Girdi: rapor HTML'i (bolumler ve kaynakca atiflari), uretim/kaynakca.py (K sozlugu), veri/ham/derin/* ozet ve ham dosyalari.
Cikti: VitrA_E-Ticaret_Kaynak_Siteler.xlsx (01 Kaynaklar, 02 Alan adi ozeti, 03 Yontem). Tekrar calistirilabilir."""
import os, sys, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont

import kaynak_ortak as O
import kaynakca
import kaynak_veri_a, kaynak_veri_b, kaynak_veri_c, kaynak_veri_d, kaynak_veri_e, kaynak_veri_f, kaynak_veri_g, kaynak_veri_h

INK = "10332F"; BAS = "434343"; COR = "FF7B52"; CIZ = "E0E0E0"; ZEB = "F7F5F2"
XLSX = os.path.join(O.KOK, "VitrA_E-Ticaret_Kaynak_Siteler.xlsx")

def F(b=False, c=INK, sz=10, u=None):
    return Font(name="Calibri", bold=b, color=c, size=sz, underline=u)
def AL(h="left", v="center", w=True):
    return Alignment(horizontal=h, vertical=v, wrap_text=w)
BORD = Border(top=Side(style="thin", color=CIZ), bottom=Side(style="thin", color=CIZ))

# ---------------------------------------------------------------- alan adi turleri
TUR = {}
def _t(tur, *alanlar):
    for a in alanlar:
        TUR[a] = tur
_t("haber ve sektör kaynağı", "aa.com.tr", "newsfilecorp.com", "sanitaerwirtschaft.de", "serfed.com")
_t("marka sitesi", "eczacibasi.com.tr")
_t("pazaryeri", "trendyol.com", "hepsiburada.com", "n11.com", "amazon.com.tr")
_t("perakendeci", "koctas.com.tr", "bauhaus.com.tr", "bauhaus.info", "ikea.com.tr", "tekzen.com.tr", "evidea.com", "banyomarka.com", "banyoline.com", "homedepot.com",
   "victorianplumbing.co.uk", "vivense.com", "yerevdekor.com", "yurtbayseramik.com", "turkmenleryapi.com.tr", "egeseramikshop.com", "yapilir.com", "banyomoda.com.tr",
   "balneom.com", "yapimanya.com", "banyomega.com", "banyotrendy.com", "yapimarket.com.tr", "banyome.com")
_t("marka sitesi", "vitra.com.tr", "artema.com.tr", "kale.com.tr", "creavit.com.tr", "eca.com.tr", "ecebanyo.com", "serel.com.tr", "serelseramik.com.tr", "geberit.com.tr", "geberit.de",
   "grohe.com", "grohe.com.tr", "duravit.com", "duravit.com.tr", "hansgrohe.com.tr", "hansgrohe-usa.com", "villeroy-boch.co.uk", "kohler.com", "idealstandard.com.tr",
   "turkuazseramik.com.tr", "ngkutahyaseramik.com.tr", "egeseramik.com", "kalekim.com", "kalekim.com.tr", "isvea.com.tr", "bienbanyo.com.tr", "bien.com.tr", "roca.com.tr")
_t("fiyat karşılaştırma", "akakce.com", "cimri.com")
_t("arama motoru", "google.com.tr", "google.com")
_t("API", "dataforseo.com", "ahrefs.com", "apify.com")
_t("sosyal", "youtube.com", "pinterest.com", "instagram.com", "tiktok.com", "sikayetvar.com")
_t("kamu verisi", "tcmb.gov.tr")
_t("marka sitesi", "seramiksan.com.tr")
_t("API", "similarweb.com", "seomonitor.com")
_t("yapay zeka", "chatgpt.com")
_t("açık bilgi kaynağı", "wikidata.org", "wikipedia.org")
_t("dahili (Inbound)", "github.com")

NOT = {
    "trendyol.com": "Doğrudan erişimde 403; tarayıcı ve Apify ile okundu, yardım sayfaları 30.09.2026'da Chrome ile doğrulandı",
    "hepsiburada.com": "Bot korumalı sayfalar için tarayıcı (Playwright ve Chrome) kullanıldı; ödeme ve kolay iade sayfalarında bir bölüm arama özetinden alındı",
    "koctas.com.tr": "curl 403; Apify rag-web-browser, tarayıcı ve Chrome ile okundu; kategori sitemap'i 403 döndüğü için tarayıcıyla",
    "akakce.com": "Doğrudan erişim yaklaşık 15 istekten sonra doğrulama sayfası verdi (29.09.2026); 30.09.2026'da Chrome ile 24 ürün ve 12 kategori sayfası okundu",
    "cimri.com": "Arama sayfası doğrulama katmanı nedeniyle açılamadı; kategori, marka ve ürün sayfaları Chrome ile okundu; 10 SKU eşleşmedi",
    "n11.com": "curl 403; yardım sayfaları 30.09.2026'da Chrome ile okundu, bir bölüm arama özetinden",
    "amazon.com.tr": "curl 403; yardım sayfaları Chrome ile okundu, bir bölüm arama özetinden",
    "bauhaus.com.tr": "curl ile okundu; kategori sitemap'i 1.007 adres",
    "duravit.com.tr": "curl 403; SSS ve teknik servis sayfaları Chrome ile okundu",
    "instagram.com": "Girişe kapalı; sayılar Google SERP snippet'inden, yaklaşık",
    "tiktok.com": "Girişe kapalı; sayı Google SERP snippet'inden, yaklaşık",
    "sikayetvar.com": "Marka sayfaları ve şikayet detayları curl ile okundu (Apify actor'ı çalıştırılmadı); pazaryeri ve kampanya konu sayfaları 404",
    "github.com": "Inbound'un önceki VitrA çalışması; dahili repo",
    "ahrefs.com": "Ahrefs MCP; Türkiye; değerler Ahrefs tahminidir",
    "dataforseo.com": "Canlı (live) uç noktalar; Türkiye (2792), Türkçe",
    "tcmb.gov.tr": "EVDS API; anahtar HTTP başlığıyla gönderildi",
    "google.com": "Search Console API (OAuth), Google Maps ve Shopping sonuçları DataForSEO ile",
    "google.com.tr": "Autocomplete ve SERP DataForSEO ile; sıralamalar tek günlük gözlemdir",
    "apify.com": "Trendyol scraper 14 çalıştırma; rag-web-browser 16 çağrı; Hepsiburada aktörü kredi yetersizliği nedeniyle çalıştırılmadı",
}

def tarih_sirala(L):
    return sorted(L, key=lambda t: tuple(reversed(t.split("."))))

# ---------------------------------------------------------------- satirlari topla
for m in (kaynak_veri_a, kaynak_veri_b, kaynak_veri_c, kaynak_veri_d, kaynak_veri_e, kaynak_veri_f, kaynak_veri_g, kaynak_veri_h):
    m.doldur()

# Kaynakca (K) adreslerinin tamami satir olmali
eksik = []
for kod, (tr, en, urls) in kaynakca.K.items():
    for u in urls:
        r = O.SATIR.get(O.anahtar(u))
        if not r:
            eksik.append((kod, u)); continue
        if kod not in r["kod"]:
            r["kod"].append(kod)
if eksik:
    raise SystemExit("Kaynakcada olup satirda bulunmayan adresler: %s" % eksik)

def bolum_no(r):
    return min(O.BOLUM[s][0] for s in r["bolum"])

SATIRLAR = sorted(O.SATIR.values(), key=lambda r: (bolum_no(r), O.alan_adi(r["url"]), r["url"]))
for r in SATIRLAR:
    if not r["bolum"]:
        raise SystemExit("Bolumsuz satir: %s" % r["url"])
    if not r["amac"] or not r["bilgi"]:
        raise SystemExit("Amac ya da bilgi bos: %s" % r["url"])
    if not r["yontem"] or not r["tarih"]:
        raise SystemExit("Yontem ya da tarih bos: %s" % r["url"])

def kod_sirala(kodlar):
    def k(c):
        return ({"D": 0, "Y": 1, "B": 2}[c[0]], int(c[1:]))
    return sorted(kodlar, key=k)

def temizle(t):
    """Marka yazimi (VitrA), tire ve bosluk duzeni; alintilanan baslik metinlerine de uygulanir."""
    t = re.sub(r"\b(Vitra|VITRA|VİTRA)\b", "VitrA", t)
    t = t.replace("\u2014", "-").replace("\u2013", "-")
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()

def satir_degerleri(r):
    secs = sorted(r["bolum"], key=lambda s: O.BOLUM[s][0])
    return [r["url"], O.alan_adi(r["url"]), temizle(" | ".join(r["amac"])), " · ".join(O.bolum_adi(s) for s in secs), temizle(" | ".join(r["bilgi"])),
            " · ".join(tarih_sirala(r["tarih"])), " · ".join(r["yontem"]), " · ".join(kod_sirala(r["kod"])) if r["kod"] else "-"]

# ---------------------------------------------------------------- Excel yardimcilari
def not_hucresi(ws, notlar, ncol):
    """A2: tum notlar tek hucrede, 'Etiket: govde' bicimi (etiket kalin coral), A sutunundan tablo genisligine birlesik."""
    ins = []
    for i, (e, g) in enumerate(notlar):
        ins.append(TextBlock(InlineFont(rFont="Calibri", b=True, color=COR, sz=10), e + ": "))
        ins.append(TextBlock(InlineFont(rFont="Calibri", color=INK, sz=10), g + ("\n" if i < len(notlar) - 1 else "")))
    c = ws.cell(row=2, column=1, value=CellRichText(*ins))
    c.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)
    c.border = Border(top=Side(style="thin", color=CIZ))
    if ncol > 1:
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncol)
    return c

def yuksek(metin, genislik, min_=15):
    """Satir yuksekligi tahmini (Calibri 10)."""
    satir = 0
    for parca in str(metin).split("\n"):
        satir += max(1, math.ceil(len(parca) / max(6, genislik * 1.05)))
    return max(min_, 13.5 * satir + 3)

def sayfa(wb, ad, baslik, notlar, basliklar, satirlar, genislik, merkez=(), link_sutun=None, sayisal=(), hrefs=None):
    ws = wb.create_sheet(ad)
    ncol = len(basliklar)
    c = ws.cell(row=1, column=1, value=baslik); c.font = F(True, INK, 13); c.alignment = AL("left")
    ws.row_dimensions[1].height = 24
    not_hucresi(ws, notlar, ncol)
    top_w = sum(genislik)
    ws.row_dimensions[2].height = min(409, sum(yuksek(("%s: %s" % n), top_w) - 3 for n in notlar) + 8)
    for i, b in enumerate(basliklar, 1):
        h = ws.cell(row=4, column=i, value=b)
        h.font = F(True, "FFFFFF"); h.fill = PatternFill("solid", fgColor=BAS); h.alignment = AL("center"); h.border = BORD
        ws.column_dimensions[get_column_letter(i)].width = genislik[i - 1]
    ws.row_dimensions[4].height = 30
    for j, sat in enumerate(satirlar):
        rr = 5 + j
        yk = 15
        for i, v in enumerate(sat, 1):
            c = ws.cell(row=rr, column=i, value=v)
            c.font = F(False, INK)
            ortala = (i - 1) in merkez or (i - 1) in sayisal
            c.alignment = AL("center" if ortala else "left")
            c.border = BORD
            if (i - 1) in sayisal and isinstance(v, int):
                c.number_format = "#,##0"
            yk = max(yk, yuksek(v, genislik[i - 1]))
        if link_sutun is not None:
            href = hrefs[j]
            if href:
                c = ws.cell(row=rr, column=link_sutun + 1)
                c.hyperlink = href
                c.font = F(False, INK, 10, "single")
        ws.row_dimensions[rr].height = min(409, yk)
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(ncol), 4 + len(satirlar))
    ws.sheet_view.zoomScale = 100
    return ws

# ---------------------------------------------------------------- 01 Kaynaklar
satirlar_href = [r["href"] for r in SATIRLAR]
S1 = [satir_degerleri(r) for r in SATIRLAR]
ADET = {}
for r in SATIRLAR:
    a = O.alan_adi(r["url"])
    ADET[a] = ADET.get(a, 0) + r["adet"]

# ---------------------------------------------------------------- 02 Alan adi ozeti
alanlar = {}
for r in SATIRLAR:
    a = O.alan_adi(r["url"])
    d = alanlar.setdefault(a, {"bolum": set(), "yontem": [], "tarih": [], "satir": 0})
    d["bolum"] |= set(r["bolum"]); d["satir"] += 1
    for y in r["yontem"]:
        if y not in d["yontem"]:
            d["yontem"].append(y)
    for t in r["tarih"]:
        if t not in d["tarih"]:
            d["tarih"].append(t)
bilinmeyen = [a for a in alanlar if a not in TUR]
if bilinmeyen:
    raise SystemExit("Kaynak turu tanimsiz alan adlari: %s" % bilinmeyen)
S2 = []
for a in sorted(alanlar, key=lambda a: (-ADET[a], a)):
    d = alanlar[a]
    secs = sorted(d["bolum"], key=lambda s: O.BOLUM[s][0])
    not_ = NOT.get(a) or "Yöntem: %s; erişim %s" % (", ".join(d["yontem"]), ", ".join(tarih_sirala(d["tarih"])))
    S2.append([a, ADET[a], " · ".join("%02d" % O.BOLUM[s][0] for s in secs) if len(secs) > 6 else " · ".join(O.bolum_adi(s) for s in secs), TUR[a], not_])

# ---------------------------------------------------------------- 03 Yontem
S3 = [temizle(m) for m in kaynak_veri_f.yontem_maddeleri(len(SATIRLAR), len(alanlar))]

def uret():
    wb = Workbook(); wb.remove(wb.active)
    nkal = sum(1 for r in SATIRLAR if r["adet"] > 1)
    n1 = [
        ("Okuma", "Bir satır bir URL'yi ya da API kaynağının taban adresini gösterir; toplu okunan sayfalarda (ürün sayfaları, arama sorguları, listeler) kalıp adres ve adet tek satırdadır, adet 'Hangi bilgiler alındı' alanında yazılıdır. Süslü parantezli adresler kalıp adrestir; köprü, kalıba uyan gerçek bir örnek sayfaya gider."),
        ("Kapsam", "Rapor HTML'indeki 44 kaynakça girdisinin tüm adresleri, rapordaki bağlantılar, alt ajan araştırmalarında okunan sayfalar ve API kaynakları; politika, garanti ve servis sayfalarının her biri ayrı satırdadır."),
        ("Sıralama", "Bölüm sırasına göre, aynı bölüm içinde alan adına göre; birden fazla bölüme kaynak sağlayan adresler ilk bölümde durur, bölümler '·' ile birleştirilmiştir."),
        ("Kaynakça kodu", "Rapor kaynakçasındaki (D, Y, B) kod; kaynakçada yer almayan destek sayfaları '-' ile işaretlidir."),
        ("Tarih", "Erişim tarihi GG.AA.YYYY: 28.09.2026 (Ahrefs, Search Console, Keyword Planner, EVDS, autocomplete), 29.09.2026 (derin araştırma turu), 30.09.2026 (tarayıcı doğrulaması)."),
    ]
    ws = sayfa(wb, "01 Kaynaklar", "VitrA e-ticaret büyüme fırsatları · kaynak siteler ve sayfalar (%d satır, %d alan adı)" % (len(SATIRLAR), len(alanlar)), n1,
               ["URL", "Alan adı", "Ne için bakıldı", "Raporun hangi bölümüne kaynak sağladı", "Hangi bilgiler alındı", "Erişim tarihi", "Yöntem (tarayıcı / API / curl / MCP)", "Kaynakça kodu"],
               S1, [58, 24, 52, 40, 72, 15, 26, 13], merkez=(5, 7), link_sutun=0, hrefs=satirlar_href)
    n2 = [
        ("Okuma", "Alan adı, 01 Kaynaklar sayfasındaki satırların kayıtlı alan adıdır (alt alan adları kök alan adına indirilmiştir)."),
        ("Sayfa/sorgu sayısı", "Alan adına ait satırların adet toplamıdır; kalıp adres satırlarında adet dahildir. Ahrefs ve DataForSEO kayıt sayıları (top pages satırları, sorgu sonuçları) toplama katılmaz, ilgili satırda yazılıdır."),
        ("Kullanıldığı bölümler", "Alan adının kaynak sağladığı bölümler; altıdan fazla bölüm bulunan alan adlarında yalnızca bölüm numaraları verilmiştir."),
        ("Kaynak türü", "pazaryeri, perakendeci (yapı market ve mobilya), marka sitesi, fiyat karşılaştırma, arama motoru, API, sosyal (video, sosyal ağ ve şikayet platformu), kamu verisi, dahili (Inbound önceki çalışması)."),
    ]
    sayfa(wb, "02 Alan adı özeti", "Alan adı özeti (%d alan adı)" % len(alanlar), n2,
          ["Alan adı", "Sayfa/sorgu sayısı", "Kullanıldığı bölümler", "Kaynak türü (pazaryeri / marka sitesi / fiyat karşılaştırma / arama motoru / API / sosyal / kamu verisi)", "Not"],
          S2, [30, 16, 62, 26, 72], merkez=(3,), sayisal=(1,))
    n3 = [
        ("Okuma", "Her satır bir madde; hangi araçla ne okunduğu, erişim tarihleri ve bot koruması nedeniyle alınamayan ya da kısmen alınan kalemler."),
        ("Not", "Alınamayan kalemler raporda boş bırakılmamış, ilgili satırlar çıkarılmış ya da kaynağıyla birlikte işaretlenmiştir."),
    ]
    sayfa(wb, "03 Yöntem", "Yöntem ve alınamayanlar", n3, ["Madde"], [[m] for m in S3], [170], link_sutun=None)
    wb.save(XLSX)
    return XLSX

if __name__ == "__main__":
    yol = uret()
    print(yol, len(S1), "satir", len(S2), "alan adi", len(S3), "yontem maddesi")
