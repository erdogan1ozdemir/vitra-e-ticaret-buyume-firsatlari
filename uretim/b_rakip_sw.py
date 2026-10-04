# -*- coding: utf-8 -*-
"""Rakip bolumu eki: site trafigi, kanal kirilimi ve etkilesim (Similarweb, Haz - Agu 2026)."""
from ortak import *
from ortak import _J
from grafik2 import yigin, f_pay
from b_talep import sekmeler

SW = {r["alan"]: r for r in _J("islenmis", "similarweb.json")["siteler"]}
V = SW["vitra.com.tr"]
GRUP = {"marka": ("Marka sitesi", "Brand site"), "uzman": ("Uzman ve pure player", "Specialist and pure player"),
        "yapi": ("Yapı market ve mobilya", "DIY and furniture retailer"), "pazar": ("Pazaryeri ve fiyat karşılaştırma", "Marketplace and price comparison")}
AD = {"vitra.com.tr": "VitrA", "kale.com.tr": "Kale", "creavit.com.tr": "Creavit", "eca.com.tr": "E.C.A.", "egeseramik.com": "Ege Seramik",
      "seramiksan.com.tr": "Seramiksan", "turkuazseramik.com.tr": "Turkuaz", "geberit.com.tr": "Geberit", "banyomarka.com": "Banyomarka",
      "koctas.com.tr": "Koçtaş", "bauhaus.com.tr": "Bauhaus", "tekzen.com.tr": "Tekzen", "ikea.com.tr": "IKEA", "trendyol.com": "Trendyol",
      "hepsiburada.com": "Hepsiburada", "amazon.com.tr": "Amazon", "n11.com": "n11", "akakce.com": "Akakçe", "cimri.com": "Cimri",
      "evidea.com": "Evidea", "vivense.com": "Vivense", "banyomega.com": "Banyomega", "artema.com.tr": "Artema", "hansgrohe.com.tr": "Hansgrohe",
      "roca.com.tr": "Roca", "duravit.com.tr": "Duravit", "grohe.com.tr": "Grohe", "banyome.com": "Banyome", "banyoline.com": "Banyoline",
      "serelseramik.com.tr": "Serel", "bien.com.tr": "Bien"}
for _a in AD.values(): x(_a, _a)

def kn(r, *alan): return sum(r["kanal"][a] for a in alan)
def sosyal(r): return kn(r, "sosyal_org", "sosyal_ucretli")
def diger(r): return kn(r, "eposta", "display", "affiliate")
def sure(sn):
    d, s = divmod(int(sn or 0), 60)
    return x("%d dk %02d sn" % (d, s), "%d min %02d s" % (d, s))

SERI = [(x("Direct", "Direct"), "#D9E6E3"), (x("Organik arama", "Organic search"), "#9CCFC5"), (x("Ücretli arama", "Paid search"), "#FFB599"),
        (x("Sosyal medya", "Social media"), "#E85F36"), (x("Referans", "Referral"), "#4E6E68"), (x("E-posta, display, affiliate", "Email, display, affiliate"), "#10332F"),
        (x("AI asistanları", "AI assistants"), "#8A6FB0")]
def dagilim(r): return [kn(r, "direct"), kn(r, "organik"), kn(r, "ucretli"), sosyal(r), kn(r, "referans"), diger(r), kn(r, "ai")]

_mk = sorted([r for r in SW.values() if r["grup"] == "marka" and not r["modellenmis"]], key=lambda r: -r["ort_ziyaret"])
_sk = sorted([r for r in SW.values() if r["grup"] != "marka" and not r["modellenmis"]], key=lambda r: -r["ort_ziyaret"])
G1 = yigin([(AD[r["alan"]], dagilim(r)) for r in _mk], SERI,
           x("Ziyaretin kanallara dağılımı (%100) · marka siteleri · Haz - Ağu 2026 · %5 ve üzeri paylar etiketli", "Distribution of visits by channel (100%) · brand sites · Jun - Aug 2026 · shares of 5% and above labelled"), sol=110, bh=28, ara=10, esik=5)
G2 = yigin([(AD[r["alan"]], dagilim(r)) for r in _sk], SERI,
           x("Ziyaretin kanallara dağılımı (%100) · pazaryeri, yapı market ve uzman siteler · Haz - Ağu 2026 · %5 ve üzeri paylar etiketli", "Distribution of visits by channel (100%) · marketplaces, DIY and specialist sites · Jun - Aug 2026 · shares of 5% and above labelled"), sol=110, bh=26, ara=8, esik=5)
GRAFIK = sekmeler([("Marka siteleri", "Brand sites", G1), ("Pazaryeri, yapı market ve uzman siteler", "Marketplaces, DIY and specialist sites", G2)], "gtabs")

def _p(v): return n(yzd(v)) if v is not None else n("-")
def satir(r):
    m = r["modellenmis"]
    kanal = [n("-")] * 7 if m else [_p(v) for v in dagilim(r)]
    return [u("https://www." + r["alan"], r["alan"]), etk(*GRUP[r["grup"]]), cellk(r["ort_ziyaret"]), n("-") if m else _p(r["tr_pay"])] + kanal + [
        _p(r["hemen_cikma"]), n(f1(r["sayfa_ziyaret"]) if r["sayfa_ziyaret"] is not None else "-"), n(sure(r["sure_sn"]))]
BAS = [th("Alan adı", "Domain", "Similarweb ile ölçülen site; yeni sekmede açılır.", "Site measured with Similarweb; opens in a new tab."),
       th("Grup", "Group", "Sitenin iş modeline göre grubu.", "Group of the site by business model."),
       th("Aylık ziyaret", "Monthly visits", "Haz, Tem ve Ağu 2026 tahmini aylık ziyaretlerinin ortalaması; tüm ülkeler, masaüstü ve mobil.", "Average of estimated monthly visits for Jun, Jul and Aug 2026; all countries, desktop and mobile.", True),
       th("Türkiye payı", "Turkey share", "Ziyaretlerin Türkiye'den gelen payı (Ağu 2026).", "Share of visits coming from Turkey (Aug 2026).", True),
       th("Direct", "Direct", "Adres çubuğuna yazarak, yer imiyle ya da uygulama üzerinden gelen ziyaret payı.", "Share of visits arriving by typing the address, via bookmarks or apps.", True),
       th("Organik arama", "Organic search", "Arama motorlarının ücretsiz sonuçlarından gelen ziyaret payı.", "Share of visits from search engines' free results.", True),
       th("Ücretli arama", "Paid search", "Arama motoru reklamlarından gelen ziyaret payı.", "Share of visits from search engine ads.", True),
       th("Sosyal medya", "Social media", "Sosyal ağlardan gelen ziyaret payı; organik ve ücretli toplamı.", "Share of visits from social networks; organic and paid combined.", True),
       th("Referans", "Referral", "Başka sitelerdeki bağlantılardan gelen ziyaret payı.", "Share of visits from links on other sites.", True),
       th("E-posta, display, affiliate", "Email, display, affiliate", "E-posta, görsel reklam ve satış ortaklığı bağlantılarından gelen ziyaret payı toplamı.", "Combined share of visits from email, display ads and affiliate links.", True),
       th("AI asistanları", "AI assistants", "ChatGPT gibi AI asistanlarındaki bağlantılardan gelen ziyaret payı.", "Share of visits from links in AI assistants such as ChatGPT.", True),
       th("Hemen çıkma", "Bounce rate", "Tek sayfa görüntüleyip ayrılan ziyaret oranı (Ağu 2026).", "Share of visits leaving after a single page (Aug 2026).", True),
       th("Sayfa / ziyaret", "Pages / visit", "Ziyaret başına ortalama sayfa görüntüleme (Ağu 2026).", "Average page views per visit (Aug 2026).", True),
       th("Ort. süre", "Avg. duration", "Ziyaret başına ortalama süre (Ağu 2026).", "Average duration per visit (Aug 2026).", True)]
_tum = sorted(SW.values(), key=lambda r: -r["ort_ziyaret"])
TABLO = sekmeler([("Tümü (%d)" % len(_tum), "All (%d)" % len(_tum), tablo(BAS, [satir(r) for r in _tum], "uzun genis"))] +
                 [("%s (%d)" % (GRUP[g][0], sum(r["grup"] == g for r in _tum)), "%s (%d)" % (GRUP[g][1], sum(r["grup"] == g for r in _tum)),
                   tablo(BAS, [satir(r) for r in _tum if r["grup"] == g], "genis")) for g in ("marka", "uzman", "yapi", "pazar")])

K, CR, GB, BM, KC, N11, HB = (SW[d] for d in ("kale.com.tr", "creavit.com.tr", "geberit.com.tr", "banyomarka.com", "koctas.com.tr", "n11.com", "hepsiburada.com"))
_ru = next((c["pay"] for c in V["ulkeler"] if c["ulke"] == "RU"), 0)
_mod = [AD[r["alan"]] for r in _tum if r["modellenmis"]]
x(", ".join(_mod), ", ".join(_mod))

HTML = """
<h3>%s</h3>
<div class="kpis">%s%s%s%s</div>
%s
%s
%s
%s
%s
""" % (
 x("Site trafiği ve kanal kırılımı", "Site traffic and channel breakdown"),
 kpi_kart(k(V["ort_ziyaret"]), "vitra.com.tr aylık ortalama ziyaret · Haz - Ağu 2026 · tüm ülkeler", "vitra.com.tr average monthly visits · Jun - Aug 2026 · all countries"),
 kpi_kart(yzd(kn(V, "organik")), "Organik arama payı · Direct %s" % yzd(kn(V, "direct")), "Organic search share · Direct %s" % yzd(kn(V, "direct"))),
 kpi_kart(yzd(kn(V, "ucretli")), "Ücretli arama payı · Creavit %s, Geberit %s" % (yzd(kn(CR, "ucretli")), yzd(kn(GB, "ucretli"))), "Paid search share · Creavit %s, Geberit %s" % (yzd(kn(CR, "ucretli")), yzd(kn(GB, "ucretli")))),
 kpi_kart(yzd(sosyal(V)), "Sosyal medya payı · Banyomarka %s, Kale %s" % (yzd(sosyal(BM)), yzd(sosyal(K))), "Social media share · Banyomarka %s, Kale %s" % (yzd(sosyal(BM)), yzd(sosyal(K)))),
 GRAFIK,
 TABLO,
 insight("Similarweb tahminine göre vitra.com.tr Haz - Ağu 2026 döneminde aylık ortalama %s ziyaret almaktadır; ziyaretlerin %s'i organik aramadan, %s'i doğrudan girişten gelmektedir. Kale'de doğrudan giriş (%s) ve e-posta (%s) payı öne çıkarken VitrA'da organik arama ağırlığı belirgindir. "
         "Ücretli arama payı VitrA'da %s'tür; Creavit (%s) ve Geberit (%s) bu kanalı oransal olarak daha yoğun kullanmaktadır. Sosyal medyadan gelen ziyaret payı VitrA'da %s ile sınırlı kalmaktadır; Banyomarka'da bu oran %s, Kale'de %s'tür. "
         "Satış kanallarında e-posta, display ve affiliate toplam payı n11'de %s, Hepsiburada'da %s, Koçtaş'ta %s'dir; Koçtaş ayrıca ziyaretlerinin %s'ini ücretli aramadan almaktadır. "
         "Ücretli aramada Creavit ve Geberit'in, sosyal medyada Kale'nin altında kalınması, kampanya ve lansman dönemlerinde bu kanalların test edilmesi için alan bırakmaktadır."
         % (k(V["ort_ziyaret"]), yzd(kn(V, "organik")), yzd(kn(V, "direct")), yzd(kn(K, "direct")), yzd(kn(K, "eposta")), yzd(kn(V, "ucretli")), yzd(kn(CR, "ucretli")), yzd(kn(GB, "ucretli")),
            yzd(sosyal(V)), yzd(sosyal(BM)), yzd(sosyal(K)), yzd(diger(N11)), yzd(diger(HB)), yzd(diger(KC)), yzd(kn(KC, "ucretli"))),
         "According to Similarweb estimates, vitra.com.tr receives an average of %s visits a month in Jun - Aug 2026; %s of visits come from organic search and %s from direct entry. Kale stands out with direct entry (%s) and email (%s), while organic search clearly carries the weight at VitrA. "
         "VitrA's paid search share is %s; Creavit (%s) and Geberit (%s) use this channel proportionally more intensively. The share of visits from social media is limited to %s at VitrA; it is %s at Banyomarka and %s at Kale. "
         "Among sales channels, the combined email, display and affiliate share is %s at n11, %s at Hepsiburada and %s at Koçtaş; Koçtaş also gets %s of its visits from paid search. "
         "Being below Creavit and Geberit in paid search and below Kale in social media leaves room to test these channels during campaign and launch periods."
         % (k(V["ort_ziyaret"]), yzd(kn(V, "organik")), yzd(kn(V, "direct")), yzd(kn(K, "direct")), yzd(kn(K, "eposta")), yzd(kn(V, "ucretli")), yzd(kn(CR, "ucretli")), yzd(kn(GB, "ucretli")),
            yzd(sosyal(V)), yzd(sosyal(BM)), yzd(sosyal(K)), yzd(diger(N11)), yzd(diger(HB)), yzd(diger(KC)), yzd(kn(KC, "ucretli"))), "D37"),
 note("YÖNTEM", "METHOD", ul_b([
     ("Kapsam:", "Scope:", "Ziyaret değerleri tüm ülkeleri kapsayan Similarweb tahminleridir. vitra.com.tr ziyaretlerinin %s'i Türkiye'den, %s'i Rusya'dan gelmektedir; Türkiye kaynaklı ziyaret aylık ~%s düzeyindedir." % (yzd(V["tr_pay"]), yzd(_ru), k(V["ort_ziyaret"] * V["tr_pay"] / 100)),
      "Visit values are Similarweb estimates covering all countries. %s of vitra.com.tr visits come from Turkey and %s from Russia; visits from Turkey are around %s a month." % (yzd(V["tr_pay"]), yzd(_ru), k(V["ort_ziyaret"] * V["tr_pay"] / 100))),
     ("Düşük trafikli siteler:", "Low-traffic sites:", "Similarweb'in kanal dağılımını benzer sitelerden modellediği %d düşük trafikli sitede (%s) kanal ve Türkiye payı sütunları boş bırakılmış, grafikte yer verilmemiştir. Ahrefs ve Similarweb değerleri farklı yöntemlerle hesaplanan tahminlerdir; vitra.com.tr'nin Search Console verisinde Haz - Ağu 2026 Google organik tıkı aylık ~186K'dır (Bölüm [[b:organik]]). Karşılaştırmalar aynı kaynak içinde okunmalıdır." % (len(_mod), ", ".join(_mod)),
      "For the %d low-traffic sites whose channel distribution Similarweb models from similar sites (%s), the channel and Turkey-share columns are left blank and the sites are not charted. Ahrefs and Similarweb values are estimates calculated with different methods; in vitra.com.tr's Search Console data, Google organic clicks average ~186K a month in Jun - Aug 2026 (Section [[b:organik]]). Comparisons should be read within the same source." % (len(_mod), ", ".join(_mod))),
     ("Etkileşim:", "Engagement:", "vitra.com.tr'de ziyaret başına %s sayfa görüntülenmekte, ortalama süre %s, hemen çıkma oranı %s'dir (Ağu 2026)." % (f1(V["sayfa_ziyaret"]), "%d dk %02d sn" % divmod(V["sure_sn"], 60), yzd(V["hemen_cikma"])),
      "vitra.com.tr shows %s pages per visit, an average duration of %s and a bounce rate of %s (Aug 2026)." % (f1(V["sayfa_ziyaret"]), "%d min %02d s" % divmod(V["sure_sn"], 60), yzd(V["hemen_cikma"]))),
 ])),
 kaynak("Similarweb · site trafiği, kanal kırılımı ve etkileşim · Haz - Ağu 2026 · 03.10.2026", "Similarweb · site traffic, channel breakdown and engagement · Jun - Aug 2026 · 03.10.2026", "D37"),
)
