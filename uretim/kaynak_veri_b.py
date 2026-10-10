# -*- coding: utf-8 -*-
"""Kaynak dokumu · B: kanal politikalari (odeme, teslimat, iade, garanti, servis), sosyal profiller ve benchmark siteleri."""
from kaynak_ortak import *
from kaynak_veri_a import D28, D29, D30

CURL = "curl"; APF = "API (Apify rag-web-browser)"; CHR = "tarayıcı (Chrome, kullanıcı oturumu)"; OZ = "arama sonucu özeti (sayfa açılamadı)"

def P(url, amac, bilgi, yontem, tarih, kod=("D23",), bolum=("politika",)):
    ekle(url, amac, bilgi, bolum=list(bolum), yontem=yontem, tarih=tarih, kod=list(kod))

def doldur():
    # ------------------------------------------------------------ vitra.com.tr
    V = "https://www.vitra.com.tr"
    P(V, "VitrA ana sayfa: şerit mesajları (taksit ve kargo)",
      "Şeritte 'tüm ürünlerde vade farksız 9 ay taksit' ve 'tüm ürünlerde ücretsiz kargo'",
      [CURL, "tarayıcı"], "10.10.2026", kod=["D23", "D13"], bolum=["politika", "set", "benchmark", "organik"])
    P(V + "/odeme-rehberi", "VitrA ödeme yöntemleri ve taksit koşulları",
      "Yalnızca kredi kartı (iyzico altyapısı, 3D Secure); kapıda ödeme yok; havale/EFT rehberde geçmiyor; sepette kurumsal fatura bilgisi eklenebiliyor; Banyo ve Karo ürünleri taşıma koşulları nedeniyle ayrı sepette", CURL, D29)
    P(V + "/kampanyalar", "VitrA kampanya ve taksit koşulları",
      "21 Eylül - 30 Kasım 2026: seçili renkli ürünlerde %40 indirim, 9 aya varan taksit, 40.000 TL ve üzeri alışverişte ücretsiz montaj", CURL, D29)
    P(V + "/dusakabin/universal-surgulu-on-panel-mat-siyah-p-65650002270", "VitrA ürün sayfası örneği (duşakabin): taksit tablosu, kargo tarihi, montaj seçeneği ve iade ifadesi",
      "Ürün tablosunda vade farkıyla 12 taksite kadar seçenek; tahmini kargoya teslim tarihi; 30 güne kadar ücretsiz iade ifadesi; montaj hizmeti seçeneği (+5.300 TL)", CURL, D29)
    P(V + "/teslimat-rehberi", "VitrA teslimat koşulları (kargo, büyük ürün, kat teslimi)",
      "Sipariş en fazla 3 iş günü içinde paket boyutu ve adrese göre kargo veya lojistik firmasına teslim edilir; ürün sayfasında tahmini kargoya teslim tarihi; 'kapınıza kadar' teslim, kat teslimi belirtilmemiş; ücretsiz kargo eşiksiz", CURL, D29)
    P(V + "/degisim-iade-rehberi", "VitrA değişim ve iade koşulları",
      "Rehberde iade gün sayısı yazmıyor (süre yalnızca ürün sayfasında, 30 güne kadar ücretsiz iade); büyük paket adresten lojistik firmasıyla alınır; klozete özel iade koşulu bulunamadı", CURL, D29)
    P(V + "/garanti-hizmetleri", "VitrA garanti bilgisi (süre, kapsam, ek garanti paketi)",
      "Ürün sayfalarında garanti süresi yazmıyor; V-Care akıllı klozette 2 yıl (ek garanti paketiyle 4 yıl ve yıllık periyodik bakım); '+2 yıl ek garanti ve periyodik bakım paketi' sayfası", CURL, D29)
    P(V + "/musteri-hizmetleri", "VitrA müşteri hizmetleri ve iletişim kanalları",
      "Müşteri hizmetleri hattı (Pzt-Cts 09:00-18:00); online servis randevusu; WhatsApp hattı bulunamadı; ayrı yedek parça sayfası bulunamadı", CURL, D29)
    P(V + "/garanti-talep-formu", "VitrA online garanti talep formu", "Garanti talebinin fatura kaydıyla online iletilmesi; servis randevu akışıyla bağlantı", CURL, D29)
    P(V + "/servisler-ve-satis-noktalari", "VitrA resmi satış ve servis noktası bulucusu",
      "161 satış noktası ve 76 servis noktası (toplam 237); Google Maps profilleriyle karşılaştırma için resmi sayı", [CURL, "tarayıcı"], D29, bolum=("politika", "organik"))
    P(V + "/support/faq", "VitrA destek SSS sayfası", "Destek SSS sayfası; ödeme, teslimat ve iade başlıkları için taranan sayfalar arasında yer aldı", CURL, D29)

    # ------------------------------------------------------------ Koctas
    K = "https://www.koctas.com.tr"
    P(K, "Koçtaş ana sayfa: kampanya ve taksit başlıkları", "Taksit kampanyası (30 Eylül 2026'ya kadar), '3 AL 2 ÖDE' ve 1.500 TL üzeri ek 250 TL indirim başlıkları; Koçtaş Kart menüde; ilk okuma Apify ile (curl 403)", APF, D29)
    P(K + "/taksitler", "Koçtaş taksit ve vade farksız koşulları",
      "Online 5.000 TL üzeri 7 taksite kadar vade farksız (mağazada 10.000 TL üzeri); vade farklı 9 taksite kadar; Flexi kart, aidatsız kart ve TEB Worldcard kapsam dışı; alışveriş kredisi bulunamadı", APF, D29)
    P(K + "/nakliye-ve-montaj-hizmetleri", "Koçtaş nakliye ve montaj hizmetleri", "20 ilde montaj (İstanbul, Ankara, İzmir başta); seçili aydınlatma ve mobilyada ücretsiz montaj; Ustabilir hizmeti", APF, D29)
    P(K + "/myaccount/faq", "Koçtaş yardım sayfası: kargo, teslimat, iade, hasar ve ödeme koşullarının doğrulanması",
      "Ücretsiz kargo eşiği yalnız 300 TL (altı 49,90 TL); 30 desi üstü lojistikle kata teslim; iade 14 gün, iade kodu 7 gün; demonte üründe montaj yapıldıysa iade yok; klozet takımı ve kapağında ambalajı açılmamış şartı; hasar için Durum Tespit Tutanağı; kapıda ödeme yok; taksit eşiği bu sayfada 10.000 TL (/taksitler sayfasında 5.000 TL, tutarsız)",
      CHR, D30, kod=("D23", "D28"))
    P(K + "/hizmetlerimiz/montaj-hizmeti", "Koçtaş montaj hizmeti sayfası", "Montaj hizmetleri ücretli; montaj kaleminin sepete ayrıca eklenmesi gerekir; sayfada fiyat ve il sayısı yok", CHR, D30, kod=("D28",))
    ekle(K + "/hizmetlerimiz", "Koçtaş hizmetler sayfası (montaj hizmetleri ve banyo kampanyası koşulları)", "Banyo tadilatı ve montaj hizmetlerinin koşulları", bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B2"])
    ekle(K + "/banyo-kampanyasi", "Koçtaş banyo kampanyası koşulları", "Banyo kampanyasının kapsamı ve koşulları; kampanyalar mağazaya özel", bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B2"])

    # ------------------------------------------------------------ Bauhaus TR
    B = "https://www.bauhaus.com.tr"
    P(B, "Bauhaus TR ana sayfa: kampanya etiketleri", "'Vade farksız taksit seçenekleri' ve internete özel kampanya etiketleri", CURL, D29)
    P(B + "/taksit-secenekleri", "Bauhaus TR taksit koşulları", "2.500 TL ve üzeri alışverişte anlaşmalı banka kartlarıyla vade farksız (online ve şubeler); azami taksit yazmıyor", CURL, D29)
    P(B + "/sss", "Bauhaus TR SSS: ödeme yöntemleri, iade ve kargo", "Havale/EFT ile ödeme (sipariş numarası açıklamada); kapıda ödeme yok; kurumsal müşteri servisi ve Bauhaus Kurumsal Kart", CURL, D29)
    P(B + "/ucretsiz-kargo", "Bauhaus TR ücretsiz kargo ve büyük ürün teslimatı", "1.000 TL ve üzeri (belirlenen ürünlerde) ücretsiz kargo; şubelerden 40.000 TL ve üzeri şehir içi 30 km'ye kadar ücretsiz nakliye; 30 desi altı Yurtiçi/KolayGelsin, üstü Horoz/Arvato", CURL, D29)
    P(B + "/iade", "Bauhaus TR iade koşulları", "14 gün iade; iade kodu 7 gün içinde kargoya verilmeli", CURL, D29)
    P(B + "/urun-iade-garantisi", "Bauhaus TR ürün iade garantisi koşulları", "Demonte üründe kurulumdan sonra iade yok; klozet takımı ve kapağında ambalajı açılmamış ve denenmemiş şartı", CURL, D29)
    P(B + "/urun-garantisi", "Bauhaus TR ürün garantisi bilgisi", "Ürün garantisi koşulları (garanti başlığı için taranan sayfa)", CURL, D29)
    P(B + "/servisler", "Bauhaus TR servisler: montaj ve hasar bildirimi", "Usta temini müşteri hizmetleri üzerinden, fiyat bulunamadı; hasar tespit tutanağı zorunlu (tutanak yoksa kargo kaynaklı olduğu ispatlanamıyor)", CURL, D29)

    # ------------------------------------------------------------ IKEA TR
    I = "https://www.ikea.com.tr"
    P(I + "/odeme-secenekleri", "IKEA TR ödeme ve taksit koşulları", "1.500 TL üzeri 3 taksit; IKEA Aile üyelerine 7.500 TL üzeri 6 ve 20.000 TL üzeri 9 taksit (belirli kartlar); 5 Ocak 2026 - 3 Ocak 2027 arası geçerli; kapıda ödeme yok (Full 3D kart)", CURL, D29)
    P(I + "/ikea-kurumsal", "IKEA TR kurumsal sayfası", "IKEA Kurumsal Kart bilgisi (kurumsal fatura seçeneği)", CURL, D29)
    P(I + "/nakliye-hizmeti", "IKEA TR nakliye hizmeti", "Arvato, Horoz, HepsiJET, Yurtiçi, KolayGelsin; şehir içi ayrı nakliye hizmeti; daire kapısına kadar teslim; minimum sipariş 500 TL, kargo 299 TL (1.500 TL'ye kadar) ve 799 TL (7.500 TL'ye kadar), üstünde %11", CURL, D29)
    P(I + "/montaj-hizmeti", "IKEA TR montaj hizmeti", "Sepette veya sipariş numarasıyla montaj; bölgeye göre fiyat; kurulumdan itibaren 2 yıl garanti", CURL, D29, kod=("D23", "B3"), bolum=("politika", "set", "benchmark"))
    P(I + "/iade-politikasi", "IKEA TR iade politikası", "İnternet siparişlerinde 14 gün ücretsiz iade, mağazada 30 gün; ambalajı açılmamış orijinal kutu şartı; özel kesim ürünler iade dışı", CURL, D29)
    P(I + "/musteri-hizmetleri/garanti-kosullari", "IKEA TR garanti koşulları", "Garanti koşulları sayfası (garanti başlığı için taranan sayfa)", CURL, D29)
    P(I + "/musteri-hizmetleri/sikca-sorulan-sorular", "IKEA TR SSS", "SSS sayfası; hasar politikası bilgisi statik HTML'de görünmedi", CURL, D29)
    P(I + "/ikea-onemli-bilgilendirme", "IKEA TR önemli bilgilendirme sayfası", "Önemli bilgilendirme sayfası; teslimat ve ödeme başlıkları için taranan sayfalar arasında yer aldı", CURL, D29)

    # ------------------------------------------------------------ Kale
    L = "https://www.kale.com.tr"
    P(L, "Kale ana sayfa: online satış ve yönlendirme durumu", "Sitede sepet ve online satış yok, satış noktalarına yönlendirir (ödeme, kargo ve iade başlıkları uygulanamıyor)", CURL, D29)
    P(L + "/magazalar-ve-satis-noktalari", "Kale mağaza ve satış noktaları", "Online satışın olmadığı, satış noktalarına yönlendirme yapıldığı", CURL, D29)
    P(L + "/sikca-sorulan-sorular", "Kale garanti, teslimat ve iade SSS", "Seramik sağlık gereçleri ve armatürler 10 ve 5 yıl, musluk 2 yıl, duş sistemleri ve gömme rezervuar 5 yıl garanti; servis işçiliği 1 yıl; ayrı yedek parça sayfası bulunamadı", CURL, D29)
    P(L + "/yetkili-servisler-ve-hizmetler", "Kale yetkili servis ve servis talebi", "Yetkili servisler sayfasından servis talebi; servis hattı; WhatsApp destek hattı", CURL, D29)
    P(L + "/iletisim", "Kale iletişim sayfası", "İletişim kanalları ve destek hattı", CURL, D29)
    ekle(L + "/montaj-hizmetleri", "Kale montaj hizmetleri sayfası (rakip marka hizmet modeli)", "Montaj hizmetleri sayfası açılmış; 29.09.2026 itibarıyla ürün listelenmiyor; rakip marka hizmet ve yedek parçayı e-ticarete taşımaya başlıyor",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B5"])
    ekle(L + "/yedek-parcalar", "Kale yedek parça sayfası", "Yedek parça sayfası açılmış, 29.09.2026 itibarıyla ürün listelenmiyor", bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B5"])

    # ------------------------------------------------------------ Creavit
    C = "https://shop.creavit.com.tr"
    P(C, "Creavit e-mağaza ana sayfa: taksit ve iade mesajları", "Peşin fiyatına 6 ve 9 taksit ifadeleri birlikte görünüyor (banner 9, alt metin 6); 30 gün ücretsiz iade ve değişim; 3.000 TL üzeri ücretsiz kargo", CURL, D29)
    P(C + "/pages/teslimat-kosullari", "Creavit e-mağaza teslimat koşulları", "Banka onayından sonra 5 iş günü içinde kargoya, kargo 1-5 gün; 3.000 TL üzeri ücretsiz kargo; 30 gün ücretsiz iade ve değişim", CURL, D29)
    P(C + "/collections/montaj-hizmeti", "Creavit e-mağaza montaj hizmeti kalemleri ve fiyatları", "11 kalem: asma ve takım klozet 2.450 TL, rezervuar ve iç takım 1.750, armatür ve duş 1.750, lavabo 2.450, banyo mobilyası alt modül 2.450, boy dolabı 1.400, demonte takım 3.900 TL (söküm hariç)", CURL, D29)
    P(C + "/pages/contact", "Creavit e-mağaza iletişim", "E-mağaza hattı (Pzt-Cuma 08:30-17:30)", CURL, D29)
    P("https://www.creavit.com.tr", "Creavit marka sitesi ana sayfa", "Marka sitesi menüsü; garanti ve doküman alanlarına giriş", CURL, D29)
    P("https://www.creavit.com.tr/tr/iletisim/servisler/yetkili-servisler-P27", "Creavit yetkili servisler", "Yetkili servisler sayfası ve servis randevu akışı", CURL, D29)
    P("https://www.creavit.com.tr/dokumanlar/", "Creavit doküman sayfası: garanti süreleri", "12 yıllık ve 2 yıllık kullanma kılavuzu ve garanti şartları (PDF); seramik 12, gömme rezervuar 10, armatür ve duş 5 yıl (arama özeti, PDF ile kısmen doğrulandı)", CHR, D30, kod=("D23", "D28"))
    P("https://www.creavit.com.tr/dokumanlar/kataloglar/", "Creavit kataloglar sayfası: yedek parça listesi kontrolü", "15 PDF listeleniyor; hiçbirinin adında yedek parça yok, sayfada 'yedek' ifadesi geçmiyor", CHR, D30, kod=("D28",))

    # ------------------------------------------------------------ Banyomarka / Banyoline
    M = "https://www.banyomarka.com"
    P(M, "Banyomarka ana sayfa: kampanya ve kombin başlıkları", "Ürün kartında 4 taksit; Grohe kampanyalı batarya ve duş seti sayfaları; batarya ve musluk kombinleri", CURL, D29)
    P(M + "/musteri-hizmetleri.xhtml", "Banyomarka müşteri hizmetleri", "İstanbul içi kapıda nakit ödeme; WhatsApp destek; iletişim kanalları", CURL, D29)
    P(M + "/teslimat-kosullari.shtm", "Banyomarka teslimat koşulları", "3 iş günü içinde kargoya, kargo 1-3 gün; stokta yoksa 4-30 gün; ücretsiz kargo seçili ürünlerde (banner'da İstanbul içi 250 TL, güncelliği belirsiz)", CURL, D29)
    P(M + "/garanti-ve-iade-kosullari.shtm", "Banyomarka garanti ve iade koşulları", "Ürün kartında 30 gün iade; ürün kusuru durumunda 15 gün içinde bildirim; kullanılmış üründe iade ve değişim yok", CURL, D29)
    P(M + "/satis-sozlesmesi.shtm", "Banyomarka satış sözleşmesi", "Ödeme, havale/EFT ve teslimat maddeleri", CURL, D29)
    N = "https://www.banyoline.com"
    P(N, "Banyoline ana sayfa: taksit ve kargo şeritleri", "Şeritte 'peşin fiyatına 12 ay taksit' ve tüm alışverişlerde ücretsiz hızlı kargo", CURL, D29)
    P(N + "/kampanyalar", "Banyoline kampanyalar", "Kampanya ve taksit ifadeleri", CURL, D29)
    P(N + "/montaj-hizmeti", "Banyoline montaj hizmeti", "Yalnızca İstanbul'da ücretsiz montaj: Orka seçili dolaplar ve VitrA Metropole Edge, Valarte, Nest Trendy, Sento, Root modelleri; batarya ve ara musluk montajı ve ölçü alma yok; ücretsiz montajda ön hazırlık yönergesine uyulmazsa iade ve ikinci montaj yok", CURL, D29)
    P(N + "/mesafeli-satis-sozlesmesi", "Banyoline mesafeli satış sözleşmesi", "İptal ve iade talebi formu; teslim süresi bölgeye bağlı (yasal 30 günü aşmaz); teslim alırken kontrol alıcıda", CURL, D29)

    # ------------------------------------------------------------ Trendyol
    T = "https://www.trendyol.com"
    P(T + "/yardim/iade", "Trendyol iade süresi, taksit ve kapıda ödeme kuralları", "İade süresi teslimden itibaren 15 gün; taksit yalnızca taksit yapılabilen ürünlerde; kapıda ödeme ve havale seçeneği yok", CHR, D30, kod=("D23", "D28"))
    P(T + "/yardim/kargo-ve-teslimat", "Trendyol kargo ücreti ve teslimat", "Standart kargo ücreti 59,99 TL; 'kargo bedava' kampanyalı ürünlerde ücretsiz; genel alıcı eşiği yok", CHR, D30, kod=("D28",))
    P(T + "/s/mobilya-alisverisi-hakkinda-sik-sorulan-sorular", "Trendyol mobilya alışverişi SSS: montajlı ürün iadesi", "Montajlı ürünün iadesi, paketin adresten alınması ve ücretsiz yapılması adımları", CHR, D30, kod=("D28",))
    P(T + "/yardim/sorular/3?grup=1", "Trendyol yardım soruları (ödeme ve taksit)", "Taksit ve ödeme yöntemleri özeti; Trendyol Kredi Pazaryeri; sayfa açılamadı, arama sonucu özetinden alındı", OZ, D29)
    P(T + "/s/montajix-montaj-hizmeti", "Trendyol ürün sayfasında ek montaj hizmeti", "30 gün içinde randevu; tamamlanan montaj iade edilemez; sayfa açılamadı, arama sonucu özetinden alındı", OZ, D29)
    P("https://akademi.trendyol.com/satici-bilgi-merkezi/detay/275", "Trendyol satıcı bilgi merkezi: taksit ve ödeme", "Satıcı tarafı taksit ve ödeme kuralları; arama sonucu özeti", OZ, D29)
    P("https://akademi.trendyol.com/satici-bilgi-merkezi/detay/kargo-baremi-uygulamasi", "Trendyol satıcı bilgi merkezi: kargo baremi", "Satıcı bareminin 350 TL olduğu ifadesi (alıcı eşiği doğrulanamadı); arama sonucu özeti", OZ, D29)

    # ------------------------------------------------------------ Hepsiburada
    H = "https://www.hepsiburada.com"
    P(H + "/staticpage/397066447924442", "Hepsiburada mobilya ve büyük ürün teslimat, iade ve kurulum sayfası", "Mobilya birden fazla pakette ve farklı günlerde gelebilir (HepsiJET XL); adresten önceden seçilen tarihte alınır; 14 gün ücretsiz iade (demonte ve orijinal kutuyla); 69 ilde montaj (uzman ekiplerden mobilya montaj hizmeti)", [APF, CHR], [D29, D30], kod=("D23", "D28"))
    P(H + "/teslimat", "Hepsiburada teslimat sayfası: ücretsiz kargo eşiği kontrolü", "Yarın Kapında: sepet kargo bedavaya uygunsa ek ücret alınmıyor; eşik tutarı herkese açık sayfada bulunamadı", CHR, D30, kod=("D28",))
    P(H + "/odeme-secenekleri", "Hepsiburada ödeme seçenekleri", "12 aya varan taksit (Hepsiburada limiti); uygun ürünlerde kapıda nakit ödeme, üst limit 7.000 TL; alışveriş kredisi; kurumsal fatura (arama özeti)", OZ, D29)
    P(H + "/staticpage/416030025820088", "Hepsiburada ödeme ve kredi bilgi sayfası", "Alışveriş kredisi ve taksit başlıkları; sayfa açılamadı, arama sonucu özetinden alındı", OZ, D29)

    # ------------------------------------------------------------ n11, Amazon TR
    P("https://www.n11.com/destek-merkezi", "n11 destek merkezi: kargo, iade, kapıda ödeme ve kredi koşullarının doğrulanması", "Kargo için 3 seçenek (alıcı öder, mağaza öder, şartlı kargo); 14 gün cayma hakkı; kapıda ödeme yok; Garanti Alışveriş Kredisi 750-15.000 TL, 48 aya varan vade; garanti satıcı sorumluluğunda", CHR, D30, kod=("D23", "D28"))
    P("https://www.n11.com/destek-merkezi/odeme/odeme-secenekleri", "n11 ödeme seçenekleri", "Banka bazlı taksit; alışveriş kredisiyle 48 aya kadar; sayfa 403 döndü, arama sonucu özetinden alındı", OZ, D29)
    P("https://www.n11.com/kampanyalar/kredim-alisveris-kredisi-kampanyasi", "n11 alışveriş kredisi kampanyası", "Kredim 6 taksit ve İş Bankası alışveriş kredisi; arama sonucu özeti", OZ, D29)
    P("https://www.n11.com/destek-merkezi/iptal-iade-degisim/iade", "n11 iade koşulları", "14 gün cayma hakkı; arama sonucu özeti", OZ, D29)
    P("https://www.n11.com/destek-merkezi/kargo-teslimat/kargo-gonderim-sureci", "n11 kargo ve gönderim süreci", "Mağaza bazlı 300 TL şartlı kargo ifadesi (Chrome ile sayfada bulunamadı); arama sonucu özeti", OZ, D29)
    A = "https://www.amazon.com.tr/gp/help/customer/display.html?nodeId="
    P(A + "GNWCU626A4NXEEGJ", "Amazon TR standart teslimat ve ücretsiz kargo eşiği", "500 TL altında teslimat başına 49,90 TL; 500 TL ve üzeri ücretsiz", CHR, D30, kod=("D23", "D28"))
    P(A + "GKM69DUUYKQWKWX7", "Amazon TR iade koşulları", "İade süresi teslimden itibaren kategoriye göre 14 veya 30 gün; büyük üründe iade yöntemi değişebilir, evden alım sunulmayabilir", CHR, D30, kod=("D23", "D28"))
    P(A + "GRVPA5TTFNQXJ2GZ", "Amazon TR taksit seçenekleri", "Kredi kartıyla ödemede 12 aya varan taksit", CHR, D30, kod=("D23", "D28"))
    P(A + "TKE3ITKU0oMx19kIos", "Amazon TR ödeme yardım sayfası", "Fatura ve ödeme koşulları (ticari vergi mükellefi bilgisiyle fatura); arama sonucu özeti", OZ, D29)
    P(A + "GE66DNRRQVDZAR5E", "Amazon TR kargo ve iade yardım sayfası", "Sayfa 403 döndü; arama sonucu özetinden alındı", OZ, D29)

    # ------------------------------------------------------------ garanti ve servis (markalar)
    P("https://www.artema.com.tr", "Artema marka sitesi", "Marka sitesi menüsü, 360 mağaza bağlantısı, servis ve garanti girişleri", CURL, D29)
    P("https://www.artema.com.tr/garanti-hizmetleri/", "Artema garanti hizmetleri", "Sayfa mevcut, içerik statik HTML'de görünmüyor (süre okunamadı)", CURL, D29)
    P("https://www.artema.com.tr/servisler-ve-satis-noktalari", "Artema servis ve satış noktaları", "VitrA ile ortak müşteri hizmetleri ve servis sayfası", CURL, D29)
    P("https://eca.com.tr/urun/life-lavabo-bataryasi", "E.C.A. ürün sayfası örneği: garanti süresi ve yedek parça bölümü", "Life lavabo bataryasında 'Garanti Süresi: 20 Yıl' ve 'Yedek Parça Resmi' bölümü", CURL, D29)
    P("https://eca.com.tr/iletisim-bilgileri", "E.C.A. iletişim ve WhatsApp", "Servis hatları ve WhatsApp bağlantısı", CURL, D29)
    P("https://eca.com.tr/servisler", "E.C.A. yetkili servis haritası", "Yetkili servis haritası ve il bazlı servis listesi", CURL, D29)
    P("https://eca.com.tr", "E.C.A. marka sitesi ana sayfa", "Marka sitesi menüsü; servis ve tüketici köşesi girişleri", CURL, D29)
    P("https://www.geberit.com.tr/anasayfa/", "Geberit Türkiye ana sayfa", "Marka sitesi menüsü; hizmet ve destek girişi", CURL, D29)
    P("https://www.geberit.com.tr/hizmet-ve-destek/iletisim/", "Geberit Türkiye iletişim", "Müşteri hattı ve iletişim bilgileri", CURL, D29)
    P("https://www.geberit.com.tr/banyo-urunleri/ilham-alin/bayiler-yetkili-servisler/", "Geberit Türkiye bayi ve yetkili servisler", "Ürün, yedek parça ve teknik destek için bayi ve yetkili servis listesi", [CURL, CHR], [D29, D30], kod=("D23", "D28"))
    P("https://www.geberit.com.tr/hizmet-ve-destek/medya-merkezi/", "Geberit Türkiye medya merkezi: garanti koşulları PDF'i", "Geberit Banyo Ürünleri ve Serileri Garanti Koşulları (PDF); süre sayfada yazmıyor", CHR, D30, kod=("D28",))
    P("https://www.grohe.com/tr-TR", "Grohe Türkiye ana sayfa", "Marka sitesi menüsü; servis ve destek girişi", CURL, D29)
    P("https://www.grohe.com/tr-TR/servis-destek/garanti", "Grohe Türkiye garanti sayfası", "Seçili ürünlerde 10 yıla kadar; 2 yıl (çevrim içi kayıtla +1 yıl) ve 5 yıl; garanti kapsamında yedek parça 48 saatte teslim", CURL, D29)
    P("https://www.grohe.com/tr-TR/servis-destek/bayi-bulucu", "Grohe Türkiye bayi bulucu ve servis talebi", "Servis talebi formu ve bayi bulucu; yedek parça bulucu", CURL, D29)
    P("https://www.duravit.com.tr/servis_hizmeti/teknik_servisler.tr-tr.html", "Duravit Türkiye teknik servisler", "İl bazlı teknik servis listesi; tüm Türkiye'ye yayılan servis ağı", CHR, D30, kod=("D23", "D28"))
    P("https://www.duravit.com.tr/servis_hizmeti/faqs.tr-tr.html", "Duravit Türkiye SSS: garanti", "Ürüne bağlı gönüllü üretici garantisi; süre belirtilmemiş", CHR, D30, kod=("D28",))

    # ------------------------------------------------------------ sosyal profiller
    sy = [
        ("https://www.youtube.com/user/VitrAglobal/about", "VitrA Türkiye YouTube kanalı", "1,58 Mn abone, 402 video, 55.846.765 görüntüleme; 18 Ağu 2011'de katılım"),
        ("https://www.youtube.com/user/ArtemATurkiye/about", "Artema YouTube kanalı", "4,75 B abone, 33 video, 19.702.538 görüntüleme; 3 Eki 2012'de katılım"),
        ("https://www.youtube.com/user/CanakkaleSrmk/about", "Kale (Çanakkale Seramik) YouTube kanalı", "948 abone, 577 video, 1.405.640 görüntüleme; 2 Mar 2012'de katılım"),
        ("https://www.youtube.com/user/creavitturkiye/about", "Creavit YouTube kanalı", "2,17 B abone, 227 video, 7.055.522 görüntüleme; 22 Mar 2013'te katılım"),
        ("https://www.youtube.com/grohe/about", "Grohe Türkiye YouTube kanalı", "75,1 B abone, 627 video, 21.947.546 görüntüleme; 2 Mar 2007'de katılım"),
    ]
    for u, a, b in sy:
        ekle(u, a + ": abone, video ve görüntüleme sayıları (sosyal kanal karşılaştırması)", b, bolum=["politika"], yontem=CURL, tarih=D29, kod=["D23"])
    sp = [
        ("https://tr.pinterest.com/vitrabathrooms/", "VitrA Bathrooms Pinterest hesabı", "1.478 takipçi"),
        ("https://tr.pinterest.com/DesignStudioVitrA/", "Design Studio VitrA Pinterest hesabı (Artema sayfası bu hesaba bağlanıyor)", "3.825 takipçi"),
        ("http://www.pinterest.com/canakkalesrmk/", "Kale Pinterest hesabı", "943 takipçi"),
        ("https://tr.pinterest.com/creavitturkiye/", "Creavit Pinterest hesabı", "187 takipçi"),
        ("https://www.pinterest.com/grohe/", "Grohe Pinterest hesabı", "10.325 takipçi"),
    ]
    for u, a, b in sp:
        ekle(u, a + ": takipçi sayısı (sosyal kanal karşılaştırması)", b, bolum=["politika"], yontem=CURL, tarih=D29, kod=["D23"])
    ig = [
        ("https://www.instagram.com/vitraturkiye/", "VitrA Türkiye Instagram", "~144K takipçi, 1.8K+ gönderi (Google SERP snippet'inden, yaklaşık)"),
        ("https://www.instagram.com/artematurkiye/", "Artema Instagram", "~20K takipçi, 579 gönderi (SERP'ten, yaklaşık)"),
        ("https://www.instagram.com/canakkaleseramik/", "Kale Instagram", "Sayı SERP'te görünmedi, alınamadı"),
        ("https://www.instagram.com/creavitturkiye/", "Creavit Instagram", "Sayı SERP'te görünmedi, alınamadı"),
        ("https://www.instagram.com/elginkaneca/", "E.C.A. (Elginkan) Instagram", "~24K takipçi, 1694 gönderi (SERP'ten, yaklaşık)"),
        ("https://www.instagram.com/geberit.tr/", "Geberit Türkiye Instagram", "~39K takipçi, 806 gönderi (SERP'ten, yaklaşık)"),
        ("https://www.instagram.com/groheturkiye/", "Grohe Türkiye Instagram", "Sayı SERP'te görünmedi, alınamadı"),
    ]
    for u, a, b in ig:
        ekle(u, a + " profil sayısı (giriş gerektirdiğinden sayfa açılmadı)", b, bolum=["politika"], yontem="API (DataForSEO SERP snippet)", tarih=D29, kod=["D23"])
    ekle("https://www.tiktok.com/@banyobutarafta", "Creavit TikTok hesabı (VitrA ve Artema için resmi hesap bulunamadı)", "~118 takipçi (SERP'ten, yaklaşık)", bolum=["politika"], yontem="API (DataForSEO SERP snippet)", tarih=D29, kod=["D23"])
