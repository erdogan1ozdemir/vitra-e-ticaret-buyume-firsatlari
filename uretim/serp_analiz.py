# -*- coding: utf-8 -*-
"""Google TR mobil SERP analizi · ham/ (ilk 20 organik + SERP ozellikleri) + ham_ai/ (AI Overview referanslari).
Cikti: veri/ham/derin/serp/kelime_sonuc.json, ozet_veri.json, ozet.md ( bulgular.md varsa sonuna/basina eklenir )."""
import json, os, re, glob, collections, statistics
from serp_kelimeler import LISTE, KEL
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = os.path.join(B, "veri", "ham", "derin", "serp")
TEMA_SIRA = ["SSG", "BM", "Armatür-duş", "Yıkanma", "Bitişik", "Hizmet", "Karo", "Soru", "Marka"]
TEMA_ETIKET = {"SSG": "SSG", "BM": "BM", "Armatür-duş": "Armatür", "Yıkanma": "Yıkanma", "Bitişik": "Bitişik", "Hizmet": "Hizmet", "Karo": "Karo", "Soru": "Soru", "Marka": "Marka"}

def ad(k):
    return re.sub(r"[^0-9a-zA-Z]+", "_", k.replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g").replace("ö","o").replace("ü","u").replace("İ","I")).strip("_")

def kok(d):
    d = (d or "").lower()
    if d.startswith("www."): d = d[4:]
    if "amazon-com-tr" in d: return "amazon.com.tr"
    if d == "translate.google.com": return d
    p = d.split(".")
    if len(p) >= 3 and ".".join(p[-2:]) in ("com.tr", "org.tr", "net.tr", "gen.tr", "web.tr", "co.uk"): return ".".join(p[-3:])
    return ".".join(p[-2:]) if len(p) >= 2 else d

PAZAR = {"trendyol.com", "hepsiburada.com", "n11.com", "amazon.com.tr", "akakce.com", "cimri.com", "epey.com", "pttavm.com",
         "ciceksepeti.com", "yandex.com.tr", "pazarama.com", "sahibinden.com", "letgo.com", "gittigidiyor.com", "idefix.com", "temu.com", "aliexpress.com"}
SOSYAL = {"pexels.com", "instagram.com", "pinterest.com", "facebook.com", "tiktok.com", "x.com", "twitter.com"}
FORUM = {"eksisozluk.com", "sikayetvar.com", "reddit.com", "donanimhaber.com", "technopat.net", "kadinlarkulubu.com", "quora.com"}
VIDEO = {"youtube.com", "vimeo.com", "dailymotion.com"}
HIZMET = {"armut.com", "bionluk.com", "sahibinden.com_hizmet"}
BLOG_URL = re.compile(r"/(blog|rehber|makale|makaleler|icerik|ipucu|ipuclari|haber|haberler|yazi|yazilar|magazin|ilham|dergi|nedir|destek)/|blog\.|/blog$", re.I)
BLOG_TITLE = re.compile(r"\b(nedir|nasıl|nasil|rehber|rehberi|ipuçları|ipucu|nelerdir|kılavuz|hangisi)\b", re.I)
URUN = re.compile(r"(-p-\d+|/p/\d+|/urun/|/dp/|/product/|/products/|-pm-|/p-\d|/prd/|-P\d+/?$|/urunler/[^/]+/[^/]+/[^/?]+\.html|/(u|pd)/)", re.I)

def tip(d, url, title):
    k = kok(d); u = url or ""; ti = title or ""
    if k in VIDEO: return "video"
    if k in FORUM: return "forum/şikayet"
    if k in SOSYAL: return "sosyal/görsel"
    if k in HIZMET: return "hizmet platformu"
    if k == "wikipedia.org" or k.endswith("wikipedia.org"): return "blog/rehber"
    if k in PAZAR:
        if URUN.search(u): return "pazaryeri ürün"
        return "pazaryeri arama/liste"
    if BLOG_URL.search(u) or BLOG_TITLE.search(ti): return "blog/rehber"
    if URUN.search(u): return "ürün"
    return "kategori"

def yukle(dizin, kelime):
    return json.load(open(os.path.join(S, dizin, ad(kelime) + ".json")))

# ---------- hacim eslemesi (Keyword Planner, yeni_kategori.json) ----------
HK = json.load(open(os.path.join(B, "veri", "islenmis", "yeni_kategori.json")))["kelime"]
HD = {k["kw"]: k for k in HK}
def pfx(s): return tuple(w[:4] for w in s.split())
HP = collections.defaultdict(list)
for k in HK: HP[pfx(k["kw"])].append(k)
def hacim(kw):
    if kw in HD: return round(HD[kw]["v12"]), ""
    c = HP.get(pfx(kw))
    if c: return round(max(x["v12"] for x in c)), "~"
    return None, ""

kayit = []
for kw, tema in LISTE:
    r = yukle("ham", kw)
    res = r["tasks"][0]["result"][0]
    it = res["items"]
    org = [i for i in it if i["type"] == "organic"]
    top = [{"sira": i["rank_group"], "alan": kok(i["domain"]), "url": i["url"], "tip": tip(i["domain"], i["url"], i.get("title")), "baslik": i.get("title")} for i in org if i["rank_group"] <= 10]
    t20 = [{"sira": i["rank_group"], "alan": kok(i["domain"]), "url": i["url"], "tip": tip(i["domain"], i["url"], i.get("title"))} for i in org]
    vit = [x for x in t20 if x["alan"] == "vitra.com.tr"]
    artema = [x for x in t20 if x["alan"] == "artema.com.tr"]
    # ucuncu taraf sayfada VitrA urunu (url'de vitra gecen, vitra.com.tr disi, ilk 10)
    vit3 = [x for x in top if x["alan"] != "vitra.com.tr" and "vitra" in x["url"].lower()]
    tur = collections.Counter(i["type"] for i in it)
    vids = []
    for i in it:
        if i["type"] == "video":
            for e in i.get("items") or []:
                vids.append({"kaynak": e.get("source"), "baslik": e.get("title"), "url": e.get("url")})
    sv = []
    for i in it:
        if i["type"] == "short_videos":
            for e in i.get("items") or []:
                sv.append({"kaynak": e.get("source"), "alan": e.get("domain")})
    paa = []
    for i in it:
        if i["type"] == "people_also_ask":
            for e in i.get("items") or []:
                if e.get("title"): paa.append(e["title"])
    rel = []
    for i in it:
        if i["type"] == "people_also_search":
            rel += [x for x in (i.get("items") or []) if isinstance(x, str)]
    lp = [{"baslik": i.get("title"), "alan": kok(i["domain"]) if i.get("domain") else None} for i in it if i["type"] == "local_pack"]
    cs = []
    for i in it:
        if i["type"] == "compare_sites":
            cs += [kok(e.get("domain")) for e in i.get("items") or []]
    fiyatli = sum(1 for i in org if i["rank_group"] <= 10 and i.get("price"))
    # AI Overview (asenkron yeniden cekim)
    ai_var_ilk = tur.get("ai_overview", 0) > 0
    ai = None
    if ai_var_ilk:
        ra = yukle("ham_ai", kw)["tasks"][0]["result"][0]
        a = [i for i in ra["items"] if i["type"] == "ai_overview"]
        if a:
            a = a[0]
            refs = a.get("references") or []
            md = a.get("markdown") or ""
            ai = {"ref_alanlar": [kok(x.get("domain")) for x in refs], "ref_url": [x.get("url") for x in refs],
                  "vitra_ref": any(kok(x.get("domain")) == "vitra.com.tr" for x in refs),
                  "vitra_metin": bool(re.search(r"vitra", md, re.I)),
                  "artema_metin": bool(re.search(r"artema", md, re.I)),
                  "metin_uzun": len(md)}
    h, hk = hacim(kw)
    kayit.append({"kelime": kw, "tema": tema, "hacim": h, "hacim_not": hk,
                  "top10": top, "top20_organik": len(org),
                  "vitra_sira": vit[0]["sira"] if vit else None, "vitra_url": vit[0]["url"] if vit else None,
                  "vitra_tip": vit[0]["tip"] if vit else None, "vitra_sayfa_adet": len(vit),
                  "artema_sira": artema[0]["sira"] if artema else None,
                  "ucuncu_taraf_vitra": [x["url"] for x in vit3],
                  "ai_ilk_cekim": ai_var_ilk, "ai": ai,
                  "paa": paa, "video": vids, "short_video": sv, "local_pack": lp, "images": tur.get("images", 0) > 0,
                  "related": rel, "compare_sites": cs, "knowledge_graph": tur.get("knowledge_graph", 0) > 0,
                  "fiyatli_organik_top10": fiyatli, "ozellik_sayim": dict(tur)})
json.dump(kayit, open(os.path.join(S, "kelime_sonuc.json"), "w"), ensure_ascii=False, indent=1)

N = len(kayit)
tema_n = collections.Counter(k["tema"] for k in kayit)
# ---------- (a) alan adi payi ----------
dom = collections.defaultdict(lambda: {"kw": set(), "toplam": 0, "top3": set(), "sira": [], "tema": collections.Counter(), "tip": collections.Counter()})
for k in kayit:
    en_iyi = {}
    for x in k["top10"]:
        d = dom[x["alan"]]; d["toplam"] += 1; d["tip"][x["tip"]] += 1
        en_iyi[x["alan"]] = min(en_iyi.get(x["alan"], 99), x["sira"])
    for a, s in en_iyi.items():
        d = dom[a]; d["kw"].add(k["kelime"]); d["sira"].append(s); d["tema"][k["tema"]] += 1
        if s <= 3: d["top3"].add(k["kelime"])
tablo = sorted(dom.items(), key=lambda i: (-len(i[1]["kw"]), -len(i[1]["top3"]), statistics.mean(i[1]["sira"])))
# ---------- sayfa turu ----------
tip_top10 = collections.Counter(x["tip"] for k in kayit for x in k["top10"])
tip_tema = {t: collections.Counter(x["tip"] for k in kayit if k["tema"] == t for x in k["top10"]) for t in TEMA_SIRA}
tip_top3 = collections.Counter(x["tip"] for k in kayit for x in k["top10"] if x["sira"] <= 3)

# ---------- ozellikler ----------
def var(k, f):
    if f == "ai_tespit": return k["ai_ilk_cekim"]
    if f == "ai_icerik": return k["ai"] is not None
    if f == "paa": return len(k["paa"]) > 0
    if f == "video": return len(k["video"]) > 0 or len(k["short_video"]) > 0
    if f == "video_blok": return len(k["video"]) > 0
    if f == "local": return len(k["local_pack"]) > 0
    if f == "images": return k["images"]
    if f == "related": return len(k["related"]) > 0
    if f == "compare": return len(k["compare_sites"]) > 0
    if f == "kg": return k["knowledge_graph"]
OZ = [("ai_tespit", "AI Overview (tespit)"), ("ai_icerik", "AI Overview (içerik alındı)"), ("paa", "People Also Ask"), ("video", "Video / Shorts"), ("local", "Local pack"),
      ("images", "Images"), ("related", "Related searches"), ("compare", "Yer siteleri (compare)"), ("kg", "Knowledge panel")]
oz_tema = {f: {t: sum(1 for k in kayit if k["tema"] == t and var(k, f)) for t in TEMA_SIRA} for f, _ in OZ}
oz_top = {f: sum(1 for k in kayit if var(k, f)) for f, _ in OZ}
shop = sum(v for k in kayit for kk, v in k["ozellik_sayim"].items() if kk in ("shopping", "popular_products", "paid", "google_flights"))
# ---------- AI referanslari ----------
ai_alan = collections.Counter(); ai_ref_toplam = 0
for k in kayit:
    if k["ai"]:
        for a in set(k["ai"]["ref_alanlar"]): ai_alan[a] += 1
        ai_ref_toplam += len(k["ai"]["ref_alanlar"])
ai_kw = [k for k in kayit if k["ai"]]
ai_vitra_ref = [k["kelime"] for k in ai_kw if k["ai"]["vitra_ref"]]
ai_vitra_metin = [k["kelime"] for k in ai_kw if k["ai"]["vitra_metin"] and not k["ai"]["vitra_ref"]]
# ---------- video kanallari, local ----------
vk = collections.Counter(); vkw = collections.defaultdict(set)
for k in kayit:
    for v in k["video"]: vk[v["kaynak"]] += 1; vkw[v["kaynak"]].add(k["kelime"])
svk = collections.Counter(a["alan"] for k in kayit for a in k["short_video"])
lp_kw = [k for k in kayit if k["local_pack"]]
# ---------- VitrA ----------
vit_var = [k for k in kayit if k["vitra_sira"]]
vit_yok = [k for k in kayit if not k["vitra_sira"]]
# ---------- pazaryeri ----------
PZ = [("trendyol.com", "Trendyol"), ("hepsiburada.com", "Hepsiburada"), ("koctas.com.tr", "Koçtaş"), ("amazon.com.tr", "Amazon"), ("n11.com", "n11"), ("akakce.com", "akakce"), ("cimri.com", "cimri")]
pz_tema = {a: {t: 0 for t in TEMA_SIRA} for a, _ in PZ}
pz_any = {t: 0 for t in TEMA_SIRA}
pz_slot = 0; slot_toplam = 0
for k in kayit:
    top3 = [x for x in k["top10"] if x["sira"] <= 3]
    slot_toplam += len(top3)
    kume = {x["alan"] for x in top3}
    for a, _ in PZ:
        if a in kume: pz_tema[a][k["tema"]] += 1
    if any(a in kume for a, _ in PZ): pz_any[k["tema"]] += 1
    pz_slot += sum(1 for x in top3 if x["alan"] in {a for a, _ in PZ})
pz_tum = {a: sum(pz_tema[a].values()) for a, _ in PZ}
pz_top1 = collections.Counter(k["top10"][0]["alan"] for k in kayit if k["top10"])

ozet = dict(N=N, tema_n=tema_n, oz_top=oz_top, oz_tema=oz_tema, shop=shop, ai_alan=ai_alan.most_common(15), ai_ref_toplam=ai_ref_toplam,
            ai_kw=len(ai_kw), ai_vitra_ref=ai_vitra_ref, ai_vitra_metin=ai_vitra_metin, tip_top10=tip_top10, tip_top3=tip_top3,
            vit_top3=sum(1 for k in vit_var if k["vitra_sira"] <= 3), vit_top10=sum(1 for k in vit_var if k["vitra_sira"] <= 10),
            vit_top20=len(vit_var), pz_any=pz_any, pz_tum=pz_tum, pz_slot=pz_slot, slot_toplam=slot_toplam, pz_top1=pz_top1.most_common(8),
            video_kanal=vk.most_common(12), short_alan=svk.most_common(6), lp_kw=len(lp_kw))
json.dump(ozet, open(os.path.join(S, "ozet_veri.json"), "w"), ensure_ascii=False, indent=1, default=lambda o: dict(o) if isinstance(o, collections.Counter) else list(o))

# ---------- maliyet ----------
def _c(f): return json.load(open(f)).get("cost", 0)
ilk_set = {os.path.basename(f) for f in glob.glob(os.path.join(S, "ham_ilk", "*.json"))}
c_ham = sum(_c(f) for f in glob.glob(os.path.join(S, "ham", "*.json")) if os.path.basename(f) not in ilk_set)
c_ilk = sum(_c(f) for f in glob.glob(os.path.join(S, "ham_ilk", "*.json")))
c_tek = sum(_c(f) for f in glob.glob(os.path.join(S, "ham_tekrar", "*.json")))
c_ai = sum(_c(f) for f in glob.glob(os.path.join(S, "ham_ai", "*.json")))
KAYIP = 0.0035 + 0.0195 + 0.0055 + 0.007   # ilk toplu istek denemesi (reddedildi), test cekimleri, dogrulama cekimleri; ham dosyalari saklanmadi
maliyet = c_ham + c_ilk + c_tek + c_ai
n_tekrar = len(ilk_set); n_ai = len(glob.glob(os.path.join(S, "ham_ai", "*.json")))

# ================= ozet.md =================
VB = sum(1 for k in kayit if k['video'])
def yz(n, d): return "%%%d" % round(100 * n / d) if d else "-"
def fmt(n): return "{:,}".format(n).replace(",", ".")
def kisa(u, n=70):
    u = re.sub(r"\?.*$", "", u or "")
    return u if len(u) <= n else u[:n - 1] + "…"
def hucre(u):
    return "`" + kisa(u, 68) + "`" if u else "-"
L = []
w = L.append
w("# Google TR mobil SERP analizi: kategori kelimeleri\n")
w("Kaynak: Google TR mobil SERP · DataForSEO · 29.09.2026  ")
w("Kapsam: %d kelime · Türkiye (location_code 2792) · dil tr · mobil Android · depth 20 (ilk 20 organik sonuç) · ilk 10 = organik `rank_group` 1-10  " % N)
w("Tahmini maliyet: **$%.2f** (yanıtlardaki cost alanlarının toplamı: ilk çekim ve yeniden denemeler $%.3f, AI Overview asenkron çekim $%.3f, saklanmayan test ve doğrulama çekimleri $%.3f)." % (maliyet + KAYIP, c_ham + c_ilk + c_tek, c_ai, KAYIP))
w("\n**Yöntem notları**\n")
w("- DataForSEO canlı (live/advanced) uç noktası istek başına tek görev kabul ettiğinden her kelime ayrı istekle çekilmiştir; ham yanıtlar `ham/` altındadır.")
w("- Kesik dönen SERP'ler: %d kelimede ilk çekim ilk 20 yerine 13'ten az organik sonuç döndürmüştür (örn. `vitra klozet` ilk çekimde 7 organik sonuç, VitrA görünmüyor; yeniden çekimde 18 organik sonuç, VitrA 1. sıra). Bu kelimeler en fazla 3 kez yeniden çekilmiş, en çok organik sonuç dönen yanıt analize alınmıştır (ilk yanıtlar `ham_ilk/`, denemeler `ham_tekrar/`). Google SERP'i çekimler arasında değişebildiğinden sıralamalar tek gözlem olarak okunmalıdır." % n_tekrar)
w("- AI Overview bloğu %d kelimede görülmüş, içerik asenkron yüklendiği için bu kelimeler `load_async_ai_overview` ile yeniden çekilmiştir (`ham_ai/`). Yeniden çekimde %d kelimede blok içeriği ve referanslar alınabilmiştir; %d kelimede blok bu çekimde görünmemiştir. AI Overview analizleri bu %d kelime üzerindedir." % (oz_top["ai_tespit"], len(ai_kw), oz_top["ai_tespit"] - len(ai_kw), len(ai_kw)))
w("- Alan adları kök alan adına indirilmiştir (www ve alt alan adları birleştirildi; `shop.creavit.com.tr` = `creavit.com.tr`). VitrA = `vitra.com.tr`; `artema.com.tr` ayrı satırda izlenmiştir.")
w("- Aynı alan adı bir SERP'te birden çok URL ile görünebilir; \"kelime sayısı\" alan adının ilk 10'da yer aldığı kelime adedidir, \"ort. sıra\" ise alan adının o kelimelerdeki en iyi sırasının ortalamasıdır.")
w("- Sayfa türü URL ve başlık kalıplarına göre otomatik sınıflandırılmıştır (kategori, ürün, blog/rehber, pazaryeri arama/liste, pazaryeri ürün, video, forum/şikayet, sosyal/görsel, hizmet platformu); sınır durumlarında sapma olabilir.")
w("- Hacim değerleri `yeni_kategori.json` içindeki 12 aylık ortalama aylık hacimdir (Keyword Planner); kelime biçimi birebir eşleşmeyenlerde (örn. `banyo dolabı` ile `banyo dolap`) `~` ile en yakın biçim gösterilmiş, eşleşme bulunamayanlarda `-` bırakılmıştır.")
w("- Shopping / popular products / paid blokları bu 109 mobil SERP'in hiçbirinde dönmemiştir (DataForSEO çıktısında yok); ürün listeleme, organik sonuç olarak pazaryeri ve fiyat karşılaştırma sayfalarıyla görünmektedir.")
w("\n{{BULGULAR}}\n")

# ---- (a)
w("## (a) Alan adı payı: ilk 10'da en çok görünen 25 alan adı\n")
w("Tema kolonları alan adının ilk 10'da yer aldığı kelime sayısıdır. Tema büyüklükleri: " + " · ".join("%s %d" % (TEMA_ETIKET[t], tema_n[t]) for t in TEMA_SIRA) + ".\n")
w("| # | Alan adı | Kelime | Pay | Toplam sonuç | İlk 3 | Ort. sıra | " + " | ".join(TEMA_ETIKET[t] for t in TEMA_SIRA) + " |")
w("|---|---|---|---|---|---|---|" + "---|" * len(TEMA_SIRA))
for i, (a, d) in enumerate(tablo[:25], 1):
    w("| %d | %s | %d | %s | %d | %d | %.1f | %s |" % (i, a, len(d["kw"]), yz(len(d["kw"]), N), d["toplam"], len(d["top3"]), statistics.mean(d["sira"]),
                                                   " | ".join(str(d["tema"].get(t, 0) or "-") for t in TEMA_SIRA)))
w("\nNot: `artema.com.tr` ilk 10'da %d kelimede görünmüştür (VitrA ile aynı grup)." % len(dom["artema.com.tr"]["kw"]) if "artema.com.tr" in dom else "")
w("\n**Sayfa türü dağılımı (ilk 10, toplam %d sonuç)**\n" % sum(tip_top10.values()))
tipsira = [t for t, _ in tip_top10.most_common()]
w("| Sayfa türü | İlk 10 adet | Pay | İlk 3 adet | " + " | ".join(TEMA_ETIKET[t] for t in TEMA_SIRA) + " |")
w("|---|---|---|---|" + "---|" * len(TEMA_SIRA))
for t in tipsira:
    w("| %s | %d | %s | %d | %s |" % (t, tip_top10[t], yz(tip_top10[t], sum(tip_top10.values())), tip_top3[t], " | ".join(str(tip_tema[x].get(t, 0) or "-") for x in TEMA_SIRA)))

# ---- (b)
w("\n## (b) VitrA sıralaması\n")
w("VitrA (`vitra.com.tr`) %d kelimede ilk 20'de yer almaktadır: %d kelimede ilk 3, %d kelimede ilk 10. %d kelimede ilk 20'de yer almamaktadır.\n" % (len(vit_var), ozet["vit_top3"], ozet["vit_top10"], len(vit_yok)))
w("| Tema | Kelime | İlk 3 | İlk 10 | İlk 20 | İlk 20'de yok |")
w("|---|---|---|---|---|---|")
for t in TEMA_SIRA:
    ks = [k for k in kayit if k["tema"] == t]
    w("| %s | %d | %d | %d | %d | %d |" % (TEMA_ETIKET[t], len(ks), sum(1 for k in ks if k["vitra_sira"] and k["vitra_sira"] <= 3), sum(1 for k in ks if k["vitra_sira"] and k["vitra_sira"] <= 10),
                                           sum(1 for k in ks if k["vitra_sira"]), sum(1 for k in ks if not k["vitra_sira"])))
w("\n**Sıralanan kelimeler** (tema sırasıyla, sıraya göre)\n")
w("| Tema | Kelime | Aylık hacim | Sıra | Sayfa türü | URL |")
w("|---|---|---|---|---|---|")
for t in TEMA_SIRA:
    for k in sorted([k for k in kayit if k["tema"] == t and k["vitra_sira"]], key=lambda k: k["vitra_sira"]):
        hc = (k["hacim_not"] + fmt(k["hacim"])) if k["hacim"] else "-"
        w("| %s | %s | %s | %d | %s | %s |" % (TEMA_ETIKET[t], k["kelime"], hc, k["vitra_sira"], k["vitra_tip"], hucre(k["vitra_url"])))
w("\n**İlk 20'de VitrA bulunmayan kelimeler** (ilk sıradaki alan adı ile)\n")
w("| Tema | Kelime | Aylık hacim | SERP lideri | Not |")
w("|---|---|---|---|---|")
for t in TEMA_SIRA:
    for k in [k for k in kayit if k["tema"] == t and not k["vitra_sira"]]:
        hc = (k["hacim_not"] + fmt(k["hacim"])) if k["hacim"] else "-"
        lid = k["top10"][0]["alan"] if k["top10"] else "-"
        notlar = []
        if k["artema_sira"]: notlar.append("artema.com.tr %d. sırada" % k["artema_sira"])
        if k["ucuncu_taraf_vitra"]: notlar.append("VitrA ürünü 3. taraf sayfada (%d)" % len(k["ucuncu_taraf_vitra"]))
        w("| %s | %s | %s | %s | %s |" % (TEMA_ETIKET[t], k["kelime"], hc, lid, "; ".join(notlar) or "-"))
v3 = [k for k in kayit if k["ucuncu_taraf_vitra"]]
w("\nÜçüncü taraf alan adlarında VitrA ürününün göründüğü ilk 10 sonuç (URL'de `vitra` geçen): %d kelimede %d sonuç." % (len(v3), sum(len(k["ucuncu_taraf_vitra"]) for k in v3)))
vr = [k for k in kayit if any("vitra" in x.lower() for x in k["related"])]
w("Related searches içinde `vitra` geçen kelime sayısı: %d (%s)." % (len(vr), ", ".join(k["kelime"] for k in vr[:12])))

# ---- (c)
w("\n## (c) SERP özellikleri\n")
w("Hücre: özelliğin göründüğü kelime sayısı (temadaki kelimeye oranı).\n")
w("| Özellik | Toplam | " + " | ".join(TEMA_ETIKET[t] for t in TEMA_SIRA) + " |")
w("|---|---|" + "---|" * len(TEMA_SIRA))
for f, ad_ in OZ:
    w("| %s | %d (%s) | %s |" % (ad_, oz_top[f], yz(oz_top[f], N), " | ".join("%d (%s)" % (oz_tema[f][t], yz(oz_tema[f][t], tema_n[t])) for t in TEMA_SIRA)))
w("| Shopping / popular products / paid | 0 | " + " | ".join("0" for _ in TEMA_SIRA) + " |")
w("\nNot: Images bloğu neredeyse tüm SERP'lerde çıktığından ayırt edici değildir. Video / Shorts satırı video bloğu ve kısa video bloğunu birlikte sayar; yalnız video bloğu %d kelimede görülmüştür." % VB)
w("\n**AI Overview: referans verilen alan adları** (%d kelime, toplam %d referans; hücre: alan adının referans verildiği kelime sayısı)\n" % (len(ai_kw), ai_ref_toplam))
w("| Alan adı | Kelime |")
w("|---|---|")
for a, n in ai_alan.most_common(20): w("| %s | %d |" % (a, n))
w("\n**AI Overview kelime listesi**\n")
w("| Tema | Kelime | Referans sayısı | VitrA |")
w("|---|---|---|---|")
for t in TEMA_SIRA:
    for k in kayit:
        if k["tema"] == t and k["ai"]:
            vd = "referans" if k["ai"]["vitra_ref"] else ("metinde geçiyor" if k["ai"]["vitra_metin"] else "yok")
            w("| %s | %s | %d | %s |" % (TEMA_ETIKET[t], k["kelime"], len(k["ai"]["ref_alanlar"]), vd))
w("\nVitrA %d / %d AI Overview'da referans alan adı olarak yer almaktadır (%s); %d AI Overview'da yalnızca metinde geçmektedir (%s). AI Overview tespit edilen kelimelerin %d'inde blok yeniden çekimde görünmemiştir: %s." % (
    len(ai_vitra_ref), len(ai_kw), ", ".join(ai_vitra_ref), len(ai_vitra_metin), ", ".join(ai_vitra_metin),
    sum(1 for k in kayit if k["ai_ilk_cekim"] and not k["ai"]), ", ".join(k["kelime"] for k in kayit if k["ai_ilk_cekim"] and not k["ai"])))
w("\n**Video blokları**\n")
w("Video bloğu %d kelimede, kısa video (Shorts / Reels) bloğu %d kelimede görülmüştür. Video bloğundaki kaynaklar (kelime sayısı): %s." % (
    VB, sum(1 for k in kayit if k["short_video"]), ", ".join("%s (%d)" % (a, len(vkw[a])) for a, _ in vk.most_common(10))))
w("Kısa video kaynakları (öğe sayısı): %s." % ", ".join("%s (%d)" % (a.replace("www.", ""), n) for a, n in svk.most_common(5)))
w("Video bloğu çıkan kelimeler: %s." % ", ".join(k["kelime"] for k in kayit if k["video"]))
w("\n**Local pack**\n")
w("Local pack %d kelimede görülmüştür; ağırlıklı olarak tesisatçı, sıhhi tesisat malzemesi satıcısı ve banyo mağazası işletmeleridir. Kelimeler: %s." % (len(lp_kw), ", ".join(k["kelime"] for k in lp_kw)))
w("\n**Yer siteleri (compare sites)** karuselinde Sahibinden ve Armut çıkmaktadır: %s." % ", ".join(k["kelime"] for k in kayit if k["compare_sites"]))

# ---- (d)
w("\n## (d) People Also Ask soruları (tema bazında)\n")
tum = [q for k in kayit for q in k["paa"]]
w("%d kelimede PAA bloğu çıkmış; toplam %d soru, %d benzersiz soru. Aşağıdaki liste, sorunun çıktığı kelimeyle birlikte verilmiştir.\n" % (oz_top["paa"], len(tum), len(set(tum))))
for t in TEMA_SIRA:
    w("### %s\n" % TEMA_ETIKET[t])
    seen = collections.OrderedDict()
    for k in kayit:
        if k["tema"] == t:
            for q in k["paa"]: seen.setdefault(q, []).append(k["kelime"])
    if not seen: w("PAA sorusu çıkmamıştır.\n"); continue
    for q, ks in seen.items(): w("- %s _(%s)_" % (q, ", ".join(dict.fromkeys(ks))))
    w("")
# ---- (e)
w("## (e) Pazaryeri ve perakende: ilk 3'ü hangi temalarda tutuyor\n")
w("Hücre: alan adının organik ilk 3'te yer aldığı kelime sayısı (temadaki kelime sayısı parantez içinde). Koçtaş perakende zinciri olmakla birlikte istenen listede yer aldığından aynı tabloda izlenmiştir.\n")
w("| Alan adı | Toplam | " + " | ".join("%s (%d)" % (TEMA_ETIKET[t], tema_n[t]) for t in TEMA_SIRA) + " |")
w("|---|---|" + "---|" * len(TEMA_SIRA))
for a, ad_ in PZ:
    w("| %s | %d (%s) | %s |" % (ad_, pz_tum[a], yz(pz_tum[a], N), " | ".join(str(pz_tema[a][t] or "-") for t in TEMA_SIRA)))
w("| **En az biri (7 alan adı)** | %d (%s) | %s |" % (sum(pz_any.values()), yz(sum(pz_any.values()), N), " | ".join("%d (%s)" % (pz_any[t], yz(pz_any[t], tema_n[t])) for t in TEMA_SIRA)))
w("\nBu 7 alan adı, %d ilk 3 sıralama yuvasının %d'ini (%s) tutmaktadır. 1. sırayı en çok tutan alan adları (kelime sayısı): %s." % (slot_toplam, pz_slot, yz(pz_slot, slot_toplam), ", ".join("%s (%d)" % x for x in pz_top1.most_common(8))))
mt = [k["kelime"] for k in kayit if not any(x["alan"] in {a for a, _ in PZ} for x in k["top10"] if x["sira"] <= 3)]
w("Bu 7 alan adının ilk 3'te hiç görünmediği kelimeler (%d): %s." % (len(mt), ", ".join(mt)))
w("\n## Dosyalar\n")
w("- `ham/*.json`: kelime başına ham DataForSEO yanıtı (%d)" % len(glob.glob(os.path.join(S, "ham", "*.json"))))
w("- `ham_ai/*.json`: AI Overview asenkron yeniden çekim (%d)" % len(glob.glob(os.path.join(S, "ham_ai", "*.json"))))
w("- `kelime_sonuc.json`: kelime bazında işlenmiş sonuç (ilk 10, VitrA, özellikler, PAA, AI Overview referansları)")
w("- `ozet_veri.json`: toplu sayılar")
w("- Üretim: `uretim/serp_kelimeler.py`, `serp_cek.py`, `serp_ai_cek.py`, `serp_analiz.py`")
md = "\n".join(L)
bp = os.path.join(S, "bulgular.md")
md = md.replace("{{BULGULAR}}", open(bp).read() if os.path.exists(bp) else "## (f) Ana bulgular\n\n(taslak)\n")
md = md.replace("—", "-").replace("–", "-")
open(os.path.join(S, "ozet.md"), "w").write(md)
print("ozet.md yazildi", len(md))
