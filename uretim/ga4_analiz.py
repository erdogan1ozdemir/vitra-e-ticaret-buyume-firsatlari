# -*- coding: utf-8 -*-
"""GA4 dışa aktarımı (VitrA ekibi, 05.10.2026; veri/kaynak/ga4/Reports_2026-10-05.xlsx) -> veri/islenmis/ga4.json
Mülk: ECZ_EYAP_Online Vitra_TR_GA4_Genel (vitra.com.tr). Aralık 2025'te www.vitra.com.tr trafiği bu mülke katıldığı için oturum ve dönüşüm oranı
Aralık 2025 öncesi ve sonrası arasında kıyaslanmaz; satın alma ve gelir (mağaza her iki dönemde de bu mülkteydi) kıyaslanabilir.
Sayfalar: 11 = genel bakış (aylık, Oca 2025 - Eyl 2026), 4 = kanal (aylık) ve kaynak / ortam (toplam), 7 = ödeme ve teslimat türü,
9 = blog ve koleksiyon sayfaları, 10 = promosyon ve kupon. Site içi arama (sayfa 3 örneklenmiş olduğu için) ve servis düğmesi tıklaması (sayfa 8 ay sütununda yıl
taşımadığı için) VitrA ekibinin sonradan ilettiği CSV dışa aktarımlarından okunur. Anahtar olay (key event) satın alma dışında sepete ekleme, ödeme adımları, dosya indirme, favori ve üyelik olaylarını
da kapsadığından kullanılmaz; genel bakıştaki oran satın alma oranıdır.
Landing page sayfası (5) belirsiz bir süzgeçle alındığı için (13 ayda 60K oturum, gelir 0, ay sütununda yıl yok) kullanılmamıştır; yerine VitrA ekibinin
aylık landing page dışa aktarımları kullanılmıştır (landing_2025.csv: 1 Oca - 31 Ara 2025, landing_2026.csv: 1 Oca - 5 Eki 2026). Bu dosyalarda aylık gelir
genel bakışla birebir aynıdır; sayfa bazındaki oturumların toplamı ise genel bakıştaki oturumdan yüksektir, bu yüzden oturum yalnız pay olarak kullanılır."""
import json, os, re
from urllib.parse import unquote
from collections import defaultdict
import openpyxl
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X = os.path.join(P, "veri/kaynak/ga4/Reports_2026-10-05.xlsx")
wb = openpyxl.load_workbook(X, read_only=True, data_only=True)
def satirlar(s): return [list(r) for r in wb[s].iter_rows(values_only=True)]
def sayi(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    t = str(v).split(" (")[0].replace("₺", "").replace(",", "").strip()
    try: return float(t)
    except ValueError: return None
def tablo(s, bas):
    R = satirlar(s); out = []; h = None
    for i, r in enumerate(R):
        if r and r[0] == bas: h = i; continue
        if h is None: continue
        if not r or r[0] is None or str(r[0]).startswith("#"):
            if out: break
            continue
        out.append(r)
    return out
O = {"kaynak": "Google Analytics 4 · ECZ_EYAP_Online Vitra_TR_GA4_Genel (vitra.com.tr) · VitrA ekibi dışa aktarımı 05.10.2026"}
# ------------------------------------------------------------------ genel bakış
gen = {}
for r in satirlar("11"):
    if r and isinstance(r[1], (int, float)) and isinstance(r[2], (int, float)) and r[0] != "Total":
        y, m = int(r[1]), int(r[2])
        gen["%d-%02d" % (y, m)] = {"oturum": sayi(r[3]), "kullanici": sayi(r[4]), "satin": sayi(r[5]), "gelir": sayi(r[6]), "ort": sayi(r[7]), "ker": sayi(r[8])}
O["genel"] = dict(sorted(gen.items()))
# ------------------------------------------------------------------ kanal (aylık)
kan = defaultdict(dict)
for y, s in ((2025, "4 - Tablo 1 (2025)"), (2026, "4 - Tablo 1 (2026)")):
    for r in tablo(s, "Session default channel group"):
        if not isinstance(r[1], (int, float)): continue
        kan[r[0]]["%d-%02d" % (y, int(r[1]))] = {"oturum": sayi(r[2]), "kullanici": sayi(r[3]), "satin": sayi(r[8]), "gelir": sayi(r[9]), "etkilesim": sayi(r[12])}
O["kanal"] = {k: dict(sorted(v.items())) for k, v in kan.items()}
for y, s in ((2025, "4 - Tablo 2 (2025)"), (2026, "4 - Tablo 2 (2026)")):
    O["kaynak_%d" % y] = [{"sm": r[0], "oturum": sayi(r[1]), "satin": sayi(r[7]), "gelir": sayi(r[8]), "etkilesim": sayi(r[11])} for r in tablo(s, "Session source / medium")]
# ------------------------------------------------------------------ site içi arama (keşif raporu, örneklenmiş)
def terim(v):
    """Arama terimini tekilleştirir: sayısal hücre tam sayıya, URL kodlaması çözülür, sayfalama ve süzgeç parametreleri (&page=, &q=) atılır,
    Türkçe küçük harf dönüşümünden kalan birleşik nokta (i̇) temizlenir, boşluklar tekilleşir."""
    if isinstance(v, float) and v.is_integer(): v = int(v)
    t = unquote(str(v)).split("&")[0].lower().replace("\u0307", "")
    return " ".join(t.split())
import csv as _csv
def csv_oku(ad):
    """Keşif dışa aktarımı (CSV): # başlıklı satırlar ve Grand total satırı atlanır; ilk anlamlı satır başlıktır."""
    R = [r for r in _csv.reader(l for l in open(os.path.join(P, "veri/kaynak/ga4", ad), encoding="utf-8") if not l.startswith("#")) if r and any(r)]
    toplam = next((r for r in R if r[-1] == "Grand total"), None)
    return R[0], [r for r in R[1:] if r[-1] != "Grand total"], toplam
# site içi arama: VitrA ekibinin iki ayrı keşif dışa aktarımı (1 May - 31 Tem 2026, 1 Ağu - 30 Eyl 2026), örnekleme yok; olay sayısı ve oturum
ARA_DOSYA = {"2026-05/07": "arama_2026-05_07.csv", "2026-08/09": "arama_2026-08_09.csv"}
ara = defaultdict(lambda: [0, 0]); ara_don = {}
for don, ad in ARA_DOSYA.items():
    h, R, top = csv_oku(ad)
    i_e, i_q, i_c, i_s = h.index("Event name"), h.index("Search Term"), h.index("Event count"), h.index("Sessions")
    for r in R:
        if r[i_e] != "view_search_results" or not r[i_q].strip(): continue
        q = terim(r[i_q]); a = ara[q]; a[0] += int(r[i_c]); a[1] += int(r[i_s])
    ara_don[don] = {"olay": int(top[i_c]), "oturum": int(top[i_s])}   # Grand total: oturum tekil sayılır
O["arama"] = sorted([[q] + v for q, v in ara.items()], key=lambda r: -r[1])
O["arama_donem"] = ara_don
O["arama_ornek8"] = round(sum(1 for q, v in ara.items() if v[0] % 8 == 0) / len(ara), 3)
# ------------------------------------------------------------------ ödeme ve teslimat türü
od = []; kg = []   # son 12 ay (1 Eki 2025 - 30 Eyl 2026), VitrA ekibi dışa aktarımı 06.10.2026
for ad, liste in (("odeme_turu_2025-10_2026-09.csv", od), ("teslimat_turu_2025-10_2026-09.csv", kg)):
    h, R, _ = csv_oku(ad)
    for r in R: liste.append((r[1], int(r[2])))
O["odeme"] = od; O["teslimat"] = kg
# ------------------------------------------------------------------ satın alma dışı olaylar (yıl içeren dışa aktarım, 1 Eyl 2025 - 30 Eyl 2026; yalnız servisler ve satış noktaları düğme tıklaması)
ld = defaultdict(dict)
h, R, _ = csv_oku("servis_satis_noktalari_2025-09_2026-09.csv")
for r in R:
    ld[r[h.index("Event name")]]["%s-%s" % (r[h.index("Year")], r[h.index("Month")].zfill(2))] = [int(r[h.index("Event count")])]
O["olay"] = {k: dict(sorted(v.items())) for k, v in ld.items()}
# ------------------------------------------------------------------ blog ve koleksiyon sayfaları (görüntüleme, kullanıcı, anahtar olay)
O["blog"] = [[r[0], sayi(r[1]), sayi(r[2]), sayi(r[3])] for r in satirlar("9 - Tablo 1 ve Blog") if r and r[0] and str(r[0]).startswith("/")]
O["koleksiyon"] = [[r[0], sayi(r[1]), sayi(r[2]), sayi(r[3])] for r in satirlar("9 - Koleksiyon") if r and r[0] and str(r[0]).startswith("/")]
# ------------------------------------------------------------------ promosyon ve kupon
def _pad(t):
    t = str(t).replace("\u200b", "").strip()
    if "Ã" in t:
        try: t = t.encode("latin-1").decode("utf-8")
        except Exception: pass
    return " ".join(t.split())
pa = defaultdict(lambda: [0, 0])
for ad in sorted(os.listdir(os.path.join(P, "veri/kaynak/ga4/promosyon_aylik"))):
    h, R, _ = csv_oku(os.path.join("promosyon_aylik", ad))
    for r in R:
        a = pa[_pad(r[0])]; a[0] += int(r[2]); a[1] += int(r[3])
O["promosyon_12ay"] = sorted([[k, v[0], v[1]] for k, v in pa.items()], key=lambda x: -x[1])
O["promosyon"] = [{"ad": r[0], "kupon": r[1], "gor": sayi(r[2]), "tik": sayi(r[3]), "sepet": sayi(r[5]), "odeme": sayi(r[6]), "satin": sayi(r[7]), "gelir": sayi(r[8])}
                  for r in tablo("10 - Promotion", "Item promotion name")]
# ------------------------------------------------------------------ giriş sayfası (landing page) · aylık dışa aktarımlar
import csv
KAT_SLUG = ("klozet", "lavabo", "batarya", "musluk", "dolab", "dolap", "ayna", "dus", "kuvet", "rezervuar", "kumanda", "aksesuar", "havlu", "karo", "seramik", "armatur",
            "vitrifiye", "eviye", "pisuvar", "bide", "tezgah", "kapak", "sabunluk", "kagitlik", "banyo-urun")
KURUMSAL = ("katalog", "kurumsal", "hakkimizda", "basin", "kariyer", "konut", "proje", "bize-ulasin", "iletisim", "insaat", "mimari", "kvkk", "cerez")
def lp_tur(p):
    """Giriş sayfası türü: eski mağaza (/tr/...) ve yeni site adres yapısı birlikte."""
    p0 = p.split("?")[0].split("#")[0].lower()
    if p0 == "(not set)": return "diger"
    if p0 == "/tr" or p0.startswith("/tr/"): p0 = p0[3:] or "/"
    if p0 in ("/", ""): return "anasayfa"
    if p0.startswith("/checkout/orderconfirmation"): return "siparis"   # sipariş onay sayfası: oturum satın alma tamamlandıktan sonra başlıyor
    if re.match(r"^/(cart|checkout|login|misafir|register|my-account|sepet|odeme)", p0): return "odeme"
    if p0.startswith(("/search", "/arama")): return "arama"
    if p0.startswith(("/ilham-veren-fikirler", "/blog")): return "blog"
    if re.search(r"-p-[a-z0-9]|-sku-", p0) or p0.startswith("/p-"): return "urun"
    if re.search(r"-c-\d", p0) or p0.startswith("/c-"): return "kategori"
    if p0.startswith(("/servis", "/destek", "/support", "/montaj", "/sikca", "/yardim", "/360-magaza")) or any(k in p0 for k in ("satis-nokta", "bayi", "rehber")): return "destek"
    segs = [x for x in p0.split("/") if x]
    if segs and segs[0].startswith(KURUMSAL): return "kurumsal"
    if "kampanya" in p0 or "firsat" in p0 or p0.startswith(("/v/", "/v-", "/kesfet", "/banyo-koleksiyonlari", "/karo-koleksiyonlari", "/koleksiyon")): return "koleksiyon"
    if len(segs) >= 2: return "urun"   # yeni site: /kategori-adi/urun-adi
    if len(segs) == 1: return "kategori" if any(k in segs[0] for k in KAT_SLUG) else "koleksiyon"
    return "diger"
def lp_oku(ad):
    R = list(csv.reader(l for l in open(os.path.join(P, "veri/kaynak/ga4", ad), encoding="utf-8") if not l.startswith("#")))
    return [r for r in R[1:] if len(r) >= 11 and r[1].strip()]
LP = {2025: lp_oku("landing_2025.csv"), 2026: lp_oku("landing_2026.csv")}
lt = defaultdict(lambda: defaultdict(lambda: [0, 0.0, 0.0, 0.0]))   # tür -> yıl -> [oturum, gelir, anahtar olay, etkileşimli oturum] · Oca-Eyl
lp26 = defaultdict(lambda: [0, 0.0, 0.0, 0.0])
lay = defaultdict(lambda: [0.0, 0.0, 0.0])                          # ay -> [sepet, giriş ve ödeme adımında başlayan oturumların geliri, toplam gelir, sipariş onay sayfasında başlayanların geliri]
sip_no = defaultdict(set)                                           # yıl -> Oca-Eyl'de giriş sayfası olan farklı sipariş onay adresleri (sipariş numarası)
for y, R in LP.items():
    for r in R:
        m = int(r[1]); t = lp_tur(r[0]); o, g, ke, er = int(r[2]), float(r[7]), float(r[6]), float(r[10])
        lay["%d-%02d" % (y, m)][1] += g
        if t == "odeme": lay["%d-%02d" % (y, m)][0] += g
        if t == "siparis": lay["%d-%02d" % (y, m)][2] += g
        if t == "siparis" and m <= 9: sip_no[y].add(r[0].split("?")[0].lower())
        if m > 9: continue
        a = lt[t][y]; a[0] += o; a[1] += g; a[2] += ke; a[3] += o * er
        if y == 2026: b = lp26[r[0]]; b[0] += o; b[1] += g; b[2] += ke; b[3] += o * er
for y in (2025, 2026):   # gelir genel bakışla birebir olmalıdır
    for m in range(1, 13):
        k = "%d-%02d" % (y, m)
        if k in O["genel"]: assert abs(lay[k][1] - O["genel"][k]["gelir"]) < 1, ("landing gelir uyuşmuyor", k)
O["lp_tur"] = {t: {str(y): v for y, v in d.items()} for t, d in lt.items()}
O["lp_odeme_ay"] = {k: v for k, v in sorted(lay.items()) if k in O["genel"]}
O["lp_oturum_top"] = {str(y): sum(v[y][0] for v in lt.values()) for y in (2025, 2026)}
O["lp_siparis_no"] = {str(y): len(v) for y, v in sip_no.items()}
# sepet ve giriş sayfasında başlayan oturumlar (keşif, 1 Oca - 30 Eyl 2026): yalnız /cart, /login, /my-account (keşif süzgeci tam eşleşme)
h, R, top = csv_oku("odeme_giris_2026.csv")
O["odeme_giris"] = {r[0]: {"oturum": int(r[1]), "gelir": float(r[2]), "islem": int(r[3])} for r in R}
h, R, top = csv_oku("odeme_giris_kaynak_2026.csv")
kg = defaultdict(float)
for r in R: kg[r[1]] += float(r[3])
O["odeme_giris_kaynak"] = dict(sorted(kg.items(), key=lambda x: -x[1]))
# aynı sayfalarda session_start olayının sayfa yönlendireni (aylık dışa aktarımlar, Oca - Eyl 2026)
from urllib.parse import urlparse
ref_tur = defaultdict(int); ref_dis = defaultdict(int)
for ad in sorted(os.listdir(os.path.join(P, "veri/kaynak/ga4/session_start_ref"))):
    h, R, top = csv_oku(os.path.join("session_start_ref", ad))
    for r in R:
        if r[2] != "session_start": continue
        u = urlparse(r[1]); c = int(r[5])
        if u.netloc in ("www.vitra.com.tr", "vitra.com.tr", "online.vitra.com.tr"):
            pp = u.path.lower()
            ref_tur["cart" if pp.startswith("/cart") else "checkout" if pp.startswith("/checkout") else "login" if pp.startswith("/login") else "hesap" if pp.startswith("/my-account")
                    else "urun" if re.search(r"-p-|/p-", pp) else "kategori" if pp.startswith("/c-") else "anasayfa" if pp in ("", "/") else "arama" if pp.startswith("/search") else "diger"] += c
        else:
            ref_dis["(boş)" if not r[1] else ("Google" if "google" in u.netloc or "googlequicksearchbox" in r[1] else "diğer dış site")] += c
O["oturum_yenilenme"] = {"site_ici": dict(ref_tur), "dis": dict(ref_dis)}
# blog sayfalarında olaylar (keşif, 1 Eyl 2025 - 30 Eyl 2026)
h, R, top = csv_oku("blog_olaylar_2025-09_2026-09.csv")
O["blog_olay"] = {r[0]: int(r[1]) for r in R}
h, R, top = csv_oku("blog_oturum_kanal_2025-10_2026-09.csv")
bk = defaultdict(int); bl = defaultdict(int)
for r in R:
    o = int(r[h.index("Sessions")]); bk[r[h.index("Session default channel group")]] += o
    p_ = r[h.index("Landing page")].split("?")[0]; bl["blog" if p_.startswith("/ilham-veren-fikirler") else "diger"] += o
O["blog_kanal"] = dict(sorted(bk.items(), key=lambda x: -x[1])); O["blog_giris"] = dict(bl); O["blog_oturum_top"] = int(top[h.index("Sessions")])
O["lp_2026"] = sorted([[p_, lp_tur(p_)] + v for p_, v in lp26.items() if v[1] > 0 or v[0] >= 5000], key=lambda r: -r[3])[:400]
# ------------------------------------------------------------------ satın alma hunisi, alıcı tipi, yeni ve geri dönen kullanıcı (VitrA ekibi, 06.10.2026)
_hw = openpyxl.load_workbook(os.path.join(P, "veri/kaynak/ga4/huni_alici_yeni_donen.xlsx"), read_only=True, data_only=True)
def _ym(v): return v.strftime("%Y-%m") if hasattr(v, "strftime") else str(v)[:7]
HUNI_ADIM = ["view_item_list", "view_item", "add_to_cart", "begin_checkout", "add_shipping_info", "add_payment_info", "purchase"]
O["huni"] = {_ym(r[0]): [r[i] or 0 for i in range(1, 8)] for r in list(_hw["Funnel"].iter_rows(values_only=True))[1:] if r[0]}
O["alici"] = {_ym(r[0]): {"toplam": r[1], "ilk": r[2], "satin": r[3]} for r in list(_hw["Purchaser Type"].iter_rows(values_only=True))[1:] if r[0]}
yd = defaultdict(dict)
for r in list(_hw["New  Returning User"].iter_rows(values_only=True))[1:]:
    if r[0]: yd[_ym(r[0])][r[1]] = {"oturum": r[2], "islem": r[3], "gelir": r[4]}
O["yeni_donen"] = dict(sorted(yd.items()))
# ------------------------------------------------------------------ ürün performansı (item, ay × ürün). Items added to cart bazı aylarda bozuk değer taşıdığı için kullanılmaz;
# item revenue genel bakıştaki gelirden yüksek (2025 ~1,9x, 2026 ~1,13x) olduğu için yalnız pay olarak kullanılır
_iw = openpyxl.load_workbook(os.path.join(P, "veri/kaynak/ga4/urun_performansi_2025-01_2026-09.xlsx"), read_only=True, data_only=True)
_it = _iw.worksheets[0].iter_rows(values_only=True); _h = next(_it)
def _n(v): return v if isinstance(v, (int, float)) else 0
kat_u = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0.0, 0, 0]))   # yıl -> ana kategori -> [görüntülenen, ödemeye geçen, satın alınan, ürün geliri, sepete eklenen (Oca-Ağu), görüntülenen (Oca-Ağu)] · Oca-Eyl
SEPET_HATALI = {"7910B476-0090", "121-003-909", "ETIC_MTJ(KUCUK)", "ETIC_MTJ(BUYUK)", "ETIC_MTJ(ARMATUR)"}   # VitrA ekibi: sepete eklenen adet hatalı (06.10.2026)
urn = defaultdict(lambda: [None, None, None, 0, 0, 0.0])               # 2026 Oca-Eyl: ürün kodu -> [ad, kategori, marka, görüntülenen, satın alınan, ürün geliri]
mrk = defaultdict(lambda: defaultdict(float))
for r in _it:
    if not r or not r[0] or int(str(r[0])[5:7]) > 9: continue
    y = str(r[0])[:4]; c1, c2 = (r[3] or "").strip(), (r[4] or "").strip()
    ana = c2 if c1 == "Banyo" and c2 else c1   # 2026 ağacında ana kategori ikinci seviyede
    v, co, pu, rv = _n(r[7]), _n(r[10]), _n(r[11]), _n(r[13])
    a = kat_u[y][ana or "(boş)"]; a[0] += v; a[1] += co; a[2] += pu; a[3] += rv
    if int(str(r[0])[5:7]) <= 8 and str(r[1]) not in SEPET_HATALI: a[4] += _n(r[8]); a[5] += v   # Eylül 2026 add_to_cart hatalı tetiklenme nedeniyle dışarıda
    mrk[y][r[6] or "(boş)"] += rv
    if y == "2026":
        b = urn[str(r[1])]; b[0] = b[0] or r[2]; b[1] = b[1] or ana; b[2] = b[2] or r[6]; b[3] += v; b[4] += pu; b[5] += rv
O["urun_kat"] = {y: dict(d) for y, d in kat_u.items()}
O["urun_marka"] = {y: dict(d) for y, d in mrk.items()}
O["urun_2026"] = sorted([[k] + v for k, v in urn.items() if v[3] >= 3000 or v[4] >= 3], key=lambda x: -x[5])   # satın alınan adede göre
# ------------------------------------------------------------------ içerikten ürüne: blog sayfası görüntülenen ve görüntülenmeyen oturumlarda olay sayıları (aylık, Oca - Eyl 2026)
iu = {}
for ad in sorted(os.listdir(os.path.join(P, "veri/kaynak/ga4/icerik_urun_yol1"))):
    R = [r for r in csv.reader(l for l in open(os.path.join(P, "veri/kaynak/ga4/icerik_urun_yol1", ad), encoding="utf-8") if not l.startswith("#")) if r and any(r)]
    seg, bas = R[0], R[1]
    ay_ = "%s-%s" % (ad[:4], ad[4:6]); iu[ay_] = {"blog": {}, "diger": {}}
    for r in R[2:]:
        if r[-1] == "Grand total" or not r[0]: continue
        for j in range(1, len(seg)):
            if bas[j] == "Event count": iu[ay_]["blog" if seg[j].lower().startswith("blog") else "diger"][r[0]] = int(r[j])
O["icerik_urun"] = iu
# içerikten ürüne: blog görüntülenen ve görüntülenmeyen oturumlarda oturum, satın alma ve gelir (aylık, 1 Eki 2025 - 30 Eyl 2026; ilk üç değer blog dışı, son üç değer blog segmenti)
ig = {}
for ad in sorted(os.listdir(os.path.join(P, "veri/kaynak/ga4/icerik_urun_gelir"))):
    R = [r for r in csv.reader(l for l in open(os.path.join(P, "veri/kaynak/ga4/icerik_urun_gelir", ad), encoding="utf-8") if not l.startswith("#")) if r and any(r)]
    seg, bas = R[0], R[1]
    if any(seg[2:]): assert seg[2].lower().startswith("non") and seg[5].lower().startswith("blog"), ("segment sırası", ad, seg)
    r = next(x for x in R[2:] if x[-1] != "Grand total" and x[0])
    ig["%s-%s" % (r[1], r[0].zfill(2))] = {"diger": {"oturum": int(r[2]), "gelir": float(r[3]), "satin": int(r[4])}, "blog": {"oturum": int(r[5]), "gelir": float(r[6]), "satin": int(r[7])}}
O["icerik_gelir"] = dict(sorted(ig.items()))
json.dump(O, open(os.path.join(P, "veri/islenmis/ga4.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
if __name__ == "__main__":
    def top(y, a, m1=1, m2=9): return sum(O["genel"]["%d-%02d" % (y, m)][a] for m in range(m1, m2 + 1))
    for a in ("oturum", "satin", "gelir"): print(a, top(2025, a), top(2026, a), round(100 * (top(2026, a) / top(2025, a) - 1), 1))
    print("aylar", list(O["genel"])[:2], list(O["genel"])[-2:])
    def kt(y, a): return {k: sum(v.get("%d-%02d" % (y, m), {}).get(a) or 0 for m in range(1, 10)) for k, v in O["kanal"].items()}
    g5, g6 = kt(2025, "gelir"), kt(2026, "gelir"); s5, s6 = kt(2025, "satin"), kt(2026, "satin"); o5, o6 = kt(2025, "oturum"), kt(2026, "oturum")
    for k in sorted(g6, key=lambda k: -g6[k]): print("  %-26s gelir %10.0f -> %10.0f  satın %4.0f -> %4.0f  oturum %8.0f -> %8.0f" % (k, g5.get(k, 0), g6[k], s5.get(k, 0), s6[k], o5.get(k, 0), o6[k]))
    print("arama", len(O["arama"]), sum(r[1] for r in O["arama"]), O["arama_donem"], "8 katı", O["arama_ornek8"])
    print("blog", len(O["blog"]), sum(r[1] for r in O["blog"]), "koleksiyon", len(O["koleksiyon"]))
    print("olay", {k: sum(v[0] for v in d.values()) for k, d in O["olay"].items()})
    for t, d in sorted(O["lp_tur"].items(), key=lambda x: -x[1].get("2026", [0, 0])[1]):
        print("  lp %-11s" % t, {y: [v[0], round(v[1]), round(100 * v[3] / v[0], 1) if v[0] else 0] for y, v in d.items()})
