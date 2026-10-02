# -*- coding: utf-8 -*-
"""Kelime setini ihtiyaç diline (niyet) ayirir; kategori x niyet x yil tablosu."""
import json, os, re
from collections import defaultdict
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(P, "veri/kaynak/sezon_dashboard.js"), encoding="utf-8").read(); d = json.loads(s[s.index("{"):s.rindex("}")+1])
kp = json.load(open(os.path.join(P, "veri/ham/kp_sezon_2024-09_2026-08.json")))["kelimeler"]
import aykiri; kp = {k_: (dict(v_, seri=aykiri.seri(k_, v_.get("seri"))) if isinstance(v_, dict) else v_) for k_, v_ in kp.items()}   # Dunya Kupasi 2026 'wc' duzeltmesi
kat = {k["kw"].strip().lower(): (k["k1"], k["k2"], k["k3"]) for k in d["keywords"]}
MARKA = r"vitra|artema|creavit|kale|ece\b|serel|duravit|geberit|grohe|hansgrohe|roca|ideal standard|bien|kütahya|kutahya|çanakkale|canakkale|ege seramik|yurtbay|turkuaz|bocchi|newarc|isvea|toto|eca\b|nsk|ferro|penta|fixet|orka|nemo|dilara|tema\b|koçtaş|koctas|bauhaus|ikea|tekzen|trendyol|hepsiburada|n11|amazon"
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
_ilk = {}; _tekil = []
for r in rows:
    anahtar = tuple(sorted((k_, v_) for k_, v_ in r["seri"].items() if v_ is not None))
    if anahtar and sum(v_ for _, v_ in anahtar) > 0 and anahtar in _ilk:
        _ilk[anahtar].setdefault("varyant", []).append(r["kw"]); continue
    _ilk[anahtar] = r; _tekil.append(r)
print("varyant tekillestirme:", len(rows), "->", len(_tekil))
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
