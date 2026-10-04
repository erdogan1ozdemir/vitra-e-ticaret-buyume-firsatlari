# -*- coding: utf-8 -*-
"""SSG ve BM derin talep: 48 aylik cekirdek set (k2/k3) + genisletilmis evrende ozellik (modifier) analizi."""
import json, os, re, collections
import veri
K48 = veri.k48(); _CAN = veri.kanonik()
import aykiri; K48 = {k_: (dict(v_, seri=aykiri.seri(k_, v_.get("seri"))) if isinstance(v_, dict) else v_) for k_, v_ in K48.items()}   # Dunya Kupasi 2026 'wc' duzeltmesi
s = open(os.path.join(veri.V, "kaynak", "sezon_dashboard.js"), encoding="utf-8").read(); d = json.loads(s[s.index("{"):s.rindex("}") + 1])
kat = {k["kw"].strip().lower(): (k["k1"], k["k2"], k["k3"]) for k in d["keywords"]}
for k in json.load(open(os.path.join(veri.V, "kaynak", "ek_kelimeler.json"), encoding="utf-8")): kat[k["kw"]] = (k["k1"], k["k2"], k["k3"])
def ay(y1, m1, y2, m2):
    out = []; y, m = y1, m1
    while (y, m) <= (y2, m2):
        out.append("%04d-%02d" % (y, m)); m += 1
        if m > 12: y, m = y + 1, 1
    return out
AY48 = ay(2022, 9, 2026, 8); P0, P1, P2, P3 = AY48[0:12], AY48[12:24], AY48[24:36], AY48[36:48]
A25, A26 = ay(2025, 1, 2025, 8), ay(2026, 1, 2026, 8)
def ort(s, a):
    v = [s.get(x) for x in a if s.get(x) is not None]; return sum(v) / len(v) if v else 0
SSG = {"Vitrifiyeler", "Rezervuarlar"}; BM = {"Banyo Mobilyaları"}
_HARIC = set(json.load(open(os.path.join(veri.V, "islenmis", "kelime_haric.json"), encoding="utf-8"))["kelimeler"])   # mutfak ve genel tezgah aramalari
# ayni seri tekillestirme (Google Ads birlesik hacim) - k3 duzeyinde
rows = []; gor = set()
for kw, v in sorted(K48.items(), key=lambda i: -(i[1].get("hacim") or 0)):
    if kw not in kat or not v.get("seri") or kw in _HARIC or _CAN.get(kw, kw) in _HARIC: continue
    k1, k2, k3 = kat[kw]; sg = tuple(v["seri"].get(x) for x in AY48)
    if (k3, sg) in gor: continue
    gor.add((k3, sg))
    rows.append({"kw": _CAN.get(kw, kw), "k1": k1, "k2": k2, "k3": k3, "seg": "SSG" if k1 in SSG else ("BM" if k1 in BM else "Diğer"),
                 **{p: ort(v["seri"], a) for p, a in (("p0", P0), ("p1", P1), ("p2", P2), ("p3", P3), ("a25", A25), ("a26", A26))},
                 "seri": [v["seri"].get(x) for x in AY48]})
def top(key):
    t = collections.defaultdict(lambda: {"n": 0, "p0": 0, "p1": 0, "p2": 0, "p3": 0, "a25": 0, "a26": 0, "seri": [0] * 48})
    for r in rows:
        g = t[key(r)]; g["n"] += 1
        for p in ("p0", "p1", "p2", "p3", "a25", "a26"): g[p] += r[p]
        g["seri"] = [a + (b or 0) for a, b in zip(g["seri"], r["seri"])]
    for g in t.values():
        g["yoy"] = (g["a26"] / g["a25"] - 1) * 100 if g["a25"] else None; g["uc"] = (g["p3"] / g["p0"] - 1) * 100 if g["p0"] else None
    return t
O = {"aylar": AY48, "seg": top(lambda r: r["seg"]), "k1": top(lambda r: r["k1"]), "k2": top(lambda r: r["seg"] + "|" + r["k1"] + "|" + r["k2"]),
     "k3": top(lambda r: r["seg"] + "|" + r["k2"] + "|" + r["k3"])}
O["kw_ssgbm"] = [(r["kw"], r["seg"], r["k2"], r["k3"], round(r["p3"]), round((r["a26"] / r["a25"] - 1) * 100, 1) if r["a25"] else None, round((r["p3"] / r["p0"] - 1) * 100, 1) if r["p0"] else None)
                 for r in sorted([r for r in rows if r["seg"] in ("SSG", "BM")], key=lambda r: -r["p3"])]
# --- ozellik analizi (genisletilmis evren, SSG ve BM temalari) ---
YK = json.load(open(os.path.join(veri.V, "islenmis", "yeni_kategori.json"), encoding="utf-8"))
import tema
SSGT = {k for k, m in tema.META.items() if m["grup"] == "SSG"}; BMT = {k for k, m in tema.META.items() if m["grup"] == "BM"}
OZ = [
 ("Tip", [("Asma", r"\basma\b"), ("Yerden / takım", r"yerden|takım klozet|klozet takım|monoblok"), ("Gömme", r"gömme|ankastre"), ("Kanalsız / rimless", r"kanalsız|rimless|rim-ex|rimex"),
          ("Çanak / tezgah üstü", r"çanak|tezgah üstü|tezgahüstü"), ("Etajerli / ayaklı", r"etajer|ayaklı"), ("Köşe", r"köşe"), ("Alaturka", r"alaturka|hela|tuvalet taşı"), ("Lavabolu", r"lavabolu|lavabo dahil|dolaplı lavabo"), ("Aynalı", r"aynalı"), ("Boy / kolon", r"boy dola|kolon")]),
 ("Ölçü", [("Ölçü (cm)", r"\b\d{2,3} ?cm\b|\b\d{2,3}x\d{2,3}\b|\b(40|45|50|55|60|65|70|75|80|85|90|100|120)\b"), ("Ölçüleri / boyut", r"ölçü|boyut|kaç cm")]),
 ("Renk ve malzeme", [("Siyah / antrasit", r"siyah|antrasit|füme|mat siyah"), ("Beyaz", r"beyaz"), ("Ahşap / meşe", r"ahşap|meşe|ceviz|masif"), ("Gri / renkli", r"\bgri\b|renkli|yeşil|mavi|bej|pembe|kahve"), ("Altın / bakır", r"altın|gold|bakır|bronz"),
                      ("PVC / suya dayanıklı", r"pvc|suya dayanıklı|su geçirmez|\bnem"), ("MDF / lake", r"mdf|lake|akrilik|kompakt")]),
 ("Özellik", [("Akıllı / elektronik", r"akıllı|elektronik|sensörlü|fotoselli|temassız"), ("Yavaş kapanan", r"yavaş kapan|amortisör"), ("Işıklı / ledli", r"ışıklı|ledli|led\b|aydınlatma"), ("Çekmeceli / kapaklı", r"çekmece|kapaklı"), ("Duvara tam dayalı", r"duvara (tam )?dayalı")]),
 ("İhtiyaç ve bağlam", [("Küçük / dar banyo", r"küçük|\bdar\b|\bmini\b|kompakt"), ("Modern / tasarım", r"modern|tasarım|lüks|\bşık\b|dekoratif"), ("Engelli / çocuk", r"engelli|çocuk|cocuk|yaşlı"), ("Modeller", r"model"), ("Fiyat", r"fiyat|ucuz|indirim|uygun"), ("Tamir / parça", r"tamir|iç takım|şamandıra|menteşe|yedek|conta|parça")]),
 ("Marka ve kanal", [("VitrA", r"vitra"), ("Rakip marka", r"\b(kale|creavit|serel|ece|eca|bocchi|geberit|grohe|duravit|roca|ideal standard|turkuaz|isvea|visam|artema|seranit|yurtbay|ege seramik|çanakkale)\b"),
                     ("Perakendeci / pazaryeri", r"koçtaş|koctas|ikea|bauhaus|tekzen|trendyol|hepsiburada|n11|amazon|evidea|vivense|\bbim\b|a101|\bşok\b")]),
]
def oz(temalar):
    rr = [r for r in YK["kelime"] if r["tema"] in temalar]
    tot = sum(r["v12"] for r in rr); tot25 = sum(r["a25"] for r in rr); tot26 = sum(r["a26"] for r in rr)
    out = []
    for grp, lst in OZ:
        for ad, rx in lst:
            c = re.compile(rx); m = [r for r in rr if c.search(r["kw"])]
            v = sum(r["v12"] for r in m); a25 = sum(r["a25"] for r in m); a26 = sum(r["a26"] for r in m)
            out.append({"grup": grp, "ad": ad, "n": len(m), "v12": v, "pay": 100 * v / tot if tot else 0, "yoy": (a26 / a25 - 1) * 100 if a25 else None,
                        "ornek": [r["kw"] for r in sorted(m, key=lambda r: -r["v12"])[:5]]})
    return {"toplam": tot, "yoy": (tot26 / tot25 - 1) * 100, "n": len(rr), "ozellik": out}
O["oz_ssg"] = oz(SSGT); O["oz_bm"] = oz(BMT)
json.dump(O, open(os.path.join(veri.V, "islenmis", "ssg_bm.json"), "w", encoding="utf-8"), ensure_ascii=False, default=float)
for sg in ("SSG", "BM"):
    g = O["seg"][sg]; print(f"\n##### {sg}: p0 {g['p0']:.0f} p1 {g['p1']:.0f} p2 {g['p2']:.0f} p3 {g['p3']:.0f}  3y {g['uc']:+.1f}%  yoy {g['yoy']:+.1f}%  n={g['n']}")
    for k, v in sorted([(k, v) for k, v in O["k2"].items() if k.startswith(sg + "|")], key=lambda i: -i[1]["p3"]):
        print(f"  {k.split('|',1)[1]:55} p3 {v['p3']:8.0f}  3y {v['uc'] or 0:+6.1f}%  yoy {v['yoy'] or 0:+6.1f}%  n={v['n']}")
    print("  -- k3")
    for k, v in sorted([(k, v) for k, v in O["k3"].items() if k.startswith(sg + "|")], key=lambda i: -i[1]["p3"])[:40]:
        print(f"    {k.split('|',1)[1]:60} p3 {v['p3']:8.0f}  3y {v['uc'] or 0:+6.1f}%  yoy {v['yoy'] or 0:+6.1f}%")
for sg in ("oz_ssg", "oz_bm"):
    o = O[sg]; print(f"\n##### {sg} toplam {o['toplam']:.0f} yoy {o['yoy']:+.1f}% n={o['n']}")
    for x in o["ozellik"]: print(f"  {x['grup'][:12]:12} {x['ad']:26} pay {x['pay']:5.1f}%  v {x['v12']:8.0f}  yoy {x['yoy'] or 0:+6.1f}%  {x['ornek'][:4]}")
