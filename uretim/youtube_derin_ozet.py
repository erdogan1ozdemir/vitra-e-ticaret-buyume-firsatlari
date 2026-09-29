# -*- coding: utf-8 -*-
"""ozet.md uretimi (arama.json + analiz.json + yorum_temalari.json)"""
import json, os, csv, re, statistics, collections
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(P, "veri/ham/derin/youtube")
A = json.load(open(os.path.join(D, "analiz.json"), encoding="utf-8"))
AR = json.load(open(os.path.join(D, "arama.json"), encoding="utf-8"))
YT = json.load(open(os.path.join(D, "yorum_temalari.json"), encoding="utf-8"))
YR = json.load(open(os.path.join(D, "yorumlar.json"), encoding="utf-8"))
rows = list(csv.DictReader(open(os.path.join(D, "arama_video_tablosu.csv"), encoding="utf-8-sig")))
for x in rows: x["izlenme"] = int(x["izlenme"]); x["sira"] = int(x["sira"])
def n(v): return f"{v:,}".replace(",", ".")
def kisa(v):
    if v >= 1e6: return f"{v/1e6:.1f}M"
    if v >= 1e3: return f"{v/1e3:.0f}K" if v >= 1e4 else f"{v/1e3:.1f}K"
    return str(v)
def t(*c): return "| " + " | ".join(str(x).replace("|", "/") for x in c) + " |"
def kes(s, k=60): return s if len(s) <= k else s[:k - 1].rstrip() + "..."
aramaz = {z["arama"]: z for z in A["arama"]}
for k, z in aramaz.items():
    r = [x for x in rows if x["arama"] == k and x["alakasiz"] == "False"]
    z["toplam"] = sum(x["izlenme"] for x in r); z["medyan"] = int(statistics.median(x["izlenme"] for x in r)); z["en"] = max(r, key=lambda x: x["izlenme"])
    vit = [x for x in rows if x["arama"] == k and x["vitra_kanali"] == "True"]
    z["vitra_txt"] = ("VitrA/Artema: sıra " + ", ".join(str(x["sira"]) for x in vit[:3])) if vit else "Yok"
L = []
w = L.append
tv = len(A["arama"])
w("# YouTube derin analiz: banyo kategorilerinde izlenen içerik, görünür kanallar ve yorum temaları")
w("")
w("Kaynak: YouTube · DataForSEO · 29.09.2026")
w("")
w("**Kapsam:** Türkiye (`location_code` 2792), Türkçe. 68 yeni arama (önceki turdaki 30 arama tekrarlanmadı), her aramada ilk 20 video (%s video satırı, %s tekil video, %s tekil kanal). Yorum analizi için %d video seçildi, %s yorum çekildi." % (n(A["toplam_satir"]), n(A["toplam_tekil_video"]), n(A["toplam_kanal"]), YT["video"], n(YT["cekilen_yorum"])))
w("")
w("**Okuma notları:** İzlenme değerleri arama sonucunda görünen anlık değerlerdir; yayın tarihi YouTube'un göreli ifadesiyle (\"7 yıl önce\") geldiği için tarih bazlı hesap yapılmamıştır. Toplam izlenme, aynı video birden fazla aramada çıksa da bir kez sayılarak hesaplanmıştır. Alakasız sonuçlar (müzik klibi, telefon pili, mobilya markası Vitra vb.) toplamlara dahil edilmemiş, satırlar CSV'de `alakasiz=True` olarak işaretlenmiştir. Tek bir viral video toplamı belirgin biçimde etkilediğinden medyan değerler de verilmiştir. Video başlıkları, arama kelimeleri ve yorum alıntıları kaynaktaki yazımıyla (ör. \"Vitra\") birebir korunmuştur. VitrA/Artema marka kanalı olarak VitrA Türkiye, VitrA Bathrooms ve Artema Türkiye sayılmıştır; Vitra Artema Yetkili Servis Başarı yapı ve Vitra Georgia \"VitrA ilişkili\" olarak ayrı işaretlenmiştir.")
w("")
# (a)
w("## (a) Grup bazında arama sonuçları")
w("")
w(t("Grup", "Arama", "Tekil video", "Toplam izlenme", "Medyan video izlenmesi", "En yüksek izlenen video", "VitrA/Artema kanalı olan arama", "VitrA marka video (tekil)", "VitrA ort. en iyi sıra"))
w(t(*["---"] * 9))
tp = collections.Counter()
for g, v in A["grup"].items():
    w(t(g, v["arama"], v["tekil_video"], kisa(v["toplam_izlenme_tekil"]), n(v["medyan_izlenme_video"]), "%s (%s)" % (kes(v["en_yuksek_video"], 45), kisa(v["en_yuksek_video_izlenme"])),
        "%d / %d" % (v["vitra_olan_arama"], v["arama"]), v["vitra_tekil_video"], v["vitra_ort_en_iyi_sira"] if v["vitra_ort_en_iyi_sira"] else "-"))
tvit = sum(v["vitra_olan_arama"] for v in A["grup"].values())
w("")
w("Toplamda 68 aramanın %d tanesinde VitrA/Artema marka kanalından en az bir video ilk 20'de yer almaktadır." % tvit)
w("")
w("### Arama bazında sonuçlar")
w("")
w(t("Grup", "Arama", "Toplam izlenme (ilk 20)", "Medyan", "En yüksek izlenen video", "VitrA / Artema"))
w(t(*["---"] * 6))
for g in A["grup"]:
    for k, z in aramaz.items():
        if z["grup"] != g: continue
        w(t(g, k, kisa(z["toplam"]), n(z["medyan"]), "%s / %s (%s)" % (kes(z["en"]["baslik"], 42), z["en"]["kanal"], kisa(z["en"]["izlenme"])), z["vitra_txt"]))
w("")
w("Ayrıntılı satırlar (68 arama x 20 video: başlık, kanal, izlenme, yayın, süre, sıra, VitrA/Artema işareti): `arama_video_tablosu.csv`.")
# (b)
w("")
w("## (b) Kanal tablosu (ilk 30, görünme sayısına göre)")
w("")
w("Görünme: 68 aramanın ilk 20 sonuçlarında kanalın yer aldığı toplam satır sayısı. Toplam izlenme: kanalın görünen tekil videolarının toplamı. Tür sınıflaması kanal adı ve video başlıklarına göre kural tabanlıdır (ilk 30 kanal elle doğrulanmıştır).")
w("")
w(t("#", "Kanal", "Tür", "Görünme", "Arama", "Tekil video", "Toplam izlenme", "Grup dağılımı"))
w(t(*["---"] * 8))
kisa_g = {"Seçim ve karşılaştırma": "Seçim", "Montaj": "Montaj", "Tamir ve bakım": "Tamir", "İlham ve tadilat": "İlham", "Marka ve rakip": "Marka", "Yeni kategoriler": "Yeni"}
for i, z in enumerate(A["kanal"][:30], 1):
    w(t(i, z["kanal"], z["tur"], z["gorunme"], z["arama_sayisi"], z["tekil_video"], kisa(z["toplam_izlenme_tekil"]), ", ".join("%s %d" % (kisa_g[g], c) for g, c in sorted(z["gruplar"].items(), key=lambda q: -q[1]))))
w("")
w("Tüm kanal listesi (%s kanal): `kanal_analizi.csv`." % n(A["toplam_kanal"]))
w("")
w("### Kanal türü dağılımı")
w("")
w(t("Tür", "Kanal", "Görünme", "Görünme payı", "Toplam izlenme (tekil video)"))
w(t(*["---"] * 5))
tg = sum(v["gorunme"] for v in A["tur"].values())
for k, v in sorted(A["tur"].items(), key=lambda q: -q[1]["gorunme"]):
    w(t(k, v["kanal"], v["gorunme"], "%%%.1f" % (100 * v["gorunme"] / tg), kisa(v["izlenme"])))
w("")
w("\"Diğer\" türü; tek görünmeli, video başlığından türü anlaşılamayan kanalları ve alakasız sonuçları içerir.")
# (c)
w("")
w("## (c) VitrA ve rakip marka kanallarının görünürlüğü")
w("")
w("Hücre değeri: görünme sayısı / görünülen arama sayısı (ilk 20 içinde).")
w("")
G = list(A["grup"])
w(t("Kanal", *[kisa_g[g] for g in G], "Toplam görünme", "Arama", "Tekil video", "Toplam izlenme"))
w(t(*["---"] * (len(G) + 5)))
for k, v in A["marka_kanal"].items():
    w(t(k, *["%d / %d" % (v[g]["gorunme"], v[g]["arama"]) if v[g]["gorunme"] else "-" for g in G], v["toplam"]["gorunme"], v["toplam"]["arama"], v["toplam"]["tekil_video"], kisa(v["toplam"]["izlenme_tekil"])))
w("")
w("### Video başlığında marka adı geçen içerikler (tüm kanallar)")
w("")
w("Başlıkta marka adı geçen tekil videolar; \"üçüncü taraf\" marka kanalı dışındaki (usta, perakendeci, dekorasyon vb.) kanalların videolarıdır.")
w("")
w(t("Marka", "Tekil video", "Toplam izlenme", "Üçüncü taraf video", "Üçüncü taraf izlenme", "Üçüncü taraf tamir videosu", "Görülen arama"))
w(t(*["---"] * 7))
for k, v in sorted(A["marka_bahis"].items(), key=lambda q: -q[1]["ucuncu_taraf_izlenme"]):
    w(t(k, v["tekil_video"], kisa(v["izlenme"]), v["ucuncu_taraf_video"], kisa(v["ucuncu_taraf_izlenme"]), v["ucuncu_taraf_tamir_video"], v["arama_sayisi"]))
w("")

# (d) yorumlar
w("## (d) Yorum madenciliği")
w("")
w("### Seçilen videolar ve çekilen yorumlar")
w("")
w("Seçim ölçütü: VitrA/Artema ürünü içeren tamir ve montaj videoları, rakip marka tamir/montaj videoları, marka belirsiz ama yüksek izlenmeli tamir videoları, seçim/satın alma ve tadilat videoları. Her video için en fazla 100 yorum çekilmiştir (API üst sınırı sonuç sayfasıdır; videonun toplam yorum sayısı daha düşükse tamamı alınmıştır). E8Dz5MTFIBg (Banyotrendy, V-Care) videosunda yorum verisi dönmediği için analize alınamamıştır.")
w("")
w(t("Video", "Kanal", "Tür", "İzlenme", "Toplam yorum", "Çekilen", "Analize giren"))
w(t(*["---"] * 7))
vmeta = {x["video_id"]: x for x in rows}
kanal_v = {}
for k, v in AR["aramalar"].items():
    for x in v["videolar"]:
        if x.get("video_id"): kanal_v.setdefault(x["video_id"], (x["kanal"], x["goruntulenme"]))
old = json.load(open(os.path.join(P, "veri/ham/autocomplete_youtube.json"), encoding="utf-8"))["youtube"]
for v in old.values():
    for x in v:
        m = re.search(r"(?:v=|shorts/)([\w-]{11})", x.get("url") or "")
        if m: kanal_v.setdefault(m.group(1), (x["kanal"], x["goruntulenme"]))
for v in sorted(YT["videolar"], key=lambda q: (q["tur"], -(kanal_v.get(q["video_id"], ("", 0))[1] or 0))):
    kv = kanal_v.get(v["video_id"], ("?", 0))
    w(t("[%s](https://www.youtube.com/watch?v=%s)" % (kes(v["baslik"], 55), v["video_id"]), kv[0], v["tur"], n(kv[1] or 0), v["toplam_yorum"], v["cekilen"], v["gecerli"]))
w("")
w("Toplam: %d video, %s yorum çekildi; %d kanal sahibi yorumu ve %d telefon/iletişim paylaşımı (reklam niteliğinde) hariç tutuldu; **%s yorum** sınıflandırmaya girdi." % (YT["video"], n(YT["cekilen_yorum"]), YT["sahip_yorumu"], YT["reklam_iletisim"], n(YT["gecerli"])))
w("")
w("### Tema tablosu")
w("")
w("Bir yorum birden fazla temaya girebildiği için satır toplamı %100'ü aşar. Pay, sınıflandırmaya giren yorumlar içindeki orandır. VitrA/Artema sütunu, VitrA/Artema ürünlü tamir-montaj videolarındaki yorum sayısıdır.")
w("")
w(t("Tema", "Yorum", "Pay", "VitrA/Artema videolarında", "Rakip marka videolarında", "Marka belirsiz tamir videolarında", "Seçim/satın alma videolarında", "Tadilat videolarında"))
w(t(*["---"] * 8))
TURK = ["VitrA/Artema ürünlü tamir-montaj", "Rakip marka tamir-montaj", "Marka belirsiz tamir-montaj (yüksek izlenmeli)", "Seçim, inceleme, satın alma", "Tadilat ve ilham"]
for ad, v in YT["temalar"].items():
    w(t(ad, v["yorum"], "%%%.1f" % v["pay_gecerli"], *[v["tur_dagilim"].get(k, 0) for k in TURK]))
w(t("Temasız / sınıflanamayan", YT["temasiz"], "%%%.1f" % YT["temasiz_pay"], "", "", "", "", ""))
w(t("*Analize giren yorum*", YT["gecerli"], "", *[YT["tur_yorum"].get(k, 0) for k in TURK]))
w("")
w("### Yorumlarda anılan markalar")
w("")
mm = sorted(YT["marka_anilma"].items(), key=lambda q: -q[1])
w(t("Marka", "Anıldığı yorum"))
w(t("---", "---"))
for k, v in mm: w(t(k, v))
w("")
w("### Tema başına alıntılar (birebir, en fazla 25 kelime)")
for ad, v in YT["temalar"].items():
    w("")
    w("**%s** (%d yorum, %%%.1f)" % (ad, v["yorum"], v["pay_gecerli"]))
    w("")
    for q in v["alintilar"]:
        w("- \"%s\" ([video](%s), %d beğeni)" % (q["metin"].replace("\n", " ").strip(), q["url"], q["begeni"]))
w("")
w("### Sınıflama kuralları")
w("")
w("Sınıflama anahtar kelime listeleriyle yapılmıştır (`uretim/youtube_derin_yorum_analiz.py`, TEMALAR sözlüğü). Metin önce Türkçe karakter uyumlu küçük harfe çevrilir; kurallar düzenli ifadedir. Sınıflandırma öncesi iki ayıklama yapılır: (1) yazarı videonun kanalıyla aynı olan yorumlar (kanal sahibi), (2) telefon numarası, WhatsApp/iletişim kalıbı içeren yorumlar (hizmet reklamı).")
w("")
w(t("Tema", "Kural (özet)"))
w(t("---", "---"))
w(t("Parça bulma / yedek parça", "\"yedek parça\", \"parça bul\", \"temin\" ya da parça kelimesi (iç takım, conta, kartuş, şamandıra, mekanizma, kumanda, sifon, menteşe, hortum, kapak vb.) ile edinme/uyum kelimesinin (nereden, bulamadım, satın, link, kod, model, uyar, orijinal, ölçü, hangi vb.) birlikte geçmesi"))
w(t("Servis ve garanti", "servis, garanti, yetkili, müşteri hizmetleri, çağrı merkezi, şikayet, iade, değişim yaptı, üretici"))
w(t("Montaj zorluğu / uygulama soruları", "takamadım, oturmuyor, sıkıştı, sökemedi, beceremedim, uymuyor, olmadı, nasıl takılır/sökülür/ayarlanır/değiştirilir, hangi anahtar/tornavida, kaç mm"))
w(t("Usta ücreti / usta bulma", "usta/tesisatçı çağırma-bulamama-ücret-istedi ifadeleri, işçilik, servis ücreti, \"biri var mı\", \"gelir misiniz\", bölge/hizmet sorusu"))
w(t("Fiyat", "fiyat, pahalı, ucuz, para, TL/lira/₺, maliyet, bütçe, kazık, ödedim, indirim, taksit, \"kaç para\", \"ne kadar\""))
w(t("Ürün kalitesi / kırılma / sızıntı", "sızdır, sızıntı, su kaçır(ıyor), kırıl, çatla, bozuk/bozul, kalitesiz, defolu, arıza, paslan, ömrü, plastik, dökül, damlıyor, akıtıyor, tutmuyor, çalışmıyor"))
w(t("Marka karşılaştırması", "aynı yorumda iki farklı marka adı ya da bir marka adı + karşılaştırma ifadesi (daha iyi, yerine, tercih, hangisi, aynı sorun, bende de vb.)"))
w(t("Satın alma kanalı", "Koçtaş, Trendyol, Hepsiburada, N11, Amazon, Bauhaus, Tekzen, IKEA, mağaza, \"nereden aldın/alınır\", sipariş, kargo, internetten, bayi, hırdavat, satın al, link"))
w(t("Teşekkür / genel", "teşekkür, sağ ol, eline sağlık, emeğine, Allah razı olsun, harika, süper, işime yaradı, çözüldü, çalıştı, kurtardın, faydalı"))
w("")
w("Sınırlılıklar: kural tabanlı yöntem ironi ve bağlamı ayırt edemez; \"su kaçırıyor\" gibi ifadeler videonun konusunu tarif ettiği için ürün kalitesi temasını şişirebilir (tamir videolarında yorumcunun kendi ürününü anlatması bu temaya girer). Oranlar yön göstericidir; kesin ölçüm değildir. Tüm sınıflanmış yorumlar `yorumlar_siniflandirilmis.csv` dosyasındadır.")
w("")

# (e) firsatlar
BAGLAR = ['Var (gömme rezervuar videoları)', 'Var (gömme rezervuar videoları)', 'Var (gömme rezervuar, kumanda paneli videoları)', 'Var (Artema batarya videoları)', 'Kısmen (lavabo ürünleri)', 'Dolaylı', 'Var (Artema batarya videoları)', 'Doğrulanmadı', 'Kısmen (duş teknesi videosu var, duşakabin doğrulanmadı)', 'Dolaylı (tadilat serisi)', 'Dolaylı (tadilat serisi)', 'Dolaylı (tadilat serisi)', 'Var (V-Care)', 'Var (V-Fix)', 'Var (banyo dolabı videosu)', 'Kısmen', 'Var (Artema batarya videoları)', 'Doğrulanmadı', 'Doğrulanmadı', 'Doğrulanmadı', 'Doğrulanmadı']
FIRSAT = [
 ("Klozet sifon / iç takım değiştirme, su kaçırma", ["sifon değiştirme"], "VitrA gömme rezervuar iç takım ve conta değişimi: parça numaralarıyla adım adım video"),
 ("Rezervuar şamandıra ve su seviyesi ayarı", ["rezervuar şamandıra ayarı"], "VitrA gömme rezervuar şamandıra ve su seviyesi ayarı, 3 dakikada"),
 ("Gömme rezervuar su doldurmuyor / geç doluyor", ["gömme rezervuar su doldurmuyor"], "VitrA gömme rezervuar su doldurmuyor: nedenleri ve çözümü"),
 ("Batarya damlatıyor, aç-kapa kartuş değişimi", ["batarya damlatıyor", "musluk kartuşu değişimi"], "Artema batarya damlatıyor: kartuş değişimi ve parça bulma"),
 ("Lavabo sifonu tıkanıklığı ve sifon temizliği", ["lavabo sifonu tıkandı"], "VitrA lavabo sifonu tıkandı: sökmeden ve sökerek açma"),
 ("Banyoda silikon çekme", ["silikon çekme banyo"], "Lavabo, klozet ve duş teknesi çevresinde silikon uygulaması"),
 ("Batarya kireç temizliği", ["kireç temizliği batarya"], "Artema batarya kireç temizliği ve bakım rehberi"),
 ("Taharet musluğu takma", ["taharet musluğu takma"], "Taharet musluğu montajı (klozet ve batarya uyumuyla)"),
 ("Duşakabin kurulum, seçim ve teker değişimi", ["duşakabin kurulumu", "duşakabin nasıl seçilir", "duşakabin tekeri değişimi"], "Duşakabin nasıl seçilir, nasıl kurulur, teker nasıl değişir (üç kısa video)"),
 ("Banyo tadilatı maliyeti ve öncesi-sonrası", ["banyo tadilatı maliyeti", "banyo tadilatı öncesi sonrası"], "Banyo tadilatı maliyet kalemleri: ürün seçimi ve işçilik"),
 ("Küçük banyo ve kiralık ev banyo yenileme", ["küçük banyo yenileme", "kiralık ev banyo yenileme", "banyo dekorasyonu"], "Kırmadan dökmeden banyo yenileme: klozet, lavabo, batarya değişimiyle"),
 ("Fayans boyama ve fayans üstüne fayans", ["fayans boyama", "fayans üstüne fayans"], "Tadilat serisine bağlanan içerik; ürün bağı zayıf, izlenme yüksek"),
 ("Akıllı klozet karar içeriği", ["akıllı klozet alınır mı"], "Akıllı klozet alınır mı: V-Care için kullanım, bakım ve fiyat/değer videosu"),
 ("Rakip gömme rezervuar karşılaştırması (Geberit)", ["geberit gömme rezervuar"], "VitrA V-Fix ile Geberit gömme rezervuar karşılaştırması"),
 ("Banyo dolabı marka ve malzeme kararı", ["en iyi banyo dolabı markası", "trendyol banyo dolabı inceleme"], "Banyo dolabı hangi marka, hangi malzeme: VitrA banyo dolabı inceleme"),
 ("Lavabo seçimi", ["lavabo nasıl seçilir"], "Lavabo nasıl seçilir: çanak, tezgah üstü, asma karşılaştırması"),
 ("Ankastre ve termostatik batarya montajı", ["ankastre batarya montajı"], "Artema ankastre duş bataryası montajı"),
 ("Havlupan montajı ve elektrikli havlupan", ["havlupan montajı", "elektrikli havlupan"], "Havlupan montajı: kablo, bağlantı ve duvar hazırlığı"),
 ("Çocuk klozet adaptörü", ["çocuk klozet adaptörü"], "Çocuk klozet adaptörü kullanımı ve klozet kapağı uyumu"),
 ("Engelli banyo düzenlemesi", ["engelli banyo düzenlemesi"], "Engelli ve yaşlı için banyo düzeni: klozet, lavabo, duş seçimi"),
 ("Çamaşır makinesi dolabı montajı", ["çamaşır makinesi dolabı montajı"], "Çamaşır makinesi dolabı montajı ve banyo yerleşimi"),
]
w("## (e) VitrA için video fırsatları")
w("")
w("Ölçüt: aranan konuda ilk 20 sonuçta VitrA/Artema marka kanalından video bulunmayan ya da yalnızca üçüncü taraf kanalların VitrA konusunu anlattığı başlıklar. \"VitrA anılan üçüncü taraf video\" sütunu, başlığında VitrA/Artema geçen ama marka kanalına ait olmayan videoları gösterir. Ürün bağı kanalın mevcut video envanterinden (VitrA Türkiye montaj videoları: gömme rezervuar, kumanda paneli, klozet kapağı, banyo dolabı, batarya, duş sistemi, duş teknesi) çıkarılmış, katalog doğrulaması yapılmamıştır.")
w("")
w(t("#", "Konu", "Arama", "Toplam izlenme (ilk 20)", "En yüksek video", "VitrA/Artema marka videosu", "VitrA anılan üçüncü taraf video", "Ürün bağı", "Önerilen video"))
w(t(*["---"] * 9))
firsat_out = []
for i, (konu, aramalar, oneri) in enumerate(FIRSAT, 1):
    ks = [k for k in aramalar if k in aramaz]
    tk = {}
    for k in ks:
        for x in rows:
            if x["arama"] == k and x["alakasiz"] == "False": tk[x["video_id"]] = x
    top = sum(x["izlenme"] for x in tk.values())
    en = max(tk.values(), key=lambda x: x["izlenme"])
    vm = {x["video_id"]: x for x in tk.values() if x["vitra_kanali"] == "True"}
    v3 = {x["video_id"]: x for x in tk.values() if re.search("vitra|artema", x["baslik"], re.I) and x["vitra_kanali"] != "True"}
    vm_txt = ("%d video (en iyi sıra %d)" % (len(vm), min(x["sira"] for x in vm.values()))) if vm else "Yok"
    v3_txt = ("%d video / %s" % (len(v3), kisa(sum(x["izlenme"] for x in v3.values())))) if v3 else "Yok"
    aramatxt = "; ".join("%s (%s)" % (k, kisa(aramaz[k]["toplam"])) for k in ks)
    firsat_out.append({"konu": konu, "arama": ks, "toplam": top, "en": en["baslik"], "en_kanal": en["kanal"], "en_izlenme": en["izlenme"], "vitra_marka_video": len(vm), "vitra_ucuncu_taraf": len(v3)})
    w(t(i, konu, aramatxt, kisa(top), "%s / %s (%s)" % (kes(en["baslik"], 40), en["kanal"], kisa(en["izlenme"])), vm_txt, v3_txt, BAGLAR[i - 1], oneri))
w("")
json.dump(firsat_out, open(os.path.join(D, "video_firsatlari.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# yorum ek istatistikleri
cs = list(csv.DictReader(open(os.path.join(D, "yorumlar_siniflandirilmis.csv"), encoding="utf-8-sig")))
gec = [x for x in cs if x["sahip_yorumu"] == "False" and x["reklam_iletisim"] == "False"]
def kk(s): return s.replace("İ", "i").replace("I", "ı").lower()
vv = [x for x in gec if x["tur"].startswith("VitrA")]
vt = collections.Counter(tt for x in vv for tt in x["temalar"].split(" | ") if tt)
vanilan = [x for x in gec if re.search(r"vitra|artema", kk(x["metin"]))]
vneg = [x for x in vanilan if re.search(r"sızdır|sızıntı|kaçır|pişman|tavsiye etmiy|kalitesiz|bozul|uzak durun|arıza|sorun|dert", kk(x["metin"]))]
vpos = [x for x in vanilan if re.search(r"kaliteli|memnun|sağlam|tavsiye ederim|sıkıntı yok", kk(x["metin"]))]
serv = [x for x in gec if "Servis ve garanti" in x["temalar"]]
serv_ucret = [x for x in serv if re.search(r"servis (ücret|çağır|para)|ödemedik|vermeden|çağırmadan|ücreti|lira|\btl", kk(x["metin"]))]
serv_erisim = [x for x in serv if re.search(r"servisiniz var|servis var mı|hangi servis|yetkili", kk(x["metin"]))]
def pay(k, tam=len(gec)): return YT["temalar"][k]["yorum"], YT["temalar"][k]["pay_gecerli"]
def vp(k): return "%d (%%%.1f)" % (vt[k], 100 * vt[k] / len(vv))
gv = A["grup"]
ust = A["marka_bahis"]["VitrA"]
mk = A["marka_kanal"]
tur = A["tur"]; tg2 = sum(v["gorunme"] for v in tur.values())
def top(kn): return next(z for z in A["kanal"] if z["kanal"] == kn)
tam_ar = [z for z in A["arama"] if z["grup"] == "Tamir ve bakım"]
tam_vitra_yok = sum(1 for z in tam_ar if not z["vitra_var"])
# (f)
w("## (f) Ana bulgular")
w("")
F = []
F.append("**Marka kanalı görünürlüğü ürün ve montaj aramalarında yoğunlaşıyor.** VitrA/Artema marka kanalı 68 aramanın %d'inde (%%%.0f) ilk 20'de yer almaktadır. Grup bazında: Montaj %d/%d, Seçim %d/%d, Marka %d/%d, Tamir %d/%d, İlham ve tadilat %d/%d, Yeni kategoriler %d/%d. Marka kanalı yalnızca 7 aramada 1. sıradadır (gömme rezervuar kurulumu, klozet kapağı takma, küvet montajı, duş teknesi montajı, termostatik batarya montajı, vitra, vitra v-care)." % (tvit, 100 * tvit / 68, gv["Montaj"]["vitra_olan_arama"], gv["Montaj"]["arama"], gv["Seçim ve karşılaştırma"]["vitra_olan_arama"], gv["Seçim ve karşılaştırma"]["arama"], gv["Marka ve rakip"]["vitra_olan_arama"], gv["Marka ve rakip"]["arama"], gv["Tamir ve bakım"]["vitra_olan_arama"], gv["Tamir ve bakım"]["arama"], gv["İlham ve tadilat"]["vitra_olan_arama"], gv["İlham ve tadilat"]["arama"], gv["Yeni kategoriler"]["vitra_olan_arama"], gv["Yeni kategoriler"]["arama"]))
F.append("**VitrA Türkiye tek başına en görünür kanal.** %d görünme, %d arama, %d tekil video, %s toplam izlenme, ortalama sıra 9.4; ikinci ve üçüncü kanallar Tesisat Servisim (%d görünme, %d arama) ve Macit Tesisat (%d görünme, %d arama). VitrA/Artema marka videolarında medyan süre 78 sn, Macit Tesisat 374 sn, Tesisat Servisim 209 sn." % (top("VitrA Türkiye")["gorunme"], top("VitrA Türkiye")["arama_sayisi"], top("VitrA Türkiye")["tekil_video"], kisa(top("VitrA Türkiye")["toplam_izlenme_tekil"]), top("Tesisat Servisim")["gorunme"], top("Tesisat Servisim")["arama_sayisi"], top("Macit Tesisat")["gorunme"], top("Macit Tesisat")["arama_sayisi"]))
F.append("**Tamir aramalarında sonuçları usta kanalları taşıyor.** Tamir ve bakım grubunda 10 aramanın %d'sinde marka kanalından video yoktur; grubun toplam izlenmesi %s'dir. Tüm sonuçlarda tesisatçı/usta türü %d kanalla görünmelerin %%%.1f'ini, marka türü %d kanalla %%%.1f'ini oluşturmaktadır." % (tam_vitra_yok, kisa(gv["Tamir ve bakım"]["toplam_izlenme_tekil"]), tur["Tesisatçı / usta"]["kanal"], 100 * tur["Tesisatçı / usta"]["gorunme"] / tg2, tur["Marka"]["kanal"], 100 * tur["Marka"]["gorunme"] / tg2))
F.append("**VitrA konusu usta kanallarında anlatılıyor.** Başlığında VitrA/Artema geçen ve marka kanalına ait olmayan %d tekil video %s izlenmeye ulaşmıştır; bunların %d tanesi tamir/onarım içeriğidir. En yüksek örnekler: Macit Tesisat (447K, gömme rezervuar su kaçırma), Tesisat Servisim (247K, gömme rezervuar su dolmuyor), Banyomoda (231K, gömme rezervuar montajı). \"gömme rezervuar su doldurmuyor\" aramasında ilk 20'de bu tür 4 video (756K izlenme) bulunurken marka kanalı yoktur." % (ust["ucuncu_taraf_video"], kisa(ust["ucuncu_taraf_izlenme"]), ust["ucuncu_taraf_tamir_video"]))
F.append("**İlham/tadilat ve yeni kategori aramalarında marka kanalı hiç görünmüyor.** 16 aramanın hiçbirinde VitrA/Artema videosu yoktur; bu iki grubun ilk 20 sonuçlarındaki toplam izlenme %s ve %s'dir (medyan video izlenmesi %s ve %s). En yüksek hacim: fayans üstüne fayans (%s), engelli banyo düzenlemesi (%s), fayans boyama (%s), banyo tadilatı maliyeti (%s)." % (kisa(gv["İlham ve tadilat"]["toplam_izlenme_tekil"]), kisa(gv["Yeni kategoriler"]["toplam_izlenme_tekil"]), n(gv["İlham ve tadilat"]["medyan_izlenme_video"]), n(gv["Yeni kategoriler"]["medyan_izlenme_video"]), kisa(aramaz["fayans üstüne fayans"]["toplam"]), kisa(aramaz["engelli banyo düzenlemesi"]["toplam"]), kisa(aramaz["fayans boyama"]["toplam"]), kisa(aramaz["banyo tadilatı maliyeti"]["toplam"])))
F.append("**En yüksek hacimli tamir konuları marka kanalında karşılıksız.** sifon değiştirme %s, batarya damlatıyor %s, rezervuar şamandıra ayarı %s, musluk kartuşu değişimi %s, gömme rezervuar su doldurmuyor %s, lavabo sifonu tıkandı %s toplam izlenme (her birinde ilk 20). Aynı konularda marka kanalı ilk 20'de yer almamaktadır." % tuple(kisa(aramaz[k]["toplam"]) for k in ["sifon değiştirme", "batarya damlatıyor", "rezervuar şamandıra ayarı", "musluk kartuşu değişimi", "gömme rezervuar su doldurmuyor", "lavabo sifonu tıkandı"]))
mal_u = [x for x in gec if any(tt in x["temalar"] for tt in ["Fiyat", "Usta ücreti / usta bulma", "Servis ve garanti"])]
mal_ut = [x for x in mal_u if "Teşekkür / genel" in x["temalar"]]
F.append("**Yorumların ana teması teşekkür; ikinci sırada sızıntı ve maliyet geliyor.** %s yorum çekilmiş, %s yorum analize girmiştir. Teşekkür/genel %%%.1f; ürün kalitesi/sızıntı %d yorum (%%%.1f); fiyat %d (%%%.1f); montaj zorluğu %d (%%%.1f); usta ücreti/usta bulma %d (%%%.1f); servis ve garanti %d (%%%.1f); parça bulma %d (%%%.1f); satın alma kanalı %d (%%%.1f); marka karşılaştırması %d (%%%.1f). Fiyat, usta ücreti veya servis temalarından en az birine giren %d yorumun (%%%.1f) %d tanesi teşekkür içeriklidir: yorumcular videoyu usta ya da servis ücreti ödememek için izlediğini belirtmektedir (örnek: 250 lira servis ücreti ve 2.500 TL usta bedeli karşısında 20-40 TL'lik conta)." % ((n(YT["cekilen_yorum"]), n(YT["gecerli"]), YT["temalar"]["Teşekkür / genel"]["pay_gecerli"]) + tuple(x for k in ["Ürün kalitesi / kırılma / sızıntı", "Fiyat", "Montaj zorluğu / uygulama soruları", "Usta ücreti / usta bulma", "Servis ve garanti", "Parça bulma / yedek parça", "Satın alma kanalı", "Marka karşılaştırması"] for x in (YT["temalar"][k]["yorum"], YT["temalar"][k]["pay_gecerli"])) + (len(mal_u), 100 * len(mal_u) / len(gec), len(mal_ut))))
F.append("**VitrA/Artema videolarındaki yorumlarda sızıntı ve fiyat öne çıkıyor.** Bu videolarda %d yorum analize girmiştir; ürün kalitesi/sızıntı %s, fiyat %s, servis ve garanti %s, montaj zorluğu %s, usta ücreti %s, parça bulma %s. Yorumlarda VitrA/Artema adı %d yorumda anılmakta; bunların %d'inde sızıntı, arıza veya memnuniyetsizlik ifadesi, %d'inde olumlu ifade (kaliteli, memnun, sağlam, tavsiye) geçmektedir (anahtar kelime taraması, yön göstericidir)." % (len(vv), vp("Ürün kalitesi / kırılma / sızıntı"), vp("Fiyat"), vp("Servis ve garanti"), vp("Montaj zorluğu / uygulama soruları"), vp("Usta ücreti / usta bulma"), vp("Parça bulma / yedek parça"), len(vanilan), len(vneg), len(vpos)))
F.append("**Parça ve servis talebi düşük hacimli ama net.** %d parça yorumunda \"parça numarası\", \"hiçbir nalburda yok\", \"aynısından nereden bulurum\" ifadeleri yer almaktadır; birkaç yorum contanın yetkili servisten alındığını belirtmektedir. %d servis yorumunun %d'inde ücret ifadesi (servis ücretinden kaçınma), %d'inde servisin varlığı ya da yetkili servis erişimi geçmektedir (\"Avrupa yakasında servisiniz var mı\", \"Şirinevlerde servisiniz var mı\")." % (YT["temalar"]["Parça bulma / yedek parça"]["yorum"], len(serv), len(serv_ucret), len(serv_erisim)))
F.append("**Rakip marka kanalları tek aramada yoğunlaşıyor.** hansgrohe %d görünme/%d arama, BOCCHI %d/%d, SEREL %d/%d, Kale Banyo %d/%d, E.C.A. %d/%d, Creavit %d/%d; VitrA Türkiye %d görünme/%d arama. Rakip marka kanalları tamir ve bakım aramalarında neredeyse yoktur (yalnızca Creavit 1 görünme). Rakip markaların tamir içeriği de usta kanallarında bulunmaktadır: başlıkta Serel geçen %d, E.C.A. geçen %d, Geberit geçen %d üçüncü taraf tamir videosu." % (mk["hansgrohe"]["toplam"]["gorunme"], mk["hansgrohe"]["toplam"]["arama"], mk["BOCCHI"]["toplam"]["gorunme"], mk["BOCCHI"]["toplam"]["arama"], mk["SEREL"]["toplam"]["gorunme"], mk["SEREL"]["toplam"]["arama"], mk["Kale Banyo"]["toplam"]["gorunme"], mk["Kale Banyo"]["toplam"]["arama"], mk["E.C.A."]["toplam"]["gorunme"], mk["E.C.A."]["toplam"]["arama"], mk["Creavit"]["toplam"]["gorunme"], mk["Creavit"]["toplam"]["arama"], mk["VitrA Türkiye"]["toplam"]["gorunme"], mk["VitrA Türkiye"]["toplam"]["arama"], A["marka_bahis"]["Serel"]["ucuncu_taraf_tamir_video"], A["marka_bahis"]["E.C.A."]["ucuncu_taraf_tamir_video"], A["marka_bahis"]["Geberit"]["ucuncu_taraf_tamir_video"]))
F.append("**Karşılaştırma ve seçim aramalarında VitrA konusu üçüncü taraflarca anlatılıyor.** \"geberit gömme rezervuar\" aramasında marka kanalı yoktur; ilk 20'de başlığında VitrA geçen 2 üçüncü taraf video (292K izlenme) bulunmaktadır ve yorumlarda \"Geberit diyon Vitra çıkıyor\" tepkisi görülmektedir. \"akıllı klozet alınır mı\" aramasında V-Care içeriği Banyotrendy (216K) ve ShiftDelete.Net kanallarından gelmektedir; VitrA marka videosu görünmemektedir.")
F.append("**Etkileşim farkı: usta videoları çok daha fazla yorum alıyor.** VitrA Türkiye'nin gömme rezervuar ve klozet kapağı montaj videoları (316K ve 339K izlenme) 49 ve 14 yorum almıştır; benzer izlenmeli VitrA gömme rezervuar tamir videoları Macit Tesisat (448K izlenme, 490 yorum) ve Sende Yapabilirsin (347K izlenme, 407 yorum) kanallarında yüksek yorum almıştır. Yorumlarda soru sorulan ve cevap beklenen içerikler usta kanallarında toplanmaktadır (küçük örnek, 4 video).")
for i, f in enumerate(F, 1): w("%d. %s" % (i, f))
w("")
# (g)
mal_ara = AR["maliyet_usd"]; mal_yor = YR["maliyet_usd"]
w("## (g) Tahmini maliyet")
w("")
w(t("Kalem", "Adet", "Birim (USD)", "Tutar (USD)"))
w(t(*["---"] * 4))
w(t("YouTube organic arama (live)", 68, "0.002", "%.3f" % mal_ara))
w(t("YouTube video yorumları (live, depth 100)", "%d video + 1 deneme çağrısı" % YT["video"], "0.006-0.010", "%.3f" % (mal_yor + 0.01)))
w(t("**Toplam**", "", "", "**%.2f**" % (mal_ara + mal_yor + 0.01)))
w("")
w("Toplu istekte 68 aramanın 61'i boş döndüğü için bu aramalar tek tek yeniden çalıştırıldı; boş dönen görevler ücretlendirilmemiştir (arama maliyeti 68 x 0.002 = 0.136 USD ile örtüşmektedir). `video_info` ve `video_subtitles` uç noktaları kullanılmamıştır.")
w("")
w("## Dosyalar")
w("")
w("- `arama.json`: 68 aramanın ham sonucu (grup, video, kanal, izlenme, yayın, süre, sıra)")
w("- `arama_video_tablosu.csv`: 68 arama x 20 video düz tablo (VitrA/Artema işaretli, alakasız sonuç işaretli)")
w("- `kanal_analizi.csv` ve `analiz.json`: kanal, grup, marka görünürlüğü hesapları")
w("- `yorumlar.json`: 33 videonun ham yorumları")
w("- `yorumlar_siniflandirilmis.csv` ve `yorum_temalari.json`: yorum bazında tema etiketleri ve tema özeti")
w("- `video_firsatlari.json`: fırsat listesi (makine okunur)")
w("- Betikler: `uretim/youtube_derin_arama.py`, `youtube_derin_analiz.py`, `youtube_derin_kanal.py`, `youtube_derin_yorum.py`, `youtube_derin_yorum_analiz.py`, `youtube_derin_ozet.py`")
w("")
w("Kaynak: YouTube · DataForSEO · 29.09.2026")
open(os.path.join(D, "ozet.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
