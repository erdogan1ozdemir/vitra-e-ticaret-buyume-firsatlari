# -*- coding: utf-8 -*-
"""ozet.md uretimi (tum sayilar veriden hesaplanir)."""
import json, csv, collections, statistics as st, re
from fm_ortak import *
import fm_analiz as A   # analiz ciktilarini yeniden uretir
O=json.load(open(KOK+"_ozet_sayilar.json")); SH=json.load(open(KOK+"shopping.json")); KP=json.load(open(KOK+"_karsilastirma.json")); CA=json.load(open(KOK+"cimri_akakce.json"))
OFIS=A.OFIS
def tl(x): return "-" if x is None else f"{round(x):,}".replace(",",".")
def yz(x,isaret=False): 
    if x is None: return "-"
    v=round(x); return (("+" if v>0 else "")+f"%{v}") if isaret and v>0 else (f"-%{abs(v)}" if v<0 else f"%{v}")
DEGER=("vitra klozet","vitra lavabo","vitra batarya")
GEN=[s for s in SH["ilanlar"] if s["kelime"] not in DEGER]
def pay(rows,alan,top=12):
    c=collections.Counter(s[alan] for s in rows); n=sum(c.values()); return [(k,v,v/n*100) for k,v in c.most_common(top)],n
L=[]
def w(s=""): L.append(s)
# ---------- maliyet ----------
mal=collections.defaultdict(lambda:[0,0.0])
for l in open(KOK+"maliyet_dfs.jsonl"):
    d=json.loads(l); k=d["is"].split(":")[0]; mal[k][0]+=1; mal[k][1]+=d["maliyet_usd"]
toplam_dfs=sum(v[1] for v in mal.values())
# ---------- sellers ozet ----------
VS=O["vs_ozet"]; KO=O["kanal_ozet"]
vo_var=[r for r in VS if r["vitra_online_var"]]
fark=[r["vitra_online_en_dusuge_fark_yuzde"] for r in vo_var]
yay=[r["yayilim_yuzde"] for r in VS if r["satici_sayisi"]>=5]
ucuz_say=collections.Counter(r["en_ucuz_mecra"] for r in VS)
w("# VitrA Türkiye: Banyo Ürünlerinde Kanal ve Fiyat Manzarası")
w()
w("Veri tarihi: 29 Eylül 2026. Kapsam: Türkiye, Türkçe. Kaynaklar: Google Shopping (DataForSEO), Cimri, Akakçe. Fiyatlar TL, KDV dahil, listede görünen satış fiyatıdır (kargo hariç, kampanya ve sepet indirimleri dahil değildir).")
w()
w("## 1. Yöntem ve kapsam")
w()
w("- **Google Shopping kategori taraması:** 30 kelime (27 kategori kelimesi + 3 markalı kelime: vitra klozet, vitra lavabo, vitra batarya), her kelime için ilk 120 ürün listelemesi (DataForSEO `merchant/google/products`, location 2792, language tr). Toplam %d listeleme satırı; her satırda ürün, satıcı/mağaza, fiyat, (varsa) puan ve değerlendirme bulunuyor. Puan ve değerlendirme sayısı listelemelerin çok küçük bir bölümünde dolu geldiği için analize girmedi." % len(SH["ilanlar"]))
w("- **VitrA ürün bazında satıcı listeleri:** 12 ürün adı (VitrA S20, Integra, Sento, Metropole, Shift, Nest Trendy klozetleri; Integra klozet kapağı; Root ve Sento lavabo dolabı; Artema Solid S, Minimax S lavabo bataryası, Flo S banyo bataryası) aranmış, her arama için eşleşen ilk 2 ürün listesinin satıcı dökümü alınmıştır (DataForSEO `merchant/google/sellers`, listeleme başına en fazla 10 satıcı). Toplam %d ürün listesi." % len(VS))
w("- **Cimri:** cimri.com doğrudan istekte (curl, tarayıcı User-Agent) ve Apify `rag-web-browser` üzerinden 403 (Cloudflare) döndü. Bu nedenle Cimri sonuçları Google arama sonuçlarının özetlerinden (DataForSEO SERP) okunmuştur: 30 kategori kelimesi için 2, 12 VitrA ürünü için 1 sorgu (72 sorgu). Bu yolla ürün ve kategori sayfası başlığı, başlangıç fiyatı ve (bazı sayfalarda) satıcı sayısı okunabilmiştir; satıcı listesi, en yüksek fiyat ve en ucuz satıcı adı Cimri için alınamamıştır.")
w("- **Akakçe:** Akakçe için curl (tarayıcı User-Agent) ile ilk yaklaşık 15 istek 200 dönmüş (3 kategori sayfası ve 8 ürün sayfası, ek olarak bir VitrA S20 ürün sayfası), ardından site 429 ve Cloudflare doğrulama sayfası vermiştir. Doğrulama aşılmamış, denemeler durdurulmuş; Apify da aynı siteden 403 almıştır. Kalan veri Cimri'deki gibi Google arama özetlerinden (72 sorgu) okunmuştur.")
w("- **Fiyat matrisi kuralları:** Aynı kelime için medyanın 0.2 katından düşük ve 5 katından yüksek fiyatlar (aksesuar, yedek parça, set/paket gürültüsü) çıkarılmıştır (%d listeleme); aynı ürün tipinde aynı satıcı, başlık ve fiyat tekrarı bir kez sayılmıştır. Kalan %d tekil ilan matrise girmiştir. Ürün tipi, kelimeden atanmıştır (örneğin lavabo dolabı, banyo dolabı, çamaşır makinesi dolabı ve boy dolabı = Banyo mobilyası)." % (O["aykiri"],O["ilan_tekil"]))
w("- **Mecra sınıflaması:** Satıcı adından atanmıştır: Trendyol, Hepsiburada, Amazon TR, Çiçeksepeti, Koçtaş, Bauhaus, IKEA, VitrA Online (vitra.com.tr), diğer resmi marka mağazaları (Creavit, E.C.A, Turkuaz vb.), Banyomarka, diğer pazaryeri/genel perakende (n11, PttAVM, Pazarama, A101 vb.) ve bağımsız banyo & yapı mağazaları (geri kalan tüm satıcılar). Sellers verisinde alan adı da kullanılmıştır; `VitrA Online` mağazasının alan adı www.vitra.com.tr olarak doğrulanmıştır.")
w("- **Marka ataması:** Ürün başlığındaki marka/seri adından yapılmıştır (VitrA için VitrA ve yaygın seri adları; Artema ayrı). Başlığında marka geçmeyen veya listede tek tek yer almayan markalar `Diğer markalar` altında toplanmıştır.")
w()
w("## 2. Maliyet")
w()
w("| Kalem | İstek | Maliyet (USD) |"); w("|---|---:|---:|")
ad={"products":"Google Shopping kategori taraması (products, 30 kelime)","products_urun":"Google Shopping VitrA ürün araması (products, 12 ürün)","sellers":"Google Shopping satıcı listesi (sellers, 24 liste)","sellers_tekrar":"Satıcı listesi yeniden deneme (3 liste)","serp_cimri":"Cimri özetleri için Google SERP (72 sorgu)","serp_akakce":"Akakçe özetleri için Google SERP (72 sorgu)"}
for k,v in mal.items(): w("| %s | %d | %.3f |"%(ad.get(k,k),v[0],v[1]))
w("| **DataForSEO toplam** | %d | **%.2f** |"%(sum(v[0] for v in mal.values()),toplam_dfs))
w("| Apify `rag-web-browser` (3 çalışma, üçü de hedef sitede 403 ile sonuçlandı, 0.078 compute unit) | 3 | yaklaşık 0.03 |")
w()
w("Kaynak: DataForSEO görev yanıtları (`cost` alanı), Apify çalışma istatistikleri. Ayrıntılı kayıt: `maliyet_dfs.jsonl`. Akakçe'ye doğrudan istekler (curl) ücretsizdir.")
w()
# ---------- bulgular ----------
vg=[s for s in GEN if s["marka"] in ("VitrA","Artema")]
vg_kanal,_=pay(vg,"mecra",20); vg_kanal=dict((k,(n,p)) for k,n,p in vg_kanal)
vo=[s for s in GEN if s["mecra"]==OFIS]; vo_kw=sorted(set(s["kelime"] for s in vo)); n_gen_kw=len(set(s["kelime"] for s in GEN))
marka_gen,ng=pay(GEN,"marka",30); marka_gen10,ng10=pay([s for s in GEN if s["sira"]<=10],"marka",30)
mg=dict((k,(n,p)) for k,n,p in marka_gen)
w("## 3. Öne çıkan bulgular")
w()
w("1. **VitrA resmi mağazası Google Shopping'de sınırlı görünüyor.** VitrA Online (vitra.com.tr) genel kategori kelimelerinin %d'sinde (%d kelime içinden %d) toplam %d listelemeyle yer alıyor; genel kategori listelemelerinin %s'ünü oluşturuyor. Markalı üç kelimede (vitra klozet, vitra lavabo, vitra batarya) ise 27 listelemeyle ilk sıralarda görünüyor; yani mağaza marka aramalarında öne çıkıyor, kategori aramalarında ise belirgin biçimde geride kalıyor." % (round(len(vo_kw)/n_gen_kw*100),n_gen_kw,len(vo_kw),len(vo),yz(len(vo)/len(GEN)*100).replace("%","%")))
w("2. **VitrA ve Artema ürünlerinin büyük bölümü üçüncü taraf mecralardan listeleniyor.** Genel kategori sonuçlarında %d VitrA/Artema listelemesinin %s'i bağımsız banyo & yapı mağazalarından, %s'i Trendyol'dan, %s'i VitrA Online'dan, %s'i Koçtaş'tan, %s'i Hepsiburada'dan geliyor." % (len(vg),yz(vg_kanal["Bağımsız banyo & yapı mağazası"][1]),yz(vg_kanal["Trendyol"][1]),yz(vg_kanal[OFIS][1]),yz(vg_kanal["Koçtaş"][1]),yz(vg_kanal["Hepsiburada"][1])))
w("3. **Aynı üründe resmi mağaza fiyatı en düşük fiyatın üzerinde kalıyor.** Satıcı dökümü alınan %d ürün listesinin %d'sinde VitrA Online ilk 10 satıcı arasında yer alıyor; bu listelerde resmi mağaza fiyatı listedeki en düşük fiyattan medyan %s yüksek (aralık %s ile %s). VitrA Online'ın hiç görünmediği %d listede ise resmi mağaza ilk 10 satıcı içinde bulunmuyor." % (len(VS),len(vo_var),yz(st.median(fark)),yz(min(fark)),yz(max(fark)),len(VS)-len(vo_var)))
w("4. **En düşük fiyat çoğunlukla küçük bağımsız mağazalarda.** 24 ürün listesinde en ucuz satıcı: bağımsız banyo & yapı mağazası %d, Trendyol %d, Banyomarka %d, Amazon TR %d, Çiçeksepeti %d, Koçtaş %d, diğer pazaryeri %d, Hepsiburada %d. Aynı ürün için en yüksek fiyat, en düşük fiyatın medyan %s üzerinde (en az 5 satıcılı %d listede)." % (ucuz_say.get("Bağımsız banyo & yapı mağazası",0),ucuz_say.get("Trendyol",0),ucuz_say.get("Banyomarka (uzman e-ticaret)",0),ucuz_say.get("Amazon TR",0),ucuz_say.get("Çiçeksepeti",0),ucuz_say.get("Koçtaş",0),ucuz_say.get("Diğer pazaryeri / genel perakende",0),ucuz_say.get("Hepsiburada",0),yz(st.median(yay)),len(yay)))
tipv={}
for t in ("Klozet","Rezervuar","Banyo mobilyası","Lavabo","Batarya","Akıllı klozet","Ayna","Duşakabin & duş teknesi","Küvet","Aksesuar & havlupan","Mutfak (evye & batarya)","Klozet kapağı","Duş seti"):
    r=[s for s in GEN if s["tip"]==t]; tipv[t]=(sum(1 for s in r if s["marka"] in("VitrA","Artema")),len(r))
w("5. **VitrA payı klozet ve rezervuarda yüksek, bitişik tiplerde düşük.** VitrA + Artema listeleme payı: klozet %s, rezervuar %s, akıllı klozet %s, lavabo %s, banyo mobilyası %s, batarya %s; ayna %s, duşakabin & duş teknesi %s, küvet %s, aksesuar & havlupan %s, mutfak %s." % tuple(yz(tipv[t][0]/tipv[t][1]*100) for t in ("Klozet","Rezervuar","Akıllı klozet","Lavabo","Banyo mobilyası","Batarya","Ayna","Duşakabin & duş teknesi","Küvet","Aksesuar & havlupan","Mutfak (evye & batarya)")) if False else "")
L.pop()
w("5. **VitrA payı klozet ve rezervuarda yüksek, bitişik tiplerde düşük.** VitrA + Artema listeleme payı: " + ", ".join("%s %s"%(t.lower(),yz(tipv[t][0]/tipv[t][1]*100)) for t in ("Klozet","Rezervuar","Akıllı klozet","Lavabo","Banyo mobilyası","Batarya","Ayna","Duşakabin & duş teknesi","Küvet","Aksesuar & havlupan","Mutfak (evye & batarya)"))+".")
w("6. **Marka payı sıralaması:** genel kategori listelemelerinde (ilk 120 sonuç) VitrA %s, Creavit %s, Kale %s, ECA %s, Turkuaz %s, Grohe %s, Serel %s, Artema %s; ilk 10 sonuçta VitrA %s, Creavit %s, Kale %s." % (yz(mg["VitrA"][1]),yz(mg["Creavit"][1]),yz(mg["Kale"][1]),yz(mg["ECA"][1]),yz(mg["Turkuaz"][1]),yz(mg["Grohe"][1]),yz(mg["Serel"][1]),yz(mg["Artema"][1]),yz(dict((k,(n,p)) for k,n,p in marka_gen10)["VitrA"][1]),yz(dict((k,(n,p)) for k,n,p in marka_gen10)["Creavit"][1]),yz(dict((k,(n,p)) for k,n,p in marka_gen10)["Kale"][1])))
w()
w("Not: Bulguların hepsi Google Shopping'in 29 Eylül 2026 tarihli, masaüstü Türkiye görünümündeki listelemelerine dayanıyor; fiyatlar günlük değişebilir.")
w()
# ---------- matris ----------
w("## 4. Ürün tipi × mecra fiyat bandı (Google Shopping)")
w()
w("Tüm markalar birlikte. Hücre: medyan fiyat (ilan adedi). Yalnızca en az 3 ilanı olan hücreler gösterilmiştir; min ve maks değerleri `fiyat_matrisi.csv` dosyasında tam listelenmiştir. Mecra medyanları marka ve model karışımından etkilenir; örneğin tek markalı resmi mağazalar premium seriler ağırlıklıdır. Aynı ürün üzerinden karşılaştırma için bölüm 6 kullanılabilir.")
w()
MEC=["Trendyol","Hepsiburada","Amazon TR","Çiçeksepeti","Koçtaş","Bauhaus","IKEA",OFIS,"Banyomarka (uzman e-ticaret)","Bağımsız banyo & yapı mağazası"]
short={OFIS:"VitrA Online","Banyomarka (uzman e-ticaret)":"Banyomarka","Bağımsız banyo & yapı mağazası":"Bağımsız mağaza"}
mat={(r["urun_tipi"],r["mecra"]):r for r in O["matris"]}
tipler=sorted(set(r["urun_tipi"] for r in O["matris"]))
w("| Ürün tipi | "+" | ".join(short.get(m,m) for m in MEC)+" | Tüm mecralar |")
w("|---|"+"---:|"*(len(MEC)+1))
for t in tipler:
    hs=[]
    for m in MEC:
        r=mat.get((t,m)); hs.append("%s (%d)"%(tl(r["medyan"]),r["urun_adedi"]) if r and r["urun_adedi"]>=3 else "-")
    r=mat[(t,"TÜM MECRALAR")]; w("| %s | %s | %s (%d) |"%(t," | ".join(hs),tl(r["medyan"]),r["urun_adedi"]))
w()
w("Tüm mecralar için ürün tipi bazında min, medyan ve maks fiyat:")
w()
w("| Ürün tipi | İlan | Min | Medyan | Maks |"); w("|---|---:|---:|---:|---:|")
for t in tipler:
    r=mat[(t,"TÜM MECRALAR")]; w("| %s | %d | %s | %s | %s |"%(t,r["urun_adedi"],tl(r["min"]),tl(r["medyan"]),tl(r["maks"])))
w()
w("Not: Min değerleri hâlâ set dışı parça ve aksesuar içerebilir (özellikle batarya ve rezervuar tiplerinde); orta bant için medyan ve p25-p75 (CSV) daha güvenilirdir.")
w()
w("Kaynak: Google Shopping, DataForSEO merchant/google/products | 29 Eylül 2026 | Türkiye")
w()
w("### 4.1. Mecra bazında en ucuz ve en pahalı (çok markalı mecralar, en az 5 ilan)")
w()
w("Tek markalı resmi mağazalar (VitrA Online, Creavit, E.C.A vb.) sıralamaya dahil değildir.")
w()
w("| Ürün tipi | En düşük medyanlı mecra | Medyan | En yüksek medyanlı mecra | Medyan | Tüm mecralar medyanı |"); w("|---|---|---:|---|---:|---:|")
for t,v in O["en_ucuz"].items():
    w("| %s | %s | %s | %s | %s | %s |"%(t,short.get(v["en_ucuz_mecra"],v["en_ucuz_mecra"]),tl(v["medyan"]),short.get(v["en_pahali_mecra"],v["en_pahali_mecra"]),tl(v["en_pahali_medyan"]),tl(v["tum_medyan"])))
w()
w("Not: Küvet tipinde yalnızca bağımsız mağazaların yeterli ilanı bulunuyor; kıyaslama yapılamamıştır.")
w()
# ---------- vitra/artema kontrollu ----------
w("### 4.2. VitrA ve Artema ürünlerinde mecra medyanı ve VitrA Online farkı")
w()
w("Yalnızca başlığında VitrA veya Artema geçen ilanlar. Fark: mecra medyanının VitrA Online medyanına göre yüzde farkı (VitrA Online'da o tipte en az 2 ilan olan satırlarda). Aynı model karışımını garanti etmediği için yön göstergesidir.")
w()
mv={(r["urun_tipi"],r["mecra"]):r for r in O["matris_vitra"]}
MEC2=["Trendyol","Hepsiburada","Amazon TR","Koçtaş","Bağımsız banyo & yapı mağazası"]
w("| Ürün tipi | VitrA Online medyan (ilan) | "+" | ".join(short.get(m,m)+" medyan (ilan) · fark" for m in MEC2)+" |"); w("|---|---:|"+"---:|"*len(MEC2))
for t in tipler:
    o=mv.get((t,OFIS))
    if not o or o["urun_adedi"]<2: continue
    hs=[]
    for m in MEC2:
        r=mv.get((t,m)); hs.append("%s (%d) · %s"%(tl(r["medyan"]),r["urun_adedi"],yz(r["vitra_online_medyanina_fark_yuzde"],True)) if r and r["urun_adedi"]>=2 and r["vitra_online_medyanina_fark_yuzde"] is not None else "-")
    w("| %s | %s (%d) | %s |"%(t,tl(o["medyan"]),o["urun_adedi"]," | ".join(hs)))
w()
w("Kaynak: Google Shopping, DataForSEO merchant/google/products | 29 Eylül 2026")
w()
# ---------- vitra satici ----------
w("## 5. VitrA ürünlerinde satıcı sayısı ve en ucuz satıcı (Google Shopping satıcı dökümü)")
w()
w("Her satır bir ürün listesidir (Google Shopping'de aynı ürünün satıcıları). Satıcı sayısı listeleme başına en fazla 10 ile sınırlıdır; bu yüzden 10 değeri `10 ve üzeri` anlamına gelir. Fiyatlar listelenen toplam fiyattır (kargo ayrıca gösterilmemiştir).")
w()
w("| Ürün araması | Liste | Satıcı | En ucuz satıcı (mecra) | Min | Medyan | Maks | VitrA Online fiyat (sıra) | VitrA Online / en düşük |"); w("|---|---|---:|---|---:|---:|---:|---|---:|")
for r in VS:
    vf="%s (%d.)"%(tl(r["vitra_online_fiyat"]),r["vitra_online_sira"]) if r["vitra_online_var"] else "listede yok"
    w("| %s | %s | %d | %s (%s) | %s | %s | %s | %s | %s |"%(r["urun_sorgusu"],r["liste_basligi"][:48],r["satici_sayisi"],r["en_ucuz_satici"],short.get(r["en_ucuz_mecra"],r["en_ucuz_mecra"]),tl(r["en_dusuk"]),tl(r["medyan"]),tl(r["en_yuksek"]),vf,yz(r["vitra_online_en_dusuge_fark_yuzde"],True) if r["vitra_online_var"] else "-"))
w()
w("Mecra bazında özet (24 listede görülme, en ucuz olma, en düşük fiyata medyan fark):")
w()
w("| Mecra | Görüldüğü liste | En ucuz olduğu liste | En düşük fiyata medyan fark |"); w("|---|---:|---:|---:|")
for r in KO: w("| %s | %d / %d | %d | %s |"%(short.get(r["mecra"],r["mecra"]),r["listede_gorulme"],r["liste_toplam"],r["en_ucuz_sayisi"],yz(r["en_dusuk_fiyata_medyan_fark_yuzde"],True)))
w()
w("Not: Aynı liste içinde satıcıların sunduğu varyant (kapak dahil/hariç, renk) farklı olabilir; bu nedenle çok düşük bazı fiyatlar farklı paket içeriğinden kaynaklanabilir. Tam satıcı dökümü: `vitra_saticilar.csv`.")
w()
w("Kaynak: Google Shopping, DataForSEO merchant/google/sellers | 29 Eylül 2026 | Türkiye")
w()
# ---------- marka mağaza payı ----------
w("## 6. Marka ve mağaza payı (Google Shopping listelemeleri)")
w()
w("Payda: 27 genel kategori kelimesinin ilk 120 listelemesi (%d satır; markalı üç kelime hariç, VitrA payını şişirmemek için). Bir ürün birden fazla kelimede geçebildiğinden pay, listeleme payıdır." % len(GEN))
w()
w("| Marka | Listeleme | Pay (tüm ilk 120) | İlk 10'daki listeleme | Pay (ilk 10) |"); w("|---|---:|---:|---:|---:|")
d10=dict((k,(n,p)) for k,n,p in marka_gen10)
for m in ["VitrA","Artema","Kale","Creavit","Turkuaz","ECA","Grohe","Serel","Geberit","Seramiksan","Bocchi","Duravit","Hansgrohe","Teka","Franke","Blanco"]:
    a=mg.get(m,(0,0)); b=d10.get(m,(0,0)); w("| %s | %d | %s | %d | %s |"%(m,a[0],yz(a[1]),b[0],yz(b[1])))
dm=mg.get("Diğer markalar",(0,0)); w("| Diğer markalar (küçük veya başlığında marka geçmeyen) | %d | %s | %d | %s |"%(dm[0],yz(dm[1]),d10.get("Diğer markalar",(0,0))[0],yz(d10.get("Diğer markalar",(0,0))[1])))
w()
w("VitrA + Artema toplamı (grup): %d listeleme, %s; ilk 10'da %d listeleme, %s." % (mg["VitrA"][0]+mg["Artema"][0],yz(mg["VitrA"][1]+mg["Artema"][1]),d10["VitrA"][0]+d10["Artema"][0],yz(d10["VitrA"][1]+d10["Artema"][1])))
w()
w("Ürün tipine göre VitrA + Artema listeleme payı:")
w()
w("| Ürün tipi | VitrA + Artema listeleme | Toplam listeleme | Pay | Tipin en yüksek paylı ilk 3 markası |"); w("|---|---:|---:|---:|---|")
for t in tipler:
    r=[s for s in GEN if s["tip"]==t]; c=collections.Counter(s["marka"] for s in r if s["marka"]!="Diğer markalar"); n=len(r)
    top3=", ".join("%s %s"%(k,yz(v/n*100)) for k,v in c.most_common(3))
    a=sum(1 for s in r if s["marka"] in("VitrA","Artema")); w("| %s | %d | %d | %s | %s |"%(t,a,n,yz(a/n*100),top3))
w()
w("### 6.1. Mağaza / mecra payı")
w()
mec_gen,_=pay(GEN,"mecra",20); mec_10,_=pay([s for s in GEN if s["sira"]<=10],"mecra",20); m10=dict((k,(n,p)) for k,n,p in mec_10)
w("| Mecra | Listeleme | Pay (ilk 120) | İlk 10'da listeleme | Pay (ilk 10) |"); w("|---|---:|---:|---:|---:|")
for k,n,p in mec_gen: w("| %s | %d | %s | %d | %s |"%(short.get(k,k),n,yz(p),m10.get(k,(0,0))[0],yz(m10.get(k,(0,0))[1])))
w()
sat_gen,_=pay(GEN,"satici",15)
w("En çok listelenen mağaza adları (Google Shopping'deki yazımıyla; Trendyol ve trendyol.com gibi yazım varyantları ayrı satırdır): "+", ".join("%s (%d)"%(k,n) for k,n,p in sat_gen)+".")
w()
w("### 6.2. vitra.com.tr (VitrA Online) mağazasının Shopping görünürlüğü")
w()
vo_by=collections.defaultdict(list)
for s in vo: vo_by[s["kelime"]].append(s)
w("Genel 27 kelimeden %d'sinde, %d listelemeyle (%d farklı ürün başlığı) görünüyor; ilk 10 sonuçta %d listeleme. Markalı 3 kelimede ise vitra klozet 9, vitra lavabo 27, vitra batarya 27 listeleme (sırasıyla ilk görünme sırası 3, 1, 2)." % (len(vo_by),len(vo),len(set(s["baslik"] for s in vo)),len([s for s in vo if s["sira"]<=10])))
w()
w("| Kelime | VitrA Online listeleme | En iyi sıra |"); w("|---|---:|---:|")
for k in KATEGORILER:
    if k in DEGER: continue
    v=vo_by.get(k)
    w("| %s | %d | %s |"%(k,len(v) if v else 0,min(s["sira"] for s in v) if v else "-"))
w()
w("Görünmediği kelimeler: "+", ".join(k for k in KATEGORILER if k not in DEGER and k not in vo_by)+".")
w()
w("Kaynak: Google Shopping, DataForSEO merchant/google/products | 29 Eylül 2026 | Türkiye")
w()
# ---------- Cimri / Akakce ----------
w("## 7. Cimri ve Akakçe")
w()
w("### 7.1. Akakçe: doğrudan okunan sayfalar")
w()
w("İlk yaklaşık 15 istekte (ardından Cloudflare doğrulaması geldiği için durduruldu) alınan sayfalar. Kategori listesinin ilk sayfası popülerlik sırasındadır; fiyat, ürünün en düşük fiyatıdır; `+N fiyat` ek satıcı teklif sayısını gösterir.")
w()
ad_=CA["akakce_dogrudan"]
w("| Kategori sayfası | Toplam ürün | İlk sayfada VitrA ürünü | İlk sayfada marka dağılımı (en çok 4) | İlk sayfa en düşük fiyat medyanı |"); w("|---|---:|---:|---|---:|")
for k,v in ad_["kategori"].items():
    c=collections.Counter(u["marka"] for u in v["ilk_sayfa"]); fy=[u["en_dusuk_fiyat"] for u in v["ilk_sayfa"] if u["en_dusuk_fiyat"]]
    w("| %s (%s) | %s | %d | %s | %s |"%(k,v["sayfa_url"].replace("https://www.",""),f'{v["toplam_urun"]:,}'.replace(",","."),c.get("VitrA",0),", ".join("%s %d"%(a,b) for a,b in c.most_common(4)),tl(st.median(fy)) if fy else "-"))
w()
w("| Ürün (Akakçe ürün sayfası) | Teklif sayısı | En düşük | En yüksek | JSON-LD'de görünen satıcılar |"); w("|---|---:|---:|---:|---|")
sat_akk=[]
for k,v in ad_["kategori"].items():
    for d in v["urun_sayfalari"]:
        p=d["sayfa"]; sat_akk.append(p)
s20=ad_["vitra"].get("vitra s20 asma klozet",{}).get("urun_sayfasi")
if s20: sat_akk.append(s20)
for p in sat_akk:
    w("| %s | %d | %s | %s | %s |"%(p["ad"][:56],p["teklif_sayisi"],tl(p["en_dusuk"]),tl(p["en_yuksek"]),", ".join(sorted(set(s["satici"] for s in p["saticilar"])))[:80]))
w()
w("Not: Akakçe ürün sayfasındaki yapılandırılmış veri, teklif sayısı yüksek ürünlerde teklifin yalnızca bir bölümünü listeliyor; bu yüzden satıcı adları eksik olabilir ve en ucuz satıcı adı her satırda yazılamamıştır. Akakçe'de VitrA S20 7508L003-0850 için 4 teklif, 7.999 - 8.400 TL bandında ve satıcılar Hepsiburada ile PttAVM.")
w()
w("### 7.2. Cimri ve Akakçe: marka sayfaları (VitrA ile bazı markaların ürün sayısı)")
w()
w("Google arama özetinden okunan marka+kategori sayfaları (ilgili platformda o markanın o kategoride listelenen ürün sayısı ve sayfanın başlangıç fiyatı). Başlangıç fiyatı aksesuar ve parça içerebileceğinden fiyat bandı olarak değil, kapsam göstergesi olarak okunmalıdır.")
w()
w("| Kaynak | Kategori | Marka | Ürün sayısı | Başlangıç fiyatı |"); w("|---|---|---|---:|---:|")
for x in sorted(KP["marka_sayfalari"],key=lambda x:(x["kaynak"],x["kategori"],-x["urun_sayisi"])):
    w("| %s | %s | %s | %s | %s |"%(x["kaynak"],x["kategori"].replace("-"," "),x["marka"].capitalize() if x["marka"]!="eca" else "ECA",f'{x["urun_sayisi"]:,}'.replace(",","."),tl(x["baslangic_fiyat"])))
w()
w("### 7.3. Cimri ve Akakçe: kategori sayfası büyüklüğü")
w()
w("Yalnızca kelimeyle birebir eşleşen kategori sayfaları (adresi tabloda). Sayı, platformun o kategoride listelediği seçenek sayısıdır.")
w()
w("| Kelime | Cimri sayfası | Cimri seçenek | Akakçe sayfası | Akakçe seçenek |"); w("|---|---|---:|---|---:|")
for k,v in KP["kategori"].items():
    c=v["cimri"] if v["cimri"] and v["cimri"]["tam_eslesme"] else None; a=v["akakce_serp"] if v["akakce_serp"] and v["akakce_serp"]["tam_eslesme"] else None
    if not c and not a: continue
    w("| %s | %s | %s | %s | %s |"%(k,c["url"].replace("https://www.","") if c else "-",f'{c["secenek"]:,}'.replace(",",".") if c else "-",a["url"].replace("https://www.","") if a else "-",f'{a["secenek"]:,}'.replace(",",".") if a else "-"))
w()
w("### 7.4. VitrA ürünlerinde Cimri ve Akakçe en düşük fiyatları (arama özetinden)")
w()
w("| Ürün araması | Cimri (ürün, en düşük) | Akakçe (ürün, en düşük, fiyat sayısı) |"); w("|---|---|---|")
for k,v in KP["vitra"].items():
    c="; ".join("%s: %s"%(x["urun"][:40],tl(x["en_dusuk"])) for x in v["cimri"][:2]) or "-"
    a="; ".join("%s: %s (%d)"%(n[:40],tl(d["en_dusuk"]),d["fiyat_sayisi"]) for n,d in list(v["akakce_serp"].items())[:2]) or "-"
    w("| %s | %s | %s |"%(k,c,a))
w()
w("Kaynak: Cimri ve Akakçe, Google arama sonuç özetleri (DataForSEO SERP) ve Akakçe doğrudan sayfa okuması | 29 Eylül 2026")
w()
w("## 8. Kısıtlar")
w()
w("- Cimri sayfaları curl ve Apify üzerinden Cloudflare tarafından engellendi (403); Akakçe yaklaşık 15 isteğin ardından 429 ve doğrulama sayfası verdi. Doğrulama çözülmemiş, engel aşılmamıştır. Bu nedenle iki karşılaştırma sitesi için satıcı listesi, en yüksek fiyat ve en ucuz satıcı adı 30 kelimenin çoğunda alınamamıştır; yalnızca Akakçe'de 3 kategori (klozet, asma klozet, klozet kapağı) ve 9 ürün sayfası doğrudan okunabilmiştir. Diğer veriler Google arama özetleridir ve sayfa başlığı ile açıklamasındaki sayılarla sınırlıdır.")
w("- Google Shopping listelemesi yalnızca öne çıkan bir teklifi gösterir; satıcı dökümü listeleme başına ilk 10 satıcıdır. Sepet indirimi, kupon, taksit vadesi ve kargo ücreti fiyata dahil değildir. Fiyat tek bir gün (29 Eylül 2026) içindir.")
w("- Ürün tipi × mecra medyanları model, seri ve marka karışımından etkilenir; tipler arası kıyas için dolaylı göstergedir. Aynı ürün üzerinden kıyas yalnızca bölüm 5'teki 24 listede yapılabilmiştir.")
w("- Aykırı fiyat temizliği kelime medyanına göre otomatik yapılmıştır; akıllı klozet, küvet, batarya gibi geniş fiyat aralıklı tiplerde bazı aksesuar/parça ilanları kalmış olabilir.")
w("- Marka ataması ürün başlığına dayanır; başlığında marka geçmeyen listelemeler `Diğer markalar` altında yer alır (%s)." % yz(mg["Diğer markalar"][1]))
w("- Google Shopping puan ve değerlendirme alanları listelemelerin çok küçük bir bölümünde dolu geldiği için puan analizi yapılmamıştır.")
w("- Google Shopping'de yalnızca Google'a ürün besleme (feed) gönderen satıcılar görünür; VitrA Online mağazasının görünürlüğü bu feed kapsamını da yansıtır.")
w()
w("## Dosyalar")
w()
for f,a in [("shopping.json","Shopping listelemeleri (temizlenmemiş 3.600 satır), VitrA ürün listeleri, satıcı özetleri"),("cimri_akakce.json","Cimri/Akakçe verileri (doğrudan okunanlar, SERP özetleri, ayıklanan alanlar)"),("fiyat_matrisi.csv","ürün tipi × mecra: adet, min, p25, medyan, p75, maks (tüm markalar; VitrA+Artema kolonları dahil)"),("fiyat_matrisi_vitra_artema.csv","yalnızca VitrA + Artema ilanları"),("vitra_saticilar.csv","12 ürün için 24 liste, satıcı satırları"),("maliyet_dfs.jsonl","her DataForSEO çekiminin maliyeti")]:
    w("- `%s`: %s"%(f,a))
open(KOK+"ozet.md","w",encoding="utf-8").write("\n".join(L)+"\n")
print("ozet.md yazildi",len(L),"satir")
