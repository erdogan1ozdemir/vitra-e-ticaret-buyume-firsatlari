# -*- coding: utf-8 -*-
"""Bolum: Kategori talebi ve donemsel degisim (Keyword Planner, 2.420 kelime)."""
from ortak import *
from rapor_parca1 import T, cizgi, barlar
import veri
K1 = A["k1"]; K2 = A["k2"]; TOP = A["toplam"]; AYK = A["aylik_k1"]
KAT_EN = {"Banyo Mobilyaları": "Bathroom Furniture", "Vitrifiyeler": "Sanitaryware", "Armatürler": "Taps and Mixers", "Yıkanma Alanları": "Bathing Areas",
          "Karo Seramik Ürünleri": "Ceramic Tiles", "Banyo Aksesuarları": "Bathroom Accessories", "Duşlar": "Showers", "Rezervuarlar": "Cisterns", "Toplam": "Total"}
K2_EN = {"Balkon, Teras & Bahçe Karo Seramikleri": "Balcony, Terrace & Garden Tiles", "Duşlar": "Showers", "Banyo Karo Seramikleri": "Bathroom Tiles", "Ankastre Duş Yönlendiriciler": "Concealed Shower Diverters",
         "Banyo Mobilyaları": "Bathroom Furniture", "Klozetler": "WCs", "Banyo Tezgahları": "Bathroom Countertops", "Duş Kanalları": "Shower Channels", "Duş Tekneleri": "Shower Trays",
         "Armatür Tamamlayıcı Ürünleri": "Tap Accessories", "Tuvalet Fırçaları": "Toilet Brushes", "Duvar Karoları": "Wall Tiles", "Lavabo Dolapları": "Washbasin Units", "Banyo Aksesuar Setleri": "Bathroom Accessory Sets",
         "Bideler": "Bidets", "Banyo Aynaları": "Bathroom Mirrors", "Banyo Aksesuarları": "Bathroom Accessories", "Banyo Set Modülleri": "Bathroom Set Modules", "Tuvalet Kağıtlıkları": "Toilet Roll Holders",
         "Banyo Mobilya Tamamlayıcıları": "Bathroom Furniture Add-ons", "Duş Başlıkları": "Shower Heads", "Duş Tamamlayıcı Ürünleri": "Shower Accessories", "Banyo Dolapları": "Bathroom Cabinets", "Duş Setleri": "Shower Sets",
         "Lavabolar": "Washbasins", "Klozet Kapakları": "Toilet Seats", "Gömme Rezervuarlar": "Concealed Cisterns", "Duşakabin": "Shower Enclosures", "Küvetler": "Bathtubs", "Eviye Bataryaları": "Kitchen Taps",
         "Lavabo Bataryaları": "Basin Taps", "Banyo Bataryaları": "Bath Taps", "Ev İçi Zemin Karo Seramikleri": "Indoor Floor Tiles", "Porselen Karolar": "Porcelain Tiles", "Yer Karoları": "Floor Tiles",
         "Musluk ve Ara Musluklar": "Taps and Stop Valves", "Rezervuar Kumanda Panelleri": "Flush Plates", "Akıllı Klozet": "Smart WC", "Havluluklar": "Towel Rails", "Sabunluklar": "Soap Dispensers",
         "El Duşu Takımları": "Hand Shower Sets", "Bataryalı Duş Sistemleri": "Shower Systems with Mixer", "Duş Kolonları": "Shower Columns", "Pisuvarlar": "Urinals", "Eviyeler": "Kitchen Sinks",
         "Vitrifiye Tamamlayıcıları": "Sanitaryware Accessories", "Mutfak Karo Seramikleri": "Kitchen Tiles", "Havuz Karo Seramikleri": "Pool Tiles", "Ticari & Endüstriyel Alan Karo Seramikleri": "Commercial & Industrial Tiles",
         "Karo Seramik Ürünleri": "Ceramic Tiles", "Gömme Rezervuar Montaj Aksesuarları": "Concealed Cistern Fitting Accessories", "Gömme Rezervuar Setleri": "Concealed Cistern Sets", "Taşıyıcı Aparatlar": "Support Frames",
         "Vitrifiyeler": "Sanitaryware", "Duş Üniteleri": "Shower Units", "Yıkanma Alanları": "Bathing Areas", "Yıkanma Alanı Tamamlayıcı Ürünler": "Bathing Area Accessories", "Armatürler": "Taps and Mixers",
         "Bide Bataryaları": "Bidet Taps", "Banyo Askıları": "Bathroom Hooks", "Banyo Çöp Kovaları": "Bathroom Bins", "Diğer Banyo Aksesuarları": "Other Bathroom Accessories", "Diş Fırçalıkları": "Toothbrush Holders",
         "Masajlı Duş Sistemleri": "Massage Shower Systems", "Sürgülü El Duşu Takımları": "Sliding Hand Shower Sets"}
K2_EN.update({'Akıllı Klozet Seti': 'Smart WC Sets', 'Akıllı Kumanda Panelleri': 'Smart Flush Plates', 'Ankastre Bataryalar': 'Concealed Mixers', 'Ankastre Lavabo Bataryaları': 'Concealed Basin Mixers', 'Ankastre Stop Valfler': 'Concealed Stop Valves', 'Asma Klozet Takımları': 'Wall-hung WC Sets', 'Asma Klozetler': 'Wall-hung WCs', 'Asma Klozetler için Gömme Rezervuarlar': 'Concealed Cisterns for Wall-hung WCs', 'Aynalı Banyo Dolabı': 'Mirror Cabinets', 'Banyo Batarya Çıkış Uçları': 'Bath Spouts', 'Banyo Dolabı Kulpları': 'Cabinet Handles', 'Banyo Dolap Ayakları': 'Cabinet Feet', 'Banyo Konsolları': 'Bathroom Consoles', 'Banyo Malzemelikleri': 'Bathroom Caddies', 'Banyo Rafları': 'Bathroom Shelves', 'Banyo Tutunma Barları': 'Grab Bars', 'Duvar Önü Rezervuarlar': 'Exposed Cisterns', 'Duvardan Banyo Bataryaları': 'Wall-mounted Bath Mixers', 'Duş Dirsekleri': 'Shower Elbows', 'Duş Teknesi Panelleri': 'Shower Tray Panels', 'Duş Teknesi ve Küvet Ayakları': 'Shower Tray and Bathtub Feet', 'Düz Aynalar': 'Flat Mirrors', 'Etajerli Lavabolar': 'Washbasins with Shelf', 'Hidromasajlı Bağımsız Küvetler': 'Freestanding Whirlpool Baths', 'Hidromasajlı Standart Küvetler': 'Standard Whirlpool Baths', 'Hidromasajsız Bağımsız Küvetler': 'Freestanding Baths', 'Küvet Bataryaları': 'Bath Mixers', 'Küvet Panelleri': 'Bath Panels', 'Lavabo Sifon ve Süzgeçleri': 'Basin Siphons and Wastes', 'Makyaj Aynaları ve Diğer Aksesuarlar': 'Make-up Mirrors and Other Accessories', 'Monoblok Lavabolar': 'Monoblock Washbasins', 'Pisuvar Ara Bölmeleri': 'Urinal Dividers', 'Pisuvar Yıkama Sistemleri': 'Urinal Flush Systems', 'Rezervuar ve Klozet İç Takımları': 'Cistern and WC Inner Mechanisms', 'Sifonlar': 'Siphons', 'Standart Lavabo ve Ayakları': 'Standard Washbasins and Pedestals', 'Standart ve Gömme Küvetler': 'Standard and Built-in Baths', 'Sıva Altı ve Diğer Tamamlayıcılar': 'Concealed Bodies and Other Accessories', 'Taharet El Duşları': 'Bidet Hand Sprays', 'Takım Klozetler': 'Close-coupled WCs', 'Tek Armatür Delikli Lavabo Bataryaları': 'Single-hole Basin Mixers', 'Temassız Lavabo Bataryaları': 'Touchless Basin Mixers', 'Termostatik Bataryalar': 'Thermostatic Mixers', 'Tezgahaltı Lavabolar': 'Under-counter Washbasins', 'Tezgahüstü Lavabolar': 'Countertop Washbasins', 'Tuvalet Taşları için Gömme Rezervuarlar': 'Concealed Cisterns for Squat Toilets', 'VitrA Kaydırmaz': 'VitrA Anti-slip', 'Yarım Tezgah Lavabolar': 'Semi-recessed Washbasins', 'Yerden Tek Klozetler': 'Floor-standing WCs', 'Çamaşır Makinesi Dolapları': 'Washing Machine Cabinets', 'Çanak Lavabo Bataryaları': 'Bowl Basin Mixers', 'Çanak Lavabolar': 'Bowl Washbasins', 'İki veya Üç Delikli Lavabo Bataryaları': 'Two or Three-hole Basin Mixers'})
def kat(k): return x(k, KAT_EN.get(k, k))
def kat2(k): return x(k, K2_EN.get(k, k))
toplam_yoy = (TOP["a26"] / TOP["a25"] - 1) * 100
sira = sorted(K1, key=lambda k: -K1[k]["a26"])
RENK = {"Banyo Mobilyaları": "#E85F36", "Vitrifiyeler": "#10332F", "Armatürler": "#2E7D32", "Yıkanma Alanları": "#F5A623", "Karo Seramik Ürünleri": "#7A8C89", "Banyo Aksesuarları": "#B96BC2", "Duşlar": "#4A90D9", "Rezervuarlar": "#8B5A2B"}
GRAFIK = cizgi([(kat("Toplam"), "#E85F36", AYK["Toplam"])] , y_etiket=x("Aylık arama hacmi · 2.420 kelime toplamı", "Monthly search volume · total of 2,420 keywords"), aylar=veri.AYLAR)
GRAFIK_K = cizgi([(kat(k), RENK[k], AYK[k]) for k in sira[:5]], y_etiket=x("Aylık arama hacmi · en büyük 5 kategori", "Monthly search volume · five largest categories"), aylar=veri.AYLAR)
BAR = barlar([(_q, K1[_q]["yoy"], "#2E7D32" if K1[_q]["yoy"] > 0 else "#D32F2F") for _q in sorted(K1, key=lambda q: -K1[q]["yoy"])])
for _kk in K1: kat(_kk)
tbl = tablo([th("Kategori", "Category", "VitrA kategori ağacındaki ana kategori; 2.420 kelime 8 ana kategoriye dağıtılmıştır.", "Main category in the VitrA category tree; 2,420 keywords are distributed across 8 main categories."),
             th("Kelime", "Keywords", "Kategoriye atanan kelime sayısı.", "Number of keywords assigned to the category.", True),
             th("2025 aylık ort.", "2025 monthly avg.", "Ocak - Ağustos 2025 aylık ortalama arama hacmi (kategorideki kelimelerin toplamı, aya bölünmüş), Google Keyword Planner, Türkiye.", "Average monthly search volume for January - August 2025 (sum of the category's keywords, divided by months), Google Keyword Planner, Turkey.", True),
             th("2026 aylık ort.", "2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama arama hacmi; aynı takvim aylarını kapsar.", "Average monthly search volume for January - August 2026; covers the same calendar months.", True),
             th("YoY", "YoY", "İki pencere arasındaki yüzde değişim; mevsimsellikten arındırılmıştır.", "Percentage change between the two windows; seasonally aligned.", True),
             th("Pay", "Share", "Kategorinin 2026 penceresindeki toplam hacim içindeki payı.", "The category's share of total volume in the 2026 window.", True)],
            [[kat(k), cell(K1[k]["n"]), cell(K1[k]["a25"]), cell(K1[k]["a26"]), n(yz(K1[k]["yoy"])), n(yzd(100 * K1[k]["a26"] / TOP["a26"]))] for k in sira] +
            [["<b>%s</b>" % kat("Toplam"), n("<b>%s</b>" % bin(TOP["n"])), n("<b>%s</b>" % bin(TOP["a25"])), n("<b>%s</b>" % bin(TOP["a26"])), n(yz(toplam_yoy)), n("%100")]])
def k2rows(liste):
    out = []
    for key, a26, yoy in liste:
        k1, k2 = key.split("|"); v = K2[key]
        out.append([kat(k1), kat2(k2), cell(v["n"]), cell(v["a25"]), cell(a26), n(yz(yoy))])
    return out
bas2 = [th("Ana kategori", "Main category", "Alt kategorinin bağlı olduğu ana kategori.", "Main category the sub-category belongs to."),
        th("Alt kategori", "Sub-category", "VitrA kategori ağacındaki alt kategori.", "Sub-category in the VitrA category tree."),
        th("Kelime", "Keywords", "Alt kategoriye atanan kelime sayısı.", "Number of keywords assigned to the sub-category.", True),
        th("2025 aylık ort.", "2025 monthly avg.", "Ocak - Ağustos 2025 aylık ortalama arama hacmi.", "Average monthly search volume, January - August 2025.", True),
        th("2026 aylık ort.", "2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama arama hacmi.", "Average monthly search volume, January - August 2026.", True),
        th("YoY", "YoY", "İki pencere arasındaki yüzde değişim. Tabloya aylık 3.000 ve üzeri hacimli alt kategoriler alınmıştır.", "Percentage change between the two windows. Sub-categories with monthly volume of 3,000 and above are listed.", True)]
kloz = K2["Vitrifiyeler|Klozetler"]; bm = K1["Banyo Mobilyaları"]; ld = K2["Banyo Mobilyaları|Lavabo Dolapları"]; bk = K2["Karo Seramik Ürünleri|Banyo Karo Seramikleri"]
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
%s
%s
<h3>%s</h3>
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
%s
""" % (
 x("Talep tabanı, VitrA kategori ağacına eşlenmiş 2.420 arama kelimesidir; hacimler Google Keyword Planner'dan Eylül 2024 - Ağustos 2026 dönemi için aylık olarak alınmıştır. Karşılaştırma, aynı takvim aylarını kapsayan Ocak - Ağustos pencereleri üzerinden yapılmaktadır.",
   "The demand base is 2,420 search keywords mapped to the VitrA category tree; volumes were taken monthly from Google Keyword Planner for September 2024 - August 2026. The comparison uses January - August windows that cover the same calendar months."),
 kpi_kart(k(TOP["a26"]), "Aylık ortalama arama · 2026 (Oca-Ağu), 2.420 kelime", "Average monthly searches · 2026 (Jan-Aug), 2,420 keywords"),
 kpi_kart(yz(toplam_yoy), "Toplam talep değişimi · 2026 / 2025, aynı aylar", "Total demand change · 2026 / 2025, same months", "dn"),
 kpi_kart(yz(kloz["yoy"]), "Klozetler · en büyük alt kategoride büyüme", "WCs · growth in the largest sub-category", "up"),
 kpi_kart(yz(bm["yoy"]), "Banyo Mobilyaları · en büyük kategoride daralma", "Bathroom Furniture · contraction in the largest category", "dn"),
 GRAFIK,
 insight("2.420 kelimenin toplam talebi 2026'nın ilk sekiz ayında bir önceki yılın aynı dönemine göre %s daralmıştır. Aylık seri, Mart - Mayıs bahar tepesinin 2026'da 2025'e göre daha düşük kaldığını; Haziran - Ağustos yaz döneminde ise farkın kapanmaya başladığını göstermektedir. Daralma kategori genelinde bir performans kaybı değil, makro ortamla (Bölüm [[b:makro]]) uyumlu bir talep ertelemesi olarak okunabilir." % yz(toplam_yoy),
         "Total demand for the 2,420 keywords contracted %s in the first eight months of 2026 compared with the same period a year earlier. The monthly series shows the March - May spring peak stayed lower in 2026 than in 2025, while the gap started to close in the June - August summer period. The contraction can be read as a demand deferral consistent with the macro environment (Section [[b:makro]]) rather than a category-wide loss of performance." % yz(toplam_yoy), "D1", "D11"),
 x("Ana kategori düzeyinde değişim", "Change at main category level"),
 tbl, BAR,
 x("Kategorilerin aylık seyri", "Monthly course of the categories"),
 GRAFIK_K,
 insight("Sekiz ana kategorinin tamamı yatay veya negatif seyretmektedir; en dayanıklı kategoriler Karo Seramik (%s), Rezervuarlar (%s) ve Vitrifiyeler (%s), en belirgin daralma ise Banyo Mobilyaları (%s), Duşlar (%s) ve Banyo Aksesuarlarındadır (%s). Vitrifiyeler içinde Klozetler alt kategorisinin %s büyümesi dikkat çekmektedir: klozet, yenileme ertelense bile arıza ve değişim ihtiyacı nedeniyle talebi süren \"zorunlu\" ürün grubudur. Banyo mobilyası ise ertelenebilir, tasarım odaklı ve yüksek sepetli bir karar olduğundan daralmanın merkezindedir." % (yz(K1["Karo Seramik Ürünleri"]["yoy"]), yz(K1["Rezervuarlar"]["yoy"]), yz(K1["Vitrifiyeler"]["yoy"]), yz(bm["yoy"]), yz(K1["Duşlar"]["yoy"]), yz(K1["Banyo Aksesuarları"]["yoy"]), yz(kloz["yoy"])),
         "All eight main categories are flat or negative; the most resilient are Ceramic Tiles (%s), Cisterns (%s) and Sanitaryware (%s), while the sharpest contraction is in Bathroom Furniture (%s), Showers (%s) and Bathroom Accessories (%s). Within Sanitaryware the %s growth of the WCs sub-category stands out: the WC is the \"must-have\" product group whose demand continues through breakdown and replacement needs even when renovation is postponed. Bathroom furniture, a deferrable, design-led and high-basket decision, sits at the centre of the contraction." % (yz(K1["Karo Seramik Ürünleri"]["yoy"]), yz(K1["Rezervuarlar"]["yoy"]), yz(K1["Vitrifiyeler"]["yoy"]), yz(bm["yoy"]), yz(K1["Duşlar"]["yoy"]), yz(K1["Banyo Aksesuarları"]["yoy"]), yz(kloz["yoy"])), "D1"),
 x("Büyüyen alt kategoriler", "Growing sub-categories"), tablo(bas2, k2rows(A["k2_yukselen"]), "dar"),
 x("Daralan alt kategoriler", "Contracting sub-categories"), tablo(bas2, k2rows(A["k2_dusen"]), "dar"),
 insight("Büyüyen alt kategoriler üç örüntü taşımaktadır: (1) zorunlu değişim ürünleri (Klozetler %s), (2) dış mekan ve banyo karosu gibi tadilatın görünür yüzeyleri (Balkon-Teras Karoları %s, Banyo Karoları %s), (3) tezgah ve duş kanalı gibi tamamlayıcı ürünler. Daralan tarafta ise Lavabo Dolapları (%s), Banyo Aynaları (%s) ve Aksesuar Setleri (%s) gibi \"mobilya ve estetik\" ürünler yer almaktadır. E-ticaret kanalı için bu ayrım, kampanya ve set kurgusunun hangi kategoride talebi yakalayacağını göstermektedir: klozet ve rezervuar tarafında talep hazırdır; mobilya tarafında talebin kampanya ve içerikle oluşturulması gerekmektedir." % (yz(kloz["yoy"]), yz(K2["Karo Seramik Ürünleri|Balkon, Teras & Bahçe Karo Seramikleri"]["yoy"]), yz(bk["yoy"]), yz(ld["yoy"]), yz(K2["Banyo Mobilyaları|Banyo Aynaları"]["yoy"]), yz(K2["Banyo Aksesuarları|Banyo Aksesuar Setleri"]["yoy"])),
         "The growing sub-categories carry three patterns: (1) mandatory replacement products (WCs %s), (2) the visible surfaces of a refit such as outdoor and bathroom tiles (Balcony-Terrace Tiles %s, Bathroom Tiles %s), (3) complementary products such as countertops and shower channels. On the contracting side sit \"furniture and aesthetics\" products such as Washbasin Units (%s), Bathroom Mirrors (%s) and Accessory Sets (%s). For the e-commerce channel this distinction shows where campaign and set design will capture demand: on the WC and cistern side demand is ready; on the furniture side demand needs to be created through campaigns and content." % (yz(kloz["yoy"]), yz(K2["Karo Seramik Ürünleri|Balkon, Teras & Bahçe Karo Seramikleri"]["yoy"]), yz(bk["yoy"]), yz(ld["yoy"]), yz(K2["Banyo Mobilyaları|Banyo Aynaları"]["yoy"]), yz(K2["Banyo Aksesuarları|Banyo Aksesuar Setleri"]["yoy"])), "D1"),
 kaynak("Google Ads Keyword Planner · Türkiye, Türkçe · 2.420 kelime · aylık hacim Eyl 2024 - Ağu 2026 · kategori eşlemesi Inbound kelime araştırması (2025)",
        "Google Ads Keyword Planner · Turkey, Turkish · 2,420 keywords · monthly volume Sep 2024 - Aug 2026 · category mapping from Inbound keyword research (2025)", "D1", "D11"),
)
