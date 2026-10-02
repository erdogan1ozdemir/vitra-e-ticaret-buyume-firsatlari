# -*- coding: utf-8 -*-
"""Hepsiburada resmi magaza satis raporu (son 12 ay) -> veri/islenmis/hb_satis.json.
Rapora TL ciro girmez: yalniz adet, pay, ortalama fiyat ve komisyon orani tasinir. Ham dosya repoya kopyalanmaz."""
import openpyxl, json, os, collections, veri
HAM = os.path.join(os.path.dirname(veri.V), "pazaryeri-verileri", "HB", "HB Satış - 1 yıllık.xlsx")
wb = openpyxl.load_workbook(HAM, read_only=True, data_only=True)
R = list(wb.active.iter_rows(values_only=True)); h = R[0]
rows = [dict(zip(h, r)) for r in R[1:] if r[0]]
f = lambda v: float(v or 0)
ad = sum(f(r["Toplam Satis Adedi"]) for r in rows); ci = sum(f(r["Toplam Satis Tutari(₺)"]) for r in rows)
def marka(r): return "Artema" if str(r["Urun Adi"]).strip().lower().startswith("artema") or r["Marka"] == "Artema" else ("Punto" if r["Marka"] == "Punto" else "VitrA")
mk = collections.defaultdict(lambda: [0, 0])
for r in rows: mk[marka(r)][0] += f(r["Toplam Satis Adedi"]); mk[marka(r)][1] += f(r["Toplam Satis Tutari(₺)"])
kt = collections.defaultdict(lambda: [0, 0, 0])
for r in rows:
    k = r["Alt Kategori"] or "Diğer"; kt[k][0] += f(r["Toplam Satis Adedi"]); kt[k][1] += f(r["Toplam Satis Tutari(₺)"]); kt[k][2] += 1
kat = [{"kategori": k, "urun": int(v[2]), "adet": int(v[0]), "adet_pay": 100 * v[0] / ad, "ciro_pay": 100 * v[1] / ci, "ort_fiyat": v[1] / v[0] if v[0] else None}
       for k, v in sorted(kt.items(), key=lambda i: -i[1][1])]
top = sorted(rows, key=lambda r: -f(r["Toplam Satis Adedi"]))[:12]
urun = [{"ad": str(r["Urun Adi"]).strip()[:70], "kod": str(r["SaticiSKU"] or "").strip(), "kategori": r["Alt Kategori"], "adet": int(f(r["Toplam Satis Adedi"])), "ort_fiyat": f(r["Ortalama Satis Fiyatı(₺)"])} for r in top]
kom = collections.Counter(f(r["Komisyon(%)"]) for r in rows)
pareto = sorted((f(r["Toplam Satis Tutari(₺)"]) for r in rows), reverse=True); s_ = 0; c80 = None
for i, v in enumerate(pareto, 1):
    s_ += v
    if c80 is None and s_ >= 0.8 * ci: c80 = i
out = {"donem": "son 12 ay (rapor 02.10.2026)", "urun_satir": len(rows), "adet": int(ad), "ort_fiyat": ci / ad,
       "marka": {k: {"adet_pay": 100 * v[0] / ad, "ciro_pay": 100 * v[1] / ci} for k, v in mk.items()},
       "kategori": kat, "urun_adet": urun, "komisyon": {str(k): n for k, n in kom.most_common()}, "ciro80_urun": c80}
json.dump(out, open(os.path.join(veri.V, "islenmis", "hb_satis.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), int(ad), round(ci / ad), {k: round(v["adet_pay"], 1) for k, v in out["marka"].items()}, c80, kom.most_common(3))
