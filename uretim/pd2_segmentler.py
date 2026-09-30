# VitrA e-ticaret alt kategori taramasi (2. tur): kesit tanimlari.
# (anahtar, ana kategori, alt kategori, arama ifadesi, eslesme regex (ASCII katlanmis, kucuk harf), vitra.com.tr kategori yolu)
SEGMENTLER = [
 # Klozet
 ("yerden-tek-klozet","Klozet","Yerden tek klozet (ayaklı klozet)","ayaklı klozet",r"^(?!.*(kapak|firca|ortu|adaptor|oturak|dispenser|paspas|batarya))(?=.*(klozet|wc))",['/c-yerden-tek-klozetler']),
 ("asma-klozet-takimi","Klozet","Asma klozet takımı (klozet + gömme rezervuar seti)","asma klozet takımı rezervuar seti",r"^(?!.*(kapak|firca|ortu|adaptor|oturak|dispenser|paspas))(?=.*klozet)",['/c-asma-klozet-takimlari']),
 ("tuvalet-tasi-alaturka","Klozet","Tuvalet taşı (alaturka)","alaturka tuvalet taşı",r"alaturka|tuvalet tas|helatas|hela tas|turk tipi|yer klozet",['/c-tuvalet-tasi']),
 ("cocuk-klozet","Klozet","Çocuk klozet","çocuk klozeti",r"cocuk",[]),
 ("engelli-klozet","Klozet","Engelli klozet","engelli klozeti",r"^(?=.*engelli)(?=.*(klozet|wc|tuvalet))",[]),
 # Lavabo
 ("canak-lavabo","Lavabo","Çanak lavabo","çanak lavabo",r"^(?!.*batarya)(?=.*(canak|tezgah ustu|tezgahustu))",['/c-canak-lavabolar']),
 ("monoblok-lavabo","Lavabo","Monoblok lavabo","monoblok lavabo",r"monoblok",['/c-monoblok-lavabolar']),
 ("yarim-tezgah-lavabo","Lavabo","Yarım tezgah lavabo","yarım tezgah lavabo",r"yarim",['/c-yarim-tezgah-lavabolar']),
 ("etajerli-lavabo","Lavabo","Etajerli lavabo","etajerli lavabo",r"etajer",['/c-etajerli-lavabolar']),
 ("ayakli-lavabo","Lavabo","Ayaklı (standart) lavabo","ayaklı lavabo",r"ayakli|pedestal|tam ayak|yarim ayak",['/c-standart-lavabo-ve-ayaklari']),
 ("kose-lavabo","Lavabo","Köşe lavabo","köşe lavabo",r"kose",[]),
 ("lavabo-ayagi","Lavabo","Lavabo ayağı","lavabo ayağı",r"lavabo.*ayak|ayak.*lavabo|yarim ayak|tam ayak",[]),
 # Armatür
 ("bide-bataryasi","Armatür","Bide bataryası","bide bataryası",r"bide.*batarya|batarya.*bide|taharet.*batarya|taharet musluk",['/c-bide-bataryalari']),
 ("kuvet-bataryasi","Armatür","Küvet bataryası","küvet bataryası",r"(kuvet|banyo|duvardan).*batarya|batarya.*(kuvet|banyo)",['/c-kuvet-bataryalari']),
 ("termostatik-batarya","Armatür","Termostatik batarya","termostatik batarya",r"termostatik",['/c-termostatik-bataryalar']),
 ("fotoselli-lavabo-bataryasi","Armatür","Temassız (fotoselli) lavabo bataryası","fotoselli lavabo bataryası",r"(foto|temassiz|sensor|otomatik).*(batarya|musluk)|(batarya|musluk).*(foto|temassiz|sensor|otomatik)",['/c-temassiz-lavabo-bataryalari']),
 ("siva-ustu-banyo-bataryasi","Armatür","Duvardan (sıva üstü) banyo bataryası","sıva üstü banyo bataryası",r"siva ustu|duvardan|duvar tip",['/c-duvardan-banyo-bataryalari']),
 ("yuksek-canak-lavabo-bataryasi","Armatür","Çanak lavabo bataryası (yüksek)","yüksek çanak lavabo bataryası",r"yuksek|canak|uzun",['/c-canak-lavabo-bataryalari']),
 ("ankastre-stop-valf","Armatür","Ankastre stop valf","ankastre stop valf",r"stop valf|valf|ara kesme|vana",['/c-ankastre-stop-valfler']),
 ("lavabo-sifonu-susuzgeci","Armatür","Lavabo sifon ve süzgeci","lavabo sifonu süzgeci",r"sifon|suzgec",['/c-lavabo-sifon-ve-suzgecleri']),
 ("armatur-cikis-ucu-dirsek","Armatür","Armatür tamamlayıcı (çıkış ucu, dirsek)","duş çıkış ucu dirsek",r"cikis|dirsek|nipel",['/c-banyo-batarya-cikis-uclari', '/c-dus-dirsekleri']),
 # Duşlar
 ("dus-kolonu","Duşlar","Duş kolonu","duş kolonu",r"kolon|dus sistem|yagmurlama|robot dus",['/c-dus-kolonlari']),
 ("el-dusu-takimi","Duşlar","El duşu takımı","el duşu takımı",r"el dusu",['/c-el-dusu-takimlari']),
 ("surgulu-el-dusu-takimi","Duşlar","Sürgülü el duşu takımı","sürgülü el duşu takımı",r"surgulu",['/c-surgulu-el-dusu-takimlari']),
 ("masajli-dus-sistemi","Duşlar","Masajlı duş sistemi","masajlı duş sistemi",r"masaj",['/c-masajli-dus-sistemleri']),
 ("bataryali-dus-sistemi","Duşlar","Bataryalı duş sistemi","bataryalı duş sistemi",r"bataryali|dus sistem|dus seti",['/c-bataryali-dus-sistemleri']),
 ("ankastre-dus-yonlendirici","Duşlar","Ankastre duş yönlendirici","ankastre duş yönlendirici",r"yonlendirici|divertor|ankastre",['/c-ankastre-dus-yonlendiriciler']),
 # Rezervuar
 ("kumanda-paneli-mekanik","Rezervuar","Rezervuar kumanda paneli (mekanik)","mekanik kumanda paneli rezervuar",r"kumanda",['/c-mekanik-kumanda-panelleri']),
 ("kumanda-paneli-temassiz","Rezervuar","Rezervuar kumanda paneli (temassız)","temassız kumanda paneli rezervuar",r"kumanda",['/c-temassiz-kumanda-panelleri']),
 ("kumanda-paneli-akilli","Rezervuar","Rezervuar kumanda paneli (akıllı)","akıllı kumanda paneli rezervuar",r"kumanda",['/c-akilli-kumanda-panelleri']),
 ("tasiyici-aparat","Rezervuar","Taşıyıcı aparat (asma klozet taşıyıcı)","asma klozet taşıyıcı",r"tasiyici|montaj sistem|gomme rezervuar|klozet aparat",['/c-tasiyici-aparatlar']),
 ("duvar-onu-rezervuar","Rezervuar","Duvar önü rezervuar","duvar önü rezervuar",r"rezervuar",['/c-duvar-onu-rezervuarlar']),
 ("tuvalet-tasi-rezervuari","Rezervuar","Tuvalet taşı rezervuarı","tuvalet taşı rezervuarı",r"rezervuar",['/c-tuvalet-taslari-icin-gomme-rezervuarlar']),
 # Yıkanma alanları
 ("dus-kanali","Yıkanma alanları","Duş kanalı","duş kanalı",r"kanal|gider|suzgec",['/c-dus-kanallari']),
 ("dus-unitesi","Yıkanma alanları","Duş ünitesi (kompakt duş kabini)","kompakt duş kabini",r"kompakt dus|dus unite|dus kabin",['/c-dus-uniteleri']),
 ("hidromasajli-kuvet","Yıkanma alanları","Hidromasajlı küvet","hidromasajlı küvet",r"hidromasaj|kuvet",['/c-hidromasajli-bagimsiz-kuvetler', '/c-hidromasajli-standart-kuvetler']),
 ("bagimsiz-kuvet","Yıkanma alanları","Bağımsız küvet","bağımsız küvet",r"bagimsiz|kuvet",['/c-hidromasajsiz-bagimsiz-kuvetler']),
 ("kuvet-paneli","Yıkanma alanları","Küvet paneli","küvet paneli",r"panel",['/c-kuvet-panelleri']),
 ("dus-teknesi-paneli","Yıkanma alanları","Duş teknesi paneli","duş teknesi paneli",r"panel|tekne",['/c-dus-teknesi-panelleri']),
 ("kaydirmaz","Yıkanma alanları","Kaydırmaz","küvet kaydırmaz",r"kaydirmaz|kaymaz",['/c-vitra-kaydirmaz']),
 # Banyo mobilyası
 ("banyo-tezgahi","Banyo mobilyası","Banyo tezgahı","banyo tezgahı",r"tezgah",['/c-banyo-tezgahlari']),
 ("banyo-konsolu","Banyo mobilyası","Banyo konsolu","banyo konsolu",r"konsol",['/c-banyo-konsollari']),
 ("banyo-set-modulu","Banyo mobilyası","Banyo set modülü","banyo mobilya set modül",r"set|modul|banyo mobilya",['/c-banyo-set-modulleri']),
 ("malzemelik","Banyo mobilyası","Malzemelik","banyo malzemelik dolabı",r"malzemelik|boy dolab",['/c-banyo-malzemelikleri']),
 ("dolap-kulpu","Banyo mobilyası","Dolap kulpu","banyo dolap kulpu",r"kulp",['/c-banyo-dolabi-kulplari']),
 ("dolap-ayagi","Banyo mobilyası","Dolap ayağı","banyo dolap ayağı",r"ayak",['/c-banyo-dolap-ayaklari']),
 ("makyaj-aynasi","Banyo mobilyası","Makyaj aynası","makyaj aynası",r"makyaj|ayna",['/c-makyaj-aynalari-ve-diger-aksesuarlar']),
 ("aynali-dolap","Banyo mobilyası","Aynalı dolap","aynalı banyo dolabı",r"aynali|ayna",['/c-aynali-banyo-dolabi']),
 # Banyo aksesuarı
 ("sabunluk","Banyo aksesuarı","Sabunluk","banyo sabunluk",r"sabunluk|sabun kabi|dispenser",['/c-sabunluklar']),
 ("dis-fircaligi","Banyo aksesuarı","Diş fırçalığı","diş fırçalığı",r"dis fircal|fircalik|dis fir",['/c-dis-fircaliklari']),
 ("tuvalet-kagitligi","Banyo aksesuarı","Tuvalet kağıtlığı","tuvalet kağıtlığı",r"kagitlik|kagit",['/c-tuvalet-kagitliklari']),
 ("tuvalet-fircasi","Banyo aksesuarı","Tuvalet fırçası","tuvalet fırçası",r"firca",['/c-tuvalet-fircalari']),
 ("banyo-askisi","Banyo aksesuarı","Banyo askısı","banyo askısı",r"aski|havlu",['/c-banyo-askilari']),
 ("banyo-cop-kovasi","Banyo aksesuarı","Banyo çöp kovası","banyo çöp kovası",r"cop|kova",['/c-banyo-cop-kovalari']),
 ("havluluk","Banyo aksesuarı","Havluluk","havluluk",r"havlu",['/c-havluluklar']),
 # Vitrifiye tamamlayıcı
 ("pisuvar-ara-bolmesi","Vitrifiye tamamlayıcı","Pisuvar ara bölmesi","pisuvar ara bölmesi",r"bolme",['/c-pisuvar-ara-bolmeleri']),
 ("pisuvar-yikama-sistemi","Vitrifiye tamamlayıcı","Pisuvar yıkama sistemi","pisuvar yıkama sistemi",r"yikama|flush|pisuvar",['/c-pisuvar-yikama-sistemleri']),
]
OZEL_SAYFALAR = [("online-ozel","/c-online-ozel"),("kampanyali-urunler","/c-kampanyali-urunler"),("ucretsiz-montaj","/c-ucretsiz-montaj")]
