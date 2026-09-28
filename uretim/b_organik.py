# -*- coding: utf-8 -*-
"""Bolum: Organik kanal performansi (Search Console)."""
from ortak import *
from rapor_parca1 import T, cizgi
from b_talep import kat, KAT_EN
GA = A["gsc_aylar"]; GM = A["gsc_aylik"]; GT = A["gsc_tur"]; GK = A["gsc_kat"]; GC = A["gsc_cihaz"]; GU = A["gsc_ulke"]; ON = A["online_aylik"]; MT = A["gsc_ay_toplam"]; TS = A["top_sayfa_3ay"]
aylar = [m for m in GA if m <= "2026-08"]
tur_en = {"kategori": "Category pages", "urun": "Product pages", "eski-online": "Old online.vitra.com.tr addresses", "anasayfa": "Home page", "icerik": "Content and inspiration", "diger": "Other", "servis-bayi": "Service and dealer", "koleksiyon": "Collection pages", "kurumsal": "Corporate", "katalog": "Catalogue", "urun-teknik": "Product technical sheets"}
tur_tr = {"kategori": "Kategori sayfaları", "urun": "Ürün sayfaları", "eski-online": "Eski online.vitra.com.tr adresleri", "anasayfa": "Ana sayfa", "icerik": "İçerik ve ilham", "diger": "Diğer", "servis-bayi": "Servis ve bayi", "koleksiyon": "Koleksiyon sayfaları", "kurumsal": "Kurumsal", "katalog": "Katalog", "urun-teknik": "Ürün teknik föyleri"}
ttot = sum(v[0] for v in GT.values())
rows = [[x(tur_tr[t], tur_en[t]), cell(v[2]), cell(v[0]), n(yzd(100 * v[0] / ttot)), cell(v[1]), n(yzd(100 * v[0] / v[1]) if v[1] else "-")] for t, v in sorted(GT.items(), key=lambda i: -i[1][0])]
tbl = tablo([th("Sayfa türü", "Page type", "Adres yapısına göre sayfa sınıfı; /c- ve kategori dizinleri kategori, -p-a kodlu adresler ürün sayfasıdır.", "Page class by URL structure; /c- and category directories are category pages, -p-a coded addresses are product pages."),
             th("Sayfa", "Pages", "Dönemde en az bir gösterim almış sayfa sayısı (ilk 25.000 sayfa).", "Number of pages with at least one impression in the period (top 25,000 pages).", True),
             th("Tık", "Clicks", "1 Haz 2025 - 25 Eyl 2026 toplam tık.", "Total clicks, 1 Jun 2025 - 25 Sep 2026.", True),
             th("Pay", "Share", "Sayfa türünün toplam tık içindeki payı.", "Page type's share of total clicks.", True),
             th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
             th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)], rows)
ktot = sum(v[0] for v in GK.values())
k1s = {}
for key, v in GK.items():
    k1 = key.split("|")[0]; k1s.setdefault(k1, [0, 0, 0]); k1s[k1][0] += v[0]; k1s[k1][1] += v[1]; k1s[k1][2] += v[2]
KAT_EN2 = dict(KAT_EN); KAT_EN2["Karo Seramik"] = "Ceramic Tiles"; KAT_EN2["Diğer"] = "Other"
rows2 = [[x(k1, KAT_EN2.get(k1, k1)), cell(v[2]), cell(v[0]), n(yzd(100 * v[0] / ktot)), cell(v[1]), n(yzd(100 * v[0] / v[1]))] for k1, v in sorted(k1s.items(), key=lambda i: -i[1][0])]
tbl2 = tablo([th("Kategori", "Category", "Kategori ve ürün sayfalarının adres yapısından türetilen ana kategori.", "Main category derived from the URL structure of category and product pages."),
              th("Sayfa", "Pages", "Kategoriye eşlenen sayfa sayısı.", "Number of pages mapped to the category.", True),
              th("Tık", "Clicks", "1 Haz 2025 - 25 Eyl 2026 toplam tık.", "Total clicks, 1 Jun 2025 - 25 Sep 2026.", True),
              th("Pay", "Share", "Kategori ve ürün sayfaları toplamı içindeki pay.", "Share within the total of category and product pages.", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)], rows2, "dar")
def seri(k): return [GM[k][GA.index(m)][0] for m in aylar]
GRAFIK = cizgi([(kat("Vitrifiyeler"), "#10332F", seri("Vitrifiyeler")), (x("Karo Seramik", "Ceramic Tiles"), "#7A8C89", seri("Karo Seramik")), (kat("Armatürler"), "#2E7D32", seri("Armatürler")),
                (kat("Banyo Mobilyaları"), "#E85F36", seri("Banyo Mobilyaları")), (kat("Yıkanma Alanları"), "#F5A623", seri("Yıkanma Alanları"))],
               y_etiket=x("Aylık organik tık · kategori ve ürün sayfaları", "Monthly organic clicks · category and product pages"), aylar=aylar)
GRAFIK2 = cizgi([(x("vitra.com.tr", "vitra.com.tr"), "#10332F", [ON[m][1] for m in aylar]), (x("online.vitra.com.tr (eski adresler)", "online.vitra.com.tr (old addresses)"), "#E85F36", [ON[m][0] for m in aylar])],
                y_etiket=x("Aylık organik tık · alan adına göre", "Monthly organic clicks · by host"), aylar=aylar)
mob = 100 * GC["MOBILE"][0] / sum(v[0] for v in GC.values()); mob_i = 100 * GC["MOBILE"][1] / sum(v[1] for v in GC.values())
ctr_m = 100 * GC["MOBILE"][0] / GC["MOBILE"][1]; ctr_d = 100 * GC["DESKTOP"][0] / GC["DESKTOP"][1]
son12 = sum(MT[m][0] for m in aylar[-12:]); son12i = sum(MT[m][1] for m in aylar[-12:])
x("/ (ana sayfa)", "/ (home page)")
rows3 = [[u("https://www.vitra.com.tr" + p_, p_ if p_ != "/" else "/ (ana sayfa)"), cell(c)] for p_, c in [(uu.replace("https://www.vitra.com.tr", ""), cc) for uu, cc in TS[:15]]]
tbl3 = tablo([th("Sayfa adresi", "Page address", "Sayfa adresi; bağlantı canlı sayfaya gider.", "Page address; the link opens the live page."),
              th("Tık · Tem-Eyl 2026", "Clicks · Jul-Sep 2026", "1 Temmuz - 25 Eylül 2026 organik tık.", "Organic clicks, 1 July - 25 September 2026.", True)], rows3, "dar")
kloz = GK.get("Vitrifiyeler|Klozetler", [0,0,0]); lav = GK.get("Vitrifiyeler|Lavabolar", [0,0,0]); karo = k1s["Karo Seramik"]
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
%s
<h3>%s</h3>
%s
%s
<div class="two">
<div><h3>%s</h3>%s</div>
<div><h3>%s</h3>%s</div>
</div>
%s
""" % (
 x("Search Console verisi, vitra.com.tr'nin Google'dan aldığı trafiğin hangi sayfa türlerine ve kategorilere geldiğini göstermektedir. Dönem 1 Haziran 2025 - 25 Eylül 2026'dır; Aralık 2025'te online.vitra.com.tr adreslerinin ana alan adına taşınması dönem içinde yer almaktadır.",
   "Search Console data shows which page types and categories the traffic vitra.com.tr receives from Google lands on. The period is 1 June 2025 - 25 September 2026; the migration of online.vitra.com.tr addresses to the main domain in December 2025 falls within it."),
 kpi_kart(k(son12), "Organik tık · son 12 ay (Eyl 2025 - Ağu 2026)", "Organic clicks · last 12 months (Sep 2025 - Aug 2026)"),
 kpi_kart(yzd(100 * son12 / son12i), "Ortalama CTR · son 12 ay", "Average CTR · last 12 months"),
 kpi_kart(yzd(mob), "Mobil tık payı · gösterim payı %s" % yzd(mob_i), "Mobile click share · impression share %s" % (yzd(mob_i).replace("%", "") + "%")),
 kpi_kart(yzd(GU[0][2]), "Türkiye payı · ikinci sırada Almanya %s" % yzd(GU[1][2]), "Turkey share · Germany second at %s" % (yzd(GU[1][2]).replace("%", "") + "%")),
 x("Trafik hangi sayfa türlerine geliyor?", "Which page types does the traffic land on?"),
 tbl,
 insight("Organik tıkların %s'i kategori sayfalarına, %s'i ürün sayfalarına gelmektedir; kategori sayfası başına ortalama tık ürün sayfasının yaklaşık %s katıdır. Ürün sayfaları %s gösterimle %s CTR üretirken kategori sayfaları %s CTR ile çalışmaktadır: kullanıcı jenerik aramada kategori sayfasını, model aramasında ürün sayfasını görmektedir. Eski online.vitra.com.tr adresleri dönemin ilk yarısında %s tık taşımış ve Aralık 2025'te sıfırlanmıştır; taşınma sonrasında toplam trafik korunmuştur (aşağıdaki grafik)." % (yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot), ("%.0f" % ((GT["kategori"][0] / GT["kategori"][2]) / (GT["urun"][0] / GT["urun"][2]))), k(GT["urun"][1]), yzd(100 * GT["urun"][0] / GT["urun"][1]), yzd(100 * GT["kategori"][0] / GT["kategori"][1]), k(GT["eski-online"][0])),
         "%s of organic clicks land on category pages and %s on product pages; the average click per category page is about %s times that of a product page. Product pages produce %s CTR on %s impressions while category pages work at %s CTR: the user sees the category page in generic searches and the product page in model searches. Old online.vitra.com.tr addresses carried %s clicks in the first half of the period and dropped to zero in December 2025; total traffic was preserved after the migration (chart below)." % (yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot), ("%.0f" % ((GT["kategori"][0] / GT["kategori"][2]) / (GT["urun"][0] / GT["urun"][2]))), yzd(100 * GT["urun"][0] / GT["urun"][1]), k(GT["urun"][1]), yzd(100 * GT["kategori"][0] / GT["kategori"][1]), k(GT["eski-online"][0])), "D2"),
 x("Kategori bazında organik trafik", "Organic traffic by category"),
 tbl2, GRAFIK,
 insight("Kategori ve ürün sayfalarına gelen tıkların %s'i Vitrifiyeler (Lavabolar %s, Klozetler %s) ve %s'i Karo Seramik sayfalarındadır. Arama talebinde en büyük kategori olan Banyo Mobilyaları (talep payı %s) organik tıkta yalnızca %s pay almaktadır: talebin büyüklüğü ile sitenin bu talepten aldığı pay arasındaki en geniş açık bu kategoridedir. Karo Seramik ise tam tersi profildedir; talep payı %s iken tık payı %s'e ulaşmaktadır. Aylık seride Vitrifiyeler ve Yıkanma Alanları Aralık 2025 taşınmasından sonra yükselirken Banyo Mobilyaları 2026 yazında gerilemiştir." % (yzd(100 * k1s["Vitrifiyeler"][0] / ktot), k(lav[0]), k(kloz[0]), yzd(100 * karo[0] / ktot), yzd(100 * A["k1"]["Banyo Mobilyaları"]["a26"] / A["toplam"]["a26"]), yzd(100 * k1s["Banyo Mobilyaları"][0] / ktot), yzd(100 * A["k1"]["Karo Seramik Ürünleri"]["a26"] / A["toplam"]["a26"]), yzd(100 * karo[0] / ktot)),
         "%s of clicks landing on category and product pages are in Sanitaryware (Washbasins %s, WCs %s) and %s in Ceramic Tiles. Bathroom Furniture, the largest category in search demand (demand share %s), takes only %s of organic clicks: the widest gap between the size of demand and the share the site captures is in this category. Ceramic Tiles shows the opposite profile; its demand share is %s while its click share reaches %s. In the monthly series Sanitaryware and Bathing Areas rose after the December 2025 migration while Bathroom Furniture declined in summer 2026." % (yzd(100 * k1s["Vitrifiyeler"][0] / ktot), k(lav[0]), k(kloz[0]), yzd(100 * karo[0] / ktot), yzd(100 * A["k1"]["Banyo Mobilyaları"]["a26"] / A["toplam"]["a26"]), yzd(100 * k1s["Banyo Mobilyaları"][0] / ktot), yzd(100 * A["k1"]["Karo Seramik Ürünleri"]["a26"] / A["toplam"]["a26"]), yzd(100 * karo[0] / ktot)), "D2", "D1"),
 x("Alan adı taşınması ve toplam trafik", "Domain migration and total traffic"),
 GRAFIK2,
 insight("online.vitra.com.tr üzerindeki e-ticaret sayfaları Aralık 2025'te vitra.com.tr altına taşınmış; taşınma öncesi aylık %s civarında olan eski adres tıkları yeni adreslerde karşılanmıştır. Aralık 2025 - Nisan 2026 toplam tık, taşınma öncesi Ekim - Kasım 2025 seviyesinin (%s) altında kalsa da mevsimsel örüntüyle uyumludur; Haziran - Temmuz 2026'da %s ile taşınma öncesi seviyeye dönülmüştür. Tek alan adı yapısı, kategori sayfalarının hem bilgi hem satın alma sayfası olarak çalışmasını mümkün kılmaktadır." % (k(ON["2025-10"][0]), k(MT["2025-10"][0]), k(MT["2026-07"][0])),
         "The e-commerce pages on online.vitra.com.tr were moved under vitra.com.tr in December 2025; old-address clicks of about %s per month before the migration were absorbed by the new addresses. Although total clicks in December 2025 - April 2026 stayed below the pre-migration October - November 2025 level (%s), this follows the seasonal pattern; June - July 2026 returned to the pre-migration level at %s. The single-domain structure allows category pages to work as both information and purchase pages." % (k(ON["2025-10"][0]), k(MT["2025-10"][0]), k(MT["2026-07"][0])), "D2"),
 x("En çok tık alan sayfalar · Tem-Eyl 2026", "Pages with most clicks · Jul-Sep 2026"), tbl3,
 x("Cihaz ve ülke", "Device and country"),
 tablo([th("Kırılım", "Breakdown", "Search Console cihaz ve ülke boyutu.", "Search Console device and country dimension."),
        th("Tık", "Clicks", "1 Haz 2025 - 25 Eyl 2026 toplam.", "Total, 1 Jun 2025 - 25 Sep 2026.", True),
        th("Pay", "Share", "Toplam tık içindeki pay.", "Share of total clicks.", True),
        th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)],
       [[x("Mobil", "Mobile"), cell(GC["MOBILE"][0]), n(yzd(mob)), n(yzd(ctr_m))],
        [x("Masaüstü", "Desktop"), cell(GC["DESKTOP"][0]), n(yzd(100 * GC["DESKTOP"][0] / sum(v[0] for v in GC.values()))), n(yzd(ctr_d))],
        [x("Tablet", "Tablet"), cell(GC["TABLET"][0]), n(yzd(100 * GC["TABLET"][0] / sum(v[0] for v in GC.values()))), n(yzd(100 * GC["TABLET"][0] / GC["TABLET"][1]))],
        [x("Türkiye", "Turkey"), cell(GU[0][1]), n(yzd(GU[0][2])), n("-")], [x("Almanya", "Germany"), cell(GU[1][1]), n(yzd(GU[1][2])), n("-")], [x("KKTC", "Northern Cyprus"), cell(GU[2][1]), n(yzd(GU[2][2])), n("-")]], "dar"),
 kaynak("Google Search Console · sc-domain:vitra.com.tr · 1 Haz 2025 - 25 Eyl 2026 · sayfa, sayfa×gün, cihaz×gün ve ülke boyutları · %s" % veri.TARIH,
        "Google Search Console · sc-domain:vitra.com.tr · 1 Jun 2025 - 25 Sep 2026 · page, page×day, device×day and country dimensions · %s" % veri.TARIH, "D2"),
)
