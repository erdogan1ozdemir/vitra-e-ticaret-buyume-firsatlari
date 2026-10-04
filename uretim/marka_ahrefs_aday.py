# -*- coding: utf-8 -*-
"""Ahrefs'ten (rakip marka siteleri ve Trendyol, Hepsiburada, Koçtaş) gelen marka + kelime aramalarını süzer; Keyword Planner çekimi için aday listesi yazar.
Kural: marka adı kelime olarak geçmeli. Pazaryeri kaynaklı kelimeler yalnız kök ifadesi banyo kategorisine eşleniyorsa alınır (turkuaz kolye, orka gömlek gibi
marka dışı ürünler elenir). Marka sitesi kaynaklı kelimelerde kategoriye eşlenmeyenler "seri, model ve diğer" olarak tutulur; ısıtma, kilit, hisse gibi
banyo dışı konular elenir."""
import csv, glob, json, os, re
import marka_kok as MK
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(P, "veri/ham/marka_kelime")
from marka_analiz_tanim import MARKA, PAZAR, DISI, marka_bul, kok_cikar
def J(a): return json.load(open(os.path.join(D, a + ".json"), encoding="utf-8"))["kelimeler"]
mevcut = set(J("vitra_liste")) | set(J("rakip_liste")) | set(J("marka_yalin"))
aday = {}; red = {"disi": 0, "pazar_kat_yok": 0, "marka_yok": 0}
for f in sorted(glob.glob(os.path.join(D, "ahrefs", "*.tsv"))):
    dom = os.path.basename(f)[:-4]
    for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="\t"):
        kw = " ".join(r["keyword"].lower().split())
        m = marka_bul(kw)
        if not m: red["marka_yok"] += 1; continue
        if DISI.search(kw): red["disi"] += 1; continue
        kok = kok_cikar(kw, m)
        if dom in PAZAR and not MK.kategori(kok): red["pazar_kat_yok"] += 1; continue
        aday.setdefault(kw, {"marka": m, "kaynak": set()})["kaynak"].add(dom)
yeni = sorted(k for k in aday if k not in mevcut and len(k) <= 80 and len(k.split()) <= 10)
open(os.path.join(P, "veri/kaynak/ahrefs_marka_kelimeler.txt"), "w", encoding="utf-8").write("\n".join(yeni) + "\n")
json.dump({k: {"marka": v["marka"], "kaynak": sorted(v["kaynak"])} for k, v in aday.items()}, open(os.path.join(D, "ahrefs_aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("aday", len(aday), "yeni", len(yeni), "red", red)
