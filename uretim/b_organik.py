# -*- coding: utf-8 -*-
"""Bolum: Organik kanal performansi (Search Console)."""
from ortak import *
from rapor_parca1 import T, cizgi
from b_talep import kat, KAT_EN
GA = A["gsc_aylar"]; GM = A["gsc_aylik"]; GT = A["gsc_tur"]; GK = A["gsc_kat"]; GC = A["gsc_cihaz"]; GU = A["gsc_ulke"]; ON = A["online_aylik"]; MT = A["gsc_ay_toplam"]; TS = A["top_sayfa_3ay"]
aylar = [m for m in GA if m <= "2026-08"]
tur_en = {"kategori": "Category pages", "urun": "Product pages", "eski-online": "Old online.vitra.com.tr addresses (before the December 2025 merger)", "anasayfa": "Home page", "icerik": "Content and inspiration", "diger": "Other", "servis-bayi": "Service and dealer", "koleksiyon": "Collection pages", "kurumsal": "Corporate", "katalog": "Catalogue", "urun-teknik": "Product technical sheets"}
tur_tr = {"kategori": "Kategori sayfaları", "urun": "Ürün sayfaları", "eski-online": "Eski online.vitra.com.tr adresleri (Aralık 2025 birleşmesi öncesi)", "anasayfa": "Ana sayfa", "icerik": "İçerik ve ilham", "diger": "Diğer", "servis-bayi": "Servis ve bayi", "koleksiyon": "Koleksiyon sayfaları", "kurumsal": "Kurumsal", "katalog": "Katalog", "urun-teknik": "Ürün teknik föyleri"}
ttot = sum(v[0] for v in GT.values())
rows = [[x(tur_tr[t], tur_en[t]), cell(v[2]), cellk(v[0]), n(yzd(100 * v[0] / ttot)), cellk(v[1]), n(yzd(100 * v[0] / v[1]) if v[1] else "-")] for t, v in sorted(GT.items(), key=lambda i: -i[1][0])]
tbl = tablo([th("Sayfa türü", "Page type", "Adres yapısına göre sayfa sınıfı; /c- ve kategori dizinleri kategori, -p- ve -sku- kodlu adresler (eski adres yapısı dahil) ürün sayfasıdır.", "Page class by URL structure; /c- and category directories are category pages, addresses coded -p- and -sku- (including the old URL structure) are product pages."),
             th("Sayfa", "Pages", "Dönemde en az bir gösterim almış tekil sayfa sayısı (ilk 25.000 adres); sayfalama ve filtre parametreli adresler ana sayfayla tek sayfa sayılmıştır.", "Number of unique pages with at least one impression in the period (top 25,000 addresses); paginated and filtered addresses are counted as one page with their base page.", True),
             th("Click", "Clicks", "1 Haz 2025 - 25 Eyl 2026 toplam click.", "Total clicks, 1 Jun 2025 - 25 Sep 2026.", True),
             th("Pay", "Share", "Sayfa türünün toplam tık içindeki payı.", "Page type's share of total clicks.", True),
             th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
             th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)], rows)
ktot = sum(v[0] for v in GK.values())
k1s = {}
for key, v in GK.items():
    k1 = key.split("|")[0]; k1s.setdefault(k1, [0, 0, 0]); k1s[k1][0] += v[0]; k1s[k1][1] += v[1]; k1s[k1][2] += v[2]
KAT_EN2 = dict(KAT_EN); KAT_EN2["Karo Seramik"] = "Ceramic Tiles"; KAT_EN2["Diğer"] = "Other"
_TK = {"Karo Seramik": "Karo Seramik Ürünleri"}
def _talep_pay(k1):
    kk = _TK.get(k1, k1)
    return n(yzd(100 * A["k1"][kk]["a26"] / A["toplam"]["a26"])) if kk in A["k1"] else n("-")
rows2 = [[x(k1, KAT_EN2.get(k1, k1)), cell(v[2]), cellk(v[0]), n(yzd(100 * v[0] / ktot)), _talep_pay(k1), cellk(v[1]), n(yzd(100 * v[0] / v[1]))] for k1, v in sorted(k1s.items(), key=lambda i: -i[1][0])]
tbl2 = tablo([th("Kategori", "Category", "Kategori, ürün, koleksiyon ve eski online.vitra.com.tr sayfalarının adres yapısından türetilen ana kategori.", "Main category derived from the URL structure of category, product, collection and old online.vitra.com.tr pages."),
              th("Sayfa", "Pages", "Kategoriye eşlenen tekil sayfa sayısı; sayfalama ve filtre parametreli adresler tek sayılmıştır.", "Number of unique pages mapped to the category; paginated and filtered addresses are counted once.", True),
              th("Click", "Clicks", "1 Haz 2025 - 25 Eyl 2026 toplam click.", "Total clicks, 1 Jun 2025 - 25 Sep 2026.", True),
              th("Click payı", "Click share", "Kategoriye eşlenen sayfaların (kategori, ürün, koleksiyon, teknik föy ve eski online.vitra.com.tr adresleri) toplam click'i içindeki pay.", "Share of total clicks of pages mapped to a category (category, product, collection, technical sheet and old online.vitra.com.tr addresses).", True),
              th("Talep payı", "Demand share", "Kategorinin Oca-Ağu 2026 arama talebindeki payı (Bölüm 03, 2.349 kelime).", "The category's share of Jan-Aug 2026 search demand (Section 03, 2,349 keywords).", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)], rows2, "dar")
def seri(k): return [GM[k][GA.index(m)][0] for m in aylar]
GRAFIK = cizgi([(kat("Vitrifiyeler"), "#10332F", seri("Vitrifiyeler")), (x("Karo Seramik", "Ceramic Tiles"), "#7A8C89", seri("Karo Seramik")), (kat("Armatürler"), "#2E7D32", seri("Armatürler")),
                (kat("Banyo Mobilyaları"), "#E85F36", seri("Banyo Mobilyaları")), (kat("Yıkanma Alanları"), "#F5A623", seri("Yıkanma Alanları"))],
               y_etiket=x("Aylık organik tık · kategori ve ürün sayfaları · sayfa×gün verisinin en az 5 tık alan satırları; eğilimi gösterir, tablo toplamlarının %52-81'ini kapsar", "Monthly organic clicks · category and product pages · page×day rows with at least 5 clicks; shows the trend and covers 52-81% of the table totals"), aylar=aylar)
from grafik2 import gruplu as _gr
_GP = [(k1, 100 * A["k1"][_TK.get(k1, k1)]["a26"] / A["toplam"]["a26"], 100 * v[0] / ktot) for k1, v in sorted(k1s.items(), key=lambda i: -i[1][0]) if _TK.get(k1, k1) in A["k1"]]
GPAY = _gr([(x(k1, KAT_EN2.get(k1, k1)), [tp, cp]) for k1, tp, cp in sorted(_GP, key=lambda r: -r[1])],
           [(x("Arama talebi payı · Oca-Ağu 2026", "Search demand share · Jan-Aug 2026"), "#9AA8A5"), (x("Organik tık payı · 1 Haz 2025 - 25 Eyl 2026", "Organic click share · 1 Jun 2025 - 25 Sep 2026"), "#10332F")],
           x("Kategori bazında arama talebi payı ve vitra.com.tr organik tık payı", "Search demand share and vitra.com.tr organic click share by category"))
mob = 100 * GC["MOBILE"][0] / sum(v[0] for v in GC.values()); mob_i = 100 * GC["MOBILE"][1] / sum(v[1] for v in GC.values())
ctr_m = 100 * GC["MOBILE"][0] / GC["MOBILE"][1]; ctr_d = 100 * GC["DESKTOP"][0] / GC["DESKTOP"][1]
son12 = sum(MT[m][0] for m in aylar[-12:]); son12i = sum(MT[m][1] for m in aylar[-12:])
x("/ (ana sayfa)", "/ (home page)")
rows3 = [[u("https://www.vitra.com.tr" + (p_ or "/"), p_ if p_ not in ("", "/") else "/ (ana sayfa)"), cellk(c)] for p_, c in [(uu.replace("https://www.vitra.com.tr", ""), cc) for uu, cc in TS[:15]]]
tbl3 = tablo([th("Sayfa adresi", "Page address", "Sayfa adresi; bağlantı canlı sayfaya gider.", "Page address; the link opens the live page."),
              th("Click · Tem-Eyl 2026", "Clicks · Jul-Sep 2026", "1 Temmuz - 25 Eylül 2026 organik click.", "Organic clicks, 1 July - 25 September 2026.", True)], rows3, "dar")
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
<div class="two">
<div><h3>%s</h3>%s</div>
<div><h3>%s</h3>%s</div>
</div>
%s
""" % (
 x("Search Console verisi, vitra.com.tr'nin Google'dan aldığı trafiğin hangi sayfa türlerine ve kategorilere geldiğini göstermektedir. Dönem 1 Haziran 2025 - 25 Eylül 2026'dır. Veri alan adı düzeyindeki mülkten (sc-domain:vitra.com.tr) alınmıştır; vitra.com.tr'nin tüm alt alan adları ve adresleri tek toplam olarak kapsanmaktadır.",
   "Search Console data shows which page types and categories the traffic vitra.com.tr receives from Google lands on. The period is 1 June 2025 - 25 September 2026. Data comes from the domain-level property (sc-domain:vitra.com.tr); all subdomains and addresses of vitra.com.tr are covered as a single total."),
 kpi_kart(k(son12), "Organik tık · son 12 ay (Eyl 2025 - Ağu 2026)", "Organic clicks · last 12 months (Sep 2025 - Aug 2026)"),
 kpi_kart(yzd(100 * son12 / son12i), "Ortalama CTR · son 12 ay", "Average CTR · last 12 months"),
 kpi_kart(yzd(mob), "Mobil tık payı · gösterim payı %s" % yzd(mob_i), "Mobile click share · impression share %s" % (yzd(mob_i).replace("%", "") + "%")),
 kpi_kart(yzd(GU[0][2]), "Türkiye payı · ikinci sırada Almanya %s" % yzd(GU[1][2]), "Turkey share · Germany second at %s" % (yzd(GU[1][2]).replace("%", "") + "%")),
 x("Trafik hangi sayfa türlerine geliyor?", "Which page types does the traffic land on?"),
 tbl,
 insight("Organik tıkların %s'i kategori sayfalarına, %s'i ürün sayfalarına gelmektedir; kategori sayfası başına ortalama tık ürün sayfasının ~%sx'idir. Ürün sayfaları %s gösterimle %s CTR üretirken kategori sayfaları %s CTR ile çalışmaktadır: bu fark, kullanıcının jenerik aramada kategori sayfasına, model aramasında ürün sayfasına ulaştığına işaret etmektedir." % (yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot), ("%.0f" % ((GT["kategori"][0] / GT["kategori"][2]) / (GT["urun"][0] / GT["urun"][2]))), k(GT["urun"][1]), yzd(100 * GT["urun"][0] / GT["urun"][1]), yzd(100 * GT["kategori"][0] / GT["kategori"][1])),
         "%s of organic clicks land on category pages and %s on product pages; the average click per category page is ~%sx that of a product page. Product pages, with %s impressions, produce %s CTR while category pages work at %s CTR: this gap indicates that users reach the category page in generic searches and the product page in model searches." % (yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot), ("%.0f" % ((GT["kategori"][0] / GT["kategori"][2]) / (GT["urun"][0] / GT["urun"][2]))), k(GT["urun"][1]), yzd(100 * GT["urun"][0] / GT["urun"][1]), yzd(100 * GT["kategori"][0] / GT["kategori"][1])), "D2"),
 x("Kategori bazında organik trafik", "Organic traffic by category"),
 tbl2 + GPAY, GRAFIK,
 insight("Kategoriye eşlenen sayfalara gelen tıkların %s'i Vitrifiyeler (Lavabolar %s, Klozetler %s) ve %s'i Karo Seramik sayfalarındadır. Arama talebinde ikinci büyük kategori olan Banyo Mobilyaları (talep payı %s) organik tıkta yalnızca %s pay almaktadır: talebin büyüklüğü ile sitenin bu talepten aldığı pay arasındaki en geniş açık bu kategoridedir. Karo Seramik ise tersine dönen bir örüntü göstermektedir; talep payı %s iken tık payı %s'e ulaşmaktadır." % (yzd(100 * k1s["Vitrifiyeler"][0] / ktot), k(lav[0]), k(kloz[0]), yzd(100 * karo[0] / ktot), yzd(100 * A["k1"]["Banyo Mobilyaları"]["a26"] / A["toplam"]["a26"]), yzd(100 * k1s["Banyo Mobilyaları"][0] / ktot), yzd(100 * A["k1"]["Karo Seramik Ürünleri"]["a26"] / A["toplam"]["a26"]), yzd(100 * karo[0] / ktot)),
         "%s of clicks landing on pages mapped to a category are in Sanitaryware (Washbasins %s, WCs %s) and %s in Ceramic Tiles. Bathroom Furniture, the second-largest category in search demand (demand share %s), takes only %s of organic clicks: the widest gap between the size of demand and the share the site captures is in this category. Ceramic Tiles shows the reverse pattern; its demand share is %s while its click share reaches %s." % (yzd(100 * k1s["Vitrifiyeler"][0] / ktot), k(lav[0]), k(kloz[0]), yzd(100 * karo[0] / ktot), yzd(100 * A["k1"]["Banyo Mobilyaları"]["a26"] / A["toplam"]["a26"]), yzd(100 * k1s["Banyo Mobilyaları"][0] / ktot), yzd(100 * A["k1"]["Karo Seramik Ürünleri"]["a26"] / A["toplam"]["a26"]), yzd(100 * karo[0] / ktot)), "D2", "D1"),
 x("En çok tık alan sayfalar · Tem-Eyl 2026", "Pages with most clicks · Jul-Sep 2026"), tbl3,
 x("Cihaz ve ülke", "Device and country"),
 tablo([th("Kırılım", "Breakdown", "Search Console cihaz ve ülke boyutu.", "Search Console device and country dimension."),
        th("Click", "Clicks", "1 Haz 2025 - 25 Eyl 2026 toplam.", "Total, 1 Jun 2025 - 25 Sep 2026.", True),
        th("Pay", "Share", "Toplam tık içindeki pay.", "Share of total clicks.", True),
        th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)],
       [[x("Mobil", "Mobile"), cellk(GC["MOBILE"][0]), n(yzd(mob)), n(yzd(ctr_m))],
        [x("Masaüstü", "Desktop"), cellk(GC["DESKTOP"][0]), n(yzd(100 * GC["DESKTOP"][0] / sum(v[0] for v in GC.values()))), n(yzd(ctr_d))],
        [x("Tablet", "Tablet"), cellk(GC["TABLET"][0]), n(yzd(100 * GC["TABLET"][0] / sum(v[0] for v in GC.values()))), n(yzd(100 * GC["TABLET"][0] / GC["TABLET"][1]))],
        [x("Türkiye", "Turkey"), cellk(GU[0][1]), n(yzd(GU[0][2])), n("-")], [x("Almanya", "Germany"), cellk(GU[1][1]), n(yzd(GU[1][2])), n("-")], [x("KKTC", "Northern Cyprus"), cellk(GU[2][1]), n(yzd(GU[2][2])), n("-")]], "dar"),
 insight("Temmuz - Eylül 2026'da en çok tık alan sayfa ana sayfadır (%s); ilk 15 sayfanın %d'i kategori sayfasıdır ve listede ürün sayfası bulunmamaktadır. Cihaz kırılımında mobil, gösterimlerin %s'ini almasına karşın tıkların %s'ini üretmektedir; CTR masaüstünde %s, mobilde %s seviyesindedir." % (bin(TS[0][1]), sum(1 for uu, _ in TS[:15] if "/c-" in uu), yzd(mob_i), yzd(mob), yzd(ctr_d), yzd(ctr_m)),
         "In July - September 2026 the page with the most clicks is the home page (%s); %d of the top 15 pages are category pages and the list has no product page. By device, mobile takes %s of impressions but produces %s of clicks; CTR is %s on desktop and %s on mobile." % (bin(TS[0][1]), sum(1 for uu, _ in TS[:15] if "/c-" in uu), yzd(mob_i).replace("%", "") + "%", yzd(mob).replace("%", "") + "%", yzd(ctr_d).replace("%", "") + "%", yzd(ctr_m).replace("%", "") + "%"), "D2") +
 kaynak("Google Search Console · sc-domain:vitra.com.tr · 1 Haz 2025 - 25 Eyl 2026 · sayfa, sayfa×gün, cihaz×gün ve ülke boyutları · %s" % veri.TARIH,
        "Google Search Console · sc-domain:vitra.com.tr · 1 Jun 2025 - 25 Sep 2026 · page, page×day, device×day and country dimensions · %s" % veri.TARIH, "D2"),
)
