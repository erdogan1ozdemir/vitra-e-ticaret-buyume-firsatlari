# -*- coding: utf-8 -*-
"""Yorum ve soru temalari: kural tabanli siniflandirma (bir metin birden fazla temaya girebilir)."""
import re

def kucuk(s):
    return (s or "").replace("I", "ı").replace("İ", "i").lower()

# (anahtar, TR ad, EN ad, desen)
YORUM = [
    ("kirik", "Kırık, hasarlı veya kusurlu ürün", "Broken, damaged or defective product",
     r"kırık|kırıl|çatla|hasar|ezik|ezil|çizik|çizil|parçalan|darbe|patlak|göçük|defo|kusurlu"),
    ("eksik", "Eksik parça", "Missing parts",
     r"eksik(?!siz)|parça(sı)? yok|parçaları yok|vida(sı|ları)? (yok|çıkmadı|gelmedi)|(conta|dübel|aparat|hortum|kapak)(ı|lar)? (yok|çıkmadı|gelmedi)|içinden .{0,20}çıkmadı"),
    ("olcu", "Ölçü ve uyumluluk", "Size and compatibility",
     r"ölçü|uymadı|uymuyor|uymu(yo|o)r|oturmadı|oturmuyor|tam oturm|küçük geldi|büyük geldi|dar geldi|kısa geldi|uzun geldi|uyumlu değil|uyumsuz|uyumlu olmad|boyut|delik(ler)? (tutmadı|uymadı)|yetmedi"),
    ("montaj", "Montaj ve kurulum", "Installation and fitting",
     r"montaj|kurulum|monte|tak(ma|tık|tım|tırdık|ılması|ılıyor|ılır|arken)|usta|tesisatçı|sök"),
    ("sizinti", "Su kaçırma ve sızıntı", "Leaks",
     r"sızdır|sızıntı|damlat|damlıyor|su kaçır|akıtıyor|kaçak|su sız|su geliyor|su akıyor|su bırakıyor"),
    ("basinc", "Su basıncı ve akış", "Water pressure and flow",
     r"basınç|tazyik|suyu az|su az|zayıf ak|az akıyor|güçlü ak|akış"),
    ("yuzey", "Kireç, leke ve kaplama", "Limescale, stains and coating",
     r"kireç|lekel|leke |paslan|\bpas\b|kararm|matlaş|soyul|kaplama|sarar(dı|mış|ma)|renk değiştir"),
    ("mekanizma", "Mekanizma ve hareketli parça", "Mechanism and moving parts",
     r"yavaş kapan|amortisör|menteşe|kapak düş|kartuş|mekanizma|buton|basmalı|şamandıra|sifon|kapanmıyor|kapanmadı|çalışmıyor|çalışmadı|bozul|arıza"),
    ("kalite", "Malzeme ve sağlamlık", "Material and sturdiness",
     r"kalite|sağlam|dayanıklı|dayanıksız|ince |incecik|plastik|çürük|sallan|esnek|tok |ağır|hafif|malzeme|işçilik|dökümü"),
    ("gorunum", "Görünüm ve tasarım", "Look and design",
     r"şık|güzel dur|güzel görün|görüntü|görünüm|tasarım|renk|parlak|estetik|modern|duruşu|zarif|asil"),
    ("farkli", "Görselden / açıklamadan farklı ürün", "Different from image / description",
     r"farklı (ürün|geldi|model|renk)|yanlış ürün|başka (ürün|model)|görsel(deki|de) (gibi değil|farklı)|resim(deki|de) (gibi değil|farklı)|açıklama(da|daki) .{0,25}(değil|yok|farklı)|fotoğraf(taki|ta) gibi değil"),
    ("kargo", "Kargo ve teslimat süresi", "Shipping and delivery time",
     r"kargo|teslimat|teslim|geç geldi|hızlı geldi|erken geldi|zamanında|ertesi gün|gün(de|ünde) geldi|hızlıca geldi|çabuk geldi|hızlı gönder"),
    ("paket", "Paketleme", "Packaging",
     r"paket|ambalaj|kutu|köpük|özenle|özenli"),
    ("fiyat", "Fiyat ve fiyat/performans", "Price and value for money",
     r"fiyat|ucuz|pahalı|uygun|indirim|f/p|fp |parasına|ederinde|değer(ini|inde)|kampanya"),
    ("satis_sonrasi", "İade, değişim ve satıcı iletişimi", "Returns, exchange and seller contact",
     r"iade|değişim|değiştiril|satıcı|muhatap|ilgilen|müşteri hizmet|servis|garanti|yetkili|cevap ver"),
    ("temizlik", "Temizlik kolaylığı", "Ease of cleaning",
     r"temizl|silin|hijyen|rimless|kanalsız"),
    ("ses", "Ses ve gürültü", "Noise",
     r"ses(siz|li)? |sesi|gürültü|tıkırt"),
]
SORU = [
    ("uyum", "Uyumluluk ve kullanım yeri", "Compatibility and place of use",
     r"uyar mı|uyumlu|uyum|uygun ?mu|uygun mudur|uygunmudur|için uygun|olur mu|takılır mı|uyuyor mu|hangi model|modeline|modeli ile|ile kullanıl|kullanılır mı|kullanabilir mi|kullanılıyor mu|doğru ürün|yerine|kodlu|kodu|serisi"),
    ("olcu", "Ölçü ve boyut", "Size and dimensions",
     r"ölçü|boyut|kaç cm|cm|derinli|yüksekli|genişli|eni |boyu |mm|çap|aks|mesafe|uzunlu|kaç santim|inç|ebat|ağırlı|kilogram|kaç kg|dar model|\d+ ?[x*] ?\d+"),
    ("montaj", "Montaj ve bağlantı", "Installation and connection",
     r"montaj|kurulum|nasıl tak|takıl|monte|duvar|gömme|vida|dübel|bağlantı|tesisat|delik|zemin|yerden|sök"),
    ("icerik", "Kutu içeriği ve set kapsamı", "Box contents and set scope",
     r"dahil|içinde|içerisinde|beraber|birlikte|set|geliyor mu|gelir mi|var mı|mevcut mu|ayrı mı|ayrıca|kapağı|sifonu|bataryası|hortumu"),
    ("teknik", "Teknik özellik ve malzeme", "Technical specs and material",
     r"malzeme|seramik|porselen|krom|pirinç|paslanmaz|basınç|tazyik|termostat|bar |litre|tasarruf|rimless|kanalsız|fotosel|sıcak|soğuk|kartuş|mekanizma|yavaş kapan|duroplast|mdf|pvc|suya dayanıklı|giriş|çıkış|diş|3/4|1/2|sürgülü|filtre|kare mi|yuvarlak|plastik|metal|yapışkan|taharet"),
    ("renk", "Renk ve görünüm", "Colour and appearance",
     r"renk|beyaz|siyah|mat |matı|krem|gri|antrasit|altın|gold|bakır|bronz|parlak"),
    ("stok", "Stok, teslimat ve sipariş", "Stock, delivery and order",
     r"stok|ne zaman|teslim|kargo|gönderi|sipariş|tekrar gel|gelecek mi|bekl|elime"),
    ("fiyat", "Fiyat, kampanya ve fatura", "Price, campaign and invoice",
     r"fiyat|indirim|kampanya|taksit|pahalı|ucuz|fatura|kdv|kupon"),
    ("garanti", "Garanti, servis, yedek parça ve ürün durumu", "Warranty, service, spare parts and product condition",
     r"garanti|servis|yedek|parça|orijinal|tamir|arıza|bozul|değişim|iade|teşhir|sıfır mı|defolu|ikinci el|sızdır"),
]
_YC = [(k, re.compile(d)) for k, _, _, d in YORUM]
_SC = [(k, re.compile(d)) for k, _, _, d in SORU]
YAD = {k: (t, e) for k, t, e, _ in YORUM}
SAD = {k: (t, e) for k, t, e, _ in SORU}

def yorum_tema(metin):
    t = kucuk(metin) + " "
    return [k for k, rx in _YC if rx.search(t)]

def soru_tema(metin):
    t = kucuk(metin) + " "
    l = [k for k, rx in _SC if rx.search(t)]
    return l or ["diger"]
SAD["diger"] = ("Diğer", "Other")

def duygu(puan):
    if puan is None: return None
    return "olumlu" if puan >= 4 else ("olumsuz" if puan <= 2 else "notr")
