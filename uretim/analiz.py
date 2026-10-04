# -*- coding: utf-8 -*-
"""Rapor bolumlerinin kullandigi turetilmis sayilar -> veri/islenmis/analiz.json"""
import re, json, re, os
from collections import defaultdict, Counter
import veri
O = {}
A25 = ["2025-%02d"%m for m in range(1,9)]; A26 = ["2026-%02d"%m for m in range(1,9)]
K = veri.KELIME
# --- 1. kategori talebi ---
def top(rows, key):
    d = defaultdict(lambda: [0.0,0.0,0,0.0])
    for r in rows:
        d[key(r)][0]+=r["a25"]; d[key(r)][1]+=r["a26"]; d[key(r)][2]+=1; d[key(r)][3]+=r["hacim"]
    return {k: {"a25": v[0], "a26": v[1], "n": v[2], "hacim": v[3], "yoy": (v[1]/v[0]-1)*100 if v[0] else None} for k,v in d.items()}
O["k1"] = top(K, lambda r: r["k1"]); O["k2"] = top(K, lambda r: r["k1"]+"|"+r["k2"])
O["toplam"] = {"a25": sum(r["a25"] for r in K), "a26": sum(r["a26"] for r in K), "n": len(K)}
ay = defaultdict(lambda: defaultdict(float))
for r in K:
    for m,v in r["seri"].items():
        if v is not None: ay[r["k1"]][m]+=v; ay["Toplam"][m]+=v
O["aylik_k1"] = {k: [round(ay[k].get(m,0)) for m in veri.AYLAR] for k in ay}
O["niyet"] = top([r for r in K if not r["markali"]], lambda r: r["niyet"])
O["niyet_k1"] = top([r for r in K if not r["markali"]], lambda r: r["k1"]+"|"+r["niyet"])
# en buyuk kelimeler niyet bazinda
O["niyet_ornek"] = {}
for n in set(r["niyet"] for r in K):
    O["niyet_ornek"][n] = [(r["kw"], round(r["a26"])) for r in sorted([r for r in K if r["niyet"]==n and not r["markali"]], key=lambda r:-r["a26"])[:8]]
O["k2_yukselen"] = sorted([(k, v["a26"], v["yoy"]) for k,v in O["k2"].items() if v["a25"]>=3000 and v["yoy"] is not None], key=lambda t:-t[2])[:12]
O["k2_dusen"] = sorted([(k, v["a26"], v["yoy"]) for k,v in O["k2"].items() if v["a25"]>=3000 and v["yoy"] is not None], key=lambda t:t[2])[:12]
O["kw_top"] = [(r["kw"], r["k1"], round(r["a26"]), round((r["a26"]/r["a25"]-1)*100,1) if r["a25"] else None) for r in sorted(K, key=lambda r:-r["a26"])[:25]]
# --- 2. GSC (2. çekim, 04.10.2026: toplamlar 1 Eki 2025 - 30 Eyl 2026; sayfa türü ve kategori 1 Oca - 30 Eyl 2026) ---
G2 = veri.J("islenmis", "gsc2.json")
O["gsc_aylar"] = sorted(G2["ay"])
O["gsc_ay_toplam"] = G2["ay"]
O["gsc_tur"] = G2["tur"]; O["gsc_kat"] = G2["kat2"]
O["gsc_cihaz"] = G2["cihaz"]
O["gsc_ulke"] = [tuple(r) for r in G2["ulke"]]
so = veri.J("ham", "gsc2", "sorgu_12ay.json")
from niyet_kurallari import NIY, niyet
qs = defaultdict(lambda:[0,0,0]); ex = defaultdict(list)
brand = [0,0]
for r in so:
    q = r["keys"][0]; m = "vitra" in q or "artema" in q
    brand[0 if m else 1] += r["clicks"]
    key = ("Markalı · " if m else "Markasız · ") + niyet(q)
    qs[key][0]+=r["clicks"]; qs[key][1]+=r["impressions"]; qs[key][2]+=1
    if len(ex[key])<6: ex[key].append((q, r["clicks"]))
O["gsc_sorgu_niyet"] = {k: v for k,v in sorted(qs.items(), key=lambda x:-x[1][0])}; O["gsc_sorgu_ornek"] = dict(ex)
O["gsc_marka"] = {"markali": brand[0], "markasiz": brand[1], "toplam_sorgu": sum(r["clicks"] for r in so)}
O["gsc_top_sorgu"] = [(r["keys"][0], r["clicks"], r["impressions"], round(r["ctr"]*100,1), round(r["position"],1)) for r in so[:30]]
# --- 3. autocomplete ---
ac = veri.AY["autocomplete"]
O["auto"] = {k: [s for s in v if not s.startswith("vitray")] for k,v in ac.items()}
tema = Counter()
for k,v in ac.items():
    for s in v:
        if s.startswith("vitray"): continue
        tema[niyet(s)] += 1
O["auto_tema"] = dict(tema)
# --- 4. youtube ---
yt = veri.AY["youtube"]
O["yt"] = {}
kanal_c = Counter(); kanal_v = Counter(); vitra_rank = {}; _gor = set()
def _vid(u): return re.sub(r"[&?]pp=[^&]*", "", u or "")   # aramaya ozgu ek: ayni video tek sayilir
VKANAL = ("VitrA Türkiye", "VitrA Bathrooms")   # resmi marka kanallari; bayi ve servis kanallari haric
for q, vids in yt.items():
    v3 = [(v["baslik"], v["kanal"], v["goruntulenme"], v["url"], v["yayin"], v["sira"]) for v in vids[:5]]
    O["yt"][q] = {"n": len(vids), "top": v3, "toplam_g": sum(v["goruntulenme"] or 0 for v in vids), "vitra": [i_ + 1 for i_, v in enumerate(vids) if v["kanal"] in VKANAL],
                  "vid": sorted({_vid(v["url"]) for v in vids}), "g": {_vid(v["url"]): v["goruntulenme"] or 0 for v in vids}}
    for v in vids:
        if _vid(v["url"]) in _gor: continue
        _gor.add(_vid(v["url"])); kanal_c[v["kanal"]]+=1; kanal_v[v["kanal"]]+= v["goruntulenme"] or 0
O["yt_kanal"] = [(k, kanal_c[k], kanal_v[k]) for k,_ in kanal_c.most_common(15)]
# --- 5. EVDS ---
E = veri.EVDS; kh = E["kart_harcama_aylik_mnTL"]
def s8(y, k): return sum(kh["%d-%02d"%(y,m)][k] for m in range(1,9))
O["kart"] = {k: {"y25": s8(2025,k), "y26": s8(2026,k), "yoy": (s8(2026,k)/s8(2025,k)-1)*100} for k in ("toplam","mobilya_dekorasyon","yapi_malzemeleri","internet","elektronik","market_avm")}
O["kart_aylik"] = {k: [round(kh[m][k]) for m in veri.AYLAR] for k in ("toplam","mobilya_dekorasyon","yapi_malzemeleri","internet")}
koe = E["kartli_odeme_endeksi"]; ks = sorted(koe, key=lambda t:(int(t.split("-")[0]),int(t.split("-")[1])))
O["koe"] = {t: koe[t] for t in ks[-26:]}
te = E["tuketici_egilim"]; ts = sorted(te, key=lambda t:(int(t.split("-")[0]),int(t.split("-")[1])))
O["tuketici"] = {t: te[t] for t in ts[-26:]}
O["konut"] = E["konut_satis"]; O["banka"] = E["banka_kredi_egilim"]; O["hane"] = E["hanehalki_beklenti"]; O["kfe"] = E["konut_fiyat"]
json.dump(O, open(os.path.join(veri.V,"islenmis","analiz.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=0, default=str)
# ozet cikti
print("TOPLAM", O["toplam"])
for k,v in sorted(O["k1"].items(), key=lambda x:-x[1]["a26"]): print(f"{k:24} {v['a25']:9.0f} {v['a26']:9.0f} {v['yoy']:+.1f}% n={v['n']}")
print("\nYUKSELEN"); [print(f"  {k:55} {a:8.0f} {y:+.1f}%") for k,a,y in O["k2_yukselen"]]
print("DUSEN"); [print(f"  {k:55} {a:8.0f} {y:+.1f}%") for k,a,y in O["k2_dusen"]]
print("\nKW TOP"); [print("  ", t) for t in O["kw_top"][:15]]
print("\nNIYET"); [print(f"  {k:26} {v['a25']:9.0f} {v['a26']:9.0f} {v['yoy']:+.1f}% n={v['n']}") for k,v in sorted(O["niyet"].items(), key=lambda x:-x[1]["a26"])]
for n,l in O["niyet_ornek"].items(): print("   ", n, l[:5])
print("\nGSC cihaz", O["gsc_cihaz"]); print("GSC ulke", O["gsc_ulke"]); print("GSC marka", O["gsc_marka"])
print("GSC ay toplam"); [print("  ", m, v) for m,v in O["gsc_ay_toplam"].items()]
print("GSC sorgu niyet"); [print(f"  {k:28} {v}") for k,v in O["gsc_sorgu_niyet"].items()]
for k,v in O["gsc_sorgu_ornek"].items(): print("   ", k, v[:4])
print("\nAUTO tema", O["auto_tema"])
for k in ["vitra","vitra klozet","vitra lavabo","vitra banyo dolabı","vitra gömme rezervuar","vitra batarya","vitra akıllı klozet"]: print("  ", k, O["auto"].get(k))
print("\nYT"); [print(f"  {q:38} n={v['n']:2} g={v['toplam_g']:9} vitra={v['vitra']}  1:{v['top'][0][1]} {v['top'][0][2]}") for q,v in O["yt"].items()]
print("YT kanal", O["yt_kanal"][:10])
print("\nKART", {k: round(v["yoy"],1) for k,v in O["kart"].items()})
print("KOE son", list(O["koe"].items())[-4:]); print("TUK son", list(O["tuketici"].items())[-2:])
