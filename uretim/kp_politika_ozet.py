# -*- coding: utf-8 -*-
"""kanal_politikalari/ozet.md uretimi: politikalar.json, sosyal.json, gbp.json ve shopping_blok.json okunur; tablolar bu dosyalardan uretilir."""
import json, os, re
from kp_politika_ortak import KOK
def yukle(a): return json.load(open(os.path.join(KOK, a), encoding="utf-8"))
def vn(a): return re.sub(r"(?i)v[ıiİ]tra", "VitrA", a or "")
def n(x): return "{:,}".format(x).replace(",", ".")
def ond(x, d=2): return ("%.*f" % (d, x)).replace(".", ",") if x is not None else "-"
def tablo(basliklar, satirlar):
    s = "| " + " | ".join(basliklar) + " |\n|" + "|".join(["---"] * len(basliklar)) + "|\n"
    for r in satirlar: s += "| " + " | ".join(str(c).replace("|", "/") for c in r) + " |\n"
    return s
def uret():
    pol, sos, gbp, shp = yukle("politikalar.json"), yukle("sosyal.json"), yukle("gbp.json"), yukle("shopping_blok.json")
    T = "29 Eylül 2026"
    m = []
    A = m.append
    A("# VitrA Türkiye · Kanal politikaları ve keşif kanalları araştırması\n")
    A("Erişim tarihi: %s. Kapsam: müşteri verisi gerektirmeyen, kamuya açık kaynaklardan derlenen altı başlık (ödeme ve taksit; kargo, teslimat, kurulum ve iade; garanti ve servis; sosyal ve keşif kanalları; Google Business Profile; Google SERP'te Shopping blokları).\n" % T)
    A("Yöntem: sayfalar tarayıcı User-Agent'ı ile curl üzerinden okundu (istekler arası 3-6 sn); bot korumalı sayfalarda Apify rag-web-browser kullanıldı; Trendyol, n11, Amazon TR ve bazı Hepsiburada/Koçtaş sayfaları açılamadığı için ilgili hücreler arama sonucu özetinden alınmış ve tabloda 'arama özeti' olarak işaretlenmiştir. Başlık 4-6 verileri DataForSEO (Google TR, location_code 2792, dil tr) üzerinden çekildi. Betikler: `uretim/kp_politika_*.py`. Ham dosyalar bu klasörde (`sayfalar/`, `*_ham.json`).\n")
    A("Okuma notu: 'Bulunamadı' ifadesi bilginin sayfada bulunmadığı veya sayfanın statik HTML'de görünmediği anlamına gelir; olmadığı anlamına gelmeyebilir. Güven sütunu: sayfa = sayfa metninden doğrudan okundu, kısmi = bir bölümü okundu, arama özeti = sayfa açılamadı, doğrulanmadı.\n")
    # ---- 1
    A("## 1. Ödeme ve taksit koşulları karşılaştırması\n")
    A(tablo(["Site", "Taksit ve vade farksız koşul", "Kart ve kampanya", "Alışveriş kredisi", "Kapıda ödeme", "Kurumsal fatura", "Güven"], [
        ["vitra.com.tr", "Şeritte 'tüm ürünlerde vade farksız 6 ay taksit' (eşiksiz); ürün tablosunda 12 taksite kadar, 8-9-12 çoğunlukla vade farklı", "21 Eylül - 30 Kasım 2026: seçili renkli ürünlerde %40 indirim, 9 aya varan taksit, 40.000 TL ve üzeri ücretsiz montaj", "Bulunamadı", "Yok (yalnızca kredi kartı; iyzico, 3D Secure)", "Var (sepette)", "sayfa"],
        ["Koçtaş", "Online 5.000 TL üzeri 7 taksite kadar vade farksız (mağazada 10.000 TL üzeri); vade farklı 9 taksite kadar", "Taksit kampanyası 30 Eylül 2026'ya kadar; Flexi kart, aidatsız kart ve TEB Worldcard kapsam dışı", "Koçtaş Kart var; kredi bulunamadı", "Bulunamadı", "Bulunamadı", "sayfa"],
        ["Bauhaus TR", "2.500 TL ve üzeri anlaşmalı banka kartlarıyla vade farksız; azami taksit yazmıyor", "Ana sayfada internete özel kampanya etiketleri", "Bulunamadı", "Yok (havale/EFT var)", "Kurumsal müşteri servisi ve Kurumsal Kart", "sayfa"],
        ["IKEA TR", "1.500 TL üzeri 3 taksit; IKEA Aile üyelerine 7.500 TL üzeri 6, 20.000 TL üzeri 9 taksit (belirli kartlar)", "5 Ocak 2026 - 3 Ocak 2027 arası geçerli; diğer kartlarda tek çekim", "Bulunamadı", "Yok (Full 3D kart)", "IKEA Kurumsal Kart", "sayfa"],
        ["Kale", "Uygulanamaz: kale.com.tr'de sepet ve online satış yok, satış noktalarına yönlendirir", "-", "-", "-", "-", "sayfa"],
        ["Creavit e-mağaza", "Peşin fiyatına 6 ve 9 taksit ifadeleri birlikte görünüyor", "30 gün ücretsiz iade ve değişim; 3.000 TL üzeri ücretsiz kargo", "Bulunamadı", "Bulunamadı", "Bulunamadı", "sayfa"],
        ["Banyomarka", "Ürün kartında 4 taksit", "Grohe kampanyalı batarya ve duş seti sayfaları", "Bulunamadı", "İstanbul içi kapıda nakit ödeme", "Bulunamadı", "sayfa"],
        ["Banyoline", "Şeritte 'peşin fiyatına 12 ay taksit'", "Kampanyalar sayfası", "Bulunamadı", "Bulunamadı", "Bulunamadı", "sayfa"],
        ["Trendyol", "Kategori, tutar ve kart tipine göre; her üründe taksit yok", "Bankalara özel kampanyalar", "Trendyol Kredi Pazaryeri", "Doğrulanamadı", "Mümkün", "arama özeti"],
        ["Hepsiburada", "12 aya varan taksit (Hepsiburada limiti)", "Mobilya sayfasında alışveriş kredisi ve taksit başlığı", "Var", "Uygun ürünlerde kapıda nakit, üst limit 7.000 TL", "Mümkün", "kısmi"],
        ["n11", "Banka bazlı; alışveriş kredisiyle 48 aya kadar", "Kredim 6 taksit, İş Bankası alışveriş kredisi", "Var (Garanti 750-15.000 TL)", "Yok", "Doğrulanamadı", "arama özeti"],
        ["Amazon TR", "12 aya varan taksit (uygun kategorilerde)", "Doğrulanamadı", "Bulunamadı", "Doğrulanamadı", "Var (ticari vergi mükellefi bilgisi)", "arama özeti"],
    ]))
    A("Kaynak: vitra.com.tr/odeme-rehberi, /kampanyalar ve ürün sayfası; koctas.com.tr/taksitler; bauhaus.com.tr/taksit-secenekleri ve /sss; ikea.com.tr/odeme-secenekleri; shop.creavit.com.tr; banyomarka.com (/musteri-hizmetleri.xhtml, /satis-sozlesmesi.shtm); banyoline.com; hepsiburada.com/staticpage/397066447924442; Trendyol, n11 ve Amazon TR yardım sayfaları (arama özeti). Erişim: %s.\n" % T)
    A("**Bulgular**\n")
    A("- VitrA sitesinde taksit mesajı üç farklı düzeyde görünüyor: şeritte 6 ay vade farksız, kampanya sayfasında 9 aya varan taksit, ürün tablosunda 12 taksite kadar seçenek. Rakiplerde vade farksız taksit tutar eşiğine bağlı (Koçtaş 5.000 TL, Bauhaus 2.500 TL, IKEA 1.500 TL); VitrA şeridi eşik belirtmiyor. Aynı sepet tutarıyla karşılaştırma yapılmadığı için üstünlük ifadesi kullanılmamıştır.")
    A("- Kapıda ödeme yalnızca Banyomarka (İstanbul içi) ve Hepsiburada'da (uygun ürünler, 7.000 TL üst limit) görülüyor; VitrA'da yalnızca kredi kartı akışı tanımlı. Havale/EFT Bauhaus ve Banyomarka'da açıkça yazılıyor, VitrA ödeme rehberinde geçmiyor.")
    A("- Alışveriş kredisi Hepsiburada, n11 ve Trendyol Kredi Pazaryeri üzerinden sunuluyor; markalı sitelerin hiçbirinde bulunamadı. Banyo yenilemede sepet tutarı (BM seti + montaj kalemleri 4.000 TL ve üzeri) düşünüldüğünde finansman seçeneği rakip markalı sitelerde de boş bir alan.")
    A("- Creavit e-mağazasında banner (9 taksit) ile alt metin (6 taksit) farklı; Banyoline 12 ay peşin fiyatına taksit şeridiyle bayi kanalında en yüksek taksit mesajını taşıyor.\n")
    A("**VitrA için fırsatlar**\n")
    A("- Şerit, kampanya sayfası ve ürün tablosundaki taksit ifadelerinin tek çatı mesajda (ör. eşik ve dönem bilgisiyle) birleştirilmesi değerlendirilebilir; önceki turdaki autocomplete verisinde 'vitra taksit seçenekleri' ve '9 taksit' önerileri bu netliğe işaret ediyor.")
    A("- Havale/EFT ve kurumsal fatura seçeneğinin ödeme rehberinde görünür yazılması, profesyonel alıcılar için (Profesyonellere Özel menüsüyle birlikte) fayda sağlayabilir.")
    A("- Banyo yenileme sepetleri için bankalarla alışveriş kredisi ya da uzun vadeli taksit iş birliği araştırılabilir; Banyo Asistanı akışındaki '9 taksit' ifadesiyle uyumlu bir mesaj kurulabilir.\n")
    # ---- 2
    A("## 2. Kargo, teslimat, kurulum ve iade koşulları\n")
    A(tablo(["Site", "Ücretsiz kargo eşiği", "Büyük ürün teslimat", "Kat teslimi", "İade süresi", "Büyük ürün iade koşulu", "Güven"], [
        ["vitra.com.tr", "Eşiksiz (şeritte 'tüm ürünlerde ücretsiz kargo')", "En fazla 3 iş günü içinde kargo veya lojistik firmasına teslim; ürün sayfasında tahmini kargoya teslim tarihi", "'Kapınıza kadar'; kat teslimi belirtilmemiş", "Ürün sayfasında 30 güne kadar ücretsiz iade (iade rehberinde gün yazmıyor)", "Büyük paket adresten lojistik firmasıyla alınır; para iadesi kartta 5, debit kartta 15 iş gününe kadar", "sayfa"],
        ["Koçtaş", "300 TL ve 600 TL şeklinde iki farklı değer (arama özeti); doğrulanamadı", "Nakliye: sipariş tarihinden 4 gün içinde 09:00-19:00 (arama özeti)", "Bulunamadı", "14 gün kolay iade", "İade kodu 7 gün geçerli, ücretsiz (arama özeti)", "kısmi"],
        ["Bauhaus TR", "1.000 TL ve üzeri (belirlenen ürünlerde); şubelerden 40.000 TL ve üzeri şehir içi 30 km'ye kadar ücretsiz nakliye", "30 desi altı Yurtiçi/KolayGelsin, üstü Horoz/Arvato; adalar ve uzak yerleşimler kapsam dışı", "Bulunamadı", "14 gün (iade kodu 7 gün içinde kargoya)", "Demonte üründe kurulumdan sonra iade yok; klozet takımı ve kapağında ambalajı açılmamış ve denenmemiş şartı", "sayfa"],
        ["IKEA TR", "Eşik yok; minimum sipariş 500 TL, kargo 299 TL (1.500 TL'ye kadar) ile 799 TL (7.500 TL'ye kadar), üstünde %11", "Arvato, Horoz, HepsiJET, Yurtiçi, KolayGelsin; şehir içi ayrı nakliye hizmeti", "Daire kapısına kadar", "İnternet 14 gün (ücretsiz), mağaza 30 gün", "Ambalajı açılmamış orijinal kutu; özel kesim ürünler iade dışı", "sayfa"],
        ["Kale", "Uygulanamaz", "Uygulanamaz", "-", "-", "-", "sayfa"],
        ["Creavit e-mağaza", "3.000 TL üzeri", "Banka onayından sonra 5 iş günü içinde kargoya, kargo 1-5 gün", "Bulunamadı", "30 gün ücretsiz iade ve değişim", "Bulunamadı", "sayfa"],
        ["Banyomarka", "Seçili ürünlerde; banner'da İstanbul içi 250 TL (güncelliği belirsiz)", "3 iş günü içinde kargoya, kargo 1-3 gün; stokta yoksa 4-30 gün", "Bulunamadı", "Ürün kartında 30 gün; hatalı üründe 15 gün içinde bildirim", "Kullanılmış üründe iade ve değişim yok", "sayfa"],
        ["Banyoline", "Ana sayfada tüm alışverişlerde ücretsiz hızlı kargo", "Yasal 30 günü aşmayan bölgeye bağlı süre", "Bulunamadı", "İptal ve iade talebi formu", "Ücretsiz montaj yapılan üründe ön hazırlık yönergesine uyulmazsa iade ve ikinci montaj yok", "sayfa"],
        ["Trendyol", "Satıcı barem 350 TL; alıcı eşiği doğrulanamadı", "Satıcının anlaşmalı taşıma şirketi; süre uzayabilir", "Doğrulanamadı", "15 gün", "Belirli boyutta ürün adresten alınır; montajı tamamlanmış ürün iade edilemez", "arama özeti"],
        ["Hepsiburada", "Bulunamadı", "Mobilya birden fazla pakette ve farklı günlerde gelebilir (HepsiJET XL)", "Bulunamadı", "14 gün, ücretsiz, demonte ve orijinal kutuyla", "Adresten önceden seçilen tarihte alınır", "sayfa"],
        ["n11", "Mağaza bazlı 300 TL şartı", "Bulunamadı", "Bulunamadı", "14 gün cayma hakkı", "Bulunamadı", "arama özeti"],
        ["Amazon TR", "500 TL ve üzeri (altı 49,90 TL)", "Bulunamadı", "Bulunamadı", "14 veya 30 gün", "Yöntem ürün boyutuna göre değişiyor", "arama özeti"],
    ]))
    A("**Kurulum ve montaj**\n")
    A(tablo(["Site", "Montaj seçeneği ve fiyat", "Hasar politikası"], [
        ["vitra.com.tr", "Sitede satın alınan montaj hizmeti, 1 yıl servis garantisi: klozet 2.750 TL, gömme rezervuar 3.900, banyo mobilyası seti 4.000, lavabo 2.300, armatür ve duş 2.350, büyük 5.300, keşif 1.400 TL (duşakabin sayfasında +5.300 TL); 40.000 TL üzeri kampanyada ücretsiz; bazı ürünlerde 'Ücretsiz Montaj' rozeti", "Teslimde paket kontrolü; kırık ve hasarlı üründe kargo personelinin tutanak tutması"],
        ["Creavit e-mağaza", "11 kalem: asma/takım klozet 2.450 TL, rezervuar/iç takım 1.750, armatür/duş 1.750, lavabo 2.450, banyo mobilyası alt modül 2.450, boy dolabı 1.400, demonte takım 3.900 TL (söküm hariç)", "Bulunamadı"],
        ["Banyoline", "Yalnızca İstanbul'da ücretsiz montaj: Orka seçili dolaplar ve VitrA Metropole Edge, Valarte, Nest Trendy, Sento, Root modelleri; batarya ve ara musluk montajı ve ölçü alma yok", "Teslim alırken kontrol alıcıda"],
        ["Koçtaş", "20 ilde montaj (İstanbul, Ankara, İzmir başta); seçili aydınlatma ve mobilyada ücretsiz montaj; Ustabilir hizmeti", "Bulunamadı"],
        ["Bauhaus TR", "Usta temini müşteri hizmetleri üzerinden; fiyat bulunamadı", "Hasar tespit tutanağı zorunlu; tutanak yoksa kargo kaynaklı olduğu ispatlanamıyor"],
        ["IKEA TR", "Sepette veya sipariş numarasıyla montaj; bölgeye göre fiyat; kurulumdan itibaren 2 yıl garanti", "Bulunamadı"],
        ["Hepsiburada", "69 ilde montaj; sepete eklenebilir; Mr Usta Klozet Montaj Hizmeti 2.730 TL (önceki tur verisi)", "Ürün kargo görevlisinin yanında kontrol edilir; hasarlı pakette teslim alınmayabilir"],
        ["Trendyol", "Ürün sayfasında ek montaj hizmeti; 30 gün içinde randevu; tamamlanan montaj iade edilemez", "Kurulum gerektiren ürünlerde yetkili servis bilgisi olmadan açılan ürün iade dışı kalabilir"],
    ]))
    A("Kaynak: vitra.com.tr/teslimat-rehberi, /degisim-iade-rehberi, /c-montaj-hizmeti ve ürün sayfaları; koctas.com.tr ana sayfa (Apify) ve arama özeti; bauhaus.com.tr/ucretsiz-kargo, /iade, /sss, /servisler; ikea.com.tr/nakliye-hizmeti, /montaj-hizmeti, /iade-politikasi; shop.creavit.com.tr/pages/teslimat-kosullari ve /collections/montaj-hizmeti; banyomarka.com/teslimat-kosullari.shtm ve /garanti-ve-iade-kosullari.shtm; banyoline.com/montaj-hizmeti ve /mesafeli-satis-sozlesmesi; hepsiburada.com/staticpage/397066447924442; Trendyol, n11, Amazon TR (arama özeti). Erişim: %s.\n" % T)
    A("**Bulgular**\n")
    A("- VitrA, eşiksiz ücretsiz kargo ve ürün sayfasında 30 günlük ücretsiz iade ifadesiyle karşılaştırılan sitelerin çoğundan geniş bir vaat taşıyor (Bauhaus 1.000 TL eşik, Creavit 3.000 TL eşik, IKEA ücretli kargo). İade süresi ise Bauhaus, IKEA ve Hepsiburada'da 14 gün, Trendyol'da 15 gün; VitrA ve Creavit e-mağazası 30 gün.")
    A("- İade rehberi sayfasında gün sayısı yazmıyor, süre yalnızca ürün sayfasında görünüyor; iki yüzeyin aynı ifadeyle desteklenmesi değerlendirilebilir.")
    A("- Klozet gibi hijyen ürünlerinde iade koşulu Bauhaus'ta açıkça yazılı (ambalajı açılmamış ve denenmemiş); VitrA sayfalarında klozet iadesine özel bir koşul bulunamadı. Kurulumdan sonra iade konusu (Bauhaus, Trendyol, Banyoline'da kısıtlı) VitrA sayfalarında da netleştirilebilir.")
    A("- Montaj tarafında VitrA sitede fiyatlı ve servis ağına bağlı bir akışa sahip (76 servis noktası). Creavit e-mağazasında klozet montajı 2.450 TL, VitrA'da 2.750 TL; armatür ve duşta Creavit 1.750 TL, VitrA 2.350 TL (kapsam ve söküm koşulları farklı olduğundan birebir kıyas yapılmamıştır).")
    A("- Banyoline'ın İstanbul'da VitrA Metropole Edge, Valarte, Nest Trendy, Sento ve Root modellerini kapsayan ücretsiz montajı, VitrA ürünlerinin bayi kanalında montaj avantajıyla satıldığını gösteriyor.\n")
    A("**VitrA için fırsatlar**\n")
    A("- Teslimat ve iade rehberi sayfalarına kat/daire teslimi, hasarlı teslimde adımlar, klozet ve kurulum sonrası iade koşulu ile iade süresinin (30 gün) eklenmesi, rakip sayfalardaki netlikle uyumlu bir zemin sağlayabilir.")
    A("- 'Ücretsiz Montaj' rozetinin hangi ürün ve tutar için geçerli olduğunun ürün ve kategori sayfalarında tek biçimde gösterilmesi düşünülebilir (bugün rozet, kampanya sayfası ve ürün tablosu ayrı görünüyor).")
    A("- Banyoline gibi bayilerin İstanbul dışına yayılabilecek ücretsiz montaj modeline karşılık, servis ağı bulunan illerde kapsamın görünür kılınması test edilebilir.\n")
    # ---- 3
    A("## 3. Garanti, yedek parça ve servis iletişimi\n")
    A(tablo(["Marka", "Garanti süresi", "Yedek parça", "Servis randevu akışı", "WhatsApp / canlı destek", "Güven"], [
        ["VitrA", "Ürün sayfalarında süre yazmıyor; V-Care akıllı klozette 2 yıl (ek paketle 4 yıl ve yıllık periyodik bakım); '+2 yıl ek garanti' sayfası var", "Ayrı sayfa bulunamadı; gömme rezervuar montaj aksesuarları kategorisi var", "Online servis randevusu; garanti talep formu (fatura kaydı); 0850 311 70 70 (Pzt-Cts 09:00-18:00)", "WhatsApp bulunamadı; destek alanında 'Çevrim dışı' etiketi görünüyor, canlı sohbet doğrulanamadı", "sayfa"],
        ["Artema", "'Garanti Hizmetleri' sayfası var, içerik statik HTML'de görünmüyor", "Bulunamadı", "VitrA ile ortak müşteri hizmetleri ve servis sayfası; 360 mağaza bağlantısı", "Bulunamadı", "kısmi"],
        ["Kale", "Seramik sağlık gereçleri ve armatürler 10 ve 5 yıl, musluk 2 yıl, duş sistemleri ve gömme rezervuar 5 yıl; servis işçiliği 1 yıl", "Ayrı sayfa bulunamadı; kullanım kılavuzları sayfası var", "Yetkili servisler sayfasından talep; 0850 800 52 53", "WhatsApp destek hattı var", "sayfa"],
        ["Creavit", "Seramik 12, gömme rezervuar 10, armatür ve duş 5 yıl (arama özeti)", "Katalogda 'Yedek Parça Listesi' (arama sonucu)", "Yetkili servisler sayfası; e-mağaza hattı 0850 330 00 67 (Pzt-Cuma 08:30-17:30)", "Bulunamadı", "kısmi"],
        ["ECA", "Ürün sayfasında 'Garanti Süresi: 20 Yıl' (Life lavabo bataryası)", "Ürün sayfasında 'Yedek Parça Resmi' bölümü", "Yetkili servis haritası; 444 0 322 ve 0850 800 0 322", "WhatsApp bağlantısı var", "sayfa"],
        ["Geberit TR", "Vitrifiyede ömür boyu, AquaClean için 10 yıl yedek parça bulunabilirliği (arama özeti)", "Ürün bulunabilirliği ve yedek parça sayfası (arama sonucu)", "Bayi ve yetkili servis sayfası; 0 850 811 62 63", "Bulunamadı", "kısmi"],
        ["Grohe TR", "Seçili ürünlerde 10 yıla kadar; 2 yıl (çevrim içi kayıtla +1 yıl) ve 5 yıl", "Yedek parça bulucu; garanti kapsamında 48 saatte teslim", "Servis talebi formu ve bayi bulucu", "Bulunamadı", "sayfa"],
        ["Duravit TR", "Bulunamadı", "Bulunamadı", "Teknik servisler sayfası (il bazlı, arama sonucu)", "Bulunamadı", "arama özeti"],
    ]))
    A("Kaynak: vitra.com.tr/garanti-hizmetleri, /musteri-hizmetleri, /garanti-talep-formu, /servisler-ve-satis-noktalari (161 satış, 76 servis noktası); artema.com.tr/garanti-hizmetleri; kale.com.tr/sikca-sorulan-sorular ve /yetkili-servisler-ve-hizmetler; creavit.com.tr yetkili servisler ve shop.creavit.com.tr/pages/contact; eca.com.tr/urun/life-lavabo-bataryasi ve /iletisim-bilgileri; geberit.com.tr/hizmet-ve-destek/iletisim; grohe.com/tr-TR/servis-destek/garanti; duravit.com.tr teknik servisler. Erişim: %s.\n" % T)
    A("**Bulgular**\n")
    A("- ECA (20 yıl), Kale (10 ve 5 yıl tablosu) ve Grohe (10 yıla kadar, 48 saat yedek parça taahhüdü) garanti sürelerini açık yazıyor; VitrA'da süre bilgisi ürün sayfalarında bulunamadı, yalnızca V-Care akıllı klozet ve ek garanti paketi için var.")
    A("- Yedek parça yüzeyi rakiplerde ürün sayfasında (ECA yedek parça resmi), araçla (Grohe yedek parça bulucu) veya katalogda (Creavit yedek parça listesi) mevcut; VitrA'da ayrı bir yedek parça girişi bulunamadı. Arama tarafında autocomplete önerilerinin %18'i tamir ve yedek parça niyetli.")
    A("- WhatsApp hattı Kale ve ECA'da, Banyomarka'da var; VitrA'da bulunamadı. VitrA'nın güçlü yönü online servis randevusu ve resmi noktalar sayfasındaki 76 servis noktası.\n")
    A("**VitrA için fırsatlar**\n")
    A("- Ürün sayfalarına garanti süresinin ve kapsamının (rakip sayfalardaki gibi) eklenmesi ve garanti talep formu ile ek garanti paketine ürün sayfasından bağlantı verilmesi değerlendirilebilir.")
    A("- Ürün koduna göre yedek parça bulucu veya 'yedek parça resmi' bölümü, tamir arama niyetine karşılık gelebilir; YouTube'daki tamir videosu boşluğuyla birlikte ele alınabilir.")
    A("- WhatsApp veya canlı destek kanalının servis randevusu ve montaj sorularına açılması test edilebilir.\n")
    # ---- 4
    A("## 4. Sosyal ve keşif kanalları\n")
    def hucre(x): return x if x else "-"
    rows = []
    for r in sos["markalar"]:
        ig = r["instagram"]; yt = r["youtube"]; pn = r["pinterest"]; tt = r["tiktok"]
        rows.append([r["marka"],
                     ("~%sK (SERP'ten, yaklaşık); %s gönderi" % (n(round(ig["takipci_yaklasik"] / 1000)), ig["gonderi_metin"] or "-")) if ig["takipci_yaklasik"] else "Alınamadı (sayı SERP'te görünmedi)",
                     ("%s; %s; %s" % (yt["abone"], yt["video"], yt["goruntuleme"])) if yt else "Ayrı TR kanalı bulunamadı",
                     ("%s takipçi" % n(pn["takipci"])) if pn and pn["takipci"] else "Resmi hesap bulunamadı",
                     ("%s takipçi (SERP'ten, yaklaşık)" % n(tt["takipci_yaklasik"])) if tt else "Resmi hesap bulunamadı"])
    A(tablo(["Marka", "Instagram", "YouTube (abone; video; toplam görüntüleme)", "Pinterest", "TikTok"], rows))
    A("Notlar: YouTube ve Pinterest sayıları profil sayfalarından, Instagram ve TikTok sayıları girişe kapalı olduğu için Google SERP snippet'inden alınmıştır. VitrA YouTube kanalı @VitrATürkiye adresine yönleniyor (2011'den beri, 402 video). Pinterest'te VitrA için iki hesap görünüyor: VitrA Bathrooms (1.478 takipçi) ve Design Studio VitrA (3.825; Artema sayfası bu hesaba bağlanıyor). Grohe ve Geberit için Türkiye'ye özel YouTube kanalı bulunamadı; tabloda Grohe için global kanal (75,1 bin abone) ve Geberit için Geberit Group kanalı (69,7 bin abone) yer alıyor, karşılaştırmada global olarak okunması uygundur. Creavit TikTok hesabı @banyobutarafta. ECA TikTok aramasında çıkan hesaplar Türkiye markasına ait görünmediği için alınmadı. Kaynak: YouTube /about ve Pinterest profil sayfaları (curl), Google SERP (DataForSEO). Erişim: %s.\n" % T)
    A("**Pinterest'te 'banyo' temalı görünürlük (9 sorgu: 8'i site:pinterest.com, 1'i doğal arama; Google TR SERP)**\n")
    pg = sos["pinterest_gorunurluk"]
    rows = []
    for q in pg["sorgular"]:
        mk = q["markalar"]
        rows.append([q["sorgu"], "Evet" if q["marka_adli_sorgu"] else "Hayır", q["pinterest_sonuc"], ", ".join("%s %d" % (k, v["sonuc"]) for k, v in mk.items()) or "Marka adı geçen sonuç yok"])
    A(tablo(["Sorgu", "Marka adlı sorgu", "Pinterest sonucu", "Sonuç başlığı/açıklamasında marka adı geçen pin sayısı"], rows))
    nt = pg["marka_toplam_markasiz_sorgular"]
    gor = ", ".join("%s %d" % (k, v["top30_sonuc"]) for k, v in nt.items() if v["top30_sonuc"])
    A("Marka adı içermeyen 5 sorguda (banyo dolabı modelleri, modern banyo tasarımları, banyo dekorasyon fikirleri, küçük banyo dekorasyonu, lavabo bataryası modelleri) marka adı geçen pin sayısı: %s. VitrA ve Artema yalnızca marka adlı sorgularda görünüyor (VitrA marka adlı dört sorguda %d, Artema %d pin). Eşleşme sonuç başlığı, açıklaması ve adresinde marka adının geçmesine göredir; pin görselleri okunmamıştır.\n" % (gor or "yok", pg["marka_toplam_tum_sorgular"]["VitrA"]["top30_sonuc"], pg["marka_toplam_tum_sorgular"]["Artema"]["top30_sonuc"]))
    A("**Bulgular**\n")
    A("- YouTube'da VitrA, karşılaştırılan markalar arasında belirgin biçimde önde: 1,58 Mn abone ve 55,8 Mn görüntüleme; Artema 4,75 bin, Creavit 2,17 bin, ECA 5,1 bin, Kale 948 abone. Instagram'da VitrA ~144K, Geberit TR ~39K, ECA ~24K, Artema ~20K (yaklaşık, SERP'ten).")
    A("- Pinterest'te VitrA hesapları küçük (1.478 ve 3.825 takipçi) ve banyo temalı markasız aramalarda VitrA görünmüyor; tema aramalarında banyo markaları genel olarak sınırlı görünüyor (yalnızca Ideal Standard için 1 pin eşleşmesi). Bu kanal için yönlendirme, marka adlı aramalar dışında henüz kurulmamış bir keşif alanı gibi okunabilir.")
    A("- TikTok'ta VitrA ve Artema için resmi hesap bulunamadı; yalnızca Creavit'in 118 takipçili hesabı görülüyor. Araştırmada izlenen tamir ve montaj niyetli içerik (YouTube'da görülen kanal boşluğu) TikTok için de açık bir alan.\n")
    A("**VitrA için fırsatlar**\n")
    A("- Pinterest'te banyo teması pinlerinin (küçük banyo, banyo dolabı modelleri) ürün sayfalarına bağlanan zengin pin ve pano yapısıyla desteklenmesi test edilebilir.")
    A("- YouTube'daki abone ve görüntüleme avantajının montaj, tamir ve yedek parça videolarıyla (önceki turdaki kanal boşluğu) arama niyetine bağlanması değerlendirilebilir.\n")
    # ---- 5
    g = gbp
    mg, sv = g["magaza"], g["servis"]
    A("## 5. Google Business Profile · VitrA mağazaları\n")
    A("Yöntem: DataForSEO Google Maps SERP (`serp/google/maps/live/advanced`, location_code 2792, dil tr); 'vitra banyo mağazası <yer>' sorguları 81 il ve 22 İstanbul ilçesi için çalıştırıldı, sorgu başına ilk 20 sonuç alındı, kayıtlar cid ile tekilleştirildi. Maliyet %s USD. Kimlik bilgisi çıktıya yazılmadı.\n" % ond(g["maliyet_usd"], 3))
    A(tablo(["Gösterge", "Değer"], [
        ["Google Maps'te VitrA etiketli satış noktası profili (tekil)", n(mg["kayit"])],
        ["Bunlardan puanı ve yorumu olan profil", n(mg["puanli_kayit"])],
        ["Toplam yorum sayısı (satış noktaları)", n(mg["toplam_yorum"])],
        ["Ortalama puan (yorum ağırlıklı / düz)", "%s / %s" % (ond(mg["ortalama_puan_yorum_agirlikli"]), ond(mg["ortalama_puan_duz"]))],
        ["Profil başına yorum (medyan)", mg["medyan_yorum"]],
        ["10'dan az yorumlu profil", n(mg["yorum_10_alti"])],
        ["4,0 puanın altındaki profil", n(mg["puan_4_alti"])],
        ["Yetkili servis profili (tekil) ve toplam yorum", "%s profil, %s yorum, ortalama %s" % (n(sv["kayit"]), n(sv["toplam_yorum"]), ond(sv["ortalama_puan_yorum_agirlikli"]))],
        ["Mağaza dışı veya belirsiz kayıt (genel müdürlük, fabrika, yalnızca marka adından oluşan başlıklı kayıtlar)", g["magaza_disi_belirsiz"]],
        ["Resmi mağaza bulucu (vitra.com.tr/servisler-ve-satis-noktalari)", "%s satış noktası, %s servis noktası" % (g["resmi_magaza_bulucu"]["satis_noktasi"], g["resmi_magaza_bulucu"]["servis_noktasi"])],
        ["'VitrA Xxx Mağaza' adıyla profil (kendi adıyla)", "5: Adana 4,2 (54 yorum), Ankara 4,3 (91), Suadiye 4,4 (156), Samsun 4,5 (26), İzmir 4,3 (47)"],
        ["Profilde web sitesi alanı", "vitra.com.tr: %d, başka adres: %d, boş: %d" % (g["vitra_web_alani"]["vitra_com_tr"], g["vitra_web_alani"]["diger"], g["vitra_web_alani"]["web_yok"])],
    ]))
    A("Not: Google Maps'teki profil sayısı (%s) resmi bulucudaki satış noktası sayısından (161) yüksek; bayi, inşaat malzemesi mağazası ve mükerrer profillerin VitrA adını kullanması bu farkı açıklayabilir, birebir eşleşme beklenmemelidir.\n" % n(mg["kayit"]))
    A("**İl dağılımı (ilk 10, satış noktası profili)**\n")
    A(tablo(["İl", "Profil", "Toplam yorum", "Ortalama puan (yorum ağırlıklı)"], [[x["il"], x["satis_noktasi"], n(x["toplam_yorum"]), ond(x["ortalama_puan_yorum_agirlikli"])] for x in g["il_dagilimi"][:10]]))
    A("**Yorum sayısı en yüksek 8 profil**\n")
    A(tablo(["Profil", "İl", "Puan", "Yorum"], [[vn(x["ad"]), x["il"], ond(x["puan"], 1), x["yorum"]] for x in g["en_cok_yorum"][:8]]))
    A("**Puanı 4,0'ın altında olan ve 20 ve üzeri yorumu bulunan profiller**\n")
    A(tablo(["Profil", "İl", "Puan", "Yorum"], [[vn(x["ad"]), x["il"], ond(x["puan"], 1), x["yorum"]] for x in g["dusuk_puanli_20plus_yorum"] if x["ad"] != "VitrA Genel Müdürlüğü"][:8]))
    A("Kaynak: Google Maps (DataForSEO), sorgular %s tarihinde çalıştırıldı.\n" % T)
    A("**Bulgular**\n")
    A("- Satış noktası profillerinde yorum ağırlıklı ortalama puan %s (%s yorum); puanı bulunan profillerde medyan %s yorum var ve 10'dan az yorumlu profil sayısı %d (toplam %d profil). İstanbul %d profil ve %s yorumla dağılımın merkezinde." % (ond(mg["ortalama_puan_yorum_agirlikli"]), n(mg["toplam_yorum"]), mg["medyan_yorum"], mg["yorum_10_alti"], mg["kayit"], g["il_dagilimi"][0]["satis_noktasi"], n(g["il_dagilimi"][0]["toplam_yorum"])))
    A("- Profil adları tutarsız: 'VitrA - Artema - <bayi>' kalıbının yanında büyük harfli, bayi adı önde, yalnızca marka adından oluşan ve bayi eki olmayan başlıklar bir arada; bazı profiller mobilya, ev eşyası veya ev tadilatı kategorisiyle listelenmiş (başka bir mobilya markasıyla karışma olasılığı).")
    A("- Profil sahipliği bayi düzeyinde; VitrA'nın kendi adıyla listelenen 5 mağazası (Adana, Ankara, Suadiye, Samsun, İzmir) 26 ile 156 yorum arasında ve 4,2-4,5 puan bandında.\n")
    A("**VitrA için fırsatlar**\n")
    A("- Bayi profillerinde adlandırma ve kategori standardı (ör. 'VitrA - Artema - <bayi>' ve 'Banyo malzemeleri mağazası'), web sitesi alanının vitra.com.tr mağaza sayfasına bağlanması ve yorum toplama için QR/kısa bağlantı desteği, düşük yorumlu profillerde görünürlüğü artırabilir.")
    A("- 4,0 altı puanlı profillerde yorum yanıt akışının bayilerle birlikte kurulması ve Maps'te yalnızca marka adıyla açılmış belirsiz kayıtların sahiplenme veya birleştirme talebiyle ele alınması değerlendirilebilir.")
    A("- Mağaza profilleri, montaj ve keşif hizmetinin görünür olduğu ürünler (servis noktası olan iller) için Business Profile'da hizmet alanı ve 'randevu' bağlantısıyla zenginleştirilebilir.\n")
    # ---- 6
    so = shp["ozet"]
    A("## 6. Google Shopping ve ürün bloğu görünürlüğü (SERP düzeyinde)\n")
    A("Yöntem: 15 kategori kelimesi (ve 3 marka kelimesi) için Google TR mobil (Android) ve karşılaştırma için masaüstü organik SERP (DataForSEO organic advanced, derinlik 20). `item_types` içinde shopping, popular_products, product_considerations ve benzeri ürün bloğu tipleri arandı. Fiyat çekimi bu başlığın kapsamı dışındadır. Maliyet %s USD.\n" % ond(so["maliyet_usd"], 3))
    rows = []
    for r in shp["kategori"]:
        mo = r["mobil"]; ma = r["masaustu"]
        rows.append([r["kelime"] + (" (marka)" if r["tur"] == "marka" else ""), "Yok" if not mo["shopping_urun_blogu"] else "Var", "Var" if mo["local_pack"] else "-", "Var" if mo["ai_overview"] else "-", "Var" if mo["paa"] else "-", "Var" if mo["video"] else "-", mo["vitra_organik_sira_top10"] or "-", ", ".join(d.replace("www.", "") for d in mo["top10_domain"][:3])])
    A(tablo(["Kelime", "Shopping / ürün bloğu (mobil)", "Yerel paket", "AI Overview", "PAA", "Video", "vitra.com.tr ilk 10 sırası", "İlk 3 alan adı"], rows))
    A("Kontrol: aynı tespit yöntemi 5 genel ürün sorgusunda (iphone 15, samsung televizyon 55 inç, kablosuz kulaklık, nike air max, buzdolabı) mobil ve masaüstünde denendi; %d sorgunun hiçbirinde shopping veya ürün bloğu görünmedi. Mobilde tüm 15 kategori kelimesinde görsel bloğu (images) var; yerel paket %d, AI Overview %d, PAA %d, video %d kelimede görünüyor. Masaüstünde AI Overview %d, yerel paket %d kelimede.\n" % (so["kontrol_sorgu_sayisi"], so["mobil_local_pack"], so["mobil_ai_overview"], so["mobil_paa"], so["mobil_video"], so["masaustu_ai_overview"], so["masaustu_local_pack"]))
    import collections
    dom = collections.Counter()
    for r in shp["kategori"]:
        if r["tur"] == "kategori" and r["mobil"]:
            for x in r["mobil"]["top10_domain"]: dom[x.replace("www.", "")] += 1
    A("Mobil ilk 10 organik sonuçlarda 15 kategori kelimesi genelinde en sık görülen alan adları (sonuç sayısı): " + ", ".join("%s %d" % (k, v) for k, v in dom.most_common(9)) + ". vitra.com.tr 15 kelimenin %d'inde ilk 10'da.\n" % so["mobil_vitra_top10"])
    A("**Bulgular**\n")
    A("- Türkiye SERP'inde Shopping/ürün bloğu bu ölçümde hiçbir kategori kelimesinde ve hiçbir kontrol sorgusunda görünmedi; ürün keşfi organik sonuçlarda pazaryeri ve karşılaştırma sitelerine (Trendyol, Akakçe, Amazon TR, Hepsiburada, Cimri), görsel bloğuna ve yerel pakete dağılıyor. Bu nedenle Merchant Center verisiyle ücretsiz ürün listelemesi için TR SERP'inde ölçülebilir bir yüzey bu turda tespit edilmedi.")
    A("- Yerel paket mobilde 15 kategori kelimesinin 8'inde görünüyor (banyo dolabı, lavabo, banyo bataryası, banyo aynası, küvet, banyo aksesuarları, gömme rezervuar, duşakabin); bu, bölüm 5'teki Business Profile verisinin görünürlük değerini destekliyor.")
    A("- vitra.com.tr mobil ilk 10'da 7 kategori kelimesinde (akıllı klozet ve havluluk 1., klozet takımı ve gömme rezervuar 3., lavabo bataryası ve duşakabin 5., klozet kapağı 6.); asma klozet, lavabo, banyo dolabı, banyo bataryası, duş seti, banyo aynası, küvet ve banyo aksesuarlarında ilk 10'da yer almıyor.\n")
    A("- 'vitra lavabo bataryası' marka kelimesinde vitra.com.tr mobil ilk 10'da yer almıyor; ilk üç sırada Koçtaş, Trendyol ve Akakçe görünüyor (marka adlı diğer iki kelimede VitrA 1. sırada).\n")
    A("**VitrA için fırsatlar**\n")
    A("- Shopping bloğu yüzeyi bulunmadığından ürün görünürlüğü organik sıralama, görsel arama, yerel paket ve pazaryeri mağazası üzerinden yönetiliyor; ürün yapılandırılmış verisi (Product schema, fiyat, stok) ve görsel alt metinleri bu yüzeyler için sürdürülebilir bir zemin.")
    A("- Yerel paket görünen kelimelerde (banyo dolabı, lavabo, duşakabin) Business Profile iyileştirmeleri ile kategori sayfası iç içeriğinin birlikte ele alınması değerlendirilebilir.\n")
    # ---- kısıtlar
    A("## Kısıtlar ve alınamayanlar\n")
    for x in pol["alinamayanlar"]: A("- " + x)
    A("- Instagram (Kale, Creavit, Grohe TR) ve TikTok sayıları SERP'te görünmedi; görünen değerler yaklaşık ve SERP'ten alınmıştır. Pinterest aylık görüntülenme sayısı profil sayfalarında yer almadı.")
    A("- Google Maps sonuçları sorgu başına 20 kayıtla sınırlı; il ve ilçe sorguları dışında kalan profiller eksik olabilir. VitrA etiketli bayi ve servis kayıtlarının bir bölümü mükerrer veya farklı adla listelenmiş olabilir.")
    A("- Profil adları görüntülemede VitrA yazımına normalize edilmiştir; ham adlar gbp.json içinde. Ödeme ve iade koşulları ölçüm gününe aittir; kampanya ve eşik değerleri değişebilir (Koçtaş taksit kampanyası 30 Eylül 2026'da sona eriyor).\n")
    A("## Maliyet\n")
    A("DataForSEO toplamı yaklaşık 0,77 USD: Google Maps %s USD, Shopping ölçümü %s USD, sosyal ve Pinterest sorguları yaklaşık 0,41 USD. Apify: 16 rag-web-browser çağrısı (3'ü kullanılabilir sayfa içeriği döndürdü, diğerleri boş veya sayfa bulunamadı yanıtı verdi), toplam yaklaşık 0,1 USD (hesaplama birimi toplamı yaklaşık 0,25; 1,5 USD sınırının altında). Google Maps için sorgular 0,206 USD ile başlık 5'in, Shopping ölçümü 0,149 USD ile başlık 6'nın sınırı olan 1 USD'nin altında kaldı.\n" % (ond(g["maliyet_usd"], 3), ond(so["maliyet_usd"], 3)))
    open(os.path.join(KOK, "ozet.md"), "w", encoding="utf-8").write("\n".join(m))
    return "\n".join(m)
if __name__ == "__main__":
    t = uret(); print(len(t))
