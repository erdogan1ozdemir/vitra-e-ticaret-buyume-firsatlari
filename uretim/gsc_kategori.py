# -*- coding: utf-8 -*-
"""GSC sayfalarini kategori agacina esler; aylik kategori performansi uretir."""
import json, os, re
from collections import defaultdict
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(P, "veri/ham/gsc"); O = os.path.join(P, "veri/islenmis")
# slug -> (kat1, kat2)
K = {
 "klozet": ("Vitrifiyeler","Klozetler"), "asma-klozet": ("Vitrifiyeler","Klozetler"), "takim-klozet": ("Vitrifiyeler","Klozetler"), "akilli-klozet": ("Vitrifiyeler","Akıllı Klozet"),
 "klozet-kapak": ("Vitrifiyeler","Klozet Kapakları"), "lavabo": ("Vitrifiyeler","Lavabolar"), "canak-lavabo": ("Vitrifiyeler","Lavabolar"), "tezgah": ("Vitrifiyeler","Lavabolar"),
 "etajer": ("Vitrifiyeler","Lavabolar"), "hilton": ("Vitrifiyeler","Lavabolar"), "pisuvar": ("Vitrifiyeler","Pisuvarlar"), "bide": ("Vitrifiyeler","Bideler"), "vitrifiye": ("Vitrifiyeler","Genel"),
 "sifon": ("Vitrifiyeler","Tamamlayıcı"), "ic-takim": ("Rezervuarlar","İç Takımlar"), "rezervuar": ("Rezervuarlar","Gömme Rezervuarlar"), "kumanda": ("Rezervuarlar","Kumanda Panelleri"),
 "banyo-mobilya": ("Banyo Mobilyaları","Genel"), "banyo-dolap": ("Banyo Mobilyaları","Banyo Dolapları"), "boy-dolap": ("Banyo Mobilyaları","Banyo Dolapları"), "banyo-raf": ("Banyo Mobilyaları","Banyo Dolapları"), "lavabo-dolab": ("Banyo Mobilyaları","Lavabo Dolapları"), "aynali-banyo": ("Banyo Mobilyaları","Banyo Dolapları"), "dus-kabin": ("Yıkanma Alanları","Duşakabin"), "dus-unite": ("Yıkanma Alanları","Duş Üniteleri"), "termostatik": ("Armatürler","Banyo Bataryaları"), "havlupan": ("Banyo Aksesuarları","Havluluklar"), "tuvalet-tasi": ("Vitrifiyeler","Tuvalet Taşları"), "helatasi": ("Vitrifiyeler","Tuvalet Taşları"),
 "camasir": ("Banyo Mobilyaları","Çamaşır Makinesi Dolapları"), "ayna": ("Banyo Mobilyaları","Banyo Aynaları"), "tezgahlar": ("Banyo Mobilyaları","Tezgahlar"), "set-modul": ("Banyo Mobilyaları","Set Modülleri"),
 "eviye-batarya": ("Armatürler","Eviye Bataryaları"), "eviye": ("Armatürler","Eviyeler"), "banyo-batarya": ("Armatürler","Banyo Bataryaları"), "lavabo-batarya": ("Armatürler","Lavabo Bataryaları"),
 "armatur": ("Armatürler","Genel"), "musluk": ("Armatürler","Musluklar"), "stop-valf": ("Armatürler","Tamamlayıcı"), "ankastre": ("Armatürler","Ankastre"), "bide-batarya": ("Armatürler","Bide Bataryaları"),
 "dus-set": ("Duşlar","Duş Setleri"), "dus-basl": ("Duşlar","Duş Başlıkları"), "dus-sistem": ("Duşlar","Duş Sistemleri"), "duslar": ("Duşlar","Genel"), "el-dus": ("Duşlar","El Duşları"), "dus-kolon": ("Duşlar","Duş Kolonları"),
 "dusakabin": ("Yıkanma Alanları","Duşakabin"), "dus-tekne": ("Yıkanma Alanları","Duş Tekneleri"), "kuvet": ("Yıkanma Alanları","Küvetler"), "dus-kanal": ("Yıkanma Alanları","Duş Kanalları"), "hidromasaj": ("Yıkanma Alanları","Küvetler"),
 "karo": ("Karo Seramik","Karo Seramik"), "dus-sistem": ("Duşlar","Duş Sistemleri"), "porselen": ("Karo Seramik","Karo Seramik"), "seramik": ("Karo Seramik","Karo Seramik"),
 "aksesuar": ("Banyo Aksesuarları","Genel"), "kagitlik": ("Banyo Aksesuarları","Tuvalet Kağıtlıkları"), "havluluk": ("Banyo Aksesuarları","Havluluklar"), "firca": ("Banyo Aksesuarları","Tuvalet Fırçaları"),
 "sabunluk": ("Banyo Aksesuarları","Sabunluklar"), "cop-kova": ("Banyo Aksesuarları","Çöp Kovaları"), "tutunma": ("Banyo Aksesuarları","Tutunma Barları"), "malzemelik": ("Banyo Aksesuarları","Diğer"), "aski": ("Banyo Aksesuarları","Diğer"),
}
SIRA = ["dus-sistem","dus-kabin","dus-unite","termostatik","havlupan","tuvalet-tasi","helatasi","boy-dolap","banyo-raf","akilli-klozet","klozet-kapak","asma-klozet","takim-klozet","klozet","canak-lavabo","lavabo-dolab","lavabo-batarya","tezgahlar","tezgah","etajer","hilton","lavabo","pisuvar","bide-batarya","bide","vitrifiye","sifon",
        "ic-takim","kumanda","rezervuar","aynali-banyo","banyo-dolap","camasir","ayna","set-modul","banyo-mobilya","eviye-batarya","eviye","banyo-batarya","stop-valf","ankastre","musluk","armatur",
        "dus-set","dus-basl","dus-sistem","el-dus","dus-kolon","dusakabin","dus-tekne","dus-kanal","hidromasaj","kuvet","duslar","porselen","karo","seramik","kagitlik","havluluk","firca","sabunluk","cop-kova","tutunma","malzemelik","aski","aksesuar"]
def tur(url):
    u = url.replace("https://www.vitra.com.tr","").replace("https://vitra.com.tr","")
    if url.startswith("https://online."): return "eski-online"
    if u in ("", "/"): return "anasayfa"
    if re.search(r"-p-a?\d+", u) or u.startswith("/p-"): return "urun"
    if u.startswith("/product"): return "urun-teknik"
    if u.startswith("/c-") or u.startswith(("/karo-seramik-urunleri","/vitrifiyeler","/armaturler","/yikanma-alanlari","/banyo-mobilyalari","/banyo-aksesuarlari","/rezervuarlar","/dus-sistemleri","/duslar")): return "kategori"
    if re.search(r"^/[a-z0-9-]+/?$", u) and any(k in u for k in K): return "kategori"
    if u.startswith(("/hakkimizda","/basin-odasi","/musteri-hizmetleri","/kurumsal","/iletisim","/surdurulebilirlik","/kariyer")): return "kurumsal"
    if u.startswith("/ilham") or u.startswith("/blog"): return "icerik"
    if u.startswith("/servis") or "satis-nokta" in u or "bayi" in u: return "servis-bayi"
    if u.startswith("/katalog"): return "katalog"
    if u.startswith("/v/") or u.startswith("/koleksiyon"): return "koleksiyon"
    return "diger"
def kat(url):
    u = url.lower()
    for s in SIRA:
        if s in u: return K[s]
    return ("Diğer","Diğer")
d = json.load(open(os.path.join(G, "sayfa_16ay.json")))["rows"]
ozet = defaultdict(lambda: [0,0,0]); kat_ozet = defaultdict(lambda: [0,0,0,0])
for r in d:
    t = tur(r["keys"][0]); ozet[t][0]+=r["clicks"]; ozet[t][1]+=r["impressions"]; ozet[t][2]+=1
    if t in ("kategori","urun","eski-online","koleksiyon","urun-teknik"):
        k = kat(r["keys"][0]); kat_ozet[k][0]+=r["clicks"]; kat_ozet[k][1]+=r["impressions"]; kat_ozet[k][2]+=1
print("Sayfa türü · 16 ay tık / gösterim / sayfa")
for t,(c,i,n) in sorted(ozet.items(), key=lambda x:-x[1][0]): print(f"  {t:12} {c:9} {i:11} {n:6}")
print("\nKategori (kategori+ürün sayfaları) · 16 ay")
for k,(c,i,n,_) in sorted(kat_ozet.items(), key=lambda x:-x[1][0]): print(f"  {k[0]:20} {k[1]:26} {c:8} {i:10} {n:5}")
# aylik: sayfa_ay
rows = json.load(open(os.path.join(G, "sayfa_ay.json")))["rows"]
ay = defaultdict(lambda: defaultdict(lambda:[0,0]))
for r in rows:
    u, dt = r["keys"]; t = tur(u)
    key = kat(u)[0] if t in ("kategori","urun","eski-online","koleksiyon","urun-teknik") else ("İçerik" if t=="icerik" else ("Ana sayfa" if t=="anasayfa" else ("Servis ve bayi" if t=="servis-bayi" else "Diğer")))
    ay[key][dt[:7]][0]+=r["clicks"]; ay[key][dt[:7]][1]+=r["impressions"]
json.dump({"sayfa_turu": {k:v for k,v in ozet.items()}, "kategori": {"%s|%s"%k: v[:3] for k,v in kat_ozet.items()}, "aylik": {k: dict(v) for k,v in ay.items()}},
          open(os.path.join(O, "gsc_kategori.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
aylar = sorted({m for v in ay.values() for m in v})
print("\nAylık tık · kategori (sayfa×gün ilk 100.000 satır, büyük sayfalar)")
print("kategori".ljust(20), " ".join(m[2:] for m in aylar))
for k in sorted(ay, key=lambda x: -sum(v[0] for v in ay[x].values())): print(k.ljust(20), " ".join(f"{ay[k].get(m,[0,0])[0]:5}" for m in aylar))
