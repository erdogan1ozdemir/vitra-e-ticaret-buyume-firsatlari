# -*- coding: utf-8 -*-
"""Yorum madenciligi: kural tabanli tema siniflamasi. Girdi: yorumlar.json + arama.json (kanal handle icin). Cikti: yorum_temalari.json, yorumlar_siniflandirilmis.csv"""
import json, os, re, csv, collections
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(P, "veri/ham/derin/youtube")
Y = json.load(open(os.path.join(D, "yorumlar.json"), encoding="utf-8"))["videolar"]
def kucuk(s):
    return (s or "").replace("İ", "i").replace("I", "ı").lower()
# kanal handle -> sahibi yorumlarini disla
HANDLE = {}
for v in json.load(open(os.path.join(D, "arama.json"), encoding="utf-8"))["aramalar"].values():
    for x in v["videolar"]:
        if x.get("video_id") and x.get("kanal_url"): HANDLE[x["video_id"]] = x["kanal_url"].rstrip("/").split("/")[-1].lower()
for x in json.load(open(os.path.join(P, "veri/ham/autocomplete_youtube.json"), encoding="utf-8"))["youtube"].values():
    for y in x:
        m = re.search(r"(?:v=|shorts/)([\w-]{11})", y.get("url") or "")
        if m and y.get("kanal_url"): HANDLE.setdefault(m.group(1), y["kanal_url"].rstrip("/").split("/")[-1].lower())
TEL = re.compile(r"(?<!\d)(?:\+?90)?\s*0?\s*\(?5\d{2}\)?[\s.-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}(?!\d)|whatsapp|wp\s*:|iletişim\s*:|instagram\.com|@\w+\s*(?:dm|mesaj)")
MARKALAR = {"VitrA": r"vitra|artema", "Kale": r"\bkale\b", "Creavit": r"creavit", "Serel": r"serel", "E.C.A.": r"\beca\b|e\.c\.a", "Grohe": r"(?<!hans)grohe", "Hansgrohe": r"hansgrohe", "Geberit": r"geberit",
            "Duravit": r"duravit", "Bocchi": r"bocchi", "Bien": r"\bbien\b", "Visam": r"visam", "Alarko": r"alarko|carrier"}
# tema kurallari: (ad, regex). Bir yorum birden fazla temaya girebilir; yalnizca sahibi disi, iletisim-spam disi yorumlar siniflanir.
PARCA_KELIME = r"iç takım|ic takim|conta|kartuş|kartus|şamandıra|samandira|mekanizma|kumanda|sifon|menteşe|hortum|kapak|parça|parca|takım|flatör|flator|butonu|düğme|piston|silikon"
PARCA_EDIN = r"nereden|nerden|nerede|bulam|bulun|bulamıyor|temin|alabilir|alınır|satın|satıyor|satılıyor|link|kod|model|uyar|uyum|uygun mu|orijinal|ölçü|numara|hangi|adı ne|ismi ne|fiyatı|kaç tl"
TEMALAR = [
 ("Parça bulma / yedek parça", [r"yedek parça|yedek parca|parça bul|parçası nerede|parçayı nereden|parçalar bulunmu|temin", "COMBO:%s|%s" % (PARCA_KELIME, PARCA_EDIN)]),
 ("Servis ve garanti", [r"servis|garanti|yetkili|müşteri hizmet|musteri hizmet|çağrı merkez|cagri merkez|şikayet|sikayet|iade|değişim yap|degisim yap|ücretsiz değiş|destek hat|firmaya (ulaş|yaz|başvur)|üretici"]),
 ("Montaj zorluğu / uygulama soruları", [r"takamadım|takamıyorum|takılmıyor|takilmiyor|oturmuyor|oturmadı|sıkıştı|sökemedi|sökemiyorum|sökülmüyor|zor(lan|dur| oldu| geldi|sun)|beceremedim|yapamadım|yapamıyorum|uymadı|uymuyor|nasıl (takıl|sök|çıkar|yapıl|monte|ayarla|değiştir)|denedim ama|yerine geçmiyor|olmadı|çıkmıyor|çıkaramadım|hangi (anahtar|tornavida|numara)|kaç mm"]),
 ("Usta ücreti / usta bulma", [r"usta çağır|usta cagir|usta bulam|usta bulun|usta gelmedi|usta yok|ustaya (gitt|verdi|ver\b|sor|çağ|para)|ustaya gerek|usta(lar)? (istedi|ücret|para|kaç)|usta.{0,15}(ücret|tl\b|lira|istedi)|tesisatçı (çağır|bulam|bulun|gelmedi|yapamadı|ücret|istedi)|tesisatçı.{0,15}(tl\b|lira|istedi)|işçilik|servis ücreti|önerdiğiniz biri|önerir misiniz|tavsiye edeb|biri var mı|usta (arıyor|lazım|ihtiyaç|tavsiye)|gelir misiniz|gelebilir misiniz|gelebilir mi|hizmet veriyor|bölgemizde|bölgeme"]),
 ("Fiyat", [r"fiyat|pahalı|pahali|ucuz|\bpara\b|paramı|parası|\btl\b|₺|lira|maliyet|bütçe|butce|ekonomik|değer mi|değmez|kaça |kaç para|ne kadar|kazık|zam\b|zamlı|fahiş|ödedim|ödeyeceğ|indirim|taksit"]),
 ("Ürün kalitesi / kırılma / sızıntı", [r"sızdır|sizdir|sızıntı|sizinti|su kaçır|su kaçıyor|kaçırıyor|kaçırdı|kaçırmaya|kırıl|kırdı|kirildi|çatla|catla|bozuk|bozul|bozdu|bozuldu|kalitesiz|kalite|defolu|arızalı|arıza|ariza|paslan|ömrü|dayanıksız|dayanıklı|plastik|dökül|damlıyor|damlat|damlıy|akıtıyor|akıyor|akıttı|sürekli su|su akıt|tutmuyor|çalışmıyor|calismiyor|ömürsüz"]),
 ("Marka karşılaştırması", ["MARKA2", r"daha iyi|daha kaliteli|daha sağlam|yerine|tercih|hangisi|karşılaştır|kıyasla|aynı (sorun|problem|şey|dert)|bunda da|bizde de|bende de|onda da|diğer marka|başka marka|markadan|markalar"]),
 ("Satın alma kanalı", [r"koçtaş|koctas|trendyol|hepsiburada|\bn11\b|amazon|bauhaus|tekzen|ikea|\bbim\b|\ba101\b|\bşok\b|mağaza|magaza|nereden (aldın|aldi|alın|alabil|satın|bulu)|nerden (aldın|alın|alabil|satın|bul)|nerede satılıyor|sipariş|siparis|kargo|internetten|online|bayi|toptan|hırdavat|hirdavat|yapı market|yapi market|satın al|satin al|link (atar|verir|paylaş|at\b|var mı)|linki"]),
 ("Teşekkür / genel", [r"teşekkür|tesekkur|sağ ol|sağol|sagol|eyvallah|emeğine|emeginize|emeğinize|elinize sağlık|eline sağlık|elinize saglik|harika|süper|super\b|çok iyi|çok güzel|güzel anlat|başarılar|tebrik|allah razı|razı olsun|bravo|müthiş|işime yaradı|isime yaradi|çözüldü|cozuldu|çalıştı|calisti|kurtardın|kurtardınız|helal olsun|faydalı|yararlı|çok işe yaradı|mükemmel|paylaşım için|paylaşımınız"]),
]
def marka_say(t):
    return {m for m, rx in MARKALAR.items() if re.search(rx, t)}
def tema_bul(t):
    bul = []
    for ad, kurallar in TEMALAR:
        ok = False
        for r in kurallar:
            if r == "MARKA2":
                if len(marka_say(t)) >= 2: ok = True
                continue
            if r.startswith("COMBO:"):
                a, b = r[6:].split("|", 1)
                if re.search(a, t) and re.search(b, t): ok = True
                continue
            if ad == "Marka karşılaştırması" and len(marka_say(t)) >= 1 and re.search(r, t): ok = True; continue
            if ad == "Marka karşılaştırması": continue
            if re.search(r, t): ok = True
        if ok: bul.append(ad)
    return bul
satirlar = []
for vid, v in Y.items():
    sah = HANDLE.get(vid, "")
    for c in v["yorumlar"]:
        m = c["metin"] or ""; t = kucuk(m)
        yz = (c["yazar"] or "").lstrip("@").lower()
        sahip = bool(sah) and yz == sah.lstrip("@")
        reklam = bool(TEL.search(t)) or (len(re.findall(r"\d", m)) >= 10 and len(m.split()) < 25)
        temalar = [] if (sahip or reklam) else tema_bul(t)
        satirlar.append({"video_id": vid, "video": v["baslik"], "tur": v["tur_ad"], "yazar": c["yazar"], "metin": m, "begeni": c["begeni"] or 0, "sahip": sahip, "reklam_iletisim": reklam,
                         "temalar": temalar, "markalar": sorted(marka_say(t)) if not sahip else [], "kelime": len(m.split()), "tarih": c["tarih"]})
gecerli = [s for s in satirlar if not s["sahip"] and not s["reklam_iletisim"]]
sinif = [s for s in gecerli if s["temalar"]]
KUFUR = re.compile(r"\b(amk|aq|siktir|orospu|piç|salak|gerizekal|mal\b|lan\b)", re.I)
def alinti(ad, n=5):
    aday = [s for s in gecerli if ad in s["temalar"] and 6 <= s["kelime"] <= 25 and not KUFUR.search(s["metin"])]
    aday.sort(key=lambda s: (-s["begeni"], s["kelime"]))
    sec, kul = [], set()
    for s in aday:
        if s["video_id"] in kul and len(kul) < 6: continue
        sec.append(s); kul.add(s["video_id"])
        if len(sec) == n: break
    return [{"metin": s["metin"], "video": s["video"], "url": "https://www.youtube.com/watch?v=" + s["video_id"], "begeni": s["begeni"]} for s in sec]
# Elle secilmis alintilar: her biri ilgili tema kuralina giren, en fazla 25 kelimelik, birebir yorumlardir (baslangic metniyle eslestirilir)
SECILI = {
 "Parça bulma / yedek parça": ["parça numarasını da verebilirmisiniz", "Ustam ellerine sağlık bir sorum olacaktı bu söktüğümüz", "Serel marka iç takımın şamandırasi bozuldu", "iç takım ana gövdenin altı", "Contayı değiştirsek bile kaçırmaya devam ediyor"],
 "Servis ve garanti": ["Arkadaşlar hiçbir şey söyledikleri gibi değil vitra dan", "Sayenizde 250 servis ücreti vermeden", "Sağolun en detaylı anlatan sizsiniz  1 yılda 3 kez servis", "Sayın VİTRA üreticisi neden şu kapatma vanasını", "Şirinevlerde servisiniz var mı"],
 "Montaj zorluğu / uygulama soruları": ["2 yıldır Vitra kullanıyoruz ama o kadar pişmanız", "Montajı yaptım ama arka taraftaki ayaklar boşta", "Keşke tane tane detay vererek nasıl söküldüğünü", "Hocam bunun sökme işlemini de bir göstersen", "Ustam su tangın üst kapağını nasıl bağlarım"],
 "Usta ücreti / usta bulma": ["Allah razı olsun hocam sayenizde ustaya gerek kalmadan", "Usta çağırdım yapmaya cesaret edemedi", "Çok teşekkür ederim seni takip ederek yaptım ustanın 300 lira", "Ustam çok teşekkür ediyorum. Eve çağırdığım usta 2500 TL", "Göme reervuar saçmalıktan"],
 "Fiyat": ["Min 1500TL lik işi 90 TL ye çözdüm", "videoyu izleyerek contayı değiştirdim çok basitmiş yalnız", "Visam 275 tl zamanla conta eskiyor", "335bin TL değmez", "Teşekkürler ustam sayende yediğim kazıkların"],
 "Ürün kalitesi / kırılma / sızıntı": ["Video 357k izlenmiş. Vitra rezervuarı", "Vitra uzay üssü gibi ürün yapmış", "Usta Allah razı olsun 1 senedir su kaçırıyor", "Bende kullanıyorum ama ust kapak bozuldu", "Bizim klozetin su deposunu adamlar duvarın"],
 "Marka karşılaştırması": ["Bizim serel marka duvarın içindeki sifonumuz", "Ustam banyo eviye lavabo bataryası olarak hangi", "Geberit diyon Vitra çıkıyor", "Ustam sana zahmet  başlığı  vitra yap", "Vitra uzay üssü gibi ürün yapmış"],
 "Satın alma kanalı": ["Koçtaşın sitesinde panel açıklamalarında", "S.a  vitra conta 5 6 nalbura gittim", "Eve usta çağırdım işyeri evin arasındaydı", "Kullandığınız menteşeleri nereden alabiliriz", "Istanbuldaysaniz karakoyde hirdavatcilar"],
 "Teşekkür / genel": ["Cok tesekkurler o kdr sacma sapan", "Vatandaşın parasının cebinde kalmasına yardımcı", "İnsanların en makbulü insanlara faydalı olandır", "Değerli kardeşim ne güzel anlatmışsın", "Sorunumu hemen halledebildim"],
}
def alinti_sec(ad):
    out = []
    for pre in SECILI[ad]:
        m = [s for s in gecerli if s["metin"].startswith(pre) and ad in s["temalar"]]
        if not m:
            m = [s for s in gecerli if s["metin"].startswith(pre)]
        assert m, (ad, pre)
        s = max(m, key=lambda z: z["begeni"]); assert s["kelime"] <= 25, (ad, pre, s["kelime"])
        out.append({"metin": s["metin"], "video": s["video"], "url": "https://www.youtube.com/watch?v=" + s["video_id"], "begeni": s["begeni"], "tema_kurali_uyumlu": ad in s["temalar"]})
    return out
tema_ozet = {}
for ad, _ in TEMALAR:
    n = sum(1 for s in gecerli if ad in s["temalar"])
    tur_say = collections.Counter(s["tur"] for s in gecerli if ad in s["temalar"])
    vit = sum(1 for s in gecerli if ad in s["temalar"] and s["tur"].startswith("VitrA"))
    tema_ozet[ad] = {"yorum": n, "pay_gecerli": round(100 * n / len(gecerli), 1), "vitra_videolari_yorum": vit, "tur_dagilim": dict(tur_say), "alintilar": alinti_sec(ad)}
sinifsiz = [s for s in gecerli if not s["temalar"]]
tur_top = collections.Counter(s["tur"] for s in gecerli)
# marka anilma
marka_say_d = collections.Counter(m for s in gecerli for m in s["markalar"])
# video bazli
video_oz = []
for vid, v in Y.items():
    g = [s for s in gecerli if s["video_id"] == vid]
    video_oz.append({"video_id": vid, "baslik": v["baslik"], "tur": v["tur_ad"], "toplam_yorum": v["toplam_yorum"], "cekilen": len(v["yorumlar"]), "gecerli": len(g),
                     "sahip": sum(1 for s in satirlar if s["video_id"] == vid and s["sahip"]), "reklam": sum(1 for s in satirlar if s["video_id"] == vid and s["reklam_iletisim"])})
out = {"video": len(Y), "cekilen_yorum": len(satirlar), "sahip_yorumu": sum(1 for s in satirlar if s["sahip"]), "reklam_iletisim": sum(1 for s in satirlar if s["reklam_iletisim"] and not s["sahip"]),
       "gecerli": len(gecerli), "temali": len(sinif), "temasiz": len(sinifsiz), "temasiz_pay": round(100 * len(sinifsiz) / max(1, len(gecerli)), 1), "tur_yorum": dict(tur_top),
       "temalar": tema_ozet, "marka_anilma": dict(marka_say_d), "videolar": video_oz}
json.dump(out, open(os.path.join(D, "yorum_temalari.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(os.path.join(D, "yorumlar_siniflandirilmis.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["video_id", "video", "tur", "yazar", "begeni", "sahip_yorumu", "reklam_iletisim", "temalar", "markalar", "metin"])
    for s in satirlar: w.writerow([s["video_id"], s["video"], s["tur"], s["yazar"], s["begeni"], s["sahip"], s["reklam_iletisim"], " | ".join(s["temalar"]), " | ".join(s["markalar"]), s["metin"].replace("\n", " ")])
print(out["video"], out["cekilen_yorum"], out["sahip_yorumu"], out["reklam_iletisim"], out["gecerli"], out["temali"], out["temasiz_pay"])
for ad, t in tema_ozet.items(): print(ad, t["yorum"], t["pay_gecerli"], t["vitra_videolari_yorum"])
print(dict(marka_say_d))
