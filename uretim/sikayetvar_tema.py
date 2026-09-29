# -*- coding: utf-8 -*-
"""Sikayet tema siniflandirmasi (anahtar kelime kurallari). Coklu etiket + agirlikli skorla tek 'ana tema'.
Baslik 3 puan, govde 1 puan. Metin Turkce kucuk harfe cevrilip taranir."""
import re

def kucuk(s):
    return (s or "").replace("İ", "i").replace("I", "ı").lower()

# tema -> (etiket, [regex])
TEMALAR = {
 "kalite": ("Ürün kalitesi, sızıntı, kırılma", [
    r"sızıntı|sızdır|su kaçır|kaçırıyor|su akıt|akıtıyor|damlat|kırıl|kırık|çatla|çatlak|leke|lekel|kararma|karar[ıd]|pas(?:lan|la)|paslan|soyul|kabar|kalkma|kalkıyor|deform|kaplama|kalitesiz|kalite|dayanıksız|menteşe|arıza|bozul|bozuk|defolu|kusur|ayıplı|hatalı ürün|üretim hatası|tasarım hata|çizik|çizil|sararma|sarı leke|hijyen|kapak kayma|gevşi|patla|yavaş kapan|jilet|keskin"]),
 "montaj": ("Montaj ve usta", [
    r"montaj|usta|tesisatç|kurulum|taktır|takılma|monte|takan|takılırken|söküm|keşif"]),
 "servis_garanti": ("Yetkili servis ve garanti", [
    r"servis|garanti|yetkili|teknik ekip|arıza kayd|kullanıcı hatası|usta hatası|kontrol ücreti"]),
 "yedek_parca": ("Yedek parça bulunamaması", [
    r"yedek parça|yedek parca|parça temin|parça bulun|parçası bulun|parça(?:sı|yı|nın)? (?:sipariş|talep|gelmedi|stok|bekle|bekleme)|parça bekleme|stokta yok|üretimden kalk|üretimi dur|tek başına satış|komple set|parçası yok|parça yok|parçasını"]),
 "vitra_online": ("vitra.com.tr sipariş, teslimat ve iade", [
    r"vitra online|vitra\.com|online\.vitra|vitra sitesi|vitra internet|vitra web|vitra e-ticaret|vitra türkiye'den|vitra türkiye’den|vitra'nın sitesi|vitra’nın sitesi|resmi site|arvato|vitra\.com\.tr|vitra (?:dolap )?sipariş|vitra'dan sipariş|vitra’dan sipariş|vitra'dan (?:bir )?(?:dolap|ürün|klozet)[^.]{0,30}sipariş|siparişimi vitra|resmi internet"]),
 "pazaryeri": ("Pazaryeri ve üçüncü taraf satıcı", [
    r"trendyol|hepsiburada|\bn11\b|amazon|çiçeksepeti|pazarama|pttavm|ptt avm|idefix|akakçe|cimri|satıcı|satici|pazaryeri|marketplace|evdeniste|karo grup|banyomarka|banyoline|banyomega|evidea|ikea|hepsijet"]),
 "fiyat_kampanya": ("Fiyat ve kampanya", [
    r"fiyat|pahalı|kampanya|indirim|taksit|kupon|zam\b|zamlı|fahiş|aşırı ücret|haksız ücret|kontrol ücreti|servis ücreti|ek ücret|ücret talep|ücretli servis|iade bedel"]),
 "iletisim": ("İletişim ve çağrı merkezi", [
    r"müşteri hizmet|çağrı merkezi|iletişim|dönüş yap|geri dönüş|cevap ver|cevap alama|yanıt ver|yanıt alama|aranmad|arayan yok|ulaşılam|ulaşamı|0850|destek hatt|muhatap|ilgisiz|ilgilenmi|ilgilenmedi|kaba|saygısız|üslup"]),
 "magaza_bayi": ("Mağaza ve bayi", [
    r"bayi|mağaza|showroom|satış nokta|koçtaş|bauhaus|tekzen|yapı market|yapı merkezi|evdema|nova\b|hırdavat|inşaat malzeme"]),
}
SIRA = ["yedek_parca", "vitra_online", "pazaryeri", "montaj", "servis_garanti", "fiyat_kampanya", "iletisim", "magaza_bayi", "kalite"]
DERLI = {k: [re.compile(p) for p in v[1]] for k, v in TEMALAR.items()}

# siparis/teslimat/iade genel isaretleyici (kanal bagimsiz)
SIPARIS = re.compile(r"sipariş|teslimat|teslim|kargo|iade|iptal|değişim|hasarlı gel|kırık gel|eksik gel|yanlış ürün|para iadesi|cayma")
PLATFORMLAR = {
 "Trendyol": r"trendyol", "Hepsiburada": r"hepsiburada|hepsijet", "n11": r"\bn11\b", "Amazon": r"amazon",
 "Çiçeksepeti": r"çiçeksepeti", "Diğer pazaryeri (Pazarama, PTT AVM, idefix vb.)": r"pazarama|pttavm|ptt avm|idefix|akakçe|cimri"}
PERAKENDE = {"Koçtaş": r"koçtaş", "Bauhaus": r"bauhaus", "Tekzen": r"tekzen", "Evdema": r"evdema", "IKEA": r"ikea"}

def etiketle(baslik, govde):
    """(etiketler_kumesi, ana_tema, skorlar)"""
    b, g = kucuk(baslik), kucuk(govde)
    skor = {}
    for t, rx in DERLI.items():
        s = 0
        for r in rx:
            s += 3 * len(r.findall(b)) + min(len(r.findall(g)), 3)
        if s: skor[t] = s
    # vitra.com.tr siparis numarasi izi: metinde siparis + maskelenmis numara, baska platform/perakende adi yok
    if re.search(r"sipariş[^.\n]{0,40}\[no\]|\[no\][^.\n]{0,30}sipariş", g) and not re.search("|".join(list(PLATFORMLAR.values()) + list(PERAKENDE.values())), b + " " + g):
        skor["vitra_online"] = skor.get("vitra_online", 0) + 1
    # kanal etiketleri en az 1 baslik/govde eslesmesi ile gecerli; 'kargo' ve 'bedel/tl' gibi zayif isaretler tek basina etiket sayilmaz
    etk = {t for t, s in skor.items() if s >= (2 if t in ("iletisim", "fiyat_kampanya", "servis_garanti", "kalite") else 1)}
    if not etk:
        return set(), "diger", skor
    # ana tema: en yuksek skor, esitlikte SIRA
    ana = sorted(etk, key=lambda t: (-skor[t], SIRA.index(t)))[0]
    # yedek parca / vitra.com.tr / pazaryeri kanal-ozel temalar, ilgili sinyal basliktaysa ana tema olur; aksi halde alt etiket kalir
    return etk, ana, skor
