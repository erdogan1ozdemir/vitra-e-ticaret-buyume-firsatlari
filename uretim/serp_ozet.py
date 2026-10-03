# -*- coding: utf-8 -*-
"""Google SERP gozlemi (29.09.2026) ozet istatistikleri: tum bolumler ayni hesaptan beslenir.
Keyword Planner'da hacmi olmayan kelimeler (CIKAN) analizden cikarilir; hacim Keyword Planner'dan dogrudan alinir."""
import json, os, re, collections
import veri

_D = os.path.join(veri.V, "ham", "derin", "serp")
_HAM = json.load(open(os.path.join(_D, "kelime_sonuc.json"), encoding="utf-8"))
KP = json.load(open(os.path.join(_D, "kp_109.json"), encoding="utf-8"))["kelimeler"]   # Google Keyword Planner, Eyl 2025 - Agu 2026
CIKAN = [r["kelime"] for r in _HAM if not (KP.get(r["kelime"]) or {}).get("ort12")]
SK = [dict(r, hacim=KP[r["kelime"]]["ort12"]) for r in _HAM if r["kelime"] not in CIKAN]
N = len(SK)
TEMA_SAY = collections.Counter(r["tema"] for r in SK)
PZ = {"trendyol.com", "hepsiburada.com", "amazon.com.tr", "n11.com", "pttavm.com", "pazarama.com", "ciceksepeti.com", "koctas.com.tr", "ikea.com.tr", "bauhaus.com.tr", "tekzen.com.tr", "akakce.com", "cimri.com"}


def _alan_ozet():
    d10, d3, d1, sira, tema = collections.Counter(), collections.Counter(), collections.Counter(), collections.defaultdict(list), collections.defaultdict(collections.Counter)
    for r in SK:
        enb = {}
        for t in r["top10"]:
            enb[t["alan"]] = min(enb.get(t["alan"], 99), t["sira"])
        for a, s in enb.items():
            d10[a] += 1; sira[a].append(s); tema[a][r["tema"]] += 1
            if s <= 3: d3[a] += 1
            if s == 1: d1[a] += 1
    return d10, d3, d1, sira, tema
D10, D3, D1, SIRA, TEMA_D = _alan_ozet()


def ort_sira(a): return sum(SIRA[a]) / len(SIRA[a]) if SIRA[a] else None


VITRA = {"ilk10": sum(1 for r in SK if r.get("vitra_sira") and r["vitra_sira"] <= 10), "ilk20": sum(1 for r in SK if r.get("vitra_sira")),
         "ilk3": sum(1 for r in SK if r.get("vitra_sira") and r["vitra_sira"] <= 3), "bir": sum(1 for r in SK if r.get("vitra_sira") == 1),
         "artema10": sum(1 for r in SK if r.get("artema_sira") and r["artema_sira"] <= 10)}
AI_GORULEN = [r for r in SK if r.get("ai_ilk_cekim")]
AI_ICERIK = [r for r in SK if r.get("ai")]
AI_VITRA = [r["kelime"] for r in AI_ICERIK if "vitra.com.tr" in (r["ai"].get("ref_alanlar") or [])]
AI_ALAN = collections.Counter(d for r in AI_ICERIK for d in set(r["ai"].get("ref_alanlar") or []))

# ilk 3 yuvalarda pazaryeri ve perakende payi
_T3 = _P3 = 0
for r in SK:
    for z in sorted(r.get("top10") or [], key=lambda z: z["sira"])[:3]:
        _T3 += 1; _P3 += z["alan"] in PZ
ILK3 = {"yuva": _T3, "pz": _P3}
def tema_pz3(tema):
    l = [r for r in SK if r["tema"] == tema]
    return sum(1 for r in l if any(z["alan"] in PZ for z in r["top10"] if z["sira"] <= 3)), len(l)
_TIP = collections.Counter(t["tip"] for r in SK for t in r["top10"]); _TT = sum(_TIP.values())
TIP_PAY = {k: 100 * v / _TT for k, v in _TIP.items()}

# SERP ozellikleri
OZELLIK = {"ai": lambda r: bool(r.get("ai_ilk_cekim")), "paa": lambda r: bool(r.get("paa")), "video": lambda r: bool(r.get("video") or r.get("short_video")),
           "yerel": lambda r: bool(r.get("local_pack")), "ilan": lambda r: bool(r.get("compare_sites"))}
def ozellik(k):
    f = OZELLIK[k]; l = [r for r in SK if f(r)]
    tema = collections.Counter(r["tema"] for r in l)
    return len(l), tema
PAA_SORU = sorted({q for r in SK for q in (r.get("paa") or [])})
PAA_KELIME = sum(1 for r in SK if r.get("paa"))
_FIYAT = re.compile(r"kaç tl|kaç lira|ne kadar|fiyat|ücret|kaça", re.I)
_BILGI = re.compile(r"nedir|nasıl|ne demek|ne işe", re.I)
PAA_OZ = {"soru": len(PAA_SORU), "fiyat": sum(1 for q in PAA_SORU if _FIYAT.search(q)), "bilgi": sum(1 for q in PAA_SORU if _BILGI.search(q)),
          "vitra": sum(1 for q in PAA_SORU if "vitra" in q.lower())}
