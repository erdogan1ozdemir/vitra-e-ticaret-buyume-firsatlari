# -*- coding: utf-8 -*-
"""Bolum: Fiyat ve satici manzarasi - Google Shopping (urun tipi x mecra, VitrA urunlerinde satici dokumu)."""
from ortak import *
import csv, os, statistics
D = os.path.join(veri.V, "ham", "derin", "fiyat_manzarasi")
def C(f): return list(csv.DictReader(open(os.path.join(D, f), encoding="utf-8-sig")))
MAT = C("fiyat_matrisi.csv"); SAT = C("vitra_saticilar.csv")
TIP_EN = {"Aksesuar & havlupan": "Accessories & towel radiators", "Akıllı klozet": "Smart WC", "Ayna": "Mirror", "Banyo mobilyası": "Bathroom furniture", "Batarya": "Taps", "Duş seti": "Shower set",
          "Duşakabin & duş teknesi": "Shower enclosures and trays", "Klozet": "WC", "Klozet kapağı": "Toilet seat", "Küvet": "Bathtub", "Lavabo": "Washbasin", "Mutfak (evye & batarya)": "Kitchen (sink & tap)", "Rezervuar": "Cistern"}
MEC = [("Trendyol", "trendyol.com"), ("Hepsiburada", "hepsiburada.com"), ("Amazon TR", "amazon.com.tr"), ("Koçtaş", "koctas.com.tr"), ("Bağımsız mağaza", None), ("VitrA Online", "vitra.com.tr"), ("Tüm mecralar", None)]
MEC_EN = {"Bağımsız mağaza": "Independent store", "VitrA Online": "VitrA Online", "Tüm mecralar": "All channels"}
mat = {}
for r in MAT:
    mat.setdefault(r["urun_tipi"], {})[r["mecra"]] = r
def hucre(t, m):
    r = mat.get(t, {}).get(m)
    if not r or int(r["urun_adedi"]) < 3: return n("-")
    return n("%s (%s)" % (bin(round(float(r["medyan"]))), r["urun_adedi"]))
def mec_bas(ad):
    return lg(dict(MEC)[ad]) + veri_m(ad) if dict(MEC).get(ad) else x(ad, MEC_EN.get(ad, ad))
T_MAT = tablo([th("Ürün tipi", "Product type", "Google Shopping kelimelerinin eşlendiği ürün tipi; tüm markalar birlikte.", "Product type to which the Google Shopping keywords were mapped; all brands together.")] +
              [th(a, MEC_EN.get(a, a), "Mecradaki ilanların medyan fiyatı (TL) ve ilan adedi; en az 3 ilan. Marka ve model karışımından etkilenir.", "Median price (TL) of listings in the channel and listing count; at least 3 listings. Affected by brand and model mix.", True) for a, _ in MEC],
              [[x(t, TIP_EN[t])] + [hucre(t, a) for a, _ in MEC] for t in TIP_EN], "uzun")
UC = [("Aksesuar & havlupan", "Çiçeksepeti", 1198, "Koçtaş", 3690), ("Akıllı klozet", "Bağımsız mağaza", 15312, "Trendyol", 24196), ("Ayna", "IKEA", 1699, "Çiçeksepeti", 5174), ("Banyo mobilyası", "Amazon TR", 3299, "Bağımsız mağaza", 8400),
      ("Batarya", "Amazon TR", 996, "Çiçeksepeti", 5967), ("Duş seti", "Hepsiburada", 1200, "Koçtaş", 2948), ("Duşakabin & duş teknesi", "Koçtaş", 7690, "Çiçeksepeti", 14900), ("Klozet", "Bağımsız mağaza", 9500, "Bauhaus", 11290),
      ("Klozet kapağı", "Trendyol", 693, "Bauhaus", 2890), ("Lavabo", "Hepsiburada", 4670, "Amazon TR", 8632), ("Mutfak (evye & batarya)", "Hepsiburada", 1700, "Bağımsız mağaza", 6500), ("Rezervuar", "Amazon TR", 629, "Bağımsız mağaza", 3150)]
MEC_EN2 = dict(MEC_EN, **{"Çiçeksepeti": "Çiçeksepeti", "IKEA": "IKEA", "Bauhaus": "Bauhaus"})
T_UC = tablo([th("Ürün tipi", "Product type", "Ürün tipi.", "Product type."), th("En düşük medyanlı mecra", "Lowest-median channel", "Çok markalı mecralar arasında (en az 5 ilan) medyan fiyatı en düşük olan; resmi marka mağazaları hariç.", "Among multi-brand channels (at least 5 listings) the one with the lowest median price; official brand stores excluded."),
              th("Medyan", "Median", "TL.", "TL.", True), th("En yüksek medyanlı mecra", "Highest-median channel", "Medyan fiyatı en yüksek çok markalı mecra.", "Multi-brand channel with the highest median price."), th("Medyan", "Median", "TL.", "TL.", True)],
             [[x(a, TIP_EN[a]), x(b, MEC_EN2.get(b, b)), cell(c), x(d, MEC_EN2.get(d, d)), cell(e)] for a, b, c, d, e in UC])
VA = [("Klozet", 19216, 10, "-%18 (18)", "-%44 (14)", "-%39 (22)", "-%40 (64)"), ("Lavabo", 11552, 27, "-%29 (25)", "-%20 (6)", "-%14 (7)", "-%32 (53)"), ("Batarya", 15402, 29, "-%35 (16)", "-%10 (6)", "-%27 (23)", "-%41 (57)"), ("Banyo mobilyası", 24785, 4, "+%44 (2)", "-", "-%23 (3)", "-%32 (18)")]
T_VA = tablo([th("Ürün tipi", "Product type", "Yalnızca başlığında VitrA veya Artema geçen ilanlar.", "Only listings with VitrA or Artema in the title."),
              th("VitrA Online medyan (ilan)", "VitrA Online median (listings)", "vitra.com.tr mağazasının Shopping ilanlarında medyan fiyat (TL) ve ilan sayısı.", "Median price (TL) and listing count of the vitra.com.tr store's Shopping listings.", True),
              th("Trendyol", "Trendyol", "Mecra medyanının VitrA Online medyanına göre farkı (ilan sayısı). Model karışımı aynı değildir; yön göstergesidir.", "Difference of the channel median from the VitrA Online median (listing count). Model mix is not identical; a direction indicator.", True),
              th("Hepsiburada", "Hepsiburada", "Aynı fark.", "Same difference.", True), th("Koçtaş", "Koçtaş", "Aynı fark.", "Same difference.", True), th("Bağımsız mağaza", "Independent store", "Aynı fark.", "Same difference.", True)],
             [[x(a, TIP_EN[a]), n("%s (%d)" % (bin(b), c)), n(d), n(e), n(f), n(g)] for a, b, c, d, e, f, g in VA], "dar")
# satici dokumu: liste bazinda
import json as _json
_SH = {d_["liste_basligi"]: d_["sonuc"].get("check_url") for d_ in _json.load(open(os.path.join(D, "_sellers_ham.json"), encoding="utf-8")) if d_.get("sonuc")}
lst = {}
for r in SAT:
    l = lst.setdefault(r["liste_basligi"], {"sorgu": r["urun_sorgusu"], "fiyat": [], "sat": [], "vo": None, "ucuz": None})
    f = float(r["fiyat_try"]); l["fiyat"].append(f); l["sat"].append((r["satici"], r["mecra"], f))
    if r["en_ucuz"] == "Evet": l["ucuz"] = (r["satici"], r["mecra"])
    if r["alan_adi"].replace("www.", "") in ("vitra.com.tr", "online.vitra.com.tr") or r["mecra"] == "VitrA Online": l["vo"] = (f, int(r["fiyat_sirasi"]), r["vitra_online_fark_yuzde"])
srows = []
for b, l in lst.items():
    mn, md, mx = min(l["fiyat"]), statistics.median(l["fiyat"]), max(l["fiyat"])
    uc = l["ucuz"] or min(l["sat"], key=lambda s: s[2])[:2]
    vo = l["vo"]
    srows.append([u(_SH[b], b[:48] + ("…" if len(b) > 48 else "")) if _SH.get(b) else veri_m(b[:48] + ("…" if len(b) > 48 else "")), cell(len(l["fiyat"])), veri_m("%s (%s)" % (uc[0], uc[1])), cell(round(mn)), cell(round(md)), cell(round(mx)),
                  n("%s (%d.)" % (bin(round(vo[0])), vo[1])) if vo else x("listede yok", "not listed"), n(("+%%%s" % vo[2].replace(".", ",")) if vo and vo[2] else "-")])
T_SAT = tablo([th("Ürün listesi", "Product list", "Google Shopping'de aynı ürünü satan satıcıların toplandığı liste; VitrA ve Artema ürün adı aramalarından. Bağlantı Google Shopping satıcı listesini açar.", "List gathering the sellers of the same product on Google Shopping; from VitrA and Artema product name searches. The link opens the Google Shopping seller list."),
               th("Satıcı", "Sellers", "Listede görünen satıcı sayısı; 10 değeri \"10 ve üzeri\" anlamına gelir.", "Number of sellers shown in the list; 10 means \"10 or more\".", True),
               th("En ucuz satıcı (mecra)", "Cheapest seller (channel)", "Listede en düşük toplam fiyatı veren satıcı ve mecra türü.", "Seller and channel type with the lowest total price in the list."),
               th("Min", "Min", "TL.", "TL.", True), th("Medyan", "Median", "TL.", "TL.", True), th("Maks", "Max", "TL.", "TL.", True),
               th("VitrA Online fiyat (sıra)", "VitrA Online price (rank)", "Resmi mağazanın listedeki fiyatı ve fiyat sırası; \"listede yok\" ilk 10 satıcı arasında bulunmadığını gösterir.", "The official store's price and price rank in the list; \"not listed\" means it is not among the top 10 sellers."),
               th("VitrA Online / en düşük", "VitrA Online / lowest", "Resmi mağaza fiyatının listedeki en düşük fiyata göre farkı.", "Difference of the official store price from the lowest price in the list.", True)], srows, "uzun")
MO = [("Bağımsız mağaza", "20 / 24", 12, "%0"), ("Banyomarka", "19 / 24", 3, "+%36"), ("Trendyol", "12 / 24", 4, "+%17"), ("Diğer pazaryeri / genel perakende", "11 / 24", 1, "+%61"), ("VitrA Online", "9 / 24", 0, "+%37"), ("Çiçeksepeti", "8 / 24", 1, "+%83"), ("Hepsiburada", "6 / 24", 0, "+%101"), ("Koçtaş", "5 / 24", 1, "+%41"), ("Amazon TR", "4 / 24", 2, "+%13")]
MO_EN = {"Bağımsız mağaza": "Independent store", "Banyomarka": "Banyomarka", "Trendyol": "Trendyol", "Diğer pazaryeri / genel perakende": "Other marketplace / general retail", "VitrA Online": "VitrA Online", "Çiçeksepeti": "Çiçeksepeti", "Hepsiburada": "Hepsiburada", "Koçtaş": "Koçtaş", "Amazon TR": "Amazon TR"}
T_MO = tablo([th("Mecra", "Channel", "Satıcı dökümündeki mecra türü.", "Channel type in the seller breakdown."), th("Görüldüğü liste", "Lists appeared in", "24 ürün listesinin kaçında satıcı olarak görünüyor.", "In how many of the 24 product lists it appears as a seller.", True),
              th("En ucuz olduğu liste", "Lists where cheapest", "Kaç listede en düşük fiyatı veriyor.", "In how many lists it offers the lowest price.", True), th("En düşük fiyata medyan fark", "Median gap to lowest", "Mecranın fiyatının listedeki en düşük fiyata göre medyan farkı.", "Median difference of the channel's price from the lowest price in the list.", True)],
             [[x(a, MO_EN[a]), n(b), cell(c), n(d)] for a, b, c, d in MO], "dar")
MK = [("VitrA", 146, 4.5, 7.4), ("Creavit", 129, 4.0, 6.7), ("Kale", 112, 3.5, 3.3), ("E.C.A.", 67, 2.1, 3.3), ("Turkuaz", 54, 1.7, 2.2), ("Grohe", 50, 1.5, 0.0), ("Serel", 49, 1.5, 1.5), ("Geberit", 42, 1.3, 0.7), ("Artema", 30, 0.9, 1.1), ("Duravit", 24, 0.7, 0.0)]
T_MK = tablo([th("Marka", "Brand", "İlan başlığında geçen marka; başlığında marka geçmeyen ilanlar (%65) dışarıdadır.", "Brand appearing in the listing title; listings without a brand in the title (65%) are excluded."),
              th("Listeleme", "Listings", "27 kategori kelimesinin ilk 120 sonucundaki listeleme sayısı (3.240 satır).", "Listings in the first 120 results of 27 category keywords (3,240 rows).", True),
              th("Pay (ilk 120)", "Share (first 120)", "Tüm listelemeler içindeki pay.", "Share of all listings.", True), th("Pay (ilk 10)", "Share (first 10)", "Yalnızca ilk 10 sonuç içindeki pay.", "Share within the first 10 results only.", True)],
             [[veri_m(a), cell(b), n(yzd(c)), n(yzd(d))] for a, b, c, d in MK], "dar")
VO = [("lavabo dolabı", 3, 1), ("asma klozet", 3, 3), ("lavabo", 6, 7), ("boy dolabı", 2, 9), ("çanak lavabo", 1, 16), ("ankastre batarya", 3, 21), ("lavabo bataryası", 1, 31), ("banyo dolabı", 1, 40), ("banyo bataryası", 1, 45), ("gömme rezervuar", 1, 56), ("banyo aynası", 1, 61), ("klozet", 1, 95)]
T_VO = tablo([th("Kategori kelimesi", "Category keyword", "VitrA Online'ın Shopping sonuçlarında göründüğü 12 kelime; 15 kelimede hiç görünmüyor.", "The 12 keywords where VitrA Online appears in Shopping results; it does not appear at all in 15 keywords."),
              th("Listeleme", "Listings", "İlk 120 sonuçtaki VitrA Online ilanı.", "VitrA Online listings in the first 120 results.", True), th("En iyi sıra", "Best rank", "İlanın en iyi sırası.", "Best rank of the listing.", True)],
             [[kw(a), cell(b), cell(c)] for a, b, c in VO], "dar")
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
<div class="two"><div><h3>%s</h3>%s</div><div><h3>%s</h3>%s</div></div>
%s
<h3>%s</h3>
%s
%s
%s
<div class="two"><div><h3>%s</h3>%s</div><div><h3>%s</h3>%s</div></div>
%s
%s
%s
%s
""" % (
 x("Google Shopping'de 27 kategori ve 3 marka kelimesinin ilk 120 sonucu (3.600 ilan) ile 12 VitrA ve Artema ürün adının satıcı dökümü (24 liste) alınmıştır; Akakçe ürün ve kategori sayfaları ile Cimri kategori ve marka sayfaları ayrıca okunmuştur. Fiyatlar 29.09.2026 tarihli anlık değerlerdir ve günlük değişebilir; mecra medyanları marka ve model karışımından etkilenir, aynı ürün üzerinden kıyas yalnızca satıcı dökümünde yapılmıştır.",
   "The first 120 results (3,600 listings) for 27 category and 3 brand keywords on Google Shopping and the seller breakdown of 12 VitrA and Artema product names (24 lists) were retrieved; Akakçe product and category pages and Cimri category and brand pages were also read. Prices are snapshot values of 29.09.2026 and may change daily; channel medians are affected by brand and model mix, and like-for-like comparison is made only in the seller breakdown."),
 kpi_kart("%0,7", "VitrA Online'ın kategori kelimelerindeki Shopping listeleme payı · 27 kelimenin 12'sinde görünüyor", "VitrA Online's Shopping listing share in category keywords · appears in 12 of 27 keywords", "dn"),
 kpi_kart("+%37", "Aynı üründe resmi mağaza fiyatının en düşük satıcı fiyatına medyan farkı (9 liste, %6 - %52)", "Median gap of the official store price to the lowest seller price for the same product (9 lists, 6% - 52%)", "hi"),
 kpi_kart("12 / 24", "En ucuz satıcının bağımsız banyo ve yapı mağazası olduğu ürün listesi · Hepsiburada 0", "Product lists where the cheapest seller is an independent bathroom and building store · Hepsiburada 0"),
 kpi_kart("%10,8", "Klozet ilanlarında VitrA ve Artema payı · duşakabin %0,8, aksesuar %0,4, küvet %0", "VitrA and Artema share of WC listings · shower enclosure 0.8%, accessories 0.4%, bathtub 0%"),
 x("Ürün tipi ve mecra bazında fiyat bandı", "Price band by product type and channel"), T_MAT,
 insight("Aynı ürün tipinde mecralar arası medyan farkı büyüktür: rezervuarda Amazon TR 629 TL ile bağımsız mağazalar 3.150 TL, aksesuarda Çiçeksepeti 1.198 TL ile Koçtaş 3.690 TL arasındadır. VitrA Online'ın medyanı klozette 19.216 TL, bataryada 15.402 TL ve mobilyada 24.785 TL ile her tipte tüm mecralar medyanının üzerindedir; bu fark resmi mağazanın üst segment ürünleri listelemesinden ve indirimli üçüncü taraf ilanlarından birlikte kaynaklanmaktadır. Min değerler set dışı parça ve aksesuar içerebilir; orta bant için medyan esas alınmalıdır.",
         "Median differences between channels within the same product type are large: for cisterns between Amazon TR at 629 TL and independent stores at 3,150 TL, for accessories between Çiçeksepeti at 1,198 TL and Koçtaş at 3,690 TL. VitrA Online's median is above the all-channel median in every type, with 19,216 TL for WCs, 15,402 TL for taps and 24,785 TL for furniture; this gap stems both from the official store listing upper-segment products and from discounted third-party listings. Min values may include off-set parts and accessories; the median should be used for the middle band.", "D25"),
 x("En ucuz ve en pahalı mecra", "Cheapest and most expensive channel"), T_UC, x("VitrA ve Artema ilanlarında mecra farkı", "Channel gap in VitrA and Artema listings"), T_VA,
 insight("VitrA ve Artema ilanlarıyla sınırlandırıldığında Trendyol, Hepsiburada ve Koçtaş medyanı klozette VitrA Online'ın %18 - %44, lavaboda %14 - %29, bataryada %10 - %35 altındadır; bağımsız mağazalar her tipte %32 - %41 daha düşüktür. Yalnızca banyo mobilyasında Trendyol medyanı (2 ilan) resmi mağazanın üzerindedir. Kullanıcının Shopping ya da fiyat karşılaştırma sitesinde gördüğü tablo, resmi mağazayı fiyat değil hizmet ve güvence ile ayrışmaya yöneltmektedir.",
         "Restricted to VitrA and Artema listings, the Trendyol, Hepsiburada and Koçtaş medians are 18% - 44% below VitrA Online for WCs, 14% - 29% for washbasins and 10% - 35% for taps; independent stores are 32% - 41% lower in every type. Only in bathroom furniture is the Trendyol median (2 listings) above the official store. The picture the user sees on Shopping or a price comparison site pushes the official store to differentiate on service and assurance rather than price.", "D25"),
 x("Aynı ürünün satıcıları: 24 VitrA ve Artema listesi", "Sellers of the same product: 24 VitrA and Artema lists"), T_SAT, T_MO,
 insight("24 ürün listesinde en ucuz satıcı 12 listede bağımsız banyo ve yapı mağazası, 4'ünde Trendyol, 3'ünde Banyomarka, 2'sinde Amazon TR'dir; Hepsiburada hiçbir listede en ucuz değildir ve en düşük fiyata medyan farkı %101'dir. VitrA Online 24 listenin 9'unda ilk 10 satıcı arasındadır ve bu listelerde en düşük fiyatın medyan %37 üzerindedir (Integra asma klozet +%13, Metropole Round +%6, Sento lavabo dolabı +%47, Metropole asma klozet +%52). Artema bataryalarının 6 listesinin hiçbirinde resmi mağaza yer almamaktadır. Aynı ürün için en yüksek fiyat en düşüğün medyan %126 üzerindedir; kapak dahil ve hariç varyantlar bu farkın bir bölümünü açıklayabilir.",
         "Across the 24 product lists the cheapest seller is an independent bathroom and building store in 12, Trendyol in 4, Banyomarka in 3 and Amazon TR in 2; Hepsiburada is never the cheapest and its median gap to the lowest price is 101%. VitrA Online is among the top 10 sellers in 9 of 24 lists and sits a median 37% above the lowest price in those lists (Integra wall-hung WC +13%, Metropole Round +6%, Sento basin unit +47%, Metropole wall-hung WC +52%). The official store is absent from all 6 Artema tap lists. The highest price for the same product is a median 126% above the lowest; variants with and without the seat may explain part of this gap.", "D25"),
 x("Marka payı", "Brand share"), T_MK, x("VitrA Online'ın göründüğü kelimeler", "Keywords where VitrA Online appears"), T_VO,
 insight("Kategori kelimelerinin ilk 120 Shopping sonucunda VitrA %4,5 ile en yüksek paylı markadır (Creavit %4,0, Kale %3,5); ilk 10'da payı %7,4'e çıkmaktadır. Buna karşın vitra.com.tr mağazası listelemelerin yalnızca %0,7'sini oluşturmakta, VitrA ve Artema ilanlarının %44'ü bağımsız mağazalardan, %19'u Trendyol'dan gelmektedir. Resmi mağaza lavabo dolabında 1., asma klozette 3. sırada görünürken klozet kapağı, akıllı klozet, duşakabin, duş seti, taharet musluğu, iç takım, havlupan ve evye dahil 15 kelimede hiç görünmemektedir. Merchant Center feed'inin bu kategorileri kapsaması ve başlıkların kategori kelimesini taşıması, ürünlerin ücretsiz listelemelerde görünürlüğünü destekleyebilir.",
         "In the first 120 Shopping results of the category keywords VitrA is the brand with the highest share at 4.5% (Creavit 4.0%, Kale 3.5%); in the first 10 its share rises to 7.4%. Yet the vitra.com.tr store accounts for only 0.7% of listings, and 44% of VitrA and Artema listings come from independent stores and 19% from Trendyol. The official store ranks 1st for basin units and 3rd for wall-hung WCs but does not appear at all for 15 keywords including toilet seat, smart WC, shower enclosure, shower set, bidet valve, inner mechanism, towel radiator and sink. Covering these categories in the Merchant Center feed and carrying the category keyword in titles can support product visibility in free listings.", "D25"),
 p("Aynı model kodu üzerinden yapılan 200 eşleşmede pazaryeri fiyatı vitra.com.tr liste fiyatının medyan %14,4 altında ve \"Sepette %N indirim\" uygulanmış fiyata yakındır; üçüncü taraf satıcılarda liste fiyatının 2-3 katına çıkan ilanlar da bulunmaktadır. Kanal bazında ayrım ve örnekler [[b:derin]] bölümündedir.", "In 200 matches on the same model code the marketplace price is a median 14.4% below the vitra.com.tr list price and close to the price after the \"N% off in basket\" label; third-party sellers also list at 2-3 times the list price. The breakdown by channel and the examples are in section [[b:derin]].", "D30"),
 note("KISIT", "LIMITATION", ul_b([("Mecra medyanı model karışımıdır:", "Channel medians are a model mix:", "aynı ürün üzerinden kıyas yalnızca satıcı listelerinde yapılmıştır; ürün tipi × mecra tablosu yön gösterir.", "like-for-like comparison is made only in seller lists; the product type × channel table indicates direction."),
                                   ("Puan ve değerlendirme alanı:", "Rating and review fields:", "Shopping ilanlarında çok az dolu geldiği için analize alınmamıştır.", "were filled in very few Shopping listings and were left out of the analysis."),
                                   ("Cimri:", "Cimri:", "arama sayfası bot koruması nedeniyle okunamamış; 29 ürünün 19'u marka ve kategori sayfalarından eşlenmiş, ürün sayfaları tarayıcıda açılarak 110 teklif okunmuştur; 10 ürün eşleşmemiştir.", "the search page could not be read because of bot protection; 19 of 29 products were matched from brand and category pages and 110 offers were read by opening product pages in the browser; 10 products did not match.")])),
 kaynak("Google Shopping (DataForSEO merchant/google/products ve merchant/google/sellers) · 30 kelime × 120 ilan, 24 satıcı listesi · Türkiye, masaüstü · 29.09.2026 · Akakçe ve Cimri sınırlı okuma", "Google Shopping (DataForSEO merchant/google/products and merchant/google/sellers) · 30 keywords × 120 listings, 24 seller lists · Turkey, desktop · 29.09.2026 · Akakçe and Cimri limited reading", "D25"),
)

from b_fiyat2 import EK as _EK
from b_fiyat3 import EK2 as _EK2
HTML = HTML + _EK + _EK2
