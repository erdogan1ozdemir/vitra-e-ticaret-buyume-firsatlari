# -*- coding: utf-8 -*-
"""Bolum: Set, komple banyo ve urun + hizmet modelleri."""
from ortak import *
import gsc12 as _G12
TM = YK["tema"]; NI = A["niyet"]
# VitrA hizmet kalemleri (vitra.com.tr, 29.09.2026)
HZL = [
 ("Klozet Montaj Hizmeti", "WC Installation Service", 2750, "Asma klozette kapak, ara musluk, kumanda paneli, bide bataryası ve sifon; takım klozette iç takım, kapak ve ara musluk dahil", "For wall-hung WCs the seat, stop valve, flush plate, bidet tap and siphon; for close-coupled WCs the inner mechanism, seat and stop valve included"),
 ("Gömme Rezervuar Montaj Hizmeti", "Concealed Cistern Installation Service", 3900, "Mevcut tesisatla aynı duvarda; kırım, tesisat malzemesi ve V-Care paneli kapsam dışı", "On the same wall as existing plumbing; demolition, plumbing materials and V-Care panels excluded"),
 ("Banyo Mobilyası Seti Montaj Hizmeti", "Bathroom Furniture Set Installation Service", 4000, "Lavabo dolabı, ayna, lavabo, batarya, sifon ve ara musluk; silikon dahil", "Basin unit, mirror, basin, tap, siphon and stop valves; silicone included"),
 ("Lavabo Montaj Hizmeti", "Washbasin Installation Service", 2300, "Batarya, sifon, ara musluk ve gerekli elektrik bağlantısı dahil", "Tap, siphon, stop valves and required electrical connection included"),
 ("Armatür ve Duş Sistemleri Montaj Hizmeti", "Tap and Shower System Installation Service", 2350, "Ara musluk dahil; duş sistemine banyo bataryası dahil değil", "Stop valves included; bath tap not included with shower systems"),
 ("Diğer Banyo Mobilyaları Montaj Hizmeti", "Other Bathroom Furniture Installation Service", 2000, "Ayna ve boy dolabı; aydınlatmalı aynada mevcut hatta elektrik bağlantısı dahil", "Mirrors and tall cabinets; electrical connection to the existing line included for lit mirrors"),
 ("Büyük / Orta / Küçük Montaj Hizmeti", "Large / Medium / Small Installation Service", None, "5.300 / 2.200 / 1.150; Büyük montajda kum, çimento ve sifon dahil, kırım ve seramik hariç", "5,300 / 2,200 / 1,150; Sand, cement and siphon included in the large service, demolition and tiling excluded"),
 ("Akıllı Klozet / Akıllı Panel Montaj Hizmeti", "Smart WC / Smart Panel Installation Service", None, "2.213 / 938; Akıllı klozet ve akıllı panel için ayrı kalem (kuruşlar yuvarlanmıştır)", "2,213 / 938; Separate items for smart WCs and smart panels (rounded to the lira)"),
 ("Keşif Hizmeti", "Site Survey Service", 1400, "Ölçü, su, gider ve elektrik altyapısının ürüne uygunluğu; aynı adreste en fazla 2 banyo; rölöve, kırım ve seramik işçiliği hariç", "Suitability of dimensions, water, drain and electrical infrastructure for the product; up to 2 bathrooms at the same address; survey drawings, demolition and tiling excluded"),
]
rows = [[x(a, b), n(bin(p)) if p else n(x(c.split(";")[0], d.split(";")[0])), x(c, d) if p else x(c.split("; ", 1)[-1] if "; " in c else "-", d.split("; ", 1)[-1] if "; " in d else "-")] for a, b, p, c, d in HZL]
tbl = tablo([th("Hizmet", "Service", "vitra.com.tr'de ürün olarak satılan hizmet kalemi.", "Service item sold as a product on vitra.com.tr."),
             th("Fiyat (TL)", "Price (TL)", "29.09.2026 itibarıyla sitedeki fiyat.", "Price on the site as of 29.09.2026.", True),
             th("Kapsam", "Scope", "Hizmet sayfasındaki kapsam açıklamasının özeti. Tüm montajlarda eski ürünün sökümü ve imhası dahil, 1 yıl servis garantisi; ilave tesisat malzemesi ve silikon ayrıca ücretlendirilir.", "Summary of the scope on the service page. All installations include removal and disposal of the old product and a 1-year service warranty; extra plumbing materials and silicone are charged separately.")], rows)
VAR = marks([
 ("up", "11 montaj kalemi ve keşif hizmeti ürün olarak satılmaktadır; ürün sayfasında \"Montaj Hizmeti (+2.750 TL)\" seçeneği ve montaj bilgileri bulunmaktadır", "11 installation items and a site survey service are sold as products; the product page carries an \"Installation Service (+2,750 TL)\" option and installation information"),
 ("up", "Montajda eski ürünün sökümü ve imhası dahildir; Koçtaş'ta söküm ek ücretlidir", "Removal and disposal of the old product are included; at Koçtaş removal is charged extra"),
 ("up", "Ücretsiz montaj listesinde 89 ürün bulunmaktadır: 61'i banyo mobilyası ve ayna, diğerleri temassız batarya, sabunluk, akıllı klozet ve duş teknesi; bunların 42'si stokta görünmemektedir", "The free-installation list includes 89 products: 61 bathroom furniture and mirrors, the rest touchless taps, soap dispensers, smart WCs and shower trays; 42 of them do not appear in stock"),
 ("up", "Set ürünleri arasında 29 banyo set modülü, 9 akıllı klozet seti ve asma klozet setleri bulunmaktadır; akıllı klozet seti kategorisi 1 Ekim 2025 - 30 Eylül 2026 döneminde %s organik tık almıştır" % bin(_G12.sayfa("/c-akilli-klozet-seti")[0]), "Set products include 29 bathroom set modules, 9 smart WC sets and wall-hung WC sets; the smart WC set category received %s organic clicks in 1 October 2025 - 30 September 2026" % f"{_G12.sayfa("/c-akilli-klozet-seti")[0]:,}"),
 ("up", "Üst bantta ve kampanya görselinde vade farksız 9 taksit yer almaktadır; ürün sayfasındaki taksit tablosunda vade farkıyla 12 taksite kadar seçenek bulunmaktadır. Üst banttaki mesaj, kullanıcının aradığı \"vitra 9 taksit\" ifadesiyle örtüşmektedir", "The top banner and the campaign visual show 9 interest-free instalments; the product page instalment table offers up to 12 instalments with interest. The banner message matches the \"vitra 9 taksit\" search users make"),
 ("at", "Duşakabin, küvet ve duş teknesi için ayrı montaj kalemi bulunmamaktadır; duşakabin ürün sayfasında montaj ya da keşif seçeneği görünmemektedir", "There is no separate installation item for shower enclosures, bathtubs and shower trays; the shower enclosure product page shows no installation or survey option"),
 ("at", "Keşif hizmeti (1.400 TL) ölçüye bağlı ürünlerin sayfalarından önerilmemektedir", "The site survey service (1,400 TL) is not suggested from dimension-dependent product pages"),
 ("at", "Yenileme ya da tasarım ihtiyacı olan kullanıcı için sitede ayrı bir talep veya randevu girişi bulunmamaktadır; keşif hizmeti ürün olarak satın alınabilmektedir", "The site has no separate request or appointment entry for users with a renovation or design need; the site survey service can be bought as a product"),
 ("at", "Ürün + montaj + keşif içeren tek fiyatlı \"banyo yenileme paketi\" bulunmamaktadır; montaj hizmetleri sayfası 1 Ekim 2025 - 30 Eylül 2026 döneminde %s gösterime karşılık %s tık almıştır" % (k(_G12.sayfa("/c-montaj-hizmeti")[1]), bin(_G12.sayfa("/c-montaj-hizmeti")[0])), "There is no single-price \"bathroom renovation package\" combining product + installation + survey; the installation services page received %s clicks against %s impressions in 1 October 2025 - 30 September 2026" % (f"{_G12.sayfa("/c-montaj-hizmeti")[0]:,}", k(_G12.sayfa("/c-montaj-hizmeti")[1]))),
])
t_set, t_tad, t_tas, t_mon, t_ilh = TM["set"], TM["tadilat"], TM["tasarim"], TM["montaj_hiz"], TM["ilham"]
def _mx(d):
    if d == "v": return '<span class="mx y">%s</span>' % x("✓", "✓")
    if d == "k": return x('<span class="badge b-kis">%s</span>' % x("Kısmi", "Partial"), '<span class="badge b-kis">Partial</span>')   # rozet bloğu da kaydedilir; aksi halde n() onu çevrilmeyen sayı olarak kaydeder
    return '<span class="mx n">-</span>'
_MXS = [("Set / paket", "Set / bundle", "Ürünlerin birlikte, set ya da paket olarak sunulması."), ("Montaj hizmeti", "Installation service", "Ürünle birlikte satın alınabilen montaj ya da kurulum hizmeti."),
        ("Keşif / danışmanlık", "Survey / consultation", "Evde ya da mağazada keşif, proje veya danışmanlık hizmeti."), ("Online planlayıcı", "Online planner", "Banyoyu çevrim içi tasarlama aracı."),
        ("Finansman", "Financing", "Uzun vadeli alışveriş ya da proje kredisi; yalnızca kart taksiti Kısmi olarak işaretlenmiştir."), ("Komple banyo / tadilat", "Full bathroom / renovation", "Ürün, işçilik ve tadilatın tek hizmet olarak sunulması.")]
_MXE = {"Set / paket": "Bundling products as a set or package.", "Montaj hizmeti": "Installation or fitting service purchasable with the product.", "Keşif / danışmanlık": "Survey, design or consultation service at home or in store.",
        "Online planlayıcı": "Online bathroom design tool.", "Finansman": "Long-term shopping or project credit; card instalments alone are marked Partial.", "Komple banyo / tadilat": "Product, labour and renovation offered as one service."}
_MXR = [("VitrA", "vvvnkn"), ("Koçtaş", "kvv-kv"), ("IKEA", "vv-vk-"), ("Hepsiburada", "-v--v-"), ("Banyomarka", "v-----"), ("İDEVİT (Trendyol)", "v-----"),
        ("Bauhaus (Almanya)", "vvv--v"), ("Home Depot (ABD)", "-vv-vv"), ("Kohler Reveal (ABD)", "vv--vk")]
x("Bauhaus (Almanya)", "Bauhaus (Germany)"); x("Home Depot (ABD)", "Home Depot (USA)"); x("Kohler Reveal (ABD)", "Kohler Reveal (USA)")
MATRIS = tablo([th("Oyuncu", "Player", "İncelenen marka veya perakendeci; ✓ incelemede gözlemlendi, - gözlemlenmedi.", "Brand or retailer examined; ✓ observed in the review, - not observed.")] +
               [th(a, b, c, _MXE[a], True) for a, b, c in _MXS],
               [[("<b>%s</b>" % x(o, o)) if o == "VitrA" else x(o, o) if "(" not in o else o] + [n(_mx(d)) for d in (dd if len(dd) == 6 else dd + "-" * (6 - len(dd)))] for o, dd in _MXR], "dar")
RAK = tablo([th("Oyuncu", "Player", "İncelenen marka veya perakendeci.", "Brand or retailer examined."),
             th("Set ve paket", "Sets and bundles", "Ürünlerin birlikte sunulma biçimi.", "How products are offered together."),
             th("Hizmet", "Service", "Montaj, keşif ve tadilat hizmetleri.", "Installation, survey and renovation services."),
             th("VitrA ile fark", "Difference from VitrA", "VitrA'nın mevcut kurgusuna göre ayrışan nokta.", "Point of difference from VitrA's current setup.")],
            [[u("https://www.koctas.com.tr/banyo-tadilati", "Koçtaş"), x("\"Banyo Tadilatı\" sayfasında dolap, vitrifiye, seramik, yapı kimyasalı, tekstil, havlupan, termosifon ve el aletleri tek sayfada", "The \"Bathroom Renovation\" page gathers cabinets, sanitaryware, tiles, building chemicals, textiles, towel radiators, water heaters and hand tools on one page"),
              x("Ücretli montaj sepette, 2 yıl işçilik garantisi; söküm ek ücretli; anahtar teslim tadilat ve keşif mağazada; dönemsel ücretsiz söküm, nakliye ve montaj kampanyası (mağazaya özel)", "Paid installation in the basket, 2-year labour warranty; removal charged extra; turnkey renovation and survey in store; periodic free removal, delivery and installation campaign (store only)"),
              x("Tadilatın tamamını tek sayfada topluyor; VitrA'da tadilat sayfası yok; montaj işçilik garantisi VitrA'da 1 yıl, Koçtaş'ta 2 yıl", "Gathers the whole renovation on one page; VitrA has no renovation page; the installation labour warranty is 1 year at VitrA and 2 years at Koçtaş")],
             [u("https://www.ikea.com.tr/odalar/banyo", "IKEA"), x("Hazır banyo setleri, 7 banyo serisi", "Ready-made bathroom sets, 7 bathroom series"), x("Ücretsiz online banyo planlayıcı; montaj en az 750 TL; IKEA Aile üyelerine belirli tutarın üzerinde vade farksız 9 taksit", "Free online bathroom planner; installation from 750 TL; 9 interest-free instalments above a set amount for IKEA Family members"),
              x("Planlayıcı ve üyeye özel taksit; VitrA'da planlayıcı adresi ana sayfaya yönleniyor", "Planner and member-only instalments; VitrA's planner address redirects to the home page")],
             [u("https://www.hepsiburada.com/staticPage/12413", "Hepsiburada"), x("Pazaryeri ürünleri", "Marketplace products"), x("Kurulum hizmeti ürünle birlikte sepete ekleniyor, iş ortağı montaj firmasıyla", "Installation service added to the basket with the product, through a partner installation company"),
              x("Pazaryerinde de ürün + hizmet sepeti mümkün", "Product + service basket also possible on the marketplace")],
             [u("https://www.banyomarka.com/batarya-musluk-kombinleri", "Banyomarka"), x("Batarya ve musluk kombinleri (8 kombin), kampanyalı batarya ve ankastre setleri", "Tap and valve combinations (8 bundles), promotional tap and concealed-valve sets"), x("WhatsApp destek hattı", "WhatsApp support line"),
              x("Çok markalı kombin; VitrA'da kombin koleksiyon düzeyinde değil", "Multi-brand bundles; at VitrA bundles are not built at collection level")],
             [veri_m("İDEVİT (Trendyol)"), x("\"Tam takım klozet\": klozet, rezervuar, kapak, 2 taharet musluğu, 2 esnek hortum, iç takım ve taharet çubuğu tek pakette, 7.370 TL", "\"Complete WC set\": WC, cistern, seat, 2 bidet valves, 2 flexible hoses, inner mechanism and bidet rod in one package, 7,370 TL"), "-",
              x("Montaj parçalarını pakete dahil ediyor; kullanıcının eksik parça için yapı markete gitmesini önlüyor", "Includes fitting parts in the package; prevents the user from going to a DIY store for missing parts")],
             [u("https://www.bauhaus.info/service/leistungen/montageservice/komplettbad", "Bauhaus") + x(" (Almanya)", " (Germany)"), x("\"Komplettbad\" (komple banyo): planlama, ürün, söküm, tesisat, seramik ve montaj tek sabit fiyatta, 10.000 EUR üzeri projeler", "\"Komplettbad\" (complete bathroom): planning, products, removal, plumbing, tiling and installation at one fixed price, projects over EUR 10,000"),
              x("Proje koordinatörü, tüm banyo için garanti, 20 yılda 40.000'den fazla banyo", "Project coordinator, warranty for the whole bathroom, over 40,000 bathrooms in 20 years"), x("Komple banyo sabit fiyatla satılıyor", "The complete bathroom is sold at a fixed price")],
             [u("https://www.homedepot.com/services/c/bathroom-remodel/d9843b7cb", "Home Depot") + x(" (ABD)", " (US)"), x("Banyo yenileme hizmeti", "Bathroom remodel service"), x("Ücretsiz evde danışmanlık, lisanslı yerel uygulayıcılar, 55.000 USD'ye kadar proje kredisi", "Free in-home consultation, licensed local installers, project loans up to USD 55,000"),
              x("Evde ücretsiz keşif ve proje finansmanı", "Free in-home survey and project financing")],
             [u("https://reveal.kohler.com/en", "Kohler Reveal") + x(" (ABD)", " (US)"), x("Duş ve küvet dönüşümü paketi", "Shower and bath conversion package"), x("Bir günde kurulum, yetkili bayi ağı, ömür boyu sınırlı garanti, finansman", "Installation in as little as a day, authorised dealer network, lifetime limited warranty, financing"),
              x("Üretici markanın bayi ağıyla hizmet paketi satması", "A manufacturer brand selling a service package through its dealer network")]], "uzun")
HTML = """
<p class="lede">%s</p>
<div class="metrics">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
<h3>%s</h3>
%s
%s
""" % (
 x("VitrA'nın bugün sunduğu set, montaj ve keşif kurgusu site üzerinde incelenmiş; talep verisi ve rakip modelleriyle karşılaştırılmıştır.",
   "The set, installation and survey setup VitrA offers today has been examined on the site and compared with demand data and competitor models."),
 metric("Usta ve tesisatçı aramaları", "Installer and plumber searches", k(t_mon["v12"]), "Aylık ortalama, Eyl 2025 - Ağu 2026; 3 yılda %s" % ("+" + yzd(t_mon["uc_yil"])), "Monthly average, Sep 2025 - Aug 2026; %s over 3 years" % ("+" + yzd(t_mon["uc_yil"]).replace("%", "") + "%")),
 metric("Banyo tasarımı ve planlama", "Bathroom design and planning", k(t_tas["v12"]), "Tasarım ve planlama teması, YoY %s; \"küçük banyo tasarımı\", \"3d banyo tasarım programı\"" % yz(t_tas["yoy"]), "Design and planning theme, YoY %s; \"küçük banyo tasarımı\", \"3d banyo tasarım programı\"" % yz(t_tas["yoy"])),
 metric("Banyo tadilatı ve yenileme", "Bathroom renovation", k(t_tad["v12"]), "YoY %s; \"6 metrekare banyo tadilat fiyatları\", \"koçtaş banyo tadilat fiyatları\"" % yz(t_tad["yoy"]), "YoY %s; \"6 metrekare banyo tadilat fiyatları\", \"koçtaş banyo tadilat fiyatları\"" % yz(t_tad["yoy"])),
 metric("Banyo seti ve takımı", "Bathroom sets", k(t_set["v12"]), "YoY %s; aramaların önemli kısmı aksesuar seti anlamında" % yz(t_set["yoy"]), "YoY %s; a large part of searches mean accessory sets" % yz(t_set["yoy"])),
 x("VitrA'nın mevcut hizmet kalemleri", "VitrA's current service items"),
 tbl,
 box("MEVCUT DURUM VE BOŞLUKLAR", "CURRENT STATE AND GAPS", VAR),
 x("Rakip ve benzer modeller", "Competitor and comparable models"),
 MATRIS + RAK,
 x("Değerlendirme", "Assessment"),
 insight("VitrA ürün + hizmet modelinin temel yapı taşlarına sahiptir: fiyatlı montaj kalemleri, keşif hizmeti, ücretsiz montajlı mobilya ve set ürünler. Bu yapı taşları ise birbirine bağlı bir teklif olarak değil, ayrı ürünler olarak sunulmaktadır. Talep tarafında \"banyo tadilatı\", \"banyo tasarım\" ve \"küçük banyo tasarımı\" gibi aramalar büyümekte (tasarım ve planlama teması YoY %s, tadilat teması YoY %s), aramaların bir bölümü tadilat fiyatını metrekare üzerinden sormaktadır. Mevcut parçaların \"banyo yenileme paketi\" altında birleştirilmesi (ürün seti + montaj + keşif, küçük / orta banyo için gösterge fiyat) büyük ölçüde mevcut kalemlerle kurgulanabilir; paketin girişinde ihtiyaç, ölçü ve fotoğrafın alındığı bir talep adımı, keşif ve montaj hizmetlerini aynı akışa bağlayabilir." % (yz(t_tas["yoy"]), yz(t_tad["yoy"])),
         "VitrA has the building blocks of a product + service model: priced installation items, a site survey service, furniture with free installation and set products. These building blocks, however, are offered as separate products rather than as one connected offer. On the demand side, searches such as \"banyo tadilatı\", \"banyo tasarım\" and \"küçük banyo tasarımı\" are growing (design and planning theme YoY %s, renovation theme YoY %s), and part of the searches ask for renovation prices by square metre. Combining the existing pieces under a \"bathroom renovation package\" (product set + installation + survey, indicative price for small / medium bathrooms) can largely be set up with existing items; a request step at the entry of the package, collecting the need, dimensions and photos, can connect the survey and installation services in one flow." % (yz(t_tas["yoy"]), yz(t_tad["yoy"])), "D12", "D13", "B1", "B2"),
 kaynak("vitra.com.tr hizmet ve ürün sayfaları (29.09.2026) · Google Search Console · Google Ads Keyword Planner · rakip siteler ve kampanya sayfaları", "vitra.com.tr service and product pages (29.09.2026) · Google Search Console · Google Ads Keyword Planner · competitor sites and campaign pages", "D13", "D2", "D12", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"),
)
