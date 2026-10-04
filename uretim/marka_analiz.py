# -*- coding: utf-8 -*-
"""Marka aramaları: yalın marka adı ve marka + kategori aramaları (Keyword Planner, Eyl 2022 - Ağu 2026).
Girdi: veri/ham/marka_kelime/{vitra_liste,rakip_liste,marka_yalin}.json · Çıktı: veri/islenmis/marka_kategori.json
Yakın varyantlar (aynı aylık seri) marka ve kategori içinde tek sayılır. Dönemler: yıllık ortalama 2023-2025, Oca-Ağu ortalaması 2023-2026."""
import json, os, re, collections
import marka_kok as MK
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(a): return json.load(open(os.path.join(P, "veri/ham/marka_kelime", a + ".json"), encoding="utf-8"))["kelimeler"]
V, R, Y = J("vitra_liste"), J("rakip_liste"), J("marka_yalin")
MARKA = [("vitra", "VitrA"), ("artema", "Artema"), ("kale", "Kale"), ("creavit", "Creavit"), ("eca", "E.C.A."), ("serel", "Serel"), ("turkuaz", "Turkuaz"),
         ("duravit", "Duravit"), ("ideal standard", "Ideal Standard"), ("isvea", "Isvea"), ("geberit", "Geberit"), ("grohe", "Grohe"), ("hansgrohe", "Hansgrohe"),
         ("bocchi", "Bocchi"), ("visam", "Visam"), ("newarc", "Newarc"), ("roca", "Roca"), ("orka", "Orka"), ("idevit", "Idevit"), ("durul", "Durul"),
         ("kalebodur", "Kalebodur"), ("seranit", "Seranit"), ("ege seramik", "Ege Seramik"), ("çanakkale seramik", "Çanakkale Seramik"), ("yurtbay", "Yurtbay"), ("kütahya seramik", "Kütahya Seramik")]
def ay(y, m1=1, m2=12): return ["%d-%02d" % (y, m) for m in range(m1, m2 + 1)]
def ort(seri, aylar):
    v = [seri.get(a) for a in aylar if seri.get(a) is not None]; return sum(v) / len(v) if v else 0
PEN = {"y2023": ay(2023), "y2024": ay(2024), "y2025": ay(2025), "o2023": ay(2023, 1, 8), "o2024": ay(2024, 1, 8), "o2025": ay(2025, 1, 8), "o2026": ay(2026, 1, 8)}
AYLAR = ["%d-%02d" % (y, m) for y in (2022, 2023, 2024, 2025, 2026) for m in range(1, 13) if "2022-09" <= "%d-%02d" % (y, m) <= "2026-08"]
satir = []
for marka, ad in MARKA:
    kaynak = V if marka == "vitra" else R
    gor = set()
    for kw, v in sorted(kaynak.items(), key=lambda i: -(i[1]["hacim"] or 0)):
        if not kw.startswith(marka + " ") or not v["hacim"]: continue
        if marka == "kale" and kw.startswith("kalebodur"): continue
        kok = kw[len(marka) + 1:]
        if kok.startswith("vitra") or not kok: continue
        if kok == "seramik": continue   # "kale seramik", "yurtbay seramik": şirket adı araması; yalın marka tablosunda yer alır
        k1 = MK.kategori(kok)
        if not k1: continue
        anahtar = (k1, tuple(v["seri"].get(a) for a in AYLAR))
        if anahtar in gor: continue
        gor.add(anahtar)
        satir.append({"marka": ad, "kw": kw, "kok": kok, "k1": k1, "hacim": v["hacim"], "seri": [v["seri"].get(a) for a in AYLAR], **{p: ort(v["seri"], a) for p, a in PEN.items()}})
def topla(L):
    t = {p: sum(r[p] for r in L) for p in PEN}; t["n"] = len(L)
    t["seri"] = [sum((r["seri"][i] or 0) for r in L) for i in range(len(AYLAR))]
    t["yoy"] = (t["o2026"] / t["o2025"] - 1) * 100 if t["o2025"] else None
    t["uc"] = (t["o2026"] / t["o2023"] - 1) * 100 if t["o2023"] else None
    t["y2524"] = (t["y2025"] / t["y2024"] - 1) * 100 if t["y2024"] else None
    return t
O = {"aylar": AYLAR, "marka": {}, "marka_k1": {}, "k1": {}}
for _, ad in MARKA:
    L = [r for r in satir if r["marka"] == ad]
    if L: O["marka"][ad] = topla(L)
    for k1 in sorted({r["k1"] for r in L}):
        O["marka_k1"]["%s|%s" % (ad, k1)] = topla([r for r in L if r["k1"] == k1])
for k1 in sorted({r["k1"] for r in satir}):
    O["k1"][k1] = topla([r for r in satir if r["k1"] == k1])
# VitrA aramalarının en büyükleri ve ihtiyaç sınıfı (kelime evreni kuralları)
import importlib.util as _iu
from niyet_kurallari import niyet as _niyet
O["vitra_kw"] = [{"kw": r["kw"], "k1": r["k1"], "niyet": _niyet(r["kok"]), "o2026": r["o2026"], "o2025": r["o2025"], "o2023": r["o2023"], "hacim": r["hacim"]} for r in sorted([r for r in satir if r["marka"] == "VitrA"], key=lambda r: -r["o2026"])]
vn = collections.defaultdict(lambda: [0, 0, 0, 0])
for r in [r for r in satir if r["marka"] == "VitrA"]:
    n_ = _niyet(r["kok"]); vn[n_][0] += r["o2026"]; vn[n_][1] += r["o2025"]; vn[n_][2] += r["o2023"]; vn[n_][3] += 1
O["vitra_niyet"] = {k: {"o2026": a, "o2025": b, "o2023": c, "n": d} for k, (a, b, c, d) in vn.items()}
# yalın marka adı aramaları
YAL = {}
for kw, v in Y.items():
    if not v["hacim"]: continue
    YAL[kw] = {"hacim": v["hacim"], "seri": [v["seri"].get(a) for a in AYLAR], **{p: ort(v["seri"], a) for p, a in PEN.items()}}
    t = YAL[kw]; t["yoy"] = (t["o2026"] / t["o2025"] - 1) * 100 if t["o2025"] else None; t["uc"] = (t["o2026"] / t["o2023"] - 1) * 100 if t["o2023"] else None
    t["y2524"] = (t["y2025"] / t["y2024"] - 1) * 100 if t["y2024"] else None
O["yalin"] = YAL
O["satir"] = [{"marka": r["marka"], "kw": r["kw"], "k1": r["k1"], "niyet": _niyet(r["kok"]), "o2026": round(r["o2026"]), "o2025": round(r["o2025"]), "o2023": round(r["o2023"])} for r in satir]
O["kok_sayisi"] = {"vitra": len(V), "rakip_kok": len({kw.split(" ", 1)[1] for kw in R if kw.startswith("artema ")})}
O["kelime_sayisi"] = {"vitra_liste": len(V), "vitra_hacimli": sum(1 for v in V.values() if v["hacim"]), "rakip_liste": len(R), "rakip_hacimli": sum(1 for v in R.values() if v["hacim"]),
                      "tekil_satir": len(satir), "marka": len(MARKA)}
json.dump(O, open(os.path.join(P, "veri/islenmis/marka_kategori.json"), "w", encoding="utf-8"), ensure_ascii=False)
if __name__ == "__main__":
    print("tekil satır", len(satir), O["kelime_sayisi"])
    for ad, t in sorted(O["marka"].items(), key=lambda i: -i[1]["o2026"]):
        print("%-18s n=%4d  o23 %8.0f o25 %8.0f o26 %8.0f  yoy %+6.1f  23'ten %+6.1f  y25/24 %+6.1f" % (ad, t["n"], t["o2023"], t["o2025"], t["o2026"], t["yoy"] or 0, t["uc"] or 0, t["y2524"] or 0))
    print()
    for k, t in sorted(YAL.items(), key=lambda i: -i[1]["o2026"]):
        print("%-22s o23 %9.0f o25 %9.0f o26 %9.0f yoy %+6.1f 23'ten %+6.1f" % (k, t["o2023"], t["o2025"], t["o2026"], t["yoy"] or 0, t["uc"] or 0))
