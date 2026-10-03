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


# ---------------------------------------------------------------- site ici arama testi
GRUP_EN = {"Kategori": "Category", "Yedek parça ve aksesuar": "Spare parts and accessories", "Yazım farkı": "Spelling variant", "Ölçü ve özellik": "Size and feature",
           "Seri ve ürün kodu": "Series and product code", "Hizmet ve destek": "Service and support"}
for a, b in GRUP_EN.items(): x(a, b)


def _ilgili(r):
    rx = re.compile(r["beklenen"], re.I)
    hiz = r["grup"] == "Hizmet ve destek"   # hizmet aramalari disinda montaj hizmeti karti ilgili urun sayilmaz
    return sum(1 for u_ in r["urunler"][:8] if rx.search((u_["ad"] or "") + " " + (u_["kategori"] or "")) and (hiz or u_["kategori"] != "Montaj Hizmeti"))


def _mtj(r): return sum(1 for u_ in r["urunler"][:4] if (u_["kategori"] or "") == "Montaj Hizmeti")


def _hacim(q):
    v = (KS.get(q) or {}).get("a26") or (_SO.KP.get(q) or {}).get("ort12")
    return round(v) if v else None


SIFIR = [r for r in SA if r["sonuc"] == 0]
KARTSIZ = [r for r in SA if r["sonuc"] > 0 and not r["urunler"]]
MTJ = [r for r in SA if _mtj(r) and r["grup"] != "Hizmet ve destek"]
DUSUK = [r for r in SA if r["urunler"] and len(r["urunler"]) >= 8 and _ilgili(r) <= 3 and r["grup"] != "Hizmet ve destek"]
_SA = {r["sorgu"]: r for r in SA}


def _ilgili_h(r):
    if not r["urunler"]: return n("-")
    m = min(8, len(r["urunler"])); v = _ilgili(r)
    h = "%d / %d" % (v, m)
    return n('<span class="dn">%s</span>' % h if v <= m / 2 else h)


T_ARA = tablo([th("Arama ifadesi", "Search phrase", "vitra.com.tr arama kutusuna yazılan ifade; bağlantı arama sonucunu yeni sekmede açar.", "The term typed into the vitra.com.tr search box; the link opens the search result in a new tab."),
               th("Grup", "Group", "Aramanın türü: kategori, yedek parça ve aksesuar, yazım farkı, ölçü ve özellik, seri ve ürün kodu, hizmet ve destek.", "Type of search: category, spare parts and accessories, spelling variant, size and feature, series and product code, service and support."),
               th("Sonuç", "Results", "Arama sayfasının başlığında yazan sonuç sayısı.", "Number of results shown in the search page heading.", True),
               th("İlk 8 kartta ilgili", "Relevant in first 8 cards", "İlk 8 karttan adında ya da kategorisinde aranan ürün tipi geçen ürünlerin sayısı; ürün aramalarında montaj hizmeti kartları sayılmamıştır.", "Of the first 8 cards, how many products carry the searched product type in their name or category; installation service cards are not counted in product searches.", True),
               th("İlk 4 kartta montaj hizmeti", "Installation service in first 4", "İlk 4 kart içindeki montaj hizmeti kartı sayısı.", "Number of installation service cards among the first 4 cards.", True),
               th("İlk kart", "First card", "Sonuç listesinde ilk sıradaki kart.", "The first card in the result list."),
               th("Google aylık hacim", "Google monthly volume", "Aynı ifadenin Google'daki ortalama aylık arama hacmi, Keyword Planner, Eyl 2025 - Ağu 2026; kullanıcı dilindeki talebin büyüklüğünü gösterir.", "Average monthly Google search volume of the same term, Keyword Planner, Sep 2025 - Aug 2026; shows the size of demand in the user's own words.", True)],
              [[u(r["url"], r["sorgu"]), etk(r["grup"], GRUP_EN[r["grup"]], "sa-" + r["grup"]), cell(r["sonuc"]) if r["sonuc"] else n('<span class="dn">0</span>'),
                _ilgili_h(r), cell(_mtj(r)) if r["urunler"] else n("-"), x(r["urunler"][0]["ad"], __import__("t2_ortak").EK.get(r["urunler"][0]["ad"], r["urunler"][0]["ad"])) if r["urunler"] else x("Ürün kartı dönmedi", "No product card returned"),
                cell(_hacim(r["sorgu"])) if _hacim(r["sorgu"]) else n("-")] for r in SA], "uzun")

# ---------------------------------------------------------------- yolculuk adimlari
_kirik_v, _kirik_r = YA["marka"]["VitrA"]["tema_neg"]["kirik"], YA["rakip"]["tema_neg"]["kirik"]
_stok = 100 * _D2.top_yok / _D2.top_kart
_q1 = next(r for r in AIG["klasor_soru"] if r[1] == "vitra klozet trendyol mu hepsiburada mı daha uygun")
_q3 = next(r for r in AIG["klasor_soru"] if r[1] == "banyo ürünlerinde iade ve değişim nasıl yapılır online alışverişte")
ADIM = [
 (("Keşif: Google araması", "Discovery: Google search"),
  ("Ürün ve kategori aramalarında Trendyol %d kelimenin %s ilk 10'da; vitra.com.tr %d kelimede ilk 10'da" % (_SO.N, ek(_SO.D10["trendyol.com"], "inde"), _SO.VITRA["ilk10"]),
   "Trendyol is in the top 10 for %d of %d product and category searches; vitra.com.tr is in the top 10 for %d" % (_SO.D10["trendyol.com"], _SO.N, _SO.VITRA["ilk10"])),
  ("Kullanıcının ilk temas ettiği ürün listesi çoğunlukla pazaryerinde", "The first product list the user sees is mostly on a marketplace"),
  ("Kategori sayfalarında kullanıcı dilindeki soruların (ölçü, montaj, fiyat) yanıtlanması", "Answering the user's questions (size, installation, price) on category pages"), "Kim sıralanıyor?"),
 (("Keşif: yapay zeka yanıtı", "Discovery: AI answer"),
  ("\"vitra klozet trendyol mu hepsiburada mı daha uygun\" sorusunda VitrA %d yanıtın tamamında anılıyor, vitra.com.tr %s kaynak; iade ve değişim sorusunda VitrA %d yanıtın %s geçiyor" % (_q1[3], ek(_q1[5], "inde"), _q3[3], ek(_q3[4], "inde")),
   "For \"vitra klozet trendyol mu hepsiburada mı daha uygun\" VitrA is named in all %d answers, vitra.com.tr cited in %d; for the returns question VitrA is named in %d of %d answers" % (_q1[3], _q1[5], _q3[4], _q3[3])),
  ("Satın alma kararı anında yanıt kullanıcıyı pazaryerine yönlendiriyor", "At the moment of purchase the answer points the user to a marketplace"),
  ("Teslimat, iade, kurulum ve satın alma koşullarının vitra.com.tr'de soru-cevap biçiminde yer alması", "Presenting delivery, returns, installation and purchase terms on vitra.com.tr as questions and answers"), "Satın alma ve montaj sorularında VitrA ve vitra.com.tr"),
 (("Kategori sayfası", "Category page"),
  ("%s varyant kartının %s stoklu süzgecinin dışında; %d alt kesitte stoklu ürün yok" % (bin(_D2.top_kart), yzd(_stok), len(_D2.sifir)),
   "%s of %s variant cards are outside the in-stock filter; %d sub-segments have no in-stock product" % (("%.1f" % _stok) + "%", f"{_D2.top_kart:,}", len(_D2.sifir))),
  ("Kullanıcı ürünü bulsa da satın alamıyor ve başka kanala geçebiliyor", "The user finds the product but cannot buy it and may move to another channel"),
  ("Stokta olmayan ürünlerin listede sona alınması, tahmini tedarik tarihi ya da yakın model önerisi", "Moving out-of-stock products to the end of lists, an estimated restock date or a close alternative"), "vitra.com.tr kategori sayfaları: ürün, fiyat aralığı ve stok"),
 (("Site içi arama", "Site search"),
  ("%d test aramasının %s sonuç dönmüyor (şamandıra, kartuş, garanti, yazım farkları); %d ürün aramasında ilk 4 kartta montaj hizmeti çıkıyor" % (len(SA), ek(len(SIFIR), "inde"), len(MTJ)),
   "%d of %d test searches return no results (float valve, cartridge, warranty, spelling variants); in %d product searches an installation service appears among the first 4 cards" % (len(SIFIR), len(SA), len(MTJ))),
  ("Aradığını bulamayan kullanıcı siteden çıkabiliyor ya da Google'a dönüyor", "A user who cannot find the product may leave the site or return to Google"),
  ("Eş anlamlı ve yazım farkı sözlüğü, sıfır sonuçta öneri, montaj hizmeti kartlarının ürün sonuçlarından ayrılması", "A synonym and spelling-variant dictionary, suggestions on zero results, separating installation service cards from product results"), "Site içi arama: kullanıcının yazdığı ifadeler ne döndürüyor?"),
 (("Ürün sayfası: fiyat", "Product page: price"),
  ("İncelenen 29 VitrA ürününün 19'unda en düşük fiyat vitra.com.tr'de değil, bir pazaryeri satıcısında", "For 19 of the 29 VitrA products reviewed, the lowest price is not on vitra.com.tr but at a marketplace seller"),
  ("Fiyat karşılaştıran kullanıcı satın almayı pazaryerinde tamamlayabiliyor", "A user comparing prices may complete the purchase on a marketplace"),
  ("Sepette uygulanan indirimin ürün sayfasında görünmesi; kanal fiyat politikasının gözden geçirilmesi", "Showing the in-cart discount on the product page; reviewing the channel price policy"), "VitrA ürünlerinde kanal fiyat farkı: 29 ürün"),
 (("Ürün sayfası: taksit ve garanti", "Product page: instalments and warranty"),
  ("Taksit mesajı üç yüzeyde farklı (üst bant 6, kampanya sayfası 9, ürün tablosu 12 ay); ürün sayfalarında garanti süresi yer almıyor", "The instalment message differs across three surfaces (banner 6, campaign page 9, product table 12 months); product pages show no warranty period"),
  ("Ödeme koşulu ve güvence bilgisi karar anında belirsiz kalıyor", "Payment terms and assurance remain unclear at the point of decision"),
  ("Tek taksit mesajı; garanti süresinin ürün sayfasında ve sepette gösterilmesi", "A single instalment message; showing the warranty period on the product page and in the cart"), "Ödeme ve taksit koşulları"),
 (("Sepet", "Cart"),
  ("Montaj hizmetleri ve \"VitrA'nın senin için seçtikleri\" alanları sepet listesinin ve sipariş özetinin altında; masaüstünde montaj kartları ekranın alt kenarında başlıyor", "The installation services and \"VitrA picks for you\" areas sit below the cart list and order summary; on desktop the installation cards start at the bottom edge of the screen"),
  ("Kaydırma yapmayan kullanıcı montaj hizmetini ve tamamlayıcı ürünleri görmüyor", "A user who does not scroll does not see the installation service or complementary products"),
  ("Karusellerin küçültülüp sepet listesinin hemen altına taşınması", "Making the carousels smaller and moving them directly below the cart list"), "Sepet ve ödeme: üyeliksiz alışverişte ek adımlar"),
 (("Ödeme", "Checkout"),
  ("Üyeliksiz alışverişte adres adımına gelmeden önce iki ara ekran ve üç tıklama gerekiyor", "Guest checkout needs two intermediate screens and three clicks before the address step"),
  ("Her ek ekran, ödeme adımına gelmeden çıkış ihtimalini artırır", "Each extra screen increases the chance of leaving before payment"),
  ("Sepet özetinde e-posta veya telefon alanı ve \"Üye olmadan satın al\" butonu", "An e-mail or phone field and a \"Buy without an account\" button in the order summary"), "Sepet ve ödeme: üyeliksiz alışverişte ek adımlar"),
 (("Teslimat", "Delivery"),
  ("Pazaryerlerindeki olumsuz VitrA yorumlarında kırık veya hasarlı teslimat payı %s (rakiplerde %s)" % (yzd(_kirik_v), yzd(_kirik_r)),
   "%s of negative VitrA reviews on marketplaces concern broken or damaged deliveries (%s for competitors)" % (("%.1f" % _kirik_v) + "%", ("%.1f" % _kirik_r) + "%")),
  ("Hasarlı teslimat iade ve olumsuz yorum olarak geri dönüyor", "Damaged deliveries come back as returns and negative reviews"),
  ("Hacimli ürünlerde ambalaj ve teslimat kontrolü; teslimat koşullarının ürün sayfasında anlatılması", "Packaging and delivery checks for bulky products; explaining delivery terms on the product page"), "Pain point profili: kategori geneli mi, markaya özgü mü?"),
 (("Satış sonrası", "After-sales"),
  ("Şikayetvar'daki VitrA şikayetlerinin %76,9'u servis, yedek parça, montaj veya müşteri hizmetlerine ulaşma konularını içeriyor", "76.9% of VitrA complaints on Şikayetvar mention service, spare parts, installation or reaching customer service"),
  ("Satın alma sonrası deneyim bir sonraki satın almayı ve yorumları etkiliyor", "The after-purchase experience affects the next purchase and reviews"),
  ("Yedek parçanın sitede bulunabilir ve aranabilir olması; servis talebinin siteden açılabilmesi", "Making spare parts findable and searchable on the site; allowing service requests from the site"), "Şikayet temaları ve örnek alıntılar"),
]
T_YOL = tablo([th("Adım", "Step", "Kullanıcının keşiften satış sonrasına kadar geçtiği adım.", "The step the user passes through from discovery to after-sales."),
               th("Gözlem", "Observation", "Adımda ölçülen ya da gözlenen durum; ok simgesi ayrıntının yer aldığı alt başlığa gider.", "The measured or observed situation at the step; the arrow goes to the sub-heading with the detail."),
               th("Kullanıcıya etkisi", "Effect on the user", "Gözlemin satın alma yolculuğuna olası etkisi.", "Possible effect of the observation on the purchase journey."),
               th("Önerilen düzenleme", "Recommended change", "Adımdaki bariyeri azaltabilecek düzenleme.", "A change that may reduce the barrier at the step.")],
              [["<b>%s</b>" % x(*a), x(*g) + git(h), x(*e), x(*o)] for a, g, e, o, h in ADIM], "uzun")

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

AKIS = tablo([th("", "", "Akış.", "Flow."),
              th("Mevcut akış", "Current flow", "04.10.2026 tarihinde masaüstünde gözlenen adımlar.", "Steps observed on desktop on 04.10.2026."),
              th("Önerilen akış", "Proposed flow", "Sepet özetinde tek adımda üyeliksiz satın alma.", "Guest purchase in one step in the order summary.")],
             [[x("1", "1"), x("Sepet: \"Sepeti Onayla\"", "Cart: \"Confirm cart\""), x("Sepet: \"Sepeti Onayla\" butonunun altında e-posta veya cep telefonu alanı", "Cart: an e-mail or mobile phone field below the \"Confirm cart\" button")],
              [x("2", "2"), x("Giriş paneli: Giriş Yap / Üye Ol / Üye Olmadan Devam Et", "Sign-in panel: Sign in / Register / Continue without an account"), x("Alan doldurulunca etkinleşen \"Üye olmadan satın al\" butonu", "A \"Buy without an account\" button that activates once the field is filled")],
              [x("3", "3"), x("Üyeliksiz Alışveriş: e-posta alanı ve \"Devam Et\"", "Guest Checkout: e-mail field and \"Continue\""), x("Doğrudan adres ve ödeme adımı; üyeler için \"Giriş yap\" bağlantısı aynı alanda", "Straight to address and payment; a \"Sign in\" link for members in the same area")],
              [x("4", "4"), x("Adres ve ödeme", "Address and payment"), x("Satın alma sonrası tek tıkla hesap oluşturma seçeneği", "Option to create an account with one click after purchase")]])

# ---------------------------------------------------------------- donusum firsatlari
OC = {"Öncelik 1": "b-o1", "Öncelik 2": "b-o2", "Öncelik 3": "b-o3"}; OE = {"Öncelik 1": "Priority 1", "Öncelik 2": "Priority 2", "Öncelik 3": "Priority 3"}
def _ob(o): return '<span class="badge %s">%s</span>' % (OC[o], x(o, OE[o]))
FIRSAT = [
 ("Öncelik 1", ("Üyeliksiz satın almanın sepette tek adıma indirilmesi", "Reducing guest purchase to a single step in the cart"),
  ("E-posta veya telefon alanı ve \"Üye olmadan satın al\" butonu sipariş özetine alınabilir; giriş paneli ve ayrı e-posta ekranı aradan çıkar.", "An e-mail or phone field and a \"Buy without an account\" button can be placed in the order summary; the sign-in panel and the separate e-mail screen drop out.")),
 ("Öncelik 1", ("Site içi aramada sıfır sonucun ve alakasız ilk sonuçların azaltılması", "Reducing zero results and irrelevant first results in site search"),
  ("Kullanıcı dilindeki ifadeler (şamandıra, kartuş, taharet musluğu, menteşe) ve yazım farkları (dusakabin, rezarvuar) için eş anlamlı sözlüğü; ürün aramalarında montaj hizmeti kartlarının ayrı bir şeritte gösterilmesi değerlendirilebilir.", "A synonym dictionary for user terms (float valve, cartridge, bidet tap, hinge) and spelling variants (dusakabin, rezarvuar); showing installation service cards in a separate strip in product searches can be considered.")),
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

_ilk = _SA["banyo dolabı"]
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
 x("Bu bölüm, kullanıcının VitrA ürününü bulmasından satın almasına ve teslimat sonrasına kadar geçtiği adımları vitra.com.tr üzerinden ele almaktadır. Raporun diğer bölümlerindeki bulgular yolculuk sırasına göre bir araya getirilmiş; site içi arama ve sepet-ödeme adımları için ayrıca gözlem yapılmıştır. Gözlemler 4 Ekim 2026 tarihlidir ve oturum açılmadan yapılmıştır.",
   "This section covers the steps a user goes through on vitra.com.tr from finding a VitrA product to purchase and after delivery. Findings from other sections of the report are brought together in journey order; site search and the cart-checkout steps were observed separately. Observations are dated 4 October 2026 and were made without signing in."),
 kpi_kart("3", "Üyeliksiz alışverişte \"Sepeti Onayla\"dan adres adımına kadar tıklama · iki ara ekran", "Clicks from \"Confirm cart\" to the address step in guest checkout · two intermediate screens", "dn"),
 kpi_kart("%d / %d" % (len(SIFIR), len(SA)), "Sonuç dönmeyen site içi arama (şamandıra, kartuş, garanti, yazım farkları) · 04.10.2026", "Site searches returning no results (float valve, cartridge, warranty, spelling variants) · 04.10.2026", "dn"),
 kpi_kart("%d / %d" % (len(MTJ), len([r for r in SA if r["urunler"] and r["grup"] != "Hizmet ve destek"])), "İlk 4 kartta montaj hizmeti çıkan ürün araması", "Product searches with an installation service among the first 4 cards"),
 kpi_kart(yzd(_stok), "vitra.com.tr kategori sayfalarında stoklu süzgecinin dışında kalan varyant kartı payı · 30.09.2026", "Share of variant cards outside the in-stock filter on vitra.com.tr category pages · 30.09.2026", "dn"),
 x("Yolculuk adımları: gözlem, etki ve öneri", "Journey steps: observation, effect and recommendation"),
 T_YOL,
 insight("**Kullanıcı VitrA'yı çoğunlukla pazaryerinde ya da yapay zeka yanıtında tanımakta, vitra.com.tr'ye geldiğinde ise arama, stok ve ödeme adımlarında ek engellerle karşılaşmaktadır**. Keşif aşamasındaki görünürlük raporun SEO ve GEO bölümlerinde ele alınmıştır. Site içindeki bariyerlerin önemli bölümü ise arama sözlüğü, sepet yerleşimi ve ödeme akışı gibi sitenin kendi kontrolündeki düzenlemelerle azaltılabilir.",
         "**Users mostly get to know VitrA on a marketplace or in an AI answer, and when they reach vitra.com.tr they face extra barriers in search, stock and checkout**. Visibility at the discovery stage is covered in the SEO and GEO sections of the report. A large part of the on-site barriers can be reduced with changes under the site's own control, such as the search dictionary, cart layout and checkout flow.", "D40", "D41"),
 x("Site içi arama: kullanıcının yazdığı ifadeler ne döndürüyor?", "Site search: what do the user's own terms return?"),
 T_ARA,
 insight(("**%d test aramasının %s sonuç dönmemektedir**: şamandıra, kartuş ve garanti ile \"dusakabin\", \"rezarvuar\", \"klozed\" gibi yazım farkları. **Kategori aramalarında ilk sonuçlar aranan ürünle eşleşmemektedir**: \"banyo dolabı\" aramasında %s sonuç dönmekte, ancak ilk 8 kartın hiçbiri banyo dolabı değildir (montaj hizmeti, batarya, kağıtlık ve askı). %d ürün aramasında ilk 4 kartta montaj hizmeti yer almaktadır. Model adı ve ürün kodu aramaları (metropole, sento, 7906B483-0090) ise doğru ürünü ilk sıraya getirmektedir. Kullanıcının Google'da kullandığı ifadeler (taharet musluğu, şamandıra, klozet kapağı menteşesi) için eş anlamlı sözlüğü ve sıfır sonuçta öneri gösterilmesi site içi aramanın dönüşüme katkısını artırabilir.")
         % (len(SA), ek(len(SIFIR), "inde"), bin(_ilk["sonuc"]), len(MTJ)),
         ("**%d of %d test searches return no results**: float valve, cartridge and warranty, and spelling variants such as \"dusakabin\", \"rezarvuar\" and \"klozed\". **In category searches the first results do not match the searched product**: \"banyo dolabı\" returns %s results, but none of the first 8 cards is a bathroom cabinet (installation service, taps, toilet roll holders and hooks). In %d product searches an installation service appears among the first 4 cards. Searches by model name and product code (metropole, sento, 7906B483-0090) bring the right product to the top. A synonym dictionary for the terms users use on Google (bidet tap, float valve, toilet seat hinge) and suggestions on zero results can increase the contribution of site search to conversion.")
         % (len(SIFIR), len(SA), f"{_ilk['sonuc']:,}", len(MTJ)), "D40"),
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
