# -*- coding: utf-8 -*-
"""Kelime setini ihtiyaç diline (niyet) ayirir; kategori x niyet x yil tablosu."""
import json, os, re
from collections import defaultdict
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(P, "veri/kaynak/sezon_dashboard.js"), encoding="utf-8").read(); d = json.loads(s[s.index("{"):s.rindex("}")+1])
kp = json.load(open(os.path.join(P, "veri/ham/kp_sezon_2024-09_2026-08.json")))["kelimeler"]
import aykiri; kp = {k_: (dict(v_, seri=aykiri.seri(k_, v_.get("seri"))) if isinstance(v_, dict) else v_) for k_, v_ in kp.items()}   # Dunya Kupasi 2026 'wc' duzeltmesi
kat = {k["kw"].strip().lower(): (k["k1"], k["k2"], k["k3"]) for k in d["keywords"]}
# sezon listesinde bulunmayan kategori bas kelimeleri (04.10.2026): ek liste ve ayri Keyword Planner cekimi
for k in json.load(open(os.path.join(P, "veri/kaynak/ek_kelimeler.json"), encoding="utf-8")):
    kat[k["kw"]] = (k["k1"], k["k2"], k["k3"])
kp.update(json.load(open(os.path.join(P, "veri/ham/kp_ek_2024-09_2026-08.json")))["kelimeler"])
import haric_kural
MARKA = haric_kural.MARKA
NIYET = [
 ("Fiyat", r"fiyat|ucuz|uygun|indirim|kampanya|outlet|kaç para|ne kadar|tl\b"),
 ("Taksit ve ödeme", r"taksit|kredi|ödeme|vade"),
 ("Montaj", r"montaj|nasıl takılır|nasıl yapılır|kurulum|takma|bağlantı|montajı|taktır"),
 ("Tamir ve bakım", r"tamir|arıza|su kaçır|akıtı|tıkan|temizli|değişim|değiştir|onarım|bakım|yedek|iç takım|parça|şamandıra|menteşe|teker|conta|kartuş|damper|amortisör|boşaltma"),
 ("Ölçü ve teknik", r"ölçü|ölçüleri|boyut|cm\b|kaç litre|ağırlık|derinlik|yükseklik|genişlik|montaj ölçü|teknik|çizim"),
 ("Seçim ve karşılaştırma", r"en iyi|hangisi|tavsiye|öneri|yorum|karşılaştır|inceleme|nedir|ne işe|farkı|\bmi\b|\bmı\b|\bmu\b|\bmü\b|nasıl seçilir|kaliteli"),
 ("Tasarım ve fikir", r"dekorasyon|tasarım|fikir|model|modelleri|trend(?!yol)|renk|modern|küçük banyo|dekor"),
 ("Yer ve kanal", r"nereden|satış noktası|bayi|mağaza|showroom|satan|nerede"),
]
def niyet(kw):
    for ad, rx in NIYET:
        if re.search(rx, kw): return ad
    return "Jenerik ürün"
def ort(seri, ays):
    v = [seri.get(a) for a in ays if seri.get(a) is not None]; return sum(v)/len(v) if v else 0
A25 = ["2025-%02d"%m for m in range(1,9)]; A26 = ["2026-%02d"%m for m in range(1,9)]
rows = []
for kw, v in kp.items():
    if kw not in kat or not v["hacim"]: continue
    k1,k2,k3 = kat[kw]; m = bool(re.search(MARKA, kw)); n = niyet(kw)
    rows.append({"kw": kw, "k1": k1, "k2": k2, "k3": k3, "markali": m, "niyet": n, "hacim": v["hacim"], "a25": ort(v["seri"],A25), "a26": ort(v["seri"],A26), "seri": v["seri"], "cpc": v.get("cpc")})
# Keyword Planner yakin varyantlara (cogul, yazim farki) ayni aylik seriyi verir; ayni seri tek kelime sayilir
# Gorunen ad: SERP setinde ya da SEOmonitor takibinde gecen yazim, sonra Turkce karakterli ve tam yazim tercih edilir (banyo batarya -> banyo bataryası)
_TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
import serp_kelimeler as _SKL
_SERPK = {k for k, _ in _SKL.LISTE}
_SEOMV = {k_["keyword"]: (k_.get("search_data") or {}).get("search_volume") or 0 for k_ in json.load(open(os.path.join(P, "veri/ham/seomonitor/kelimeler_2026-10-03.json"), encoding="utf-8"))}
_SEOM = set(_SEOMV)
_ASC = {}
for k_ in _SERPK | _SEOM: _ASC.setdefault(k_.translate(_TR), set()).add(k_)
def _puan(k_): return (k_ in _SERPK, sum(c in "çğıöşü" for c in k_), k_ in _SEOM, _SEOMV.get(k_, 0), -k_.count(" "), len(k_))
_grup = {}; _sira = []
for r in rows:
    anahtar = tuple(sorted((k_, v_) for k_, v_ in r["seri"].items() if v_ is not None))
    if not (anahtar and sum(v_ for _, v_ in anahtar) > 0): anahtar = ("tek", r["kw"])
    if anahtar not in _grup: _grup[anahtar] = []; _sira.append(anahtar)
    _grup[anahtar].append(r)
_tekil = []
for a_ in _sira:
    L = _grup[a_]
    aday = {r["kw"] for r in L} | {t_ for r in L for t_ in _ASC.get(r["kw"].translate(_TR), ())}
    ad = max(aday, key=_puan)
    temel = next((r for r in L if r["kw"] == ad), L[0])
    r = dict(temel, kw=ad)
    var = sorted({x_["kw"] for x_ in L} - {ad})
    if var: r["varyant"] = var
    _tekil.append(r)
print("varyant tekillestirme:", len(rows), "->", len(_tekil))
# "Banyo Tezgahları" altına kaynak listeden gelen mutfak ve genel tezgah aramaları (banyo/lavabo içermeyen, büyük ölçüde mutfak
# tezgahı ve porselen levha talebi) banyo mobilyası evreninden çıkarılır; ayrı tutulup raporun yöntem notunda belirtilir.
# Kaynak kategori listesinde banyo alt kategorisine eşlenmiş, ancak Google sonuçlarında banyo dışı niyete kayan genel ifadeler (04.10.2026 SERP kontrolü,
# veri/ham/derin/serp/genel_kelime_kontrol_2026-10-04.json): mobilya kulpu ve salon konsolu, genel çöp kovası, masa peçeteliği, uygulama ve elektronik
# paneli, doğal taş traverten. Banyo bağlamı taşıyan biçimleri (banyo dolabı kulpu, tuvalet çöp kovası, kumanda paneli) evrende kalır.
import haric_kural
HARIC_GRUP = {g: [] for g in haric_kural.GRUP_AD}
for r in _tekil:
    g = haric_kural.grup(r["kw"], r["k2"], MARKA)
    if g: HARIC_GRUP[g].append(r["kw"])
HARIC_GRUP = {g: sorted(L) for g, L in HARIC_GRUP.items()}
HARIC = sorted({k_ for L in HARIC_GRUP.values() for k_ in L})
# çıkarılan kelimelerin yazım varyantları da (ör. dolap kulpu -> dolap kolu, dolap tutacağı) aynı aylık seriyi taşır; diğer hesaplarda sızmaması için listeye eklenir
HARIC_VAR = sorted({v_ for r in _tekil if r["kw"] in set(HARIC) for v_ in (r.get("varyant") or [])} - set(HARIC))
json.dump({"aciklama": "Kelime evreninden çıkarılan aramalar: mutfak ve genel tezgah, banyo dışı niyete kayan genel ifadeler ve marka adı geçen aramalar",
           "kelimeler": HARIC + HARIC_VAR, "gruplar": HARIC_GRUP, "varyant": HARIC_VAR,
           # SERP setinin C grubu (marka ve karşılaştırma) markalı aramaları bilerek içerdiği için SERP dışlaması yalnız markasız grupları kullanır
           "kelimeler_markasiz": sorted({k_ for g, L in HARIC_GRUP.items() if g != "markali" for k_ in L} | {v_ for r in _tekil if r["kw"] in {k_ for g, L in HARIC_GRUP.items() if g != "markali" for k_ in L} for v_ in (r.get("varyant") or [])}),
           "a26_toplam": sum(r["a26"] for r in _tekil if r["kw"] in HARIC),
           "grup_a26": {g: sum(r["a26"] for r in _tekil if r["kw"] in L) for g, L in HARIC_GRUP.items()}},
          open(os.path.join(P, "veri/islenmis/kelime_haric.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
_tekil = [r for r in _tekil if r["kw"] not in set(HARIC)]
# Türkçe karakter: varyant grubunda karakterli yazımı bulunmayan iki kanonik ad
_AD_TR = {"cocuk klozet": "çocuk klozet", "cocuk klozet kapak": "çocuk klozet kapak"}
for r in _tekil:
    if r["kw"] in _AD_TR: r["varyant"] = sorted(set(r.get("varyant") or []) | {r["kw"]}); r["kw"] = _AD_TR[r["kw"]]
print("dışlama:", {g: len(L) for g, L in HARIC_GRUP.items()}, "->", len(_tekil))
rows = _tekil
json.dump(rows, open(os.path.join(P, "veri/islenmis/kelime_seti.json"), "w", encoding="utf-8"), ensure_ascii=False)
T = defaultdict(lambda: [0,0,0])
for r in rows:
    key = r["niyet"] if not r["markali"] else "Markalı"
    T[key][0]+=r["a25"]; T[key][1]+=r["a26"]; T[key][2]+=1
print("Niyet · Oca-Ağu 2025 → 2026 aylık ortalama toplam · kelime sayısı")
for k,(a,b,n) in sorted(T.items(), key=lambda x:-x[1][1]): print(f"  {k:26} {a:10.0f} -> {b:10.0f}  {100*(b/a-1) if a else 0:+.1f}%  ({n})")
print("\nKategori × niyet (2026 aylık ort.)")
KT = defaultdict(lambda: defaultdict(float))
for r in rows:
    KT[r["k1"]][r["niyet"] if not r["markali"] else "Markalı"] += r["a26"]
cols = ["Jenerik ürün","Tasarım ve fikir","Seçim ve karşılaştırma","Fiyat","Ölçü ve teknik","Montaj","Tamir ve bakım","Taksit ve ödeme","Yer ve kanal","Markalı"]
print("kategori".ljust(22), " ".join(c[:9].rjust(9) for c in cols))
for k in sorted(KT, key=lambda x:-sum(KT[x].values())): print(k.ljust(22), " ".join(f"{KT[k].get(c,0):9.0f}" for c in cols))
print("\nMarkalı kelimeler içinde marka payı (2026)")
M = defaultdict(float)
for r in rows:
    if r["markali"]:
        mm = re.search(MARKA, r["kw"]).group(0); M[mm] += r["a26"]
for k,v in sorted(M.items(), key=lambda x:-x[1])[:15]: print(f"  {k:14} {v:9.0f}")
