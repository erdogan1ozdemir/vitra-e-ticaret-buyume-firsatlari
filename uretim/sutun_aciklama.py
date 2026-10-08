# -*- coding: utf-8 -*-
"""Tablo sutun basliklarina hover aciklamasi enjekte eder."""
import re, html

# Genel karsiliklar; bolume ozel olanlar OZEL sozlugunde ezilir.
GENEL = {
 "Kelime": "Almanya'da (DE) ölçülen arama ifadesi. Yazım varyantları ayrı kayıt olarak tutulur.",
 "Kelime grubu": "Google Ads'in birleşik hacim döndürdüğü kelime kümesi. Grup üyeleri satır altında listelenmiştir ve hacimleri toplanmaz.",
 "Aylık hacim": "Google Keyword Planner'ın son 12 ay için döndürdüğü ortalama aylık arama sayısı. Almanya (DE), Almanca.",
 "2026 Oca-Tem": "Ocak - Temmuz 2026 ortalama aylık arama hacmi. Temmuz, Keyword Planner'ın veri döndürdüğü son aydır.",
 "2025 Oca-Tem": "Ocak - Temmuz 2025 ortalama aylık arama hacmi; 2026 penceresiyle aynı takvim aylarını kapsar.",
 "YTD YoY": "2026 Ocak - Temmuz ile 2025 Ocak - Temmuz ortalamaları arasındaki yüzde değişim. İki pencere aynı takvim aylarını kapsadığı için mevsimsellikten arındırılmıştır.",
 "2024 → 2025 tam yıl": "2024 ve 2025 takvim yıllarının 12 aylık ortalamaları arasındaki yüzde değişim.",
 "3 yıllık · 2023 Oca-Tem": "2023 Ocak - Temmuz ile 2026 Ocak - Temmuz ortalamaları arasındaki yüzde değişim; üç yıllık yön göstergesidir.",
 "Kategori adı": "Aynı ürün grubunun Almanya'da kullanılan farklı adlarından biri.",
 "Aylık hacim": "Kelimenin son 12 ayda ölçülen ortalama aylık arama sayısı. Kaynak: Ahrefs Keywords Explorer, Almanya.",
 "Eyl 2023 - Ağu 2024": "Eylül 2023 - Ağustos 2024 penceresinin ortalama aylık arama hacmi.",
 "Eyl 2025 - Ağu 2026": "Eylül 2025 - Ağustos 2026 penceresinin ortalama aylık arama hacmi.",
 "3 yıllık değişim": "Eyl 2023 - Ağu 2024 ile Eyl 2025 - Ağu 2026 pencerelerinin ortalamaları arasındaki yüzde değişim. Tek ay karşılaştırması kullanılmamıştır.",
 "Son yıl": "Eyl 2024 - Ağu 2025 ile Eyl 2025 - Ağu 2026 pencereleri arasındaki yüzde değişim; güncel ivmeyi gösterir.",
 "Durum": "VitrA ürününün ilgili kanalda listelenip listelenmediği. Canlı katalog ve arama sonucu gözlemine dayanır.",
 "Not": "Satıra ilişkin ek gözlem veya ölçüm açıklaması.",
 "Tip": "Satırdaki aktörün türü.",
 "Kanal": "Ürünün son kullanıcıya ulaşabileceği satış noktası veya platform.",
 "Öncelik": "Kanalın kendi depodan sevkiyata uygunluğu ile VitrA'nın oradaki mevcut durumu birlikte değerlendirilerek verilen sıra. Öncelik 1 ilk fazda ele alınabilecekleri gösterir.",
}

OZEL = {
 "pazar": {
   "Almanya online ticareti": "HDE Online-Monitor 2026'nın Almanya online perakendesi için raporladığı gösterge.",
   "Gösterge": "Titze çalışmasında ölçülen pazar büyüklüğü kalemi.",
   "2025": "Çalışmanın 2025 yılı için raporladığı değer.",
   "2030 projeksiyon": "Çalışmanın 2030 yılı için öngördüğü değer.",
   "Değişim": "2025 ile 2030 arasındaki yüzde değişim.",
 },
 "kategori-dili": {
   "Kategori adı": "Aynı ürün grubunun Almanya'da kullanılan farklı adlarından biri.",
   "Okuma": "Kelimenin kategori içindeki rolü ve eğiliminin yorumu.",
 },
 "retailer-arama": {
   "Not": "Kelimenin zaman içindeki seyri ve ölçüme ilişkin açıklama.",
 },
 "vitra-gorunurluk": {
   "Site": "VitrA Dusch-WC ürünlerinin arandığı satış noktası.",
   "Tip": "Sitenin iş modeli: genel pazaryeri, DIY zinciri, banyo uzman e-ticaretçisi veya fiyat karşılaştırma.",
   "Gözlemlenen ürün": "İlgili sitede tespit edilen VitrA ürünü veya listeleme sayfası.",
   "Gözlemlenen ürün ve satıcı": "İlgili sitede 14.09.2026'da görülen VitrA ürünleri ve ilanı yayımlayan satıcı.",
   "Dusch-WC durumu": "Var: VitrA'nın elektronik veya termostatlı komple Dusch-WC'si listeleniyor. Kısmen: yalnızca bide fonksiyonlu klozet veya Dusch-WC oturak ünitesi var. Yok: bu ürün tiplerinden hiçbiri görülmedi.",
 },
 "serp": {
   "Sıra": "Sonuç sayfasındaki pozisyon. Aynı sıra numarası birden fazla satırda görünüyorsa o pozisyonda bir SERP alanı yer alıyor demektir.",
   "Adres": "Sırayı tutan sayfa ve kısa tanımı.",
   "Tip": "Sonucun türü: üretici sitesi, uzman e-ticaret, fiyat karşılaştırma veya SERP alanı.",
   "DR": "Domain Rating; sitenin backlink profilinin 100 puanlık ölçekteki gücü. Kaynak: Ahrefs.",
   "Tahmini trafik": "Sayfanın tüm kelimelerinden aldığı tahmini aylık organik ziyaret sayısı. Kaynak: Ahrefs.",
   "Marka": "Kategoride görünen üretici veya satıcı markası.",
   "Öne çıkan seri": "Markanın kategoride en çok görünen ürün serisi.",
   "Fiyat bandı": "OTTO katalogunda ve Google Shopping alanında 09.09.2026 tarihinde gözlemlenen liste fiyatı aralığı.",
 },
 "pazaryeri": {
   "Sevkiyat modeli": "Platformun siparişi kimin sevk etmesini beklediği. Satıcı sevkiyatı, ürünün VitrA'nın Almanya deposundan çıkabildiği anlamına gelir.",
   "Kendi depodan": "Siparişin VitrA'nın Almanya deposundan son kullanıcıya sevk edilmesinin mümkün olup olmadığı.",
   "Giriş koşulu": "Platformun satıcı kabulü için aradığı belgeler, tüzel kişilik ve hizmet seviyesi şartları.",
   "Ücret / komisyon": "Aylık sabit ücret ve satış başına komisyon. Eylül 2026 itibarıyla kamuya açık kaynaklardan derlenmiştir.",
   "VitrA Dusch-WC durumu": "Kanalda halihazırda VitrA Dusch-WC listelemesi bulunup bulunmadığı.",
 },
 "retailer": {
   "Sevkiyat modeli": "Perakendecinin ürünü kendi stoğundan mı yoksa üreticinin deposundan mı sevk ettiği.",
   "Kendi depodan": "Siparişin VitrA'nın Almanya deposundan son kullanıcıya sevk edilmesinin mümkün olup olmadığı.",
   "Giriş koşulu": "Perakendeciyle çalışmaya başlamak için gereken sözleşme ve veri entegrasyonu.",
   "Ücret / komisyon": "Ticari koşullar. Bu kanalda tarifeler kamuya açıklanmamaktadır.",
   "VitrA Dusch-WC durumu": "Kanalda halihazırda VitrA Dusch-WC listelemesi bulunup bulunmadığı.",
 },
 "kendi-kanal": {
   "Bileşen": "Ürün feed'ini oluşturan veri veya süreç parçası.",
   "Gereklilik": "İlgili bileşenin platformlar tarafından beklenen içeriği.",
   "Kategori için not": "Bileşenin Dusch-WC kategorisindeki özel karşılığı.",
 },
 "b2b": {
   "Kanal": "Toptan veya B2B satış noktası.",
   "Tip": "Kanalın türü: SHK uzman toptancılığı veya B2B platform.",
   "Yapı": "Kanalın ölçeği ve çalışma biçimi.",
   "Not": "Kanalın kategoriyle ilişkisine dair gözlem.",
 },
 "adimlar": {
   "Aksiyon": "Önerilen çalışma.",
   "Dayanak": "Aksiyonu destekleyen bulgu ve veri.",
   "Beklenen çıktı": "Aksiyonun tamamlanmasıyla ulaşılabilecek sonuç.",
 },
 "konumlandirma": {
   "Kavram": "Ürünün Almanya'da hangi düşünce kalıbıyla arandığını gösteren kavram grubu.",
   "Temsil eden kelime": "Kavramın en yüksek hacimli karşılığı; hacim bu kelimeye aittir.",
   "Kapsanan aramalar": "Aynı kavrama giren diğer kelimeler ve hacimleri.",
   "Ölçek": "Aylık hacmin, tablodaki en büyük kavrama göre görsel oranı.",
   "Kelime": "Almanya'da Türkçe olarak yapılan arama.",
   "Tip": "Kelimenin hangi arama niyetine karşılık geldiği: marka, kategori adı veya karar aşaması.",
 },
 "markalar": {
   "Marka": "Kategoride arama talebi ölçülen üretici veya satıcı markası.",
   "Ürün serisi": "Markanın Dusch-WC ürün serisi adı.",
   "Toplam aylık arama": "Marka adı ve seri adlarının Keyword Planner hacimlerinin toplamı. Birleşik gruplar tek kez sayılmıştır.",
   "Ölçek": "Toplam talebin, tablodaki en büyük markaya göre görsel oranı.",
   "Öne çıkan kelimeler": "Markanın en yüksek hacimli dört kelimesi ve hacimleri.",
   "Site": "Kategori sayfası incelenen site. Tıklandığında sayfa açılır.",
   "Aylık organik ziyaret": "Sayfanın kategori kelimelerinden aldığı tahmini aylık organik ziyaret. Kaynak: Ahrefs, ölçüm anına ait tahmindir.",
   "Not": "Sitenin kategorideki konumuna ilişkin gözlem.",
 },
 "dagitim": {
   "Site": "Ürünün listelenebileceği platform veya satış partneri. Tıklandığında başvuru sayfası açılır.",
   "Sevkiyat modeli": "Platformun siparişi kimin sevk etmesini beklediği.",
   "Kendi depodan": "Siparişin VitrA'nın Almanya deposundan son kullanıcıya sevk edilmesinin mümkün olup olmadığı.",
   "Giriş koşulu": "Kanala girmek için gereken hesap, sözleşme ve maliyet.",
   "Öncelik": "Kanalın kendi depodan sevkiyata uygunluğu ile VitrA'nın oradaki mevcut durumu birlikte değerlendirilerek verilen sıra.",
 },
 "komsu-kategori": {
   "Kategori": "VitrA ürün yelpazesinde yer alan ve aynı satıcı hesabıyla listelenebilecek ürün grubu.",
   "Toplam aylık arama": "Kategori için seçilmiş temsili kelimelerin Keyword Planner hacimlerinin toplamı; kategorinin tamamını değil ölçek karşılaştırmasını gösterir.",
   "Ölçek": "Kategori talebinin, tablodaki en büyük kategoriye göre görsel oranı.",
   "Öne çıkan kelimeler": "Kategorinin en yüksek hacimli dört kelimesi ve hacimleri.",
 },
 "rakip-kelime": {
   "Site": "Kategori sayfası incelenen rakip.",
   "İncelenen sayfa": "Organik kelime ve trafik verisinin alındığı adres. Tıklandığında sayfa açılır.",
   "Trafik getiren kelime": "Sayfanın ölçüm anında trafik aldığı kelime sayısı.",
   "Toplam aylık ziyaret": "Sayfanın bu kelimelerden aldığı tahmini toplam aylık organik ziyaret. Kaynak: Ahrefs.",
   "Aylık ziyaret": "Sitenin bu arama grubundaki kelimelerden aldığı tahmini aylık organik ziyaret toplamı.",
   "Pay": "Sitenin, bu arama grubunda ölçülen toplam organik trafik içindeki yüzde payı.",
   "Dağılım": "Pay sütununun görsel karşılığı.",
   "Kelime": "Arama grubuna dahil kelime. \"grup\" işareti, Google Ads'in bu kelimeyi başka kelimelerle birleşik ölçtüğünü gösterir.",
 },
 "yontem": {
   "Konu": "Rapordaki veri başlığı.",
   "Kaynak ve yöntem": "İlgili verinin hangi araçtan, hangi kapsamda ve hangi tarihte alındığı.",
 },
}

RAKIP_ADLARI = {"Hansgrohe", "Geberit", "Bernstein", "Duravit", "MEGABAD", "VitrA"}

def uygula(doc):
    """Belgedeki her <th> ogesine data-t ekler; eksik kalan basligi rapor eder."""
    eksik = []
    bolum = {"id": None}
    def bol(m):
        bolum["id"] = m.group(1); return m.group(0)
    parcalar = re.split(r'(<section id="[a-z0-9\-]+">)', doc)
    cikti = []
    aktif = None
    for parca in parcalar:
        m = re.match(r'<section id="([a-z0-9\-]+)">', parca)
        if m:
            aktif = m.group(1); cikti.append(parca); continue
        def th(mm):
            nitelik, icerik = mm.group(1), mm.group(2)
            etiket = re.sub(r'<[^>]+>', '', icerik).strip()
            for v, k in (("&rarr;", "→"), ("&middot;", "·"), ("&amp;", "&"), ("&quot;", '"')):
                etiket = etiket.replace(v, k)
            if "data-t=" in nitelik: return mm.group(0)
            ac = OZEL.get(aktif, {}).get(etiket) or GENEL.get(etiket)
            if not ac and aktif == "rakip-kelime" and etiket in RAKIP_ADLARI:
                ac = ("%s'in ilgili kelimedeki en iyi organik sırası ve o kelimeden aldığı "
                      "tahmini aylık ziyaret. \"-\" işareti, sayfanın o kelimede ölçülebilir "
                      "sıralaması bulunmadığını gösterir.") % etiket
            if not ac:
                eksik.append((aktif, etiket)); return mm.group(0)
            return '<th%s data-t="%s"><span class="q">%s</span></th>' % (
                nitelik, html.escape(ac, quote=True), icerik)
        # <thead> ile karismasin diye: <th> ya da <th ...> kabul edilir, <thead> edilmez.
        cikti.append(re.sub(r'<th((?:\s[^>]*)?)>(.*?)</th>', th, parca, flags=re.S))
    return "".join(cikti), eksik
