# -*- coding: utf-8 -*-
"""Genisletilmis evren -> tema tablosu (48 ay). Varyant tekillestirme: ayni aylik seri (Keyword Planner birlesik hacmi) temalar arasi da tek sayilir."""
import json, os, re, collections
import veri, tema, aykiri
U = json.load(open(os.path.join(veri.V, "ham", "kfk_evren.json"), encoding="utf-8"))["kelimeler"]
if True:
    for k, v in veri.k48().items():
        if k not in U and v.get("seri"):
            U[k] = {"grup": ["cekirdek"], "hacim": v["hacim"], "cpc": v["cpc"], "rekabet": v["rekabet"], "seri": v["seri"]}
CEK = {v_ for r in veri.KELIME for v_ in [r["kw"]] + list(r.get("varyant") or [])}; _CAN = veri.kanonik()
def ay(y1, m1, y2, m2):
    out = []; y, m = y1, m1
    while (y, m) <= (y2, m2):
        out.append("%04d-%02d" % (y, m)); m += 1
        if m > 12: y, m = y + 1, 1
    return out
P0, P3 = ay(2022, 9, 2023, 8), ay(2025, 9, 2026, 8)
A25, A26 = ay(2025, 1, 2025, 8), ay(2026, 1, 2026, 8)
def ort(s, a):
    v = [s.get(x) for x in a if s.get(x) is not None]; return sum(v) / len(v) if v else 0
rows = []
for kw, v in U.items():
    s = aykiri.seri(kw, v.get("seri") or {})
    if len(s) < 40: continue
    t = tema.sinif(kw)
    if not t: continue
    rows.append({"kw": _CAN.get(kw, kw), "tema": t, "v12": ort(s, P3), "v0": ort(s, P0), "a25": ort(s, A25), "a26": ort(s, A26), "cpc": v.get("cpc"),
                 "cekirdek": kw in CEK, "imza": tuple(s.get(x) for x in sorted(s))})
# varyant tekillestirme
gor = set(); tek = []
for r in sorted(rows, key=lambda r: (-r["v12"], not r["cekirdek"], -sum(c in "çğıöşü" for c in r["kw"]), r["kw"].count(" ") * 0, -len(r["kw"]) if r["cekirdek"] else len(r["kw"]))):
    if r["imza"] in gor: continue
    gor.add(r["imza"]); tek.append(r)
for r in tek: r.pop("imza")
T = collections.defaultdict(lambda: {"n": 0, "v12": 0, "v0": 0, "a25": 0, "a26": 0, "cek_v12": 0, "top": []})
for r in tek:
    t = T[r["tema"]]; t["n"] += 1
    for k in ("v12", "v0", "a25", "a26"): t[k] += r[k]
    if r["cekirdek"]: t["cek_v12"] += r["v12"]
for k, t in T.items():
    t.update(tema.META[k]); t["yoy"] = (t["a26"] / t["a25"] - 1) * 100 if t["a25"] else None; t["uc_yil"] = (t["v12"] / t["v0"] - 1) * 100 if t["v0"] else None
    t["kapsam"] = 100 * t["cek_v12"] / t["v12"] if t["v12"] else 0
    t["top"] = [(r["kw"], round(r["v12"]), round((r["a26"] / r["a25"] - 1) * 100, 1) if r["a25"] else None) for r in sorted([r for r in tek if r["tema"] == k], key=lambda r: -r["v12"])[:12]]
json.dump({"tema": T, "kelime": tek}, open(os.path.join(veri.V, "islenmis", "yeni_kategori.json"), "w", encoding="utf-8"), ensure_ascii=False, default=float)
print("sınıflanan", len(rows), "tekil", len(tek))
for g in ["SSG", "BM", "Armatür-Duş", "Yıkanma", "Karo", "Aksesuar", "Bitişik", "Hizmet-Set"]:
    print("\n##", g)
    for k, t in sorted([(k, t) for k, t in T.items() if t["grup"] == g], key=lambda i: -i[1]["v12"]):
        print(f"  {t['tr'][:40]:40} {t['durum']:5} n={t['n']:5} v12={t['v12']:9.0f} yoy={t['yoy'] or 0:+6.1f}% 3y={t['uc_yil'] or 0:+7.1f}% kapsam={t['kapsam']:4.0f}%  {[x[0] for x in t['top'][:5]]}")
