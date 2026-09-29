# -*- coding: utf-8 -*-
"""Genisletilmis kelime evreninin tema siniflandirmasi (sira onemli: ozelden genele).
(anahtar, TR ad, EN ad, grup, VitrA durumu, regex)
grup: SSG | BM | Armatür-Duş | Yıkanma | Karo | Aksesuar | Bitişik | Hizmet-Set
durum: Var | Kısmi | Yok"""
import re
T = [
 # --- hizmet ve set
 ("tadilat", "Banyo tadilatı ve yenileme", "Bathroom renovation", "Hizmet-Set", "Kısmi", r"banyo (tadilat|yenileme|renovasyon)|tadilat.*banyo|anahtar teslim banyo|banyo ustası|banyo yapımı|banyo yaptırma"),
 ("montaj_hiz", "Montaj ve usta hizmeti", "Installation and installer service", "Hizmet-Set", "Kısmi", r"montaj (ücreti|fiyat|hizmeti|servisi|ustası)|taktırma|(su|sıhhi|banyo)? ?tesisatçı(?!.*(doğalgaz|kombi|elektrik))|fayans ustası|seramik ustası|montajcı|usta fiyat"),
 ("tasarim", "Banyo tasarımı ve planlama", "Bathroom design and planning", "Hizmet-Set", "Kısmi", r"banyo tasarım|banyo çizim|3d banyo|banyo planla|banyo proje"),
 ("prefabrik", "Prefabrik ve hazır banyo", "Prefabricated bathroom pods", "Hizmet-Set", "Yok", r"prefabrik banyo|hazır banyo|modüler banyo|banyo kabini|konteyner banyo"),
 ("set", "Komple banyo ve setler", "Complete bathroom and sets", "Hizmet-Set", "Kısmi", r"komple banyo|banyo paket|vitrifiye set|klozet (ve )?lavabo|lavabo (ve )?klozet|^banyo (takımı|takımları|seti|setleri)( fiyat| model|$)"),
 # --- bitisik: su, isitma
 ("aritma_bat", "Arıtmalı ve filtreli batarya", "Filter and purifier taps", "Bitişik", "Yok", r"(arıtmalı|filtreli|3 yollu|üç yollu) (batarya|musluk|armatür)|içme suyu (musluğu|bataryası)"),
 ("aritma", "Su arıtma cihazı", "Water purifier", "Bitişik", "Yok", r"arıtma|reverse osmosis|kapalı kasa arıtma"),
 ("yumusatma", "Su yumuşatma ve kireç önleme", "Water softening and limescale", "Bitişik", "Yok", r"su yumuşat|kireç önle|kireç tutucu|manyetik kireç|yumuşatma cihaz"),
 ("sicaksu", "Şofben, termosifon ve su ısıtıcı", "Water heaters", "Bitişik", "Yok", r"şofben|sofben|termosifon|anında su ısıtıcı|ani su ısıtıcı|elektrikli su ısıtıcı(?! kettle)|boyler|sıcak su tankı"),
 ("havlupan", "Havlupan ve banyo radyatörü", "Towel radiators", "Bitişik", "Kısmi", r"havlupan|banyo radyatör|havlu ısıtıcı|havlu kurutucu"),
 ("banyo_isitici", "Banyo ısıtıcısı", "Bathroom heater", "Bitişik", "Yok", r"banyo ısıtıcı|banyo sobası|banyo için ısıtıcı"),
 ("tesisat", "Tesisat ekipmanı (hidrofor, basınç, kaçak)", "Plumbing equipment", "Bitişik", "Yok", r"hidrofor|basınç düşürücü|su kaçak|kaçak dedektör|su sayacı|pis su pompası|foseptik"),
 # --- bitisik: yapi
 ("yapi_kimya", "Yapıştırıcı, derz ve su yalıtımı", "Adhesives, grout and waterproofing", "Bitişik", "Kısmi", r"seramik yapıştır|fayans yapıştır|derz|su yalıtım|su izolasyon|banyo izolasyon|(banyo|mutfak|şeffaf|beyaz|küf önleyici) silikon|silikon tabanca|mastik|epoksi derz"),
 ("kaplama", "Alternatif duvar-zemin kaplama", "Alternative wall and floor cladding", "Bitişik", "Yok", r"lambri|pvc panel|duvar paneli|fayans boya|seramik boya|fayans üstü|seramik üstü|yapışkanlı fayans|folyo fayans|spc|vinil (zemin|parke)|zemin kaplama"),
 ("suzgec", "Yer süzgeci ve gider", "Floor drains", "Bitişik", "Kısmi", r"yer süzgeci|yer sifonu|pis su süzgeci|gider süzgeci|koku önleyici"),
 # --- bitisik: mutfak
 ("evye", "Mutfak evyesi (granit, çelik, akıllı)", "Kitchen sinks", "Bitişik", "Kısmi", r"evye|eviye|mutfak lavabo"),
 ("mutfak_tezgah", "Mutfak tezgahı", "Kitchen countertops", "Bitişik", "Yok", r"mutfak tezgah|porselen tezgah|çimstone|cimstone|quartz|kuvars|granit tezgah|mermer tezgah|kompakt laminat|belenco|silestone"),
 ("cop_ogutucu", "Çöp öğütücü", "Food waste disposer", "Bitişik", "Yok", r"çöp öğüt"),
 # --- bitisik: aksesuar, tekstil, duzen
 ("tekstil", "Banyo tekstili (havlu, bornoz, paspas, perde)", "Bath textiles", "Bitişik", "Yok", r"bornoz|banyo havlu|havlu set|el havlu|yüz havlu|banyo paspas|klozet paspas|banyo halı|duş perde|banyo perde"),
 ("duzen", "Banyo düzenleme ve depolama", "Bathroom storage and organisation", "Bitişik", "Kısmi", r"banyo düzenleyici|banyo organizer|duş rafı|köşe raf|banyo tabure|çamaşır sepet|kirli sepet|ecza dola[bp]|banyo arabası|banyo sepet|şampuanlık"),
 ("aydinlatma", "Banyo aydınlatması ve ışıklı ayna", "Bathroom lighting and lit mirrors", "BM", "Kısmi", r"ledli ayna|led ayna|ışıklı ayna|aydınlatmalı ayna|akıllı ayna|banyo aydınlatma|banyo aplik|ayna aplik|banyo lamba"),
 ("tarti", "Banyo tartısı", "Bathroom scale", "Bitişik", "Yok", r"banyo tartı|baskül"),
 # --- bitisik: ozel ihtiyac
 ("cocuk", "Çocuk ve bebek banyo ürünleri", "Children's and baby bathroom products", "Bitişik", "Kısmi", r"klozet adaptör|(ç|c)ocuk klozet|çocuk lavabo|bebek.*(küvet|kuvet)|skip hop|lazımlık|çocuk basamak|klozet basamak|oturak adaptör"),
 ("engelli", "Yaşlı ve engelli banyo ürünleri", "Accessible bathroom products", "Bitişik", "Kısmi", r"engelli|yaşlı|tutunma|tutamak|duş oturağı|duş sandalye|klozet yükselt|hasta klozet|refakatçi"),
 ("taharet_aparat", "Taharet aparatı ve bide kapağı", "Bidet attachments and seats", "SSG", "Yok", r"taharet aparat|bide aparat|taharet kapağı|bide kapağı|washlet|elektrikli klozet kapağı|ısıtmalı klozet kapağı|elektronik klozet kapağı|bide makinesi"),
 ("ticari", "Ticari hijyen (dispenser, el kurutma)", "Commercial hygiene", "Bitişik", "Kısmi", r"el kurutma|dispenser|kağıt havluluk|havlu makinesi|fotoselli sabun|sensörlü sabun"),
 ("yedek", "Yedek parça (kartuş, başlık, perlatör)", "Spare parts", "Armatür-Duş", "Kısmi", r"kartuş|perlatör|aeratör|musluk başlığı|musluk ucu|batarya ucu|musluk contası|batarya tamir|musluk tamir|\bspiral\b(?!li)|flexible hortum|esnek hortum|duş hortumu|şamandıra|\bkada\b|boşaltma grubu|klozet menteşe|kapak menteşe|menteşesi|yedek parça"),
 ("taharet_musluk", "Taharet musluğu ve el duşu", "Bidet valves and hand sprays", "Armatür-Duş", "Kısmi", r"taharet musluğ|taharet el duşu|taharet çubuğu|taharet ucu|taharet borusu"),
 ("bahce", "Bahçe, havuz ve dış mekan suyu", "Garden and outdoor water", "Bitişik", "Yok", r"bahçe musluğ|bahçe duş|havuz duş|dış mekan duş|bahçe lavabo|bahçe çeşme"),
 ("camasir_musluk", "Çamaşır makinesi musluğu", "Washing machine valve", "Armatür-Duş", "Kısmi", r"çamaşır makinesi musluğ|çamaşır musluğ"),
 ("wellness", "Sauna, buhar ve ev spası", "Sauna, steam and home spa", "Yıkanma", "Yok", r"sauna (kabin|soba|fiyat|odası|taş|ısıtıcı|yapım|malzeme|model)|ev tipi sauna|infrared sauna|^sauna$|buhar (odası|kabin|jeneratör)|hamam kabini|ev tipi hamam|infrared kabin"),
 ("jakuzi", "Jakuzi ve hidromasaj", "Jacuzzi and whirlpool", "Yıkanma", "Var", r"jakuzi|hidromasaj|spa havuz|şişme jakuzi"),
 # --- SSG
 ("akilli_klozet", "Akıllı klozet", "Smart WC", "SSG", "Var", r"akıllı klozet|akıllı tuvalet|smart klozet|japon tuvalet"),
 ("klozet_kapak", "Klozet kapağı", "Toilet seat", "SSG", "Var", r"klozet kapa|klozet kapağ|tuvalet kapağ|wc kapa"),
 ("ic_takim", "Rezervuar iç takımı", "Cistern inner mechanism", "SSG", "Var", r"iç takım|ic takim|rezervuar takım"),
 ("gomme_rez", "Gömme rezervuar ve kumanda paneli", "Concealed cistern and flush plate", "SSG", "Var", r"gömme rezervuar|gomme rezervuar|kumanda panel|gömme sifon"),
 ("rezervuar", "Rezervuar (dış)", "Cistern", "SSG", "Var", r"rezervuar"),
 ("pisuvar", "Pisuvar", "Urinal", "SSG", "Var", r"pisuvar|urinal"),
 ("hela", "Hela taşı", "Squat toilet", "SSG", "Var", r"hela taşı|helataşı|tuvalet taşı|alaturka"),
 ("bide", "Bide", "Bidet", "SSG", "Var", r"\bbide\b"),
 ("klozet", "Klozet", "WC", "SSG", "Var", r"klozet|klozed|alafranga tuvalet|tuvalet takımı|\bwc\b"),
 ("lavabo_dolap", "Lavabo dolabı", "Washbasin unit", "BM", "Var", r"lavabo dola[bp]|lavabolu dolap|lavabolu banyo dola[bp]|dolaplı lavabo"),
 ("dus_sis", "Duş sistemi, başlık ve set", "Shower systems", "Armatür-Duş", "Var", r"duş (sistem|başlı|seti|takımı|kolon|paneli)|yağmurlama|tepe duş|el duşu|duş bataryası"),
 ("batarya", "Batarya ve musluk", "Taps and mixers", "Armatür-Duş", "Var", r"batarya|musluk|armatür"),
 ("sifon", "Sifon", "Siphon", "Armatür-Duş", "Var", r"sifon"),
 ("lavabo", "Lavabo", "Washbasin", "SSG", "Var", r"lavabo"),
 # --- BM
 ("camasir_dolap", "Çamaşır ve kurutma makinesi dolabı", "Washer and dryer cabinet", "BM", "Var", r"(çamaşır|kurutma|bulaşık) makine(si)? dola[bp]|makine dola[bp]|çamaşır dola[bp]"),
 ("boy_dolap", "Banyo boy dolabı", "Tall cabinet", "BM", "Var", r"boy dola[bp]"),
 ("aynali_dolap", "Aynalı banyo dolabı", "Mirror cabinet", "BM", "Var", r"aynalı (banyo )?dolap|ayna dola[bp]"),
 ("ayna", "Banyo aynası", "Bathroom mirror", "BM", "Var", r"banyo ayna|lavabo ayna|tuvalet ayna|makyaj ayna"),
 ("banyo_raf", "Banyo rafı ve kulp", "Bathroom shelves and handles", "BM", "Kısmi", r"banyo raf|dolap kulp|banyo kulp|klozet üstü|klozet arkası|havluluk raf"),
 ("tezgah", "Banyo tezgahı", "Bathroom countertop", "BM", "Var", r"banyo tezgah|lavabo tezgah|tezgah üstü|tezgahüstü|lavabo altı tezgah"),
 ("banyo_dolap", "Banyo dolabı", "Bathroom cabinet", "BM", "Var", r"banyo dola[bp]|banyo dolap|banyo mobilya|banyo modül|pvc dolap|banyo alt dolap|banyo üst dolap"),
 # --- armatur, dus, yikanma, karo, aksesuar
 ("dusakabin", "Duşakabin", "Shower enclosure", "Yıkanma", "Var", r"duşakabin|duş kabin|duşa kabin|dusakabin|duş paravan|küvet paravan"),
 ("dus_tekne", "Duş teknesi ve kanalı", "Shower tray and channel", "Yıkanma", "Var", r"duş tekne|duş kanal|duş oluğu"),
 ("kuvet", "Küvet", "Bathtub", "Yıkanma", "Var", r"küvet|kuvet"),
 ("karo", "Karo, seramik ve fayans", "Tiles", "Karo", "Var", r"seramik|fayans|karo|porselen|granit seramik|mozaik|tezgah arası"),
 ("aksesuar", "Banyo aksesuarı", "Bathroom accessories", "Aksesuar", "Var", r"banyo aksesuar|tuvalet kağıtlı|havluluk|sabunluk|diş fırçalı|klozet fırça|tuvalet fırça|banyo askı|banyo çöp"),
 ("ilham", "Banyo ilham ve dekorasyon", "Bathroom inspiration", "Hizmet-Set", "Kısmi", r"banyo (dekorasyon|model|fikir|tasarımları)|küçük banyo|banyo (renk|trend)"),
]
NOISE = re.compile(r"(tuvalet kağıd|lavabo ?açıcı|kedi tuvalet|tuvalet eğitim|tuvalet temizl|klozet temizl|seramik (tabak|tava|kupa|fincan|vazo|saksı|atölye|kurs|boya|hamur|tencere|bardak|kase|heykel|çamur|fırın|bıçak|kaplama tava)|cihangir|otel|spa merkezi|masaj salonu|doğalgaz|kombi)|\b(prime|netflix|dizi|film|şarkı|oyun|araba|oto\b|otomobil|motor|kedi|köpek|tavuk|yemek|tarif|elbise|ayakkabı|iphone|samsung|laptop|telefon|kulaklık|saat|kitap|bebek bezi|diş macun|çay|kahve|tatlı|hamburger|pizza|minecraft|roblox|sims|gta)\b")
_C = [(k, tr, en, g, d, re.compile(rx)) for k, tr, en, g, d, rx in T]
def sinif(kw):
    if NOISE.search(kw): return None
    for k, tr, en, g, d, rx in _C:
        if rx.search(kw): return k
    return None
META = {k: {"tr": tr, "en": en, "grup": g, "durum": d} for k, tr, en, g, d, _ in T}
