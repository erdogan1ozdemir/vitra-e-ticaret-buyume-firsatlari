# -*- coding: utf-8 -*-
"""Kategori, hizmet, fiyat, rakip marka ve perakendeci kok ifadeleri icin Google autocomplete (DataForSEO) -> veri/ham/autocomplete_ek.json"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__)); import dfs, veri
GRUP = {
 "Kategori": ["klozet", "asma klozet", "akıllı klozet", "klozet kapağı", "lavabo", "çanak lavabo", "banyo dolabı", "lavabo dolabı", "gömme rezervuar", "duşakabin", "duş seti", "banyo bataryası", "lavabo bataryası", "havlupan", "banyo aksesuar"],
 "Montaj ve tamir": ["klozet montaj", "banyo dolabı montaj", "klozet tamir", "rezervuar tamiri", "klozet su kaçırıyor", "batarya değişimi", "gömme rezervuar tamiri"],
 "Yenileme ve tasarım": ["banyo yenileme", "banyo tadilat", "banyo tasarım", "küçük banyo", "banyo dekorasyon"],
 "Fiyat ve ödeme": ["klozet taksit", "klozet fiyatları", "banyo dolabı fiyatları", "banyo tadilat fiyatları", "duşakabin fiyatları"],
 "Rakip marka": ["artema", "creavit klozet", "kale klozet", "serel klozet", "turkuaz klozet", "idevit klozet", "duravit klozet", "ideal standard klozet", "isvea klozet", "roca klozet", "geberit gömme rezervuar", "grohe batarya", "eca batarya", "hansgrohe duş seti", "kale banyo dolabı", "orka banyo dolabı"],
 "Perakendeci": ["koçtaş klozet", "bauhaus banyo dolabı", "ikea banyo dolabı", "tekzen klozet", "trendyol banyo dolabı"]}
F = os.path.join(veri.V, "ham", "autocomplete_ek.json")
out = json.load(open(F, encoding="utf-8")) if os.path.exists(F) else {"grup": GRUP, "oneri": {}}
out["grup"] = GRUP
for g, lst in GRUP.items():
    for k in lst:
        if out["oneri"].get(k): continue
        s = []
        for deneme in range(3):
            try:
                r = dfs.post("/v3/serp/google/autocomplete/live/advanced", [{"keyword": k, "location_code": 2792, "language_code": "tr", "client": "chrome", "cursor_pointer": len(k)}])
                res = (r["tasks"][0].get("result") or [{}])[0]
                s = [it.get("suggestion") for it in (res.get("items") or []) if it.get("type") == "autocomplete"]
                if s: break
                time.sleep(2)
            except Exception as e:
                print("hata", k, e); time.sleep(3)
        out["oneri"][k] = [x for x in s if x and x != k][:10]
        print(g, "|", k, len(out["oneri"][k]))
json.dump(out, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# hacim: kok + oneriler, mevcut hacim dosyasina ekle
H = os.path.join(veri.V, "ham", "autocomplete_hacim.json"); hd = json.load(open(H, encoding="utf-8"))
yeni = sorted({k for lst in GRUP.values() for k in lst} | {s for v in out["oneri"].values() for s in v})
yeni = [k for k in yeni if k not in hd["kelime"] and len(k) <= 80]
for i in range(0, len(yeni), 700):
    r = dfs.post("/v3/keywords_data/google_ads/search_volume/live", [{"keywords": yeni[i:i + 700], "location_code": 2792, "language_code": "tr", "date_from": "2025-09-01", "search_partners": False}])
    for it in (r["tasks"][0].get("result") or []):
        ms = it.get("monthly_searches") or []; m26 = [m["search_volume"] for m in ms if m["year"] == 2026 and 1 <= m["month"] <= 8]
        hd["kelime"][it["keyword"]] = {"v12": it.get("search_volume"), "ort2026": (sum(m26) / len(m26) if m26 else None), "ay2026": len(m26), "aylik": [(m["year"], m["month"], m["search_volume"]) for m in ms]}
json.dump(hd, open(H, "w", encoding="utf-8"), ensure_ascii=False)
print("hacim eklendi", len(yeni))
