# -*- coding: utf-8 -*-
"""Bolum: vitra.com.tr satin alma yolculugu - kesiften odemeye adimlar, site ici arama testi, sepet ve uyeliksiz alisveris akisi, donusum firsatlari."""
from ortak import *
import json, os, re, base64, urllib.parse
import serp_ozet as _SO
import b_derin2 as _D2

_K = os.path.join(veri.V, "ham", "derin")
SA = json.load(open(os.path.join(_K, "site_arama", "sonuc.json"), encoding="utf-8"))["sorgular"]
KS = {r["kw"]: r for r in json.load(open(os.path.join(veri.V, "islenmis", "kelime_seti.json"), encoding="utf-8"))}
AIG = json.load(open(os.path.join(veri.V, "ham", "geo", "ai_gorunurluk.json"), encoding="utf-8"))
YA = json.load(open(os.path.join(veri.V, "islenmis", "yorum_analiz.json"), encoding="utf-8"))


def _img(ad):
    return "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(_K, "sepet_akisi", ad), "rb").read()).decode()


# ---------------------------------------------------------------- site ici arama testi (iki yol: anlik sonuc katmani ve Enter sonrasi sonuc sayfasi)
GRUP_EN = {"Kategori": "Category", "Yedek parça ve aksesuar": "Spare parts and accessories", "Yazım farkı": "Spelling variant", "Ölçü ve özellik": "Size and feature",
           "Seri ve ürün kodu": "Series and product code", "Hizmet ve destek": "Service and support"}
for a, b in GRUP_EN.items(): x(a, b)
KAT = json.load(open(os.path.join(_K, "site_arama", "katman.json"), encoding="utf-8"))["sonuc"]
# degerlendirme kurali (04.10.2026): her yolda ilk uc kartin en az ikisi aranan urun tipindeyse o yol uyumlu sayilir; sonuc sayisi 0 ise bos
DEG = {"U": ("Uyumlu", "Consistent"), "T": ("Anlık sonuç uyumlu, sonuç sayfası boş veya ilgisiz", "Instant results fine, results page empty or off-target"),
       "S": ("Anlık sonuç boş ya da ilgisiz, sonuç sayfası uyumlu", "Instant results empty or off-target, results page fine"), "Y": ("İki yolda da ilgili ürün yok", "No relevant product on either path"),
       "D": ("Destek sayfasına yönlendirme yok", "No route to the support page"), "P": ("Kısmen uyumlu: ilk kartlar karışık", "Partly consistent: mixed first cards"), "G": ("VitrA gamı dışında", "Outside VitrA's range")}
DEGK = {"klozet": "P", "asma klozet": "U", "lavabo": "T", "banyo dolabı": "U", "duşakabin": "U", "banyo bataryası": "U", "gömme rezervuar": "P", "havlupan": "P", "evye": "G",
        "duş seti": "U", "klozet kapağı": "U", "iç takım": "U", "rezervuar iç takımı": "P", "şamandıra": "T", "klozet kapağı menteşesi": "S", "kartuş": "Y", "conta": "Y",
        "kumanda paneli": "U", "taharet musluğu": "S", "lavabo sifonu": "U", "klozet kapagi": "P", "dusakabin": "T", "banyo dolabi": "T", "rezarvuar": "T", "klozed": "T",
        "batarya": "T", "80 cm banyo dolabı": "S", "kanalsız klozet": "P", "akıllı klozet": "P", "siyah klozet": "P", "metropole": "U", "sento": "U", "integra": "T",
        "7906B483-0090": "T", "montaj": "U", "yedek parça": "Y", "garanti": "D", "servis": "D"}
assert set(DEGK) == {r["sorgu"] for r in SA}, "degerlendirmesi olmayan arama"
for a, b in DEG.values(): x(a, b)
SAY = {k_: sum(1 for v_ in DEGK.values() if v_ == k_) for k_ in DEG}
_SA = {r["sorgu"]: r for r in SA}


def _hacim(q):
    v = (_SO.KP.get(q) or {}).get("ort12") or (KS.get(q) or {}).get("a26")
    return round(v) if v else None


def _kart(ad):
    return x(ad, __import__("t2_ortak").EK.get(ad, ad)) if ad else x("Ürün bulunamadı", "No product found")


def _sayi(v): return cell(v) if v else n('<span class="dn">0</span>')


T_ARA = tablo([th("Arama ifadesi", "Search phrase", "vitra.com.tr arama kutusuna yazılan ifade; bağlantı Enter sonrası açılan sonuç sayfasını yeni sekmede açar.", "The term typed into the vitra.com.tr search box; the link opens the results page shown after Enter in a new tab."),
               th("Grup", "Group", "Aramanın türü: kategori, yedek parça ve aksesuar, yazım farkı, ölçü ve özellik, seri ve ürün kodu, hizmet ve destek.", "Type of search: category, spare parts and accessories, spelling variant, size and feature, series and product code, service and support."),
               th("Anlık sonuç", "Instant results", "Arama kutusuna yazarken açılan sonuç katmanındaki sonuç sayısı (Chrome, 04.10.2026).", "Number of results in the layer that opens while typing in the search box (Chrome, 04.10.2026).", True),
               th("Anlık sonuçta ilk kart", "First card in instant results", "Sonuç katmanında ilk sıradaki ürün.", "The first product in the results layer."),
               th("Sonuç sayfası", "Results page", "Enter'a basıldığında açılan /search sayfasındaki sonuç sayısı.", "Number of results on the /search page that opens after pressing Enter.", True),
               th("Sonuç sayfasında ilk kart", "First card on results page", "Sonuç sayfasında ilk sıradaki ürün.", "The first product on the results page."),
               th("Değerlendirme", "Assessment", "Her yolda ilk üç kartın en az ikisi aranan ürün tipindeyse o yol uyumlu sayılmış, iki yolun sonucu birlikte sınıflanmıştır.", "A path counts as consistent when at least two of its first three cards are of the searched product type; the results of the two paths are classified together."),
               th("Google aylık hacim", "Google monthly volume", "Aynı ifadenin Google'daki ortalama aylık arama hacmi, Keyword Planner, Eyl 2025 - Ağu 2026 (bu dönem için ölçülmeyen ifadelerde Oca - Ağu 2026).", "Average monthly Google search volume of the same term, Keyword Planner, Sep 2025 - Aug 2026 (Jan - Aug 2026 for terms not measured in that period).", True)],
              [[u(r["url"], r["sorgu"]), etk(r["grup"], GRUP_EN[r["grup"]], "sa-" + r["grup"]),
                _sayi(KAT[r["sorgu"]]["sonuc"]), _kart((KAT[r["sorgu"]]["ilk"] or [None])[0]),
                _sayi(r["sonuc"]), (_kart(r["urunler"][0]["ad"]) if r["urunler"] else (n("-") if r["sonuc"] else _kart(None))),
                etk(*DEG[DEGK[r["sorgu"]]], "sd-" + DEGK[r["sorgu"]]), cell(_hacim(r["sorgu"])) if _hacim(r["sorgu"]) else n("-")] for r in SA], "uzun")
_ILG = SAY["U"] + SAY["T"]
# ---------------------------------------------------------------- yolculuk adimlari
_kirik_v, _kirik_r = YA["marka"]["VitrA"]["tema_neg"]["kirik"], YA["rakip"]["tema_neg"]["kirik"]
_stok = 100 * _D2.top_yok / _D2.top_kart
import b_geo as _BG
_q1 = _BG._Q["klozet nereden alınır en uygun fiyata"]; _q5 = _BG._Q["klozet montajı dahil satış yapan siteler"]
_q3 = next(r for r in AIG["klasor_soru"] if r[1] == "banyo ürünlerinde iade ve değişim nasıl yapılır online alışverişte")
ADIM = [
 (("Keşif: Google araması", "Discovery: Google search"),
  ("Ürün ve kategori aramalarında Trendyol %d kelimenin %s ilk 10'da; vitra.com.tr %d kelimede ilk 10'da" % (_SO.N, ek(_SO.D10["trendyol.com"], "inde"), _SO.VITRA["ilk10"]),
   "Trendyol is in the top 10 for %d of %d product and category searches; vitra.com.tr is in the top 10 for %d" % (_SO.D10["trendyol.com"], _SO.N, _SO.VITRA["ilk10"])),
  ("Kullanıcının ilk temas ettiği ürün listesi çoğunlukla pazaryerinde", "The first product list the user sees is mostly on a marketplace"),
  ("Kategori sayfalarında kullanıcı dilindeki soruların (ölçü, montaj, fiyat) yanıtlanması", "Answering the user's questions (size, installation, price) on category pages"), "A · Kim sıralanıyor?"),
 (("Keşif: yapay zeka yanıtı", "Discovery: AI answer"),
  ("\"klozet nereden alınır en uygun fiyata\" sorusunda pazaryeri kaynakları %d yanıtın %s yer alıyor; iade ve değişim sorusunda VitrA %d yanıtın %s geçiyor; montaj dahil satış sorusunda ise vitra.com.tr %d yanıtın %s kaynak" % (_q1["yanit"], ek(_q1["pazaryeri_kaynak"], "inde"), _q3[3], ek(_q3[4], "inde"), _q5["yanit"], ek(_q5["vitra_kaynak"], "inde")),
   "For \"klozet nereden alınır en uygun fiyata\" marketplace sources appear in %d of %d answers; for the returns question VitrA is named in %d of %d answers; for the question on sales including installation vitra.com.tr is cited in %d of %d answers" % (_q1["pazaryeri_kaynak"], _q1["yanit"], _q3[4], _q3[3], _q5["vitra_kaynak"], _q5["yanit"])),
  ("Satın almaya yakın sorularda yanıt çoğunlukla pazaryerlerini kaynak gösteriyor; montaj sorusu VitrA lehine", "In questions close to purchase the answer mostly cites marketplaces; the installation question favours VitrA"),
  ("Teslimat, iade, kurulum ve satın alma koşullarının vitra.com.tr'de soru-cevap biçiminde yer alması", "Presenting delivery, returns, installation and purchase terms on vitra.com.tr as questions and answers"), "Yapay zeka yanıt takibi · 29 satın alma ve montaj sorusunda VitrA ve vitra.com.tr"),
 (("Kategori sayfası", "Category page"),
  ("%s varyant kartının %s stoklu süzgecinin dışında; %d alt kesitte stoklu ürün yok" % (bin(_D2.top_kart), yzd(_stok), len(_D2.sifir)),
   "%s of %s variant cards are outside the in-stock filter; %d sub-segments have no in-stock product" % (("%.1f" % _stok) + "%", f"{_D2.top_kart:,}", len(_D2.sifir))),
  ("Kullanıcı ürünü bulsa da satın alamıyor ve başka kanala geçebiliyor", "The user finds the product but cannot buy it and may move to another channel"),
  ("Stokta olmayan ürünlerin listede sona alınması, tahmini tedarik tarihi ya da yakın model önerisi", "Moving out-of-stock products to the end of lists, an estimated restock date or a close alternative"), "vitra.com.tr kategori sayfaları: ürün, fiyat aralığı ve stok"),
 (("Site içi arama", "Site search"),
  ("%d aramanın %s iki yol da uyumlu; %s anlık sonuç uyumluyken Enter sonrası sonuç sayfası boş ya da ilgisiz (şamandıra, dusakabin, batarya, ürün kodu), %s tersine anlık sonuç boşken sonuç sayfası ürün getiriyor; kartuş, conta, yedek parça, garanti ve servis aramalarında iki yolda da ilgili ürün ya da destek sayfası dönmüyor" % (len(SA), ek(SAY["U"], "inde"), ek(SAY["T"], "inde"), ek(SAY["S"], "inde")),
   "Both paths are consistent for %d of %d searches; for %d the instant results are fine but the results page after Enter is empty or off-target (float valve, dusakabin, taps, product code), and for %d the reverse holds; cartridge, seal, spare part, warranty and service searches return no relevant product or support page on either path" % (SAY["U"], len(SA), SAY["T"], SAY["S"])),
  ("Enter'a basan ya da parça adıyla arayan kullanıcı aradığını bulamayabiliyor", "Users who press Enter or search by part name may not find what they are looking for"),
  ("İki arama yolunun, her aramada daha isabetli sonuç veren yolun mantığıyla tekleştirilmesi; yedek parça ve destek ifadeleri için yönlendirme kuralları", "Aligning the two search paths on the logic of whichever path returns the more accurate result for each search; routing rules for spare-part and support terms"), "Site içi arama: kullanıcının yazdığı ifadeler ne döndürüyor?"),
 (("Ürün sayfası: fiyat", "Product page: price"),
  ("İncelenen 29 VitrA ürününün 19'unda en düşük fiyat vitra.com.tr'de değil, bir pazaryeri satıcısında", "For 19 of the 29 VitrA products reviewed, the lowest price is not on vitra.com.tr but at a marketplace seller"),
  ("Fiyat karşılaştıran kullanıcı satın almayı pazaryerinde tamamlayabiliyor", "A user comparing prices may complete the purchase on a marketplace"),
  ("Sepette uygulanan indirimin ürün sayfasında görünmesi; kanal fiyat politikasının gözden geçirilmesi", "Showing the in-cart discount on the product page; reviewing the channel price policy"), "VitrA ürünlerinde kanal fiyat farkı: 29 ürün"),
 (("Ürün sayfası: taksit ve garanti", "Product page: instalments and warranty"),
  ("Taksit bilgisi üç yüzeyde farklı biçimde yer alıyor (şeritte vade farksız 6 ay, kampanyada seçili ürünlerde 9, ürün tablosunda vade farklı dahil 12); ürün sayfalarında garanti süresi yer almıyor", "Instalment information appears differently on three surfaces (6 months interest-free in the banner, 9 on selected products in the campaign, up to 12 including interest-bearing options in the product table); product pages show no warranty period"),
  ("Ödeme koşulu ve güvence bilgisi karar anında belirsiz kalıyor", "Payment terms and assurance remain unclear at the point of decision"),
  ("Vade farksız ve vade farklı seçeneklerin ve kampanya kapsamının aynı ifadeyle gösterilmesi; garanti süresinin ürün sayfasında ve sepette gösterilmesi", "Showing interest-free and interest-bearing options and campaign scope in one consistent wording; showing the warranty period on the product page and in the cart"), "Ödeme ve taksit koşulları"),
 (("Sepet", "Cart"),
  ("Montaj hizmetleri ve \"VitrA'nın senin için seçtikleri\" alanları sepet listesinin ve sipariş özetinin altında; masaüstünde montaj kartları ekranın alt kenarında başlıyor", "The installation services and \"VitrA picks for you\" areas sit below the cart list and order summary; on desktop the installation cards start at the bottom edge of the screen"),
  ("Kaydırma yapmayan kullanıcı montaj hizmetini ve tamamlayıcı ürünleri görmüyor", "A user who does not scroll does not see the installation service or complementary products"),
  ("Karusellerin küçültülüp sepet listesinin hemen altına taşınması", "Making the carousels smaller and moving them directly below the cart list"), "Sepet ve ödeme: üyeliksiz alışverişte ek adımlar"),
 (("Ödeme", "Checkout"),
  ("Üyeliksiz alışverişte adres adımına gelmeden önce iki ara ekran ve üç tıklama gerekiyor", "Guest checkout needs two intermediate screens and three clicks before the address step"),
  ("Her ek ekran, ödeme adımına gelmeden çıkış ihtimalini artırabilir", "Each extra screen can increase the chance of leaving before payment"),
  ("Sepet özetinde e-posta veya telefon alanı ve \"Üye olmadan satın al\" butonu", "An e-mail or phone field and a \"Buy without an account\" button in the order summary"), "Sepet ve ödeme: üyeliksiz alışverişte ek adımlar"),
 (("Teslimat", "Delivery"),
  ("Pazaryerlerindeki olumsuz VitrA yorumlarının %s kırık, hasarlı veya kusurlu ürüne değiniyor (rakiplerde %s)" % (yzd_ek(_kirik_v, 1, "i"), yzd(_kirik_r)),
   "%s of negative VitrA reviews on marketplaces mention broken, damaged or defective products (%s for competitors)" % (("%.1f" % _kirik_v) + "%", ("%.1f" % _kirik_r) + "%")),
  ("Hasarlı teslimat iade ve olumsuz yorum olarak geri dönüyor", "Damaged deliveries come back as returns and negative reviews"),
  ("Kırılgan ürünlerde (dolap seti lavabosu, cam aksesuar, klozet kapağı) ambalaj ve teslimat kontrolü; teslimat koşullarının ürün sayfasında anlatılması", "Packaging and delivery checks for fragile products (cabinet set basins, glass accessories, toilet seats); explaining delivery terms on the product page"), "Pain point profili: kategori geneli mi, markaya özgü mü?"),
 (("Satış sonrası", "After-sales"),
  ("Şikayetvar'daki VitrA şikayetlerinin %76,9'u servis, yedek parça, montaj veya müşteri hizmetlerine ulaşma konularını içeriyor", "76.9% of VitrA complaints on Şikayetvar mention service, spare parts, installation or reaching customer service"),
  ("Satın alma sonrası deneyim bir sonraki satın almayı ve yorumları etkiliyor", "The after-purchase experience affects the next purchase and reviews"),
  ("Yedek parçanın sitede bulunabilir ve aranabilir olması; servis talebinin siteden açılabilmesi", "Making spare parts findable and searchable on the site; allowing service requests from the site"), "Şikayet temaları ve örnek alıntılar"),
]
T_YOL = tablo([th("Adım", "Step", "Kullanıcının keşiften satış sonrasına kadar geçtiği adım.", "The step the user passes through from discovery to after-sales."),
               th("Gözlem", "Observation", "Adımda ölçülen ya da gözlenen durum; ok simgesi ayrıntının yer aldığı alt başlığa gider.", "The measured or observed situation at the step; the arrow goes to the sub-heading with the detail."),
               th("Kullanıcıya etkisi", "Effect on the user", "Gözlemin satın alma yolculuğuna olası etkisi.", "Possible effect of the observation on the purchase journey."),
               th("Önerilen düzenleme", "Recommended change", "Adımdaki bariyeri azaltabilecek düzenleme.", "A change that may reduce the barrier at the step.")],
              [["<b>%s</b>" % x(*a), '<span class="mtx">%s</span>' % x(*g) + git(h), x(*e), x(*o)] for a, g, e, o, h in ADIM], "uzun")

# ---------------------------------------------------------------- sepet ve odeme ekranlari
x("Sepet ekranı", "Cart screen"); x("Giriş ekranı", "Sign-in screen"); x("Üyeliksiz alışveriş ekranı", "Guest checkout screen")
EKRAN = '<div class="ekranlar">%s</div>' % "".join(
    '<figure><span class="eno">%d</span><img src="%s" alt="%s" loading="lazy"><figcaption><b>%s</b> %s</figcaption></figure>' % (i, _img(f), x(a, ae), x(a, ae), x(c, ce))
    for i, (f, a, ae, c, ce) in enumerate([
        ("adim_16.jpg", "Sepet ekranı", "Cart screen", "\"Sepeti Onayla\" butonu sipariş özetinde. Montaj hizmetleri ekranın alt kenarında başlıyor, \"VitrA'nın senin için seçtikleri\" bunun da altında.",
         "The \"Confirm cart\" button is in the order summary. Installation services start at the bottom edge of the screen, \"VitrA picks for you\" further below."),
        ("adim_17.jpg", "Giriş ekranı", "Sign-in screen", "\"Sepeti Onayla\" sonrası giriş paneli açılıyor; üye olmadan devam seçeneği üçüncü sırada.",
         "After \"Confirm cart\" a sign-in panel opens; continuing without an account is the third option."),
        ("adim_18.jpg", "Üyeliksiz alışveriş ekranı", "Guest checkout screen", "Üye olmadan devam edildiğinde ayrı bir ekranda e-posta isteniyor; adres adımına \"Devam Et\" ile geçiliyor.",
         "Continuing without an account asks for an e-mail on a separate screen; the address step follows \"Continue\".")], 1))

AKIS = tablo([th("Adım", "Step", "Akıştaki adım sırası.", "Order of the step in the flow."),
              th("Mevcut akış", "Current flow", "04.10.2026 tarihinde masaüstünde gözlenen adımlar.", "Steps observed on desktop on 04.10.2026."),
              th("Önerilen akış", "Proposed flow", "Sepet özetinde tek adımda üyeliksiz satın alma; önerilen akış iki adımdır.", "Guest purchase in one step in the order summary; the proposed flow has two steps.")],
             [[x("1", "1"), x("Sepet: \"Sepeti Onayla\"", "Cart: \"Confirm cart\""), x("Sepet: \"Sepeti Onayla\" altında e-posta veya cep telefonu alanı ve alan doldurulunca etkinleşen \"Üye olmadan satın al\" butonu; üyeler için \"Giriş yap\" bağlantısı aynı alanda", "Cart: an e-mail or mobile phone field below \"Confirm cart\" and a \"Buy without an account\" button that activates once the field is filled; a \"Sign in\" link for members in the same area")],
              [x("2", "2"), x("Giriş paneli: Giriş Yap / Üye Ol / Üye Olmadan Devam Et", "Sign-in panel: Sign in / Register / Continue without an account"), x("Adres ve ödeme; mevcut \"satın alma sonrası hesap oluşturma\" seçeneği korunur", "Address and payment; the existing \"create an account after purchase\" option is kept")],
              [x("3", "3"), x("Üyeliksiz Alışveriş: e-posta alanı ve \"Devam Et\"", "Guest Checkout: e-mail field and \"Continue\""), n("-")],
              [x("4", "4"), x("Adres ve ödeme", "Address and payment"), n("-")]])

# ---------------------------------------------------------------- donusum firsatlari
OC = {"Öncelik 1": "b-o1", "Öncelik 2": "b-o2", "Öncelik 3": "b-o3"}; OE = {"Öncelik 1": "Priority 1", "Öncelik 2": "Priority 2", "Öncelik 3": "Priority 3"}
def _ob(o): return '<span class="badge %s">%s</span>' % (OC[o], x(o, OE[o]))
FIRSAT = [
 ("Öncelik 1", ("Üyeliksiz satın almanın sepette tek adıma indirilmesi", "Reducing guest purchase to a single step in the cart"),
  ("E-posta veya telefon alanı ve \"Üye olmadan satın al\" butonu sipariş özetine alınabilir; giriş paneli ve ayrı e-posta ekranı aradan çıkabilir.", "An e-mail or phone field and a \"Buy without an account\" button can be placed in the order summary; the sign-in panel and the separate e-mail screen can drop out.")),
 ("Öncelik 1", ("Site içi aramanın iki yolunun tekleştirilmesi ve parça ile destek aramalarının yönlendirilmesi", "Aligning the two site search paths and routing part and support searches"),
  ("İki arama yolunun her aramada daha isabetli sonuç veren mantıkla tekleştirilmesi; kartuş, conta, menteşe, \"yedek parça\" aramalarının ilgili parça kategorisine, garanti ve servis aramalarının destek ve garanti sayfalarına yönlendirilmesi; ölçü içeren aramalarda (\"80 cm banyo dolabı\") ölçü süzgecinin uygulanması değerlendirilebilir.", "Aligning the two search paths on the logic that gives the more accurate result for each search; routing cartridge, seal, hinge and \"yedek parça\" searches to the relevant parts category and warranty and service searches to the support and warranty pages; applying the size filter for searches with sizes (\"80 cm banyo dolabı\") can be considered.")),
 ("Öncelik 2", ("Sepette montaj hizmeti ve tamamlayıcı ürünlerin görünür olması", "Making installation services and complementary products visible in the cart"),
  ("Montaj ve \"VitrA'nın senin için seçtikleri\" karuselleri küçültülüp sepet listesinin hemen altına taşınabilir; ürünle eşleşen montaj hizmeti ürün satırında önerilebilir.", "The installation and \"VitrA picks for you\" carousels can be made smaller and moved directly below the cart list; the installation service matching the product can be suggested on the product row.")),
 ("Öncelik 2", ("Stok dışı ürünlerin listede ve aramada yönetilmesi", "Managing out-of-stock products in lists and search"),
  ("Stokta olmayan kartların sona alınması, tahmini tedarik tarihi ya da yakın model önerisi kullanıcının sitede kalmasını destekleyebilir.", "Moving out-of-stock cards to the end, an estimated restock date or a close alternative can help keep the user on the site.")),
 ("Öncelik 3", ("Ürün sayfasında fiyat, taksit ve garanti bilgisinin tek ve net olması", "A single, clear price, instalment and warranty message on the product page"),
  ("Sepette uygulanan indirimin ürün sayfasında görünmesi, tek taksit mesajı ve garanti süresinin gösterilmesi karar anındaki belirsizliği azaltabilir.", "Showing the in-cart discount on the product page, a single instalment message and the warranty period can reduce uncertainty at the point of decision.")),
]
T_FIR = tablo([th("Öncelik", "Priority", "Önerilen sıra; etki ve uygulama kolaylığı birlikte değerlendirilmiştir.", "Suggested order; impact and ease of implementation are considered together."),
               th("Fırsat", "Opportunity", "Dönüşüm fırsatı.", "The conversion opportunity."),
               th("Nasıl?", "How?", "Fırsat için önerilen düzenleme.", "The change proposed for the opportunity.")],
              [[_ob(o), "<b>%s</b>" % x(*f), x(*a)] for o, f, a in FIRSAT])

from grafik2 import halka as _halka
_HRK = {"U": "#2E7D32", "P": "#9AA8A5", "T": "#F5A623", "S": "#7A8C89", "Y": "#D32F2F", "D": "#E85F36", "G": "#C9D3D1"}
HALKA_ARA = _halka([(x(*DEG[k_]), SAY[k_], _HRK[k_]) for k_ in ("U", "P", "T", "S", "Y", "D", "G") if SAY.get(k_)],
                   x("vitra.com.tr site içi arama: 38 aramanın değerlendirme sınıflarına dağılımı · 04.10.2026", "vitra.com.tr site search: 38 searches by assessment class · 04.10.2026"),
                   merkez=("38", x("site içi arama", "site searches")), deger_bicim=lambda v: x("%d arama" % v, "%d searches" % v))
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
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
%s
""" % (
 x("Kullanıcının VitrA ürününü bulmasından satın almasına ve teslimat sonrasına kadar geçtiği adımlar yolculuk sırasıyla verilmiştir. Site içi arama ve sepet-ödeme adımları 4 Ekim 2026'da vitra.com.tr'de oturum açılmadan gözlenmiş, diğer adımlar ilgili bölümlerin bulgularından derlenmiştir.",
   "The steps a user goes through from finding a VitrA product to purchase and after delivery are given in journey order. Site search and the cart-checkout steps were observed on vitra.com.tr on 4 October 2026 without signing in; the other steps are compiled from the findings of the relevant sections."),
 kpi_kart("3", "Üyeliksiz alışverişte \"Sepeti Onayla\"dan adres adımına kadar tıklama · iki ara ekran", "Clicks from \"Confirm cart\" to the address step in guest checkout · two intermediate screens", "dn"),
 kpi_kart("%d / %d" % (SAY["T"], len(SA)), "Anlık sonuçlarda bulunup Enter sonrası sonuç sayfasında boş ya da ilgisiz dönen site içi arama · 04.10.2026", "Site searches found in instant results but empty or off-target on the results page after Enter · 04.10.2026", "dn"),
 kpi_kart("%d / %d" % (SAY["Y"] + SAY["D"], len(SA)), "İki yolda da ilgili ürün ya da destek sayfası dönmeyen arama (kartuş, conta, yedek parça, garanti, servis)", "Searches returning no relevant product or support page on either path (cartridge, seal, spare part, warranty, service)", "dn"),
 kpi_kart(yzd(_stok), "vitra.com.tr'de incelenen 55 alt kategori sayfasında stoklu süzgecin dışında kalan varyant kartı payı · 30.09.2026", "Share of variant cards outside the in-stock filter on the 55 vitra.com.tr sub-category pages reviewed · 30.09.2026", "dn"),
 x("Yolculuk adımları: gözlem, etki ve öneri", "Journey steps: observation, effect and recommendation"),
 T_YOL,
 insight("**Ürünle ilk temas çoğunlukla pazaryeri listelerinde ya da yapay zeka yanıtında gerçekleşmekte, vitra.com.tr'ye gelen kullanıcı ise arama, stok ve ödeme adımlarında ek engellerle karşılaşmaktadır**. Site içindeki bariyerlerin önemli bölümü ise arama sözlüğü, sepet yerleşimi ve ödeme akışı gibi sitenin kendi kontrolündeki düzenlemelerle azaltılabilir.",
         "**The first contact with the product mostly happens in marketplace lists or AI answers, and users who reach vitra.com.tr face extra barriers in search, stock and checkout**. A large part of the on-site barriers can be reduced with changes under the site's own control, such as the search dictionary, cart layout and checkout flow.", "D40", "D41"),
 x("Site içi arama: kullanıcının yazdığı ifadeler ne döndürüyor?", "Site search: what do the user's own terms return?"),
 HALKA_ARA + T_ARA,
 insight(("**38 aramanın %s iki arama yolu da uyumlu sonuç vermektedir**; anlık sonuçlar yazım farklarını (dusakabin, rezarvuar, klozed) ve kullanıcı dilini (şamandıra yazınca iç takım) doğru eşleştirmektedir. **Enter'a basıldığında açılan sonuç sayfası ise farklı bir arama altyapısıyla çalışmaktadır**: %d aramada anlık sonuç uyumluyken sonuç sayfası boş ya da ilgisizdir (şamandıra, dusakabin, rezarvuar, klozed ve ürün kodunda boş; \"lavabo\" ve \"batarya\" yazımında ilk kartlar sifon, batarya ve çıkış ucu); %d aramada ise durum tersinedir (\"80 cm banyo dolabı\" ve \"klozet kapağı menteşesi\" anlık sonuçta boş, \"taharet musluğu\" anlık sonuçta ara musluk getirirken sonuç sayfası ürün göstermektedir). %d aramada ilk kartlarda montaj hizmeti, kapak ya da aksesuar karışmaktadır. \"banyo dolabı\" için anlık sonuçlar %s, sonuç sayfası %s sonuç göstermektedir. İki yolda da karşılığı bulunmayan aramalar yedek parça (kartuş, conta, \"yedek parça\") ve destek (garanti, servis) ifadeleridir; garanti ve servis aramalarında destek sayfası yerine montaj hizmeti ve parça kartları çıkmaktadır. İki yolun her aramada daha isabetli sonuç veren mantıkla tekleştirilmesi ve yedek parça ile destek ifadeleri için yönlendirme kuralları aramanın dönüşüme katkısını artırabilir.")
         % (ek(SAY["U"], "inde"), SAY["T"], SAY["S"], SAY["P"], bin(KAT["banyo dolabı"]["sonuc"]), bin(_SA["banyo dolabı"]["sonuc"])),
         ("**Both search paths give consistent results for %d of the 38 searches**; instant results match spelling variants (dusakabin, rezarvuar, klozed) and user language (typing float valve returns inner mechanisms) correctly. **The results page that opens after pressing Enter runs on a different search engine**: for %d searches the instant results are fine but the results page is empty or off-target (empty for float valve, dusakabin, rezarvuar, klozed and product code; for \"lavabo\" and \"batarya\" the first cards are traps, taps and spouts), and for %d searches the reverse holds (\"80 cm banyo dolabı\" and \"klozet kapağı menteşesi\" are empty in instant results, and \"taharet musluğu\" returns angle valves in instant results while the results page shows products). In %d searches installation services, seats or accessories mix into the first cards. For \"banyo dolabı\" instant results show %s results and the results page %s. Searches with no match on either path are spare-part (cartridge, seal, \"yedek parça\") and support (warranty, service) terms; warranty and service searches return installation services and part cards instead of the support page. Aligning the two paths on the logic that gives the more accurate result for each search, and routing rules for spare-part and support terms, can increase the contribution of search to conversion.")
         % (SAY["U"], SAY["T"], SAY["S"], SAY["P"], f"{KAT['banyo dolabı']['sonuc']:,}", f"{_SA['banyo dolabı']['sonuc']:,}"), "D40"),
 x("Sepet ve ödeme: üyeliksiz alışverişte ek adımlar", "Cart and checkout: extra steps in guest checkout"),
 EKRAN,
 AKIS,
 insight("**Üyeliksiz alışverişte adres adımına gelmeden iki ara ekran geçilmektedir**: \"Sepeti Onayla\" sonrası giriş paneli açılmakta, \"Üye Olmadan Devam Et\" seçildiğinde e-posta ayrı bir ekranda istenmektedir. **Sepet özetinde e-posta veya cep telefonu alanı ve alan doldurulunca etkinleşen \"Üye olmadan satın al\" butonu**, bu iki ekranı tek adıma indirebilir; üyeler için giriş bağlantısı aynı alanda kalabilir. Sepet ekranında ücretsiz kargo, sepette indirim ve tahmini kargo tarihi açık biçimde gösterilmektedir. Montaj hizmetleri ve \"VitrA'nın senin için seçtikleri\" alanları ise sepetin altında kaldığı için kaydırma yapmayan kullanıcıya görünmemektedir; bu karusellerin küçültülüp sepet listesinin hemen altına taşınması montaj hizmeti ve tamamlayıcı ürün satışını destekleyebilir.",
         "**Guest checkout passes two intermediate screens before the address step**: after \"Confirm cart\" a sign-in panel opens, and choosing \"Continue without an account\" asks for an e-mail on a separate screen. **An e-mail or mobile phone field in the order summary and a \"Buy without an account\" button that activates once the field is filled** can reduce these two screens to a single step; the sign-in link for members can stay in the same area. The cart screen clearly shows free shipping, the in-cart discount and the estimated shipping date. The installation services and \"VitrA picks for you\" areas sit below the cart and are not seen by users who do not scroll; making these carousels smaller and moving them directly below the cart list can support installation service and complementary product sales.", "D41"),
 x("Dönüşüm fırsatları", "Conversion opportunities"),
 T_FIR,
 insight("Önceliklendirme, uygulama kolaylığı ve satın almaya yakınlık birlikte değerlendirilerek yapılmıştır: ödeme akışı ve site içi arama, kullanıcı satın almaya en yakınken devreye giren ve sitenin kendi kontrolündeki adımlardır. Aksiyonların sırası VitrA ekibinin öncelikleriyle güncellenebilir.",
         "Prioritisation considers ease of implementation and closeness to purchase together: checkout flow and site search come into play when the user is closest to buying and are under the site's own control. The order of actions can be updated with the VitrA team's priorities."),
 kaynak("vitra.com.tr site içi arama, %d arama, 04.10.2026 · vitra.com.tr sepet ve üyeliksiz alışveriş ekranları, masaüstü, 04.10.2026 · diğer gözlemler ilgili bölümlerin kaynaklarındandır · Google aylık hacim Keyword Planner" % len(SA),
        "vitra.com.tr site search, %d searches, 04.10.2026 · vitra.com.tr cart and guest checkout screens, desktop, 04.10.2026 · other observations come from the sources of the related sections · Google monthly volume Keyword Planner" % len(SA), "D40", "D41"),
)
