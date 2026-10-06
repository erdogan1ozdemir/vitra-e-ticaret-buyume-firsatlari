# -*- coding: utf-8 -*-
"""GA4 dışa aktarımı (VitrA ekibi, 05.10.2026; veri/kaynak/ga4/Reports_2026-10-05.xlsx) -> veri/islenmis/ga4.json
Mülk: ECZ_EYAP_Online Vitra_TR_GA4_Genel (vitra.com.tr). Aralık 2025'te www.vitra.com.tr trafiği bu mülke katıldığı için oturum ve dönüşüm oranı
Aralık 2025 öncesi ve sonrası arasında kıyaslanmaz; satın alma ve gelir (mağaza her iki dönemde de bu mülkteydi) kıyaslanabilir.
Sayfalar: 11 = genel bakış (aylık, Oca 2025 - Eyl 2026), 4 = kanal (aylık) ve kaynak / ortam (toplam), 7 = ödeme ve teslimat türü,
9 = blog ve koleksiyon sayfaları, 10 = promosyon ve kupon. Site içi arama (sayfa 3 örneklenmiş olduğu için) ve servis düğmesi tıklaması (sayfa 8 ay sütununda yıl
taşımadığı için) VitrA ekibinin sonradan ilettiği CSV dışa aktarımlarından okunur. Anahtar olay (key event) sütunları tüm olayları kapsadığından kullanılmaz;
genel bakıştaki oran satın alma oranıdır.
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
R = satirlar("7 - Tablo 1 ve 2"); od = []; kg = []
for r in R:
    if r and r[0] == "add_payment_info" and r[1]: od.append((r[1], sayi(r[2])))
    if r and r[0] == "add_shipping_info" and r[1]: kg.append((r[1], sayi(r[2])))
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
lay = defaultdict(lambda: [0.0, 0.0])                               # ay -> [ödeme adımında başlayan oturumların geliri, toplam gelir]
for y, R in LP.items():
    for r in R:
        m = int(r[1]); t = lp_tur(r[0]); o, g, ke, er = int(r[2]), float(r[7]), float(r[6]), float(r[10])
        lay["%d-%02d" % (y, m)][1] += g
        if t == "odeme": lay["%d-%02d" % (y, m)][0] += g
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
O["lp_2026"] = sorted([[p_, lp_tur(p_)] + v for p_, v in lp26.items() if v[1] > 0 or v[0] >= 5000], key=lambda r: -r[3])[:400]
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
