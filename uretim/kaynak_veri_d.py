# -*- coding: utf-8 -*-
"""Kaynak dokumu · D: YouTube videolari, Sikayetvar, organik (GSC) sayfalar, Trendyol ve Hepsiburada listeleri."""
import os, json, csv, html
from urllib.parse import urlsplit, parse_qs, quote, unquote
from kaynak_ortak import *
from kaynak_ortak import anahtar as O_anahtar
from kaynak_veri_a import D28, D29, D30
from kaynak_veri_c import fs

def bolum_linkleri(sid):
    sec = re.search(r'<section id="%s">(.*?)</section>' % sid, H, re.S).group(1)
    out = []
    for m in re.finditer(r'<a [^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', sec, re.S):
        u = html.unescape(m.group(1)); t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        out.append((u, t))
    return out

def doldur():
    # ------------------------------------------------------------ Search Console: organik bolumundeki VitrA sayfalari
    import gsc12
    for u, t in bolum_linkleri("organik"):
        c_, i_, p_ = gsc12.sayfa(gsc12.yol(u))
        if c_ or i_:
            bilgi = "1 Eki 2025 - 30 Eyl 2026: %s tıklama, %s gösterim, ortalama sıra %s" % (fs(c_), fs(i_), fs(p_))
        else:
            bilgi = "Sayfa raporunda yer aldı"
        ekle(u, "vitra.com.tr organik kanal performansı: sayfa bazında tıklama ve gösterim (%s)" % (t if t != "/ (ana sayfa)" else "ana sayfa"), bilgi,
             bolum=["organik"], yontem="API (Search Console)", tarih=D28, kod=["D2"])

    # ------------------------------------------------------------ YouTube videolari
    vid = {}
    with open(os.path.join(DERIN, "youtube", "arama_video_tablosu.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            vid.setdefault(r["video_id"], {"baslik": r["baslik"], "kanal": r["kanal"], "izlenme": r["izlenme"], "sure": r["sure"]})
    ay = json.load(open(os.path.join(HAM, "autocomplete_youtube.json"), encoding="utf-8"))["youtube"]
    for ifade, L in ay.items():
        for r in L:
            q = parse_qs(urlsplit(r["url"]).query).get("v", [None])[0]
            if q and q not in vid:
                vid[q] = {"baslik": r["baslik"], "kanal": r["kanal"], "izlenme": r.get("goruntulenme"), "sure": r.get("sure")}
    yk = json.load(open(os.path.join(DERIN, "youtube", "yorumlar.json"), encoding="utf-8"))["videolar"]
    for q, r in yk.items():
        vid.setdefault(q, {"baslik": r["baslik"], "kanal": None, "izlenme": None, "sure": None})
    goruldu = {"a1i0pneZhdw"}
    for u, t in bolum_linkleri("youtube"):
        q = parse_qs(urlsplit(u).query).get("v", [None])[0]
        if not q or q in goruldu:
            continue
        goruldu.add(q)
        v = vid.get(q, {})
        baslik = v.get("baslik") or t
        parca = []
        if v.get("kanal"):
            parca.append("kanal: %s" % v["kanal"])
        if v.get("izlenme"):
            try:
                parca.append("%s izlenme" % fs(int(v["izlenme"])))
            except (ValueError, TypeError):
                pass
        if q in yk:
            parca.append("yorum madenciliği için seçildi (%s yorum, tür: %s)" % (fs(yk[q]["toplam_yorum"]), yk[q]["tur_ad"]))
        if not parca:
            parca.append("video sayfası rapordaki bağlantı olarak verildi")
        ekle("https://www.youtube.com/watch?v=" + q, "YouTube videosu: %s" % baslik[:110], "; ".join(parca),
             bolum=["youtube"], yontem="API (DataForSEO YouTube)", tarih=[D28, D29], kod=["D4", "D20"] if q not in ("a1i0pneZhdw",) else ["D4", "D20", "Y1"])
    m = vid.get("a1i0pneZhdw", {})
    ekle("https://www.youtube.com/watch?v=a1i0pneZhdw", "Macit Tesisat: VitrA gömme rezervuar su kaçırma tamiri videosu (tamir boşluğu örneği ve yorum madenciliği)",
         "Kanal: Macit Tesisat; %s izlenme; %s yorum (yorum madenciliği için seçildi); VitrA marka kanalından karşılığı olan bir tamir videosu bulunmuyor" % (fs(int(m.get("izlenme") or 447815)), fs(yk["a1i0pneZhdw"]["toplam_yorum"])),
         bolum=["youtube"], yontem="API (DataForSEO YouTube)", tarih=[D28, D29], kod=["Y1"])
    # rapordaki kanal tablosunda adi gecen kanallar
    sec_yt = re.search(r'<section id="youtube">(.*?)</section>', H, re.S).group(1)
    hucre = set(html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", sec_yt, re.S))
    kurl = {}
    with open(os.path.join(DERIN, "youtube", "arama_video_tablosu.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["kanal"] and r.get("kanal_url"):
                kurl.setdefault(r["kanal"], r["kanal_url"])
    for k in json.load(open(os.path.join(DERIN, "youtube", "analiz.json"), encoding="utf-8"))["kanal"]:
        if k["kanal"] in hucre and k["kanal"] in kurl:
            ekle(kurl[k["kanal"]], "YouTube kanalı: %s (%s); montaj, tamir ve karar videolarında görünürlük" % (k["kanal"].strip(), k["tur"].lower()),
                 "%d farklı aramada toplam %d görünme, %d tekil video, tekil video izlenmesi toplamı %s; en çok izlenen video: %s" % (k["arama_sayisi"], k["gorunme"], k["tekil_video"], fs(k["toplam_izlenme_tekil"]), k["en_cok_izlenen"]),
                 bolum=["youtube"], yontem="API (DataForSEO YouTube)", tarih=D29, kod=["D20"])

    # ------------------------------------------------------------ Sikayetvar
    rk = json.load(open(os.path.join(DERIN, "sikayetvar", "rakip.json"), encoding="utf-8"))
    for ad, v in rk.items():
        u = v.get("marka_sayfasi")
        if not u:
            continue
        parca = ["%s toplam şikayet" % fs(v["toplam_sikayet"])]
        if v.get("puan_100") is not None:
            parca.append("genel puan %s/100 (%s değerlendirme)" % (v["puan_100"], fs(v["degerlendirme_sayisi"])))
        if v.get("cozum_orani_tum_pct") is not None:
            parca.append("çözüm oranı %%%s (tüm dönem)" % v["cozum_orani_tum_pct"])
        if ad == "VitrA":
            parca.append("41 sayfa gezildi (978 şikayet); son 24 ay 600 şikayetin 551'inin tam metni okundu; tema, aylık seri ve alıntılar")
        elif ad == "Artema":
            parca.append("23 sayfa gezildi (544 şikayet); son 24 ay 294 şikayetin 272'sinin tam metni okundu; tema ve aylık seri")
        elif ad.startswith("VitrA Karo"):
            parca.append("VitrA'dan ayrı marka sayfası")
        else:
            parca.append("marka göstergeleri ve ilk 3 sayfada e-ticaret temalı şikayet payı")
        ekle(u, "Şikayetvar %s marka sayfası: şikayet sayısı, puan, çözüm oranı%s" % (ad, " ve şikayet metinleri" if ad in ("VitrA", "Artema") else ""), "; ".join(parca),
             bolum=["sikayet"], yontem=["curl", "tarayıcı (Chrome, kullanıcı oturumu)"] if ad in ("VitrA", "Artema") else "curl", tarih=[D29, D30] if ad in ("VitrA", "Artema") else D29, kod=["D24"], adet=41 if ad == "VitrA" else 23 if ad == "Artema" else 1)
    sik = {}
    for r in json.load(open(os.path.join(DERIN, "sikayetvar", "sikayetler.json"), encoding="utf-8")):
        if r.get("url"):
            sik[anahtar(r["url"])] = r
    cy = json.load(open(os.path.join(DERIN, "chrome_tur2", "sikayetvar_yanit.json"), encoding="utf-8"))
    url_cy = re.findall(r"https://www\.sikayetvar\.com/[a-z0-9-]+/[a-z0-9-]+", json.dumps(cy))
    linkler = [u for u, t in bolum_linkleri("sikayet")] + url_cy
    for u in dict.fromkeys(linkler):
        if u.rstrip("/").count("/") < 4:
            continue
        r = sik.get(anahtar(u))
        b = r["baslik"] if r else u.rsplit("/", 1)[-1].replace("-", " ")
        info = ["şikayet sayfası, marka: %s" % ("VitrA" if "/vitra/" in u else "Artema")]
        if r:
            info.append("tarih %s" % ".".join(reversed(r["tarih"].split("-"))))
        if u in url_cy:
            info.append("30.09.2026'da marka yanıtı bloğu kontrol edildi (yanıt bloğu yok)")
        if u in [x for x, _ in bolum_linkleri("sikayet")]:
            info.append("rapordaki tema alıntısının kaynağı")
        ekle(u, "Şikayetvar şikayet metni: %s" % b[:100], "; ".join(info),
             bolum=["sikayet"], yontem=["curl"] + (["tarayıcı (Chrome, kullanıcı oturumu)"] if u in url_cy else []), tarih=[D29] + ([D30] if u in url_cy else []), kod=["D24"] + (["D28"] if u in url_cy else []))
    ekle("https://www.sikayetvar.com/vitra/{şikayet-başlığı}", "VitrA şikayet sayfalarının tam metinleri (tema, alıntı, satın alma kanalı ve ücret ifadeleri)",
         "Son 24 ay 600 şikayetten 551'inin tam metni; yazar adı alınmadı, telefon, e-posta, sipariş numarası ve ad-soyad imzaları maskelendi; tema ataması anahtar ifadeyle",
         bolum=["sikayet"], yontem="curl", tarih=D29, kod=["D24"], adet=551, href="https://www.sikayetvar.com/vitra")
    ekle("https://www.sikayetvar.com/artema/{şikayet-başlığı}", "Artema şikayet sayfalarının tam metinleri",
         "Son 24 ay 294 şikayetten 272'sinin tam metni; kişisel veriler maskelendi; tema ataması anahtar ifadeyle",
         bolum=["sikayet"], yontem="curl", tarih=D29, kod=["D24"], adet=272, href="https://www.sikayetvar.com/artema")

    # ------------------------------------------------------------ Trendyol
    T = "https://www.trendyol.com"
    ka = json.load(open(os.path.join(DERIN, "trendyol", "kategori_agaci.json"), encoding="utf-8"))
    ekle(T + "/banyo-yapi-malzemeleri-x-c105718", "Trendyol banyo kategori ağacı: alt kategoriler ve sonuç sayıları",
         "Menü ağacı (Ev & Yaşam > Yapı Market > Banyo Yapı Malzemeleri) ve alt kategori filtreleri; sonuç sayıları: klozet 1.458, klozet kapağı 4.384, lavabo 5.806, rezervuar 4.149, pisuvar 260, duşakabin 1.982, duş teknesi 1.273, küvet 515, duş sistemi 23.213, batarya ve musluk 41.057, tesisat 23.892, banyo aksesuarı 63.531 (100.000 üstü '100000' görünür)",
         bolum=["pazaryeri"], yontem="tarayıcı", tarih=D29, kod=["D21"])
    mg = json.load(open(os.path.join(DERIN, "trendyol", "magazalar.json"), encoding="utf-8"))
    ekle(T + "/magaza/vitra-m-144409", "Trendyol VitrA mağaza sayfası: ürün sayısı, satıcı puanı ve marka payı",
         "833 ürün, satıcı puanı 8,7, doğrulanmış satıcı işareti; mağaza VitrA ve Artema ürünlerini birlikte listeliyor; marka çok satan ilk 36'sında VitrA'nın 17'si, Artema'nın 10'u bu mağazadan; mağaza dışı VitrA ve Artema listelemeleri 3. taraf satıcılardan",
         bolum=["pazaryeri", "fiyat"], yontem="tarayıcı", tarih=D29, kod=["D21", "D26"])
    ekle(T + "/magaza/{mağaza-adı}-m-{satıcı-no}", "Trendyol satıcı mağaza sayfaları: satıcı numaralarının adlandırılması ve 3. taraf satıcı yapısı",
         "180 mağaza sayfası (ör. BanyoVit 1.534 ürün, Hace Yapı Malzemeleri 648, Creavit mağazası 521); çok satan listelerindeki satıcı numaraları mağaza adı ve ticari unvanla eşlendi",
         bolum=["pazaryeri", "fiyat"], yontem=["tarayıcı", "API (Apify)"], tarih=D29, kod=["D21", "D26"], adet=180, href=T + "/magaza/vitra-m-144409")
    Hb = "https://www.hepsiburada.com"
    hp = json.load(open(os.path.join(DERIN, "hepsiburada", "hepsiburada_ham.json"), encoding="utf-8"))
    ls = json.load(open(os.path.join(DERIN, "trendyol", "cok_satanlar_ve_marka_sayfalari.json"), encoding="utf-8"))["listeler"]
    AD = {105724: "duş sistemi", 105726: "banyo aynası", 109229: "klozet kapağı", 109333: "duşakabin", 143557: "banyo bataryası", 143558: "lavabo bataryası", 143556: "ara musluk",
          144458: "rezervuar", 166314: "banyo dolabı seti", 109226: "klozet", 109227: "lavabo", 109228: "eviye", 109230: "pisuvar", 109338: "duş teknesi", 103777: "banyo aksesuarı",
          105719: "batarya ve musluk", 105722: "tesisat", 144253: "küvet", 104508: "çok amaçlı dolap", 143559: "bide bataryası (taharet musluğu)", 143560: "eviye bataryası", 104210: "banyo aksesuar seti",
          166316: "çamaşır makinesi dolabı"}
    ty_bilgi = {}
    for k, v in ls.items():
        if "wc" in v:
            ty_bilgi[v["wc"]] = "kategori sonuç sayısı %s; ilk 36 ürünün medyan fiyatı %s TL, toplam değerlendirme sayısı %s" % (fs(v["total"]), fs(round(v["medP"])), fs(v["totRC"]))
        elif "wb" in v:
            u = "%s/sr?wb=%s&sst=BEST_SELLER" % (T, v["wb"])
            ad = v["anahtar"].replace("marka_", "").capitalize().replace("Vitra", "VitrA")
            ekle(u, "Trendyol %s marka listesi (ilk 36 ürün, çok satan sıralaması)" % ad,
                 "Markanın Trendyol'daki listeleme sayısı %s; ilk 36 ürünün medyan fiyatı %s TL, toplam değerlendirme sayısı %s; satıcı ve kategori dağılımı" % (fs(v["total"]), fs(round(v["medP"])), fs(v["totRC"])),
                 bolum=["pazaryeri"], yontem="tarayıcı", tarih=D29, kod=["D21"])
    cs = json.load(open(os.path.join(DERIN, "pazaryeri_fiyat", "cok_satan.json"), encoding="utf-8"))["kategoriler"]
    # Hepsiburada ham sayfa bilgileri
    hb_bilgi = {}
    for key, e in hp.items():
        if "path" not in e or e.get("status") != 200:
            continue
        m = e.get("metrics") or {}
        parca = ["sonuç sayısı %s" % (fs(int(str(e["cnt"]))) if str(e.get("cnt")).isdigit() else e.get("cnt"))]
        if m.get("averageProductPrice"):
            parca.append("ilk 36 ürünün çok satan sıralaması; ortalama liste fiyatı %s TL" % fs(round(m["averageProductPrice"])))
        hb_bilgi[Hb + e["path"]] = (key, e, "; ".join(parca))
    hb_kullanildi = set()
    tyurl = hburl = 0
    for k, v in cs.items():
        ty = v["trendyol"]; hb = v["hepsiburada"]
        tyurl += len(ty["urunler"]); hburl += len(hb["urunler"])
        mm = re.search(r"wc=(\d+)", ty["adres"])
        ozel = ty_bilgi.get(int(mm.group(1))) if mm else None
        ekle(ty["adres"], "Trendyol %s çok satanlar listesi (ilk 36 ürün: satıcı, indirim ve 3. taraf payı)" % v["ad"].lower(),
             ("%s; " % ozel[0].upper() + ozel[1:] if ozel else "") + "ilk 36 ürün: satıcı türü (VitrA mağazası, 3. taraf), liste ve eski fiyat, puan, değerlendirme sayısı, kargo etiketi",
             bolum=["fiyat"] + (["pazaryeri"] if ozel else []), yontem="API (Apify)", tarih=D29, kod=["D26"] + (["D21"] if ozel else []))
        hu = hb["adres"]
        bilgi_hb = hb_bilgi.get(hu)
        if bilgi_hb:
            hb_kullanildi.add(hu)
        ekle(hu, "Hepsiburada %s çok satanlar listesi (ilk 36 ürün: satıcı, sepet fiyatı ve 3. taraf payı)" % v["ad"].lower(),
             ("%s; " % bilgi_hb[2] if bilgi_hb else "sonuç sayısı %s; " % fs(hb.get("sonuc_sayisi") or 0)) + "ilk 36 ürün (ilk sayfa): satıcı türü (platform, VitrA mağazası, 3. taraf), liste ve sepet fiyatı, puan, değerlendirme sayısı",
             bolum=["fiyat"] + (["pazaryeri"] if bilgi_hb else []), yontem="tarayıcı (Playwright)" if not bilgi_hb else ["tarayıcı", "tarayıcı (Playwright)"], tarih=D29, kod=["D26"] + (["D22"] if bilgi_hb else []))
    for wc, b_ in ty_bilgi.items():
        u = "%s/sr?wc=%s&sst=BEST_SELLER" % (T, wc)
        if O_anahtar(u) in SATIR:
            continue
        ekle(u, "Trendyol %s çok satanlar listesi (ilk 36 ürün: marka, fiyat, değerlendirme sayısı, satıcı)" % AD.get(wc, "kategori"), b_[0].upper() + b_[1:],
             bolum=["pazaryeri"], yontem="tarayıcı", tarih=D29, kod=["D21"])
    orn_ty = cs["klozet"]["trendyol"]["urunler"][0].get("url")
    orn_hb = cs["klozet"]["hepsiburada"]["urunler"][0].get("url")
    ekle("https://www.trendyol.com/{marka}/{ürün-adı}-p-{ürün-no}", "Trendyol çok satan ürün sayfaları: fiyat, marka, satıcı, değerlendirme (14 kategori × 36 ürün)",
         "504 ürün kaydı (ilk 36 × 14 kategori); SSG kategorilerinde satışın %78-89'u 3. taraf satıcıda; banyo mobilyası ve duşakabin listelerinde marka mağazaları öne çıkıyor",
         bolum=["fiyat"], yontem="API (Apify)", tarih=D29, kod=["D26"], adet=504, href=orn_ty)
    ekle("https://www.hepsiburada.com/{ürün-adı}-p-{ürün-kodu}", "Hepsiburada çok satan ürün sayfaları: fiyat, marka, satıcı, değerlendirme (14 kategori × 36 ürün)",
         "504 ürün kaydı (ilk sayfa, 36 × 14 kategori); VitrA/Artema HB'de 44 listelemeyle yedek parça ve kapakta görünür",
         bolum=["fiyat", "pazaryeri"], yontem="tarayıcı (Playwright)", tarih=D29, kod=["D26", "D22"], adet=504, href=orn_hb)
    # trendyol arama temalari (Apify, 13 tema)
    ekle("https://www.trendyol.com/sr?q={tema}", "Trendyol arama sonuçları: bitişik ve yeni kategori temalarının ürün düzeyinde okunması",
         "13 tema (banyo dolabı, granit evye, çocuk klozet adaptörü, rezervuar iç takımı, suya dayanıklı banyo dolabı, çamaşır makinesi dolabı, ledli banyo aynası, arıtmalı batarya, havlupan, batarya kartuşu, klozet taharet aparatı, engelli tutunma barı, klozet lavabo seti); ilk 40-45 ürün (rezervuar iç takımı 150): fiyat, marka, değerlendirme sayısı",
         bolum=["ssgbm", "katalog", "yeni"], yontem="API (Apify)", tarih=D29, kod=["D15"], adet=13, href="https://www.trendyol.com/sr?q=banyo+dolab%C4%B1")
    ao = json.load(open(os.path.join(DERIN, "trendyol", "arama_onerileri.json"), encoding="utf-8"))["oneriler"]
    ekle("https://www.trendyol.com/sr?q={kök-ifade}", "Trendyol arama kutusu önerileri ve bitişik kategori aramaları (ihtiyaç ve kategori keşfi)",
         "Arama kutusu otomatik önerileri (%d kök ifade: kategori, sorgu ve mağaza önerileri) ve bitişik kategori aramaları (granit evye, arıtmalı batarya vb.: sonuç sayısı, medyan fiyat, baskın kategori, ilk 36 marka)" % len(ao),
         bolum=["pazaryeri"], yontem="tarayıcı", tarih=D29, kod=["D21"], adet=len(ao), href="https://www.trendyol.com/sr?q=klozet")
    mk = json.load(open(os.path.join(DERIN, "trendyol", "marka_kategori_adet.json"), encoding="utf-8"))
    ekle("https://www.trendyol.com/sr?wc={kategori}&wb={marka}", "Trendyol marka × kategori sonuç sayıları (VitrA, Artema, Creavit, Kale listeleme payı)",
         "Klozet 1.458 listelemede VitrA 172 (%11,8); lavabo ve banyo dolabı kategorilerinde VitrA payı %3,2 ve %0,4; marka toplamları VitrA 2.781, Artema 1.659, Creavit 1.645, Kale 6.537",
         bolum=["pazaryeri", "katalog"], yontem="tarayıcı", tarih=D29, kod=["D21"], href="https://www.trendyol.com/sr?wc=109226&wb=109184")

    # ------------------------------------------------------------ Hepsiburada
    ekle(Hb, "Hepsiburada banyo kategori ağacı, marka filtreleri ve arama önerileri",
         "Ev, Yaşam, Kırtasiye, Ofis > Banyo & Mutfak (10.000+ ürün) ağacı; marka filtreli toplamlar (VitrA 3.191, Artema 1.938, Kale 1.376, Creavit 1.975 ürün); 13 arama kökü için arama önerisi servisi; yaklaşık 65 sayfa yüklemesi (47'si ham veriye kaydedildi); VitrA buybox payı: %19 VitrA mağazası, %13 Hepsiburada, %69 3. taraf satıcı; giriş, form ve sepet işlemi yapılmadı",
         bolum=["pazaryeri"], yontem=["tarayıcı", "API (Apify)"], tarih=D29, kod=["D22"], adet=65)
    for u, (key, e, bilgi) in hb_bilgi.items():
        if u in hb_kullanildi:
            continue
        if key.startswith("b_") or key.startswith(("v_", "a_", "k_", "c_")):
            amac = "Hepsiburada marka filtreli liste: %s (marka ve marka + kategori ürün sayısı, ilk 36 satıcı ve fiyat)" % re.sub(r"\s*\(.*?\)", "", e.get("h1") or key)
        elif key.startswith("q_"):
            amac = "Hepsiburada arama sonucu: \"%s\" araması (çok satanlar sıralaması, ürün ve hizmet ürünleri)" % unquote(parse_qs(urlsplit(u).query).get("q", [key])[0])
        else:
            amac = "Hepsiburada kategori sayfası: %s (ürün sayısı, alt kategoriler, çok satanlar)" % re.sub(r"\s*\(.*?\)", "", e.get("h1") or key)
        ekle(u, amac, bilgi[0].upper() + bilgi[1:], bolum=["pazaryeri"], yontem="tarayıcı", tarih=D29, kod=["D22"])
    for u in re.findall(r"https://www\.hepsiburada\.com/[^\s\"]+", open(os.path.join(DERIN, "chrome_tur2", "hb_sayfa2_3.jsonl"), encoding="utf-8").read()):
        pass
    sayfalar = {}
    for l in open(os.path.join(DERIN, "chrome_tur2", "hb_sayfa2_3.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        sayfalar.setdefault(r["kaynak"], 0)
        sayfalar[r["kaynak"]] += 1
    for u, n in sayfalar.items():
        kat = {"klozetler": "klozet", "lavabolar": "lavabo", "banyo-bataryalari": "banyo bataryası"}.get(re.search(r"/([a-z-]+)-c-", u).group(1), "kategori")
        ekle(u, "Hepsiburada %s çok satanlar sayfa %s (ilk sayfanın devamı)" % (kat, u.rsplit("=", 1)[-1]),
             "%d ürün kaydı; 3 kategoride toplam 216 ürün: klozette VitrA 16 ürün (11 klozet ve takım, 5 parça), lavaboda 2, banyo bataryasında Artema 9 ve VitrA 1; Artema ürünlerinin tamamı 3. taraf satıcıda" % n,
             bolum=["fiyat", "pazaryeri"], yontem=CHR_, tarih=D30, kod=["D28"])

CHR_ = "tarayıcı (Chrome, kullanıcı oturumu)"
