# -*- coding: utf-8 -*-
"""Fiyat bolumu ek 2: Akakce ve Cimri (Chrome okuma, 30.09.2026) - D27."""
from ortak import *
import json, os
D = os.path.join(veri.V, "ham", "derin", "fiyat_manzarasi", "chrome")
OZ = json.load(open(os.path.join(D, "ozet_urun.json"), encoding="utf-8"))
AK = [json.loads(l) for l in open(os.path.join(D, "akakce_kategori.jsonl"), encoding="utf-8")]
CK = [json.loads(l) for l in open(os.path.join(D, "cimri_kategori.jsonl"), encoding="utf-8")]
GRUP_EN = {"Asma klozet": "Wall-hung WC", "Lavabo": "Washbasin", "Banyo mobilyası (lavabo dolabı)": "Bathroom furniture (basin unit)", "Banyo mobilyası (boy dolabı)": "Bathroom furniture (tall cabinet)", "Armatür (lavabo bataryası)": "Tap (basin)", "Armatür (banyo bataryası)": "Tap (bath)",
           "Armatür (termostatik batarya)": "Tap (thermostatic)", "Armatür (ara musluk)": "Tap (stop valve)", "Armatür (çamaşır musluğu)": "Tap (washing machine valve)", "Duş seti": "Shower set", "Gömme rezervuar seti": "Concealed cistern set", "Klozet kapağı": "Toilet seat", "İç takım": "Inner mechanism", "Klozet (takım)": "WC (close-coupled)"}
def fyz(v):
    if v is None: return n("-")
    return n(("%+.1f" % v).replace(".", ",").replace("+", "+%").replace("-", "-%") if v else "%0")
rows = []
for r in OZ:
    if not r.get("ak_liste_n"): continue
    rows.append([veri_m(r["urun"][:40]), veri_m(r["kod"]), x(r["grup"], GRUP_EN.get(r["grup"], r["grup"])), cell(round(r["vitra_com_tr"])) if r.get("vitra_com_tr") else n("-"),
                 cell(r["ak_toplam"]), cell(round(r["ak_min"])), veri_m("%s%s" % (r["ak_min_mecra"], (" / " + r["ak_min_satici"]) if r.get("ak_min_satici") else "")), cell(round(r["ak_medyan"])),
                 fyz(r.get("ak_fark")), n("%s (%s)" % (bin(round(r["ci_en_ucuz"])), r["ci_fiyat_sayisi"])) if r.get("ci_en_ucuz") else n("-")])
T_AK = tablo([th("Ürün", "Product", "VitrA veya Artema ürünü.", "VitrA or Artema product."), th("Kod", "Code", "Ürün kodu; Akakçe ve Cimri kayıtları kodla eşlenmiştir.", "Product code; Akakçe and Cimri records matched by code."),
              th("Grup", "Group", "Ürün grubu.", "Product group."), th("vitra.com.tr", "vitra.com.tr", "Ürün sayfasındaki liste fiyatı (TL), 29.09.2026.", "List price on the product page (TL), 29.09.2026.", True),
              th("Akakçe satıcı", "Akakçe sellers", "Akakçe'nin ürün için listelediği toplam fiyat (satıcı) sayısı.", "Total number of prices (sellers) Akakçe lists for the product.", True),
              th("Akakçe en düşük", "Akakçe lowest", "Kargo dahil en düşük fiyat (TL), 30.09.2026.", "Lowest price including shipping (TL), 30.09.2026.", True),
              th("En düşük fiyatın mecrası / satıcısı", "Channel / seller of lowest price", "Akakçe'de en düşük fiyatı veren pazaryeri ve o pazaryerindeki satıcı.", "Marketplace giving the lowest price on Akakçe and the seller on that marketplace."),
              th("Akakçe medyan", "Akakçe median", "Listelenen ilk 16 satıcının medyan fiyatı (TL).", "Median price of the first 16 listed sellers (TL).", True),
              th("Fark", "Gap", "vitra.com.tr liste fiyatından Akakçe en düşük fiyata düşüş; eksi değer vitra.com.tr'nin daha düşük olduğunu gösterir.", "Reduction from the vitra.com.tr list price to the Akakçe lowest; a negative value means vitra.com.tr is lower.", True),
              th("Cimri en düşük (fiyat sayısı)", "Cimri lowest (price count)", "Cimri kategori kartındaki en düşük fiyat ve fiyat sayısı; \"-\" Cimri'de kod eşleşmesi yok.", "Lowest price and price count on the Cimri category card; \"-\" no code match on Cimri.", True)], rows, "uzun")
KAT = [("klozet", "Klozet", "WC"), ("klozet-kapagi", "Klozet kapağı", "Toilet seat"), ("lavabo", "Lavabo", "Washbasin"), ("banyo-dolabi", "Banyo dolabı", "Bathroom cabinet"), ("dusakabin", "Duşakabin", "Shower enclosure"),
       ("banyo-bataryasi", "Banyo bataryası", "Bath tap"), ("lavabo-bataryasi", "Lavabo bataryası", "Basin tap"), ("dus-seti", "Duş seti", "Shower set"), ("rezervuar", "Rezervuar", "Cistern"), ("gomme-rezervuar", "Gömme rezervuar", "Concealed cistern"), ("banyo-aynasi", "Banyo aynası", "Bathroom mirror")]
ak = {a["kat"]: a for a in AK}; ck = {c["kat"]: c for c in CK}
def mk(lst): return veri_m(", ".join(m.split(":")[0] for m in lst[:3])) if lst else n("-")
krows = []
for k, tr, en in KAT:
    a = ak.get(k); c = ck.get(k)
    if not a and not c: continue
    krows.append([x(tr, en), cell(a["toplam"]) if a and a.get("toplam") else n("-"), cell(round(a["medyan"])) if a else n("-"), mk(a["markalar"]) if a else n("-"), cell(a["ek_medyan"]) if a else n("-"),
                  cell(c["toplam"]) if c else n("-"), cell(round(c["medyan"])) if c else n("-"), veri_m(", ".join(c["markalar_sira"].split(", ")[:3])) if c else n("-"), veri_m(", ".join(c["magazalar_sira"].split(", ")[:4])) if c else n("-")])
T_KAT = tablo([th("Kategori", "Category", "Akakçe ve Cimri kategori sayfası.", "Akakçe and Cimri category page."),
               th("Akakçe ürün", "Akakçe products", "Kategorideki toplam ürün; \"-\" sayfada okunamadı.", "Total products in the category; \"-\" not readable on the page.", True),
               th("Akakçe medyan (ilk 32)", "Akakçe median (first 32)", "Popülerlik sırasındaki ilk 32 ürünün en düşük fiyat medyanı (TL).", "Median of the lowest prices of the first 32 products in popularity order (TL).", True),
               th("Akakçe ilk 3 marka", "Akakçe top 3 brands", "İlk 32 üründe en çok ürünü olan markalar.", "Brands with the most products in the first 32."),
               th("Ek fiyat medyanı", "Median extra prices", "Ürün başına ek satıcı sayısı medyanı (ilk 32).", "Median number of additional sellers per product (first 32).", True),
               th("Cimri ürün", "Cimri products", "Cimri kategori sayfasının bildirdiği toplam ürün.", "Total products reported by the Cimri category page.", True),
               th("Cimri medyan (ilk 32)", "Cimri median (first 32)", "İlk 32 ürünün en düşük fiyat medyanı (TL).", "Median of the lowest prices of the first 32 products (TL).", True),
               th("Cimri marka sırası", "Cimri brand order", "Cimri'nin marka filtresindeki ilk 3 marka (ürün sayısına göre).", "First 3 brands in Cimri's brand filter (by product count)."),
               th("Cimri mağaza sırası", "Cimri store order", "Cimri'nin mağaza filtresindeki ilk 4 mağaza.", "First 4 stores in Cimri's store filter.")], krows, "uzun")
EK2 = """
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Akakçe ve Cimri: 29 VitrA ürününde satıcı sayısı ve en düşük fiyat", "Akakçe and Cimri: seller count and lowest price for 29 VitrA products"), T_AK,
 insight("Akakçe 29 ürünün 24'ünü listelemekte, ürün başına satıcı sayısı medyanı 8'dir (1 - 68); armatür ve klozet kapağında 26 - 68 satıcı bulunurken asma klozet ve mobilyada 1 - 15 satıcı vardır. Akakçe'deki en düşük fiyat 19 üründe vitra.com.tr liste fiyatının altındadır (fark medyanı %21,3; Flow Round banyo bataryası %47,3, AquaHeat termostatik %50,0); 5 üründe (S20 asma klozet, S20 tezgahaltı lavabo, Sento lavabo dolabı, Mia boy dolabı, Mia dolap seti) vitra.com.tr daha düşük ya da eşittir. En düşük fiyatı Hepsiburada 7, n11 ve Koçtaş 4'er, Pttavm ve idefix 3'er üründe vermektedir; Trendyol Akakçe listelerinde yalnızca 1 üründe görünmektedir. VitrA'nın kendi mağazası 24 listenin 5'inde yer almakta ve yalnızca AquaHeat termostatik bataryada en düşük fiyattır. Aynı satıcı (Evdema, Evdeniste, Hace Yapı) birden fazla pazaryerinde aynı ürünü farklı fiyatla listelemektedir: S50 asma klozet için Evdema n11'de 7.308 TL, Pttavm'de 7.525 TL, Hepsiburada'da 11.041 TL. Cimri'de kod eşleşen 10 üründe en düşük fiyat Akakçe ile büyük ölçüde örtüşmektedir.",
         "Akakçe lists 24 of the 29 products, with a median of 8 sellers per product (1 - 68); taps and toilet seats have 26 - 68 sellers while wall-hung WCs and furniture have 1 - 15. The Akakçe lowest price is below the vitra.com.tr list price for 19 products (median gap 21.3%; Flow Round bath tap 47.3%, AquaHeat thermostatic 50.0%); for 5 products (S20 wall-hung WC, S20 undercounter basin, Sento basin unit, Mia tall cabinet, Mia cabinet set) vitra.com.tr is lower or equal. The lowest price comes from Hepsiburada for 7 products, n11 and Koçtaş for 4 each, Pttavm and idefix for 3 each; Trendyol appears in Akakçe lists for only 1 product. VitrA's own store is present in 5 of 24 lists and is the lowest only for the AquaHeat thermostatic tap. The same seller (Evdema, Evdeniste, Hace Yapı) lists the same product at different prices on several marketplaces: for the S50 wall-hung WC Evdema charges 7,308 TL on n11, 7,525 TL on Pttavm and 11,041 TL on Hepsiburada. For the 10 products matched on Cimri the lowest price largely coincides with Akakçe.", "D27"),
 x("Fiyat karşılaştırma sitelerinde kategori görünümü", "Category view on price comparison sites"), T_KAT,
 insight("Fiyat karşılaştırma sitelerinde mağaza sıralaması Hepsiburada, Pttavm, idefix, Koçtaş ve Amazon ile başlamakta; Trendyol yalnızca Cimri banyo dolabı listesinde görünmektedir, çünkü Trendyol fiyat karşılaştırma sitelerine ürün akışı vermemektedir. Marka sırasında VitrA klozet kapağı ve gömme rezervuarda 1., klozette Creavit'in ardından 2., lavaboda 4. sıradadır; duşakabin listelerinin tamamına yakını Durul'dur. Kategori medyanları pazaryeri çok satanlarına yakındır (klozet 6.481 - 7.308 TL, lavabo bataryası 2.847 - 3.725 TL); ürün başına ek satıcı sayısı bataryada 35 - 36 ile en yüksek, mobilya ve duşakabinde 0 - 3 ile en düşüktür. Bu tablo, fiyat karşılaştırma kullanıcısının armatür ve tamamlayıcı üründe çok satıcılı ve düşük fiyatlı bir listeyle, mobilya ve duşakabinde ise marka mağazası ağırlıklı tek fiyatlı bir listeyle karşılaştığını göstermektedir.",
         "On price comparison sites the store order starts with Hepsiburada, Pttavm, idefix, Koçtaş and Amazon; Trendyol appears only in the Cimri bathroom cabinet list, since Trendyol does not feed price comparison sites. In brand order VitrA is 1st in toilet seats and concealed cisterns, 2nd after Creavit in WCs and 4th in washbasins; shower enclosure lists are almost entirely Durul. Category medians are close to marketplace best sellers (WC 6,481 - 7,308 TL, basin tap 2,847 - 3,725 TL); the number of additional sellers per product is highest in taps at 35 - 36 and lowest in furniture and shower enclosures at 0 - 3. This shows that the price comparison user meets a multi-seller, low-priced list in taps and complements, and a brand-store-heavy single-price list in furniture and shower enclosures.", "D27"),
 kaynak("Akakçe arama, ürün ve kategori sayfaları · Cimri kategori ve marka sayfaları · Chrome, 30.09.2026 · Cimri arama sayfası bot koruması nedeniyle okunamadı, ürün sayfalarında satıcı listesi istemci tarafında yüklendiği için kart düzeyi kullanıldı", "Akakçe search, product and category pages · Cimri category and brand pages · Chrome, 30.09.2026 · the Cimri search page could not be read because of bot protection; seller lists on product pages load client-side, so card level was used", "D27"),
)
