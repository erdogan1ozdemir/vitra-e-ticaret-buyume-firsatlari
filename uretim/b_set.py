# -*- coding: utf-8 -*-
"""Bolum: Set, komple banyo ve urun + hizmet modelleri."""
from ortak import *
TM = YK["tema"]; NI = A["niyet"]
# VitrA hizmet kalemleri (vitra.com.tr, 29.09.2026)
HZL = [
 ("Klozet Montaj Hizmeti", "WC Installation Service", 2750, "Asma klozette kapak, ara musluk, kumanda paneli, bide bataryası ve sifon; takım klozette iç takım, kapak ve ara musluk dahil", "For wall-hung WCs the seat, stop valve, flush plate, bidet tap and siphon; for close-coupled WCs the inner mechanism, seat and stop valve included"),
 ("Gömme Rezervuar Montaj Hizmeti", "Concealed Cistern Installation Service", 3900, "Mevcut tesisatla aynı duvarda; kırım, tesisat malzemesi ve V-Care paneli kapsam dışı", "On the same wall as existing plumbing; breaking, plumbing materials and V-Care panels excluded"),
 ("Banyo Mobilyası Seti Montaj Hizmeti", "Bathroom Furniture Set Installation Service", 4000, "Lavabo dolabı, ayna, lavabo, batarya, sifon ve ara musluk; silikon dahil", "Basin unit, mirror, basin, tap, siphon and stop valves; silicone included"),
 ("Lavabo Montaj Hizmeti", "Washbasin Installation Service", 2300, "Batarya, sifon, ara musluk ve gerekli elektrik bağlantısı dahil", "Tap, siphon, stop valves and required electrical connection included"),
 ("Armatür ve Duş Sistemleri Montaj Hizmeti", "Tap and Shower System Installation Service", 2350, "Ara musluk dahil; duş sistemine banyo bataryası dahil değil", "Stop valves included; bath tap not included with shower systems"),
 ("Diğer Banyo Mobilyaları Montaj Hizmeti", "Other Bathroom Furniture Installation Service", 2000, "Ayna ve boy dolabı; aydınlatmalı aynada mevcut hatta elektrik bağlantısı dahil", "Mirrors and tall cabinets; electrical connection to the existing line included for lit mirrors"),
 ("Büyük / Orta / Küçük Montaj Hizmeti", "Large / Medium / Small Installation Service", None, "5.300 / 2.200 / 1.150 TL; büyükte kum, çimento ve sifon dahil, kırım ve seramik hariç", "5,300 / 2,200 / 1,150 TL; sand, cement and siphon included in large, breaking and tiling excluded"),
 ("Akıllı Klozet / Akıllı Panel Montaj Hizmeti", "Smart WC / Smart Panel Installation Service", None, "2.212,5 / 937,5 TL", "2,212.5 / 937.5 TL"),
 ("Keşif Hizmeti", "Site Survey Service", 1400, "Ölçü, su, gider ve elektrik altyapısının ürüne uygunluğu; aynı adreste en fazla 2 banyo; rölöve, kırım ve seramik işçiliği hariç", "Suitability of dimensions, water, drain and electrical infrastructure for the product; up to 2 bathrooms at the same address; survey drawings, breaking and tiling excluded"),
]
rows = [[x(a, b), n(bin(p)) if p else n(x(c.split(";")[0], d.split(";")[0])), x(c, d) if p else x(c.split("; ", 1)[-1] if "; " in c else "-", d.split("; ", 1)[-1] if "; " in d else "-")] for a, b, p, c, d in HZL]
tbl = tablo([th("Hizmet", "Service", "vitra.com.tr'de ürün olarak satılan hizmet kalemi.", "Service item sold as a product on vitra.com.tr."),
             th("Fiyat (TL)", "Price (TL)", "29.09.2026 itibarıyla sitedeki fiyat.", "Price on the site as of 29.09.2026.", True),
             th("Kapsam", "Scope", "Hizmet sayfasındaki kapsam açıklamasının özeti. Tüm montajlarda eski ürünün sökümü ve imhası dahil, 1 yıl servis garantisi; ilave tesisat malzemesi ve silikon ayrıca ücretlendirilir.", "Summary of the scope on the service page. All installations include removal and disposal of the old product and a 1-year service warranty; extra plumbing materials and silicone are charged separately.")], rows)
VAR = marks([
 ("up", "11 montaj kalemi ve keşif hizmeti ürün olarak satılıyor; ürün sayfasında \"Montaj Hizmeti (+2.750 TL)\" seçeneği ve montaj bilgileri bulunuyor", "11 installation items and a site survey service are sold as products; the product page carries an \"Installation Service (+2,750 TL)\" option and installation information"),
 ("up", "Montajda eski ürünün sökümü ve imhası dahil; Koçtaş'ta söküm ek ücretli", "Removal and disposal of the old product are included; at Koçtaş removal is charged extra"),
 ("up", "\"Ücretsiz Montaj\" rozetli 92 banyo mobilyası ürünü", "92 bathroom furniture products with a \"Free Installation\" badge"),
 ("up", "\"Banyomu Yenilemek İstiyorum\" (VitrA Banyo Asistanı): kategori sayfalarında yüzen düğme; 4 adımda ihtiyaç, fotoğraf, telefon / mağaza / görüntülü görüşme, randevu saati ve WhatsApp teyidi; %40'a varan indirim, 9 taksit ve ücretsiz mimari projelendirme vaadi", "\"I want to renovate my bathroom\" (VitrA Bathroom Assistant): a floating button on category pages; in 4 steps need, photo, phone / store / video call, appointment slot and WhatsApp confirmation; promise of up to 40% discount, 9 instalments and free architectural design"),
 ("up", "Set ürünleri: 29 banyo set modülü, 9 akıllı klozet seti, asma klozet setleri; akıllı klozet seti kategorisi 16 ayda %s organik tık" % bin(12338), "Set products: 29 bathroom set modules, 9 smart WC sets, wall-hung WC sets; the smart WC set category received %s organic clicks in 16 months" % f"{12338:,}"),
 ("at", "Duşakabin, küvet ve duş teknesi için ayrı montaj kalemi bulunmuyor; duşakabin ürün sayfasında montaj ya da keşif seçeneği görünmüyor", "There is no separate installation item for shower enclosures, bathtubs and shower trays; the shower enclosure product page shows no installation or survey option"),
 ("at", "Keşif hizmeti (1.400 TL) ölçüye bağlı ürünlerin sayfalarından önerilmiyor; Banyo Asistanı ile keşif hizmeti arasındaki bağlantı sayfada kurulmuyor", "The site survey service (1,400 TL) is not suggested from dimension-dependent product pages; the link between the Bathroom Assistant and the survey service is not made on the page"),
 ("at", "Banyo Asistanı mağaza ziyareti seçeneğinde 5 VitrA mağazası (İstanbul Suadiye, Ankara, İzmir, Adana, Samsun) listeleniyor; bayi ve yetkili servis ağı akışa dahil değil", "The Bathroom Assistant's store visit option lists 5 VitrA stores (Istanbul Suadiye, Ankara, Izmir, Adana, Samsun); the dealer and authorised service network is not part of the flow"),
 ("at", "Taksit mesajı kanala göre farklı: üst bantta \"vade farksız 6 ay\", Banyo Asistanı'nda \"9 taksit\"; kullanıcı \"vitra 9 taksit\" ve \"vitra taksit seçenekleri\" arıyor", "The instalment message differs by touchpoint: \"6 months interest-free\" in the top banner, \"9 instalments\" in the Bathroom Assistant; users search \"vitra 9 taksit\" and \"vitra taksit seçenekleri\""),
 ("at", "Ürün + montaj + keşif içeren tek fiyatlı \"banyo yenileme paketi\" bulunmuyor; montaj hizmetleri sayfası 16 ayda %s gösterime karşılık %s tık almış" % (k(95508), bin(810)), "There is no single-price \"bathroom renovation package\" combining product + installation + survey; the installation services page received %s clicks against %s impressions in 16 months" % (f"{810:,}", k(95508))),
])
t_set, t_tad, t_tas, t_mon, t_ilh = TM["set"], TM["tadilat"], TM["tasarim"], TM["montaj_hiz"], TM["ilham"]
RAK = tablo([th("Oyuncu", "Player", "İncelenen marka veya perakendeci.", "Brand or retailer examined."),
             th("Set ve paket", "Sets and bundles", "Ürünlerin birlikte sunulma biçimi.", "How products are offered together."),
             th("Hizmet", "Service", "Montaj, keşif ve tadilat hizmetleri.", "Installation, survey and renovation services."),
             th("VitrA ile fark", "Difference from VitrA", "VitrA'nın mevcut kurgusuna göre ayrışan nokta.", "Point of difference from VitrA's current setup.")],
            [[u("https://www.koctas.com.tr/banyo-tadilati", "Koçtaş"), x("\"Banyo Tadilatı\" sayfasında dolap, vitrifiye, seramik, yapı kimyasalı, tekstil, havlupan, termosifon ve el aletleri tek sayfada", "The \"Bathroom Renovation\" page gathers cabinets, sanitaryware, tiles, building chemicals, textiles, towel radiators, water heaters and hand tools on one page"),
              x("Ücretli montaj sepette, 2 yıl işçilik garantisi; söküm ek ücretli; anahtar teslim tadilat ve keşif mağazada; dönemsel ücretsiz söküm, nakliye ve montaj kampanyası (mağazaya özel)", "Paid installation in the basket, 2-year labour warranty; removal charged extra; turnkey renovation and survey in store; periodic free removal, delivery and installation campaign (store only)"),
              x("Tadilatın tamamını tek sayfada topluyor; VitrA'da tadilat hub'ı yok, garanti süresi VitrA'da 1 yıl", "Gathers the whole renovation on one page; VitrA has no renovation hub, and VitrA's warranty is 1 year")],
             [u("https://www.ikea.com.tr/odalar/banyo", "IKEA"), x("Hazır banyo setleri, 7 banyo serisi", "Ready bathroom sets, 7 bathroom series"), x("Ücretsiz online banyo planlayıcı; montaj en az 750 TL; 9 taksit ve 36 aya kadar alışveriş kredisi", "Free online bathroom planner; installation from 750 TL; 9 instalments and shopping credit up to 36 months"),
              x("Planlayıcı ve uzun vadeli finansman; VitrA'da planlayıcı adresi ana sayfaya yönleniyor", "Planner and long-term financing; VitrA's planner address redirects to the home page")],
             [u("https://www.hepsiburada.com/staticPage/12413", "Hepsiburada"), x("Pazaryeri ürünleri", "Marketplace products"), x("Kurulum hizmeti ürünle birlikte sepete ekleniyor, iş ortağı montaj firmasıyla", "Installation service added to the basket with the product, through a partner installation company"),
              x("Pazaryerinde de ürün + hizmet sepeti mümkün", "Product + service basket also possible on the marketplace")],
             [u("https://www.banyomarka.com/batarya-musluk-kombinleri", "Banyomarka"), x("Batarya ve musluk kombinleri (8 kombin), kampanyalı batarya ve ankastre setleri", "Tap and valve combinations (8 bundles), campaign tap and concealed sets"), x("WhatsApp destek hattı", "WhatsApp support line"),
              x("Çok markalı kombin; VitrA'da kombin koleksiyon düzeyinde değil", "Multi-brand bundles; at VitrA bundles are not built at collection level")],
             [veri_m("İDEVİT (Trendyol)"), x("\"Tam takım klozet\": klozet, rezervuar, kapak, 2 taharet musluğu, 2 esnek hortum, iç takım ve taharet çubuğu tek pakette, 7.370 TL", "\"Complete WC set\": WC, cistern, seat, 2 bidet valves, 2 flexible hoses, inner mechanism and bidet rod in one package, 7,370 TL"), "-",
              x("Montaj parçalarını pakete dahil ediyor; kullanıcının eksik parça için yapı markete gitmesini önlüyor", "Includes fitting parts in the package; prevents the user from going to a DIY store for missing parts")],
             [u("https://www.bauhaus.info/service/leistungen/montageservice/komplettbad", "BAUHAUS (Almanya)"), x("\"Komplettbad\": planlama, ürün, söküm, tesisat, seramik ve montaj tek sabit fiyatta, 10.000 EUR üzeri projeler", "\"Komplettbad\": planning, products, removal, plumbing, tiling and installation at one fixed price, projects over EUR 10,000"),
              x("Proje koordinatörü, tüm banyo için garanti, 20 yılda 40.000'den fazla banyo", "Project coordinator, warranty for the whole bathroom, over 40,000 bathrooms in 20 years"), x("Komple banyo sabit fiyatla satılıyor", "The complete bathroom is sold at a fixed price")],
             [u("https://www.homedepot.com/services/c/bathroom-remodel/d9843b7cb", "Home Depot (ABD)"), x("Banyo yenileme hizmeti", "Bathroom remodel service"), x("Ücretsiz evde danışmanlık, lisanslı yerel uygulayıcılar, 55.000 USD'ye kadar proje kredisi", "Free in-home consultation, licensed local installers, project loans up to USD 55,000"),
              x("Evde ücretsiz keşif ve proje finansmanı", "Free in-home survey and project financing")],
             [u("https://reveal.kohler.com/en", "Kohler Reveal (ABD)"), x("Duş ve küvet dönüşümü paketi", "Shower and bath conversion package"), x("Bir günde kurulum, yetkili bayi ağı, ömür boyu sınırlı garanti, finansman", "Installation in as little as a day, authorised dealer network, lifetime limited warranty, financing"),
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
 x("VitrA'nın bugün sunduğu set, montaj, keşif ve danışmanlık kurgusu site üzerinde incelenmiş; talep verisi ve rakip modelleriyle karşılaştırılmıştır.",
   "The set, installation, survey and consultation setup VitrA offers today has been examined on the site and compared with demand data and competitor models."),
 metric("Usta ve tesisatçı aramaları", "Installer and plumber searches", k(t_mon["v12"]), "Aylık ortalama; 3 yılda %s. Kullanıcı ürünle birlikte uygulayıcı da arıyor" % ("+" + yzd(t_mon["uc_yil"])), "Monthly average; %s over 3 years. Users search for an installer along with the product" % ("+" + yzd(t_mon["uc_yil"]).replace("%", "") + "%")),
 metric("Banyo tasarımı ve planlama", "Bathroom design and planning", k(t_tas["v12"]), "YoY %s; \"küçük banyo tasarımı\", \"3d banyo tasarım programı\"" % yz(t_tas["yoy"]), "YoY %s; \"küçük banyo tasarımı\", \"3d banyo tasarım programı\"" % yz(t_tas["yoy"])),
 metric("Banyo tadilatı ve yenileme", "Bathroom renovation", k(t_tad["v12"]), "YoY %s; \"6 metrekare banyo tadilat fiyatları\", \"koçtaş banyo tadilat fiyatları\"" % yz(t_tad["yoy"]), "YoY %s; \"6 metrekare banyo tadilat fiyatları\", \"koçtaş banyo tadilat fiyatları\"" % yz(t_tad["yoy"])),
 metric("Banyo seti ve takımı", "Bathroom sets", k(t_set["v12"]), "YoY %s; aramaların önemli kısmı aksesuar seti anlamında" % yz(t_set["yoy"]), "YoY %s; a large part of searches mean accessory sets" % yz(t_set["yoy"])),
 x("VitrA'nın mevcut hizmet kalemleri", "VitrA's current service items"),
 tbl,
 box("MEVCUT DURUM VE BOŞLUKLAR", "CURRENT STATE AND GAPS", VAR),
 x("Rakip ve benzer modeller", "Competitor and comparable models"),
 RAK,
 x("Değerlendirme", "Assessment"),
 insight("VitrA ürün + hizmet modelinin temel yapı taşlarına sahiptir: fiyatlı montaj kalemleri, keşif hizmeti, ücretsiz montajlı mobilya, randevulu Banyo Asistanı ve set ürünler. Bu yapı taşları ise birbirine bağlı bir teklif olarak değil, ayrı ürünler olarak sunulmaktadır. Talep tarafında \"banyo tadilatı\", \"banyo tasarım\" ve \"küçük banyo tasarımı\" gibi aramalar büyümekte (tasarım YoY %s, tadilat YoY %s), kullanıcı tadilat fiyatını metrekare üzerinden sormaktadır. Mevcut parçaların \"banyo yenileme paketi\" altında birleştirilmesi (ürün seti + montaj + keşif, küçük / orta banyo için gösterge fiyat) ve Banyo Asistanı'nın bu paketin giriş kapısı olarak konumlanması yeni bir yapı kurmadan uygulanabilir." % (yz(t_tas["yoy"]), yz(t_tad["yoy"])),
         "VitrA has the building blocks of a product + service model: priced installation items, a site survey service, furniture with free installation, the appointment-based Bathroom Assistant and set products. These building blocks, however, are offered as separate products rather than as one connected offer. On the demand side, searches such as \"banyo tadilatı\", \"banyo tasarım\" and \"küçük banyo tasarımı\" are growing (design YoY %s, renovation YoY %s), and users ask for renovation prices by square metre. Combining the existing pieces under a \"bathroom renovation package\" (product set + installation + survey, indicative price for small / medium bathrooms) and positioning the Bathroom Assistant as the entry point to that package can be implemented without building a new structure." % (yz(t_tas["yoy"]), yz(t_tad["yoy"])), "D12", "D13", "B1", "B2"),
 kaynak("vitra.com.tr hizmet ve ürün sayfaları (29.09.2026) · Google Search Console · Google Ads Keyword Planner · rakip siteler ve kampanya sayfaları", "vitra.com.tr service and product pages (29.09.2026) · Google Search Console · Google Ads Keyword Planner · competitor sites and campaign pages", "D13", "D2", "D12", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"),
)
