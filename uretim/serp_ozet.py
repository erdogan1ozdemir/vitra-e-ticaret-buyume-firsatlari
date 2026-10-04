# -*- coding: utf-8 -*-
"""Google SERP gozlemi (04.10.2026, genisletilmis set) ozet istatistikleri: tum bolumler ayni hesaptan beslenir.
Uc grup: A VitrA gami (kategori ve urun aramalari, soru ve hizmet dahil), B yakin kategori firsatlari, C marka ve karsilastirma.
Bas metrikler (N, SK, D10 ...) A grubundan; AI Overview ve PAA tum setten hesaplanir. Hacim Keyword Planner (Eyl 2025 - Agu 2026 ortalamasi)."""
import json, os, re, collections
import veri

_D = os.path.join(veri.V, "ham", "derin", "serp")
_V = json.load(open(os.path.join(_D, "kelime_sonuc_v2.json"), encoding="utf-8"))
TARIH = _V["tarih"]
# Analizden cikarilan kelimeler: mutfak ve genel tezgah aramalari (kelime evreninden de cikarildi) ile niyeti VitrA gami disina kayan
# genel kelimeler (kartus: yazici kartusu; samandira: olta samandirasi; banyo seti / banyo takimi: tekstil takimi)
DISLA = set(json.load(open(os.path.join(veri.V, "islenmis", "kelime_haric.json"), encoding="utf-8"))["kelimeler_markasiz"]) | {"kartuş", "şamandıra", "banyo seti", "banyo takımı"}
DISLANAN = [r["kelime"] for r in _V["kelimeler"] if r["kelime"] in DISLA]
TUM = [r for r in _V["kelimeler"] if r["kelime"] not in DISLA]
CIKAN = json.load(open(os.path.join(_D, "set_v2.json"), encoding="utf-8"))["hacimsiz_cikan"]
GRUP = {g: [r for r in TUM if r["grup"] == g] for g in "ABC"}
SK = GRUP["A"]; N = len(SK); NT = len(TUM)
GRUP_AD = {"A": ("VitrA gamı", "VitrA range"), "B": ("Yakın kategori fırsatları", "Adjacent category opportunities"), "C": ("Marka ve karşılaştırma", "Brand and comparison")}
KP = {r["kelime"]: {"ort12": r["hacim"]} for r in TUM}
TEMA_SAY = collections.Counter(r["tema"] for r in SK)
PZ = {"trendyol.com", "hepsiburada.com", "amazon.com.tr", "n11.com", "pttavm.com", "pazarama.com", "ciceksepeti.com", "koctas.com.tr", "ikea.com.tr", "bauhaus.com.tr", "tekzen.com.tr", "akakce.com", "cimri.com"}


def alan_ozet(L):
    d10, d3, d1, sira, tema = collections.Counter(), collections.Counter(), collections.Counter(), collections.defaultdict(list), collections.defaultdict(collections.Counter)
    for r in L:
        enb = dict(r["alan_med"]) if r.get("alan_med") is not None else {}   # uc gozlemin ortanca sirasi (ilk 10)
        if r.get("alan_med") is None:
            for t in r["top10"]: enb[t["alan"]] = min(enb.get(t["alan"], 99), t["sira"])
        for a, s in enb.items():
            d10[a] += 1; sira[a].append(s); tema[a][r["tema"]] += 1
            if s <= 3: d3[a] += 1
            if s == 1: d1[a] += 1
    return d10, d3, d1, sira, tema
D10, D3, D1, SIRA, TEMA_D = alan_ozet(SK)
def ort_sira(a, sira=None): s = (sira or SIRA)[a]; return sum(s) / len(s) if s else None


def vitra(L):
    h = sum(r["hacim"] or 0 for r in L) or 1
    return {"n": len(L), "ilk10": sum(1 for r in L if (r.get("vitra_sira") or 99) <= 10), "ilk3": sum(1 for r in L if (r.get("vitra_sira") or 99) <= 3),
            "bir": sum(1 for r in L if r.get("vitra_sira") == 1), "ilk20": sum(1 for r in L if r.get("vitra_sira")),
            "artema10": sum(1 for r in L if (r.get("artema_sira") or 99) <= 10),
            "hacim10": 100 * sum(r["hacim"] or 0 for r in L if (r.get("vitra_sira") or 99) <= 10) / h,
            "hacim3": 100 * sum(r["hacim"] or 0 for r in L if (r.get("vitra_sira") or 99) <= 3) / h,
            "gsc10": sum(1 for r in L if r.get("gsc") and r["gsc"]["sira"] <= 10), "hacim": h}
VITRA = vitra(SK)
# AI Overview (tum set)
AI_GORULEN = [r for r in TUM if r.get("ai_ilk_cekim")]
AI_ICERIK = [r for r in TUM if r.get("ai")]
AI_VITRA = [r["kelime"] for r in AI_ICERIK if "vitra.com.tr" in (r["ai"].get("ref_alanlar") or [])]
AI_ALAN = collections.Counter(d for r in AI_ICERIK for d in set(r["ai"].get("ref_alanlar") or []))
def ai_grup(g):
    L = GRUP[g]; return {"n": len(L), "gorulen": sum(1 for r in L if r.get("ai_ilk_cekim")), "icerik": sum(1 for r in L if r.get("ai")),
                         "vitra": sum(1 for r in L if r.get("ai") and "vitra.com.tr" in (r["ai"].get("ref_alanlar") or []))}
# ilk 3 yuvalarda pazaryeri ve perakende payi (A grubu)
_T3 = _P3 = 0
for r in SK:
    for z in sorted(r.get("top10") or [], key=lambda z: z["sira"])[:3]:
        _T3 += 1; _P3 += z["alan"] in PZ
ILK3 = {"yuva": _T3, "pz": _P3}
def tema_pz3(tema, L=None):
    l = [r for r in (L or SK) if r["tema"] == tema]
    return sum(1 for r in l if any(z["alan"] in PZ for z in r["top10"] if z["sira"] <= 3)), len(l)
def tip_pay(L):
    c = collections.Counter(t["tip"] for r in L for t in r["top10"]); t_ = sum(c.values()) or 1
    return {k: 100 * v / t_ for k, v in c.items()}
TIP_PAY = tip_pay(SK)
# SERP ozellikleri
OZELLIK = {"ai": lambda r: bool(r.get("ai_ilk_cekim")), "paa": lambda r: bool(r.get("paa")), "video": lambda r: bool(r.get("video") or r.get("short_video")),
           "yerel": lambda r: bool(r.get("local_pack")), "ilan": lambda r: bool(r.get("compare_sites"))}
def ozellik(k, L=None):
    f = OZELLIK[k]; l = [r for r in (L if L is not None else SK) if f(r)]
    return len(l), collections.Counter(r["tema"] for r in l)
PAA_SORU = sorted({q for r in TUM for q in (r.get("paa") or [])})
PAA_KELIME = sum(1 for r in TUM if r.get("paa"))
_FIYAT = re.compile(r"kaç tl|kaç lira|ne kadar|fiyat|ücret|kaça", re.I)
_BILGI = re.compile(r"nedir|nasıl|ne demek|ne işe", re.I)
PAA_OZ = {"soru": len(PAA_SORU), "fiyat": sum(1 for q in PAA_SORU if _FIYAT.search(q)), "bilgi": sum(1 for q in PAA_SORU if _BILGI.search(q)),
          "vitra": sum(1 for q in PAA_SORU if "vitra" in q.lower())}
