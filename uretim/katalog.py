# -*- coding: utf-8 -*-
"""vitra.com.tr urun sitemap -> tema bazinda urun sayisi; talep ile karsilastirma."""
import json, os, re, collections
import veri
X = open(os.path.join(veri.V, "ham", "sitemap", "vitra-products.xml"), encoding="utf-8").read()
URL = re.findall(r"<loc>([^<]+)</loc>", X)
DIR2T = {
 "karo-seramik-urunleri": "karo", "lavabo-dahil-lavabo-dolaplari": "lavabo_dolap", "lavabo-haric-lavabo-dolaplari": "lavabo_dolap", "dus-tekneleri": "dus_tekne", "dus-kanallari": "dus_tekne",
 "banyo-boy-dolaplari": "banyo_dolap", "diger-banyo-dolaplari": "banyo_dolap", "banyo-set-modulleri": "banyo_dolap", "aynali-banyo-dolabi": "aynali_dolap", "dusakabin": "dusakabin", "dus-uniteleri": "dusakabin",
 "canak-lavabolar": "lavabo", "standart-lavabo-ve-ayaklari": "lavabo", "tezgahustu-lavabolar": "lavabo", "tezgahalti-lavabolar": "lavabo", "etajerli-lavabolar": "lavabo", "monoblok-lavabolar": "lavabo", "yarim-tezgah-lavabolar": "lavabo",
 "banyo-tezgahlari": "tezgah", "klozet-kapaklari": "klozet_kapak", "asma-klozetler": "klozet", "takim-klozetler": "klozet", "yerden-tek-klozetler": "klozet", "asma-klozet-takimlari": "klozet", "akilli-klozetler": "akilli_klozet",
 "duz-aynalar": "ayna", "makyaj-aynalari-ve-diger-aksesuarlar": "ayna", "camasir-makinesi-dolaplari": "camasir_dolap", "banyo-raflari": "banyo_raf", "banyo-dolabi-kulplari": "banyo_raf", "banyo-dolap-ayaklari": "banyo_raf", "banyo-konsollari": "banyo_raf",
 "sabunluklar": "aksesuar", "havluluklar": "aksesuar", "tuvalet-kagitliklari": "aksesuar", "banyo-askilari": "aksesuar", "tuvalet-fircalari": "aksesuar", "dis-fircaliklari": "aksesuar", "banyo-cop-kovalari": "aksesuar", "banyo-aksesuar-setleri": "aksesuar", "banyo-malzemelikleri": "duzen",
 "hidromasajli-standart-kuvetler": "jakuzi", "hidromasajli-bagimsiz-kuvetler": "jakuzi", "hidromasajsiz-bagimsiz-kuvetler": "kuvet", "standart-ve-gomme-kuvetler": "kuvet", "kuvet-panelleri": "kuvet", "dus-teknesi-ve-kuvet-ayaklari": "dus_tekne", "dus-teknesi-panelleri": "dus_tekne",
 "asma-bideler": "bide", "yerden-bideler": "bide", "pisuvarlar": "pisuvar", "pisuvar-yikama-sistemleri": "pisuvar", "pisuvar-ara-bolmeleri": "pisuvar",
 "asma-klozetler-icin-gomme-rezervuarlar": "gomme_rez", "duvara-tam-dayali-klozetler-icin-gomme-rezervuarlar": "gomme_rez", "tuvalet-taslari-icin-gomme-rezervuarlar": "gomme_rez", "gomme-rezervuar-setleri": "gomme_rez", "mekanik-kumanda-panelleri": "gomme_rez",
 "temassiz-kumanda-panelleri": "gomme_rez", "akilli-kumanda-panelleri": "gomme_rez", "tasiyici-aparatlar": "gomme_rez", "gomme-rezervuar-montaj-aksesuarlari": "gomme_rez", "duvar-onu-rezervuarlar": "rezervuar", "rezervuar-ve-klozet-ic-takimlari": "ic_takim",
 "lavabo-sifon-ve-suzgecleri": "sifon", "sifonlar": "sifon", "vitrifiye-tamamlayicilari": "yedek", "taharet-el-duslari": "taharet_musluk", "havlupanlar": "havlupan", "banyo-tutunma-barlari": "engelli", "vitra-kaydirmaz": "yapi_kimya",
 "masterline-eviye-bataryasi": "batarya", "idealine-eviye-bataryasi": "batarya", "tek-armatur-delikli-lavabo-bataryalari": "batarya", "ankastre-bataryalar": "batarya", "termostatik-bataryalar": "batarya", "duvardan-banyo-bataryalari": "batarya",
 "ankastre-lavabo-bataryalari": "batarya", "canak-lavabo-bataryalari": "batarya", "temassiz-lavabo-bataryalari": "batarya", "kuvet-bataryalari": "batarya", "bide-bataryalari": "batarya", "iki-veya-uc-delikli-lavabo-bataryalari": "batarya", "banyo-batarya-cikis-uclari": "batarya",
 "musluk-ve-ara-musluklar": "batarya", "ankastre-stop-valfler": "batarya", "siva-alti-ve-diger-tamamlayicilar": "batarya",
 "el-dusu-takimlari": "dus_sis", "dus-basliklari": "dus_sis", "bataryali-dus-sistemleri": "dus_sis", "dus-dirsekleri": "dus_sis", "dus-tamamlayici-urunleri": "dus_sis", "surgulu-el-dusu-takimlari": "dus_sis", "ankastre-dus-yonlendiriciler": "dus_sis", "dus-kolonlari": "dus_sis", "dus-setleri": "dus_sis", "masajli-dus-sistemleri": "dus_sis",
 "montaj-hizmeti": "montaj_hiz", "kesif-hizmeti": "montaj_hiz", "yikanma-alani-tamamlayici-urunler": "dus_tekne",
}
c = collections.Counter(); ad = collections.defaultdict(set); bil = collections.Counter()
for u in URL:
    p = u.replace("https://www.vitra.com.tr/", "").split("/")
    t = DIR2T.get(p[0])
    if not t:
        if p[0] == "kategoriler":
            s = p[-1]; t = "pisuvar" if "pisuvar" in s else ("ic_takim" if "ic-takim" in s else ("kuvet" if "kuvet" in s else ("dus_tekne" if "profil" in s else ("karo" if "karo" in s else "aksesuar"))))
        else: bil[p[0]] += 1; continue
    c[t] += 1
    base = re.sub(r"-p-.*$", "", p[-1]); base = re.sub(r"-(beyaz|siyah|krom|mat|parlak|antrasit|gri|bej|altin|bakir|fircali|nikel|erik|mese|ceviz|kasmir|cordoba|pembe|yesil|mavi|lacivert|bronz|celik|mavisi|koyu|acik|kum|seftali|toz|vizon|kahve|fildisi)(-.*)?$", "", base)
    ad[t].add(base)
YK = json.load(open(os.path.join(veri.V, "islenmis", "yeni_kategori.json"), encoding="utf-8"))["tema"]
out = {}
for k, t in YK.items():
    out[k] = {"tr": t["tr"], "grup": t["grup"], "durum": t["durum"], "v12": t["v12"], "yoy": t["yoy"], "uc": t["uc_yil"], "urun": c.get(k, 0), "model": len(ad.get(k, ()))}
json.dump({"tema": out, "bilinmeyen": bil, "toplam_url": len(URL)}, open(os.path.join(veri.V, "islenmis", "katalog.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("eşlenmeyen dizin:", bil)
for k, v in sorted(out.items(), key=lambda i: -i[1]["v12"]):
    print(f"{v['tr'][:42]:42} {v['durum']:5} talep {v['v12']:8.0f}  ürün {v['urun']:5}  model {v['model']:4}")
