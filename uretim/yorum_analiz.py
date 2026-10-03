# -*- coding: utf-8 -*-
"""Yorum ve soru-cevap analizi: puan tabanli duygu, tema (pain point / guclu yon), marka ve kategori karsilastirmasi.
Girdi : veri/islenmis/yorum_kayit.json (yorum_hazirla.py)
Cikti : veri/islenmis/yorum_analiz.json"""
import json, os, statistics as st
from collections import Counter, defaultdict
import veri
from yorum_tema import yorum_tema, soru_tema, duygu, YORUM, SORU, YAD, SAD

ESIK_MARKA = 40          # bireysel gosterilecek rakip marka icin asgari metinli yorum
# Sektorun bilinen rakip markalari; ornekte cok satan listelerinden gelen kucuk markalar "Diger markalar" altinda toplanir
ANA = ["Kale", "Creavit", "Serel", "E.C.A.", "Grohe", "Geberit", "Turkuaz", "Turavit", "Visam", "Durul", "TEMA", "Newarc", "Hansgrohe"]
ESIK_GRUP = 25           # urun grubu karsilastirmasinda taraf basina asgari metinli yorum
VG = ("VitrA", "Artema")


def oran(a, b): return round(100 * a / b, 1) if b else None


def main():
    D = json.load(open(os.path.join(veri.V, "islenmis", "yorum_kayit.json"), encoding="utf-8"))
    Y, S = D["yorum"], D["soru"]
    for y in Y:
        y["duygu"] = duygu(y["puan"]); y["tema"] = yorum_tema(y["metin"]) if y["metin"] else []
    for s in S:
        s["tema"] = soru_tema(s["soru"])
    Ym = [y for y in Y if y["metin"]]

    # ---- marka kumeleri
    say = Counter(y["marka"] for y in Ym)
    rakip = [m for m, c in say.most_common() if m in ANA and c >= ESIK_MARKA]
    def kume(m): return m if m in VG or m in rakip else "Diğer markalar"
    for y in Y: y["kume"] = kume(y["marka"])
    for s in S: s["kume"] = kume(s["marka"])
    kumeler = list(VG) + rakip + ["Diğer markalar"]

    def profil(L):
        Lm = [y for y in L if y["metin"]]
        pu = [y["puan"] for y in L if y["puan"] is not None]
        neg = [y for y in Lm if y["duygu"] == "olumsuz"]; poz = [y for y in Lm if y["duygu"] == "olumlu"]
        nt = Counter(t for y in neg for t in y["tema"]); pt = Counter(t for y in poz for t in y["tema"])
        return {"n": len(L), "metinli": len(Lm), "ort_puan": round(st.mean(pu), 2) if pu else None,
                "olumlu": oran(sum(1 for y in L if y["duygu"] == "olumlu"), len(pu)), "notr": oran(sum(1 for y in L if y["duygu"] == "notr"), len(pu)),
                "olumsuz": oran(sum(1 for y in L if y["duygu"] == "olumsuz"), len(pu)),
                "olumsuz_metinli": len(neg), "olumlu_metinli": len(poz),
                "pain": [(t, nt[t], oran(nt[t], len(neg))) for t, _ in nt.most_common()],
                "guclu": [(t, pt[t], oran(pt[t], len(poz))) for t, _ in pt.most_common() if t not in ("satis_sonrasi",)],
                "tema_tum": {t: oran(sum(1 for y in Lm if t in y["tema"]), len(Lm)) for t in YAD},
                "tema_neg": {t: oran(nt[t], len(neg)) for t in YAD},
                "kanal": dict(Counter(y["kanal"] for y in L))}

    marka = {m: profil([y for y in Y if y["kume"] == m]) for m in kumeler}
    for m in kumeler:
        marka[m]["kanal_profil"] = {k: profil([y for y in Y if y["kume"] == m and y["kanal"] == k]) for k in ("Trendyol", "Hepsiburada")}
        marka[m]["markalar"] = Counter(y["marka"] for y in Y if y["kume"] == m).most_common(12) if m == "Diğer markalar" else []
    vg = profil([y for y in Y if y["marka"] in VG]); rk = profil([y for y in Y if y["marka"] not in VG])

    # ---- resmi magaza ve diger saticilar (VitrA + Artema)
    resmi = profil([y for y in Y if y["marka"] in VG and y.get("resmi")])
    diger_sat = profil([y for y in Y if y["marka"] in VG and not y.get("resmi") and y["kanal"] == "Hepsiburada"])
    hb_resmi = profil([y for y in Y if y["marka"] in VG and y.get("resmi") and y["kanal"] == "Hepsiburada"])

    # ---- urun grubu: VitrA grubu ve rakipler
    grup = []
    for g in sorted({y["grup"] for y in Ym}):
        a = [y for y in Y if y["grup"] == g and y["marka"] in VG]; b = [y for y in Y if y["grup"] == g and y["marka"] not in VG]
        pa, pb = profil(a), profil(b)
        if pa["metinli"] >= ESIK_GRUP and pb["metinli"] >= ESIK_GRUP:
            grup.append({"grup": g, "vitra": pa, "rakip": pb})

    # ---- urun bazli: en cok olumsuz yorum alan VitrA/Artema urunleri
    ub = defaultdict(list)
    for y in Y:
        if y["marka"] in VG: ub[(y["marka"], y["urun"])].append(y)
    urunler = []
    for (mk, ad), L in ub.items():
        pr = profil(L)
        if pr["n"] >= 15:
            urunler.append({"marka": mk, "urun": ad, "grup": L[0]["grup"], "url": next((y.get("url") for y in L if y.get("url")), None), **{k: pr[k] for k in ("n", "metinli", "ort_puan", "olumsuz", "pain")}})
    urunler.sort(key=lambda r: (-(r["olumsuz"] or 0), -r["n"]))

    # ---- aylik seyir (VitrA grubu, son 12 ay)
    ay = defaultdict(lambda: [0, 0])
    for y in Y:
        if y["marka"] in VG and y["tarih"] and y["puan"] is not None:
            ay[y["tarih"][:7]][0] += 1; ay[y["tarih"][:7]][1] += y["duygu"] == "olumsuz"

    # ---- soru-cevap
    def sprof(L):
        cev = [s for s in L if s["cevap"]]
        ss = [s["cevap_saat"] for s in cev if s.get("cevap_saat") is not None]
        tc = Counter(t for s in L for t in s["tema"])
        return {"n": len(L), "cevapli": oran(len(cev), len(L)), "medyan_saat": round(st.median(ss), 1) if ss else None,
                "24s_ici": oran(sum(1 for v in ss if v <= 24), len(ss)), "resmi_cevap": oran(sum(1 for s in cev if s.get("resmi")), len(cev)),
                "tema": [(t, c, oran(c, len(L))) for t, c in tc.most_common()]}
    soru = {m: sprof([s for s in S if s["kume"] == m]) for m in kumeler}
    for m in kumeler:
        soru[m]["kanal_profil"] = {k: sprof([s for s in S if s["kume"] == m and s["kanal"] == k]) for k in ("Trendyol", "Hepsiburada")}
    soru_vg, soru_rk = sprof([s for s in S if s["marka"] in VG]), sprof([s for s in S if s["marka"] not in VG])
    cevaplayan = Counter(s["cevaplayan"] for s in S if s["marka"] in VG and s["kanal"] == "Hepsiburada" and s["cevap"]).most_common(10)

    out = {"esik_marka": ESIK_MARKA, "kumeler": kumeler,
           "toplam": {"yorum": len(Y), "metinli": len(Ym), "soru": len(S), "urun": len({(y["kanal"], y["urun_id"]) for y in Y}),
                      "kanal": dict(Counter(y["kanal"] for y in Y)), "soru_kanal": dict(Counter(s["kanal"] for s in S)),
                      "vg_yorum": sum(1 for y in Y if y["marka"] in VG), "rakip_yorum": sum(1 for y in Y if y["marka"] not in VG),
                      "vg_soru": sum(1 for s in S if s["marka"] in VG), "rakip_soru": sum(1 for s in S if s["marka"] not in VG),
                      "donem": [min(y["tarih"] for y in Y if y["tarih"]), max(y["tarih"] for y in Y if y["tarih"])],
                      "son12": oran(sum(1 for y in Y if (y["tarih"] or "") >= "2025-10-01"), len(Y))},
           "marka": marka, "vg": vg, "rakip": rk, "resmi": resmi, "diger_satici": diger_sat, "hb_resmi": hb_resmi, "grup": grup, "urunler": urunler[:25],
           "ay": {k: v for k, v in sorted(ay.items())}, "soru": soru, "soru_vg": soru_vg, "soru_rakip": soru_rk, "cevaplayan_hb": cevaplayan}
    yol = os.path.join(veri.V, "islenmis", "yorum_analiz.json")
    json.dump(out, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # alt sayfa icin kayit duzeyi veri (kisisel veri yok)
    alt = {"yorum": [{k: y.get(k) for k in ("kanal", "marka", "kume", "grup", "urun", "url", "satici", "resmi", "puan", "duygu", "metin", "tarih", "tema")} for y in Y],
           "soru": [{k: s.get(k) for k in ("kanal", "marka", "kume", "grup", "urun", "url", "soru", "tarih", "cevap", "cevaplayan", "resmi", "cevap_saat", "tema")} for s in S]}
    json.dump(alt, open(os.path.join(veri.V, "islenmis", "yorum_alt.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("kaydedildi:", yol, "· kumeler:", kumeler)
    return out


if __name__ == "__main__":
    o = main()
    for m in o["kumeler"]:
        p = o["marka"][m]
        print("%-16s n=%5d met=%5d puan=%s olumsuz=%s pain=%s guclu=%s" % (m, p["n"], p["metinli"], p["ort_puan"], p["olumsuz"],
              [(t, r) for t, _, r in p["pain"][:4]], [(t, r) for t, _, r in p["guclu"][:3]]))
    print("VG", o["vg"]["olumsuz"], [(t, r) for t, _, r in o["vg"]["pain"][:6]])
    print("RK", o["rakip"]["olumsuz"], [(t, r) for t, _, r in o["rakip"]["pain"][:6]])
    print("resmi", o["resmi"]["n"], o["resmi"]["olumsuz"], [(t, r) for t, _, r in o["resmi"]["pain"][:5]])
    print("hb resmi", o["hb_resmi"]["n"], o["hb_resmi"]["olumsuz"])
    print("diger sat", o["diger_satici"]["n"], o["diger_satici"]["olumsuz"], [(t, r) for t, _, r in o["diger_satici"]["pain"][:5]])
    for g in o["grup"]:
        print("grup %-24s VG n=%d olumsuz=%s %s | RK n=%d olumsuz=%s %s" % (g["grup"], g["vitra"]["metinli"], g["vitra"]["olumsuz"], [t for t, _, _ in g["vitra"]["pain"][:3]],
              g["rakip"]["metinli"], g["rakip"]["olumsuz"], [t for t, _, _ in g["rakip"]["pain"][:3]]))
    for m in o["kumeler"]:
        s = o["soru"][m]; print("soru %-16s n=%d cevapli=%s medyan=%s resmi=%s tema=%s" % (m, s["n"], s["cevapli"], s["medyan_saat"], s["resmi_cevap"], [(t, r) for t, _, r in s["tema"][:4]]))
    print(o["cevaplayan_hb"])
