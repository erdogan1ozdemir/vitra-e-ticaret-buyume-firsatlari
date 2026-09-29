# -*- coding: utf-8 -*-
"""Kanal siniflama sozlugu ve marka kanali tanimlari (youtube_derin_analiz.py tarafindan kullanilir)."""
import re
VITRA_MARKA = {"VitrA Türkiye", "VitrA Bathrooms", "Artema Türkiye"}
VITRA_ILISKILI = {"Vitra Artema Yetkili Servis Başarı yapı", "Vitra Georgia"}
RAKIP_MARKA = {"Kale Banyo": "Kale", "Creavit": "Creavit", "Creavit Global": "Creavit", "GROHE": "Grohe", "GROHE America": "Grohe", "hansgrohe": "Hansgrohe", "BOCCHI": "Bocchi",
               "SEREL": "Serel", "E.C.A.": "E.C.A.", "Duravit": "Duravit", "Bien Türkiye": "Bien", "DESSONI": "Dessoni", "Kuysen": "Duravit (dağıtıcı)"}
MARKA = {"Kale Banyo","Creavit","Creavit Global","GROHE","GROHE America","hansgrohe","BOCCHI","SEREL","E.C.A.","Duravit","Bien Türkiye","DESSONI","VitrA Türkiye","VitrA Bathrooms","Artema Türkiye",
         "Vitra Georgia","Roomart Türkiye","Rani Mobilya","Dekorister Mobilya","BAYRAK MOBİLYA","marsbanyo","YILDIZ ELEGANCE","Demirbal Mobilya","Durul Duşakabin","Dusaks Duşakabin","Çamlıca Duşakabin",
         "BAŞAK AKRİLİK - DUŞ, KÜVET VE DUŞAKABİN SİSTEMLERİ","Koresan","RADIVA | Dekoratif Radyatör ve Havlupan","İvigo Elektrikli Isıtıcılar","Hammam Radiator","Yütaş Yapı Ürünleri Tic.A.Ş.",
         "Saint-Gobain Weber Türkiye","Bianca Boya","KAIZEN HİJYEN","Derby Kimya","FATTOSON","Kuysen"}
PERAKENDE = {"Koçtaş","Tekzen","BİM Türkiye","ebebek","IKEA USA","Banyotrendy","Banyomoda","Yapı Dükkanım","Ayrıntı Shop / Yapı Malzemeleri","EGEMER YAPI","Mobilyaya Bakış","BOĞAZİÇİ 'Lİ HIRDAVATÇI",
             "Su Makinesi","faucetbestbuy","xTWOstore","RSF Bathrooms","Banyomarka","sunlighttr"}
INCELEME = {"ShiftDelete.Net","YapıStil","Mevlüt Aydemir","Şımart Teknoloji","Mendebur Lemur","Merak Ediyorum","Sosyopat","Make Life Easier","Fani Beyin"}
DEKOR = {"Dekordelisi","DEKORENZA İç Mimari Tasarım & Mobilya","decoverse","Banyo -Mutfak Mimarisi \\ Burcu Tarkan","Tasarım Budur","Dekorasyon Adam","iç mimar Sisters","Arden Mimarlık","Zeynep Bordebar",
         "Diamond Interior","Rukiye Taşçi","LUDO TASARIM MOBİLYA ","Poyraz Dekorasyon","Kılıç Tadilat","dekovincom","KIZILIN İZİNDE ","tuvba","Laçin Tenel","Evde Mimar","Melike Gümüş","Emek Dekorasyon","KS Dekorasyon"}
DIGER = {"Pil Adam","Usta Tv","Evrim Ağacı","Murat Sen","Warner Music Japan","Timur Tanyer","Olca Yapı - Mehmet Turgut","Diamond Interior","Ezhel","FPPRO","Vitra"}
USTA = {"şehmus kalkan","fırat Tali","Emrah Öztürk","Bilal Hizmet","Mühendislik Harikaları","Sanal YouTube","Cengiz Dolunay","OLCAY USTA","Erdem Fidan (ErdmFidan)"}
ALAKASIZ = re.compile(r"ezhel|warner music|evrim ağacı|telefon batarya|iphone|li-ion|\bbms\b|en iyi pil|pil adam|usta tv|chair times|fppro|^vitra$", re.I)
TESISAT_ANAHTAR = re.compile(r"tesisat|usta|tamir|teknik|servis|mekanik|tadilat|kendin|kendin yap", re.I)
BASLIK_ANAHTAR = re.compile(r"montaj|tamir|değiş|nasıl (yapılır|takılır|değiştirilir|kurulur|çekilir)|kurulum|su kaçır|arıza|damlat|tıkan|takma|ayarı", re.I)
def tur(k, basliklar=()):
    if k in USTA: return "Tesisatçı / usta"
    if k in MARKA: return "Marka"
    if k in PERAKENDE: return "Perakendeci"
    if k in INCELEME: return "İnceleme / teknoloji"
    if k in DEKOR: return "Dekorasyon / iç mimar"
    if k in DIGER: return "Diğer"
    if re.search(r"dekor|mimar|tasar|interior|mobilya", k, re.I): return "Dekorasyon / iç mimar"
    if TESISAT_ANAHTAR.search(k): return "Tesisatçı / usta"
    if sum(1 for b in basliklar if BASLIK_ANAHTAR.search(b or "")) >= max(1, len(basliklar) // 2): return "Tesisatçı / usta"
    return "Diğer"
