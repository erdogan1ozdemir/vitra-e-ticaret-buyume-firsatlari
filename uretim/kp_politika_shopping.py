# -*- coding: utf-8 -*-
"""Baslik 6: Google TR mobil (ve karsilastirma icin masaustu) organik SERP'te Shopping / urun bloklari (DataForSEO serp/google/organic/live/advanced).
Yalnizca blok varligi, blok icindeki satici/alan adi ve VitrA gorunurlugu alinir; fiyat cekimi baska bir ajanin isidir.
Cikti: kanal_politikalari/shopping_ham.json ve shopping_blok.json."""
import json, os, re, time
from urllib.parse import urlparse
import dfs
from kp_politika_ortak import KOK, TARIH
KATEGORI = ["klozet takımı","asma klozet","akıllı klozet","klozet kapağı","gömme rezervuar","lavabo","banyo dolabı","lavabo bataryası","banyo bataryası","duş seti","duşakabin","banyo aynası","havluluk","küvet","banyo aksesuarları"]
MARKA = ["vitra klozet","vitra banyo dolabı","vitra lavabo bataryası"]
HEDEF_TIPLER = {"shopping","popular_products","product_considerations","google_shopping","paid","local_pack","commercial_units","refine_products","find_results_on","images","video","ai_overview","featured_snippet","people_also_ask","related_searches","top_stories","short_videos","discussions_and_forums","carousel","knowledge_graph","explore_brands","hotels_pack"}
def dom(u):
    try: return urlparse(u).netloc.replace("www.", "")
    except Exception: return None
def calistir():
    yol = os.path.join(KOK, "shopping_ham.json")
    ham = json.load(open(yol)) if os.path.exists(yol) else {}
    for cihaz in ("mobile", "desktop"):
        for kw in KATEGORI + MARKA:
            anahtar = "%s|%s" % (cihaz, kw)
            if anahtar in ham: continue
            g = {"keyword": kw, "location_code": 2792, "language_code": "tr", "device": cihaz, "depth": 20}
            if cihaz == "mobile": g["os"] = "android"
            t = dfs.post("/v3/serp/google/organic/live/advanced", [g])["tasks"][0]
            res = (t.get("result") or [{}])[0]
            items = res.get("items") or []
            kayit = {"cost": t.get("cost"), "item_types": res.get("item_types"), "check_url": res.get("check_url"), "blok": [], "organik": []}
            for it in items:
                ty = it.get("type")
                if ty == "organic":
                    if it.get("rank_group", 99) <= 10:
                        kayit["organik"].append({"sira": it.get("rank_group"), "domain": it.get("domain"), "url": it.get("url"), "baslik": it.get("title")})
                elif ty in HEDEF_TIPLER and ty not in ("related_searches", "people_also_ask"):
                    alt = []
                    for s in (it.get("items") or [])[:12]:
                        alt.append({k: s.get(k) for k in ("type", "title", "seller", "domain", "url", "price", "brand") if k in s})
                    kayit["blok"].append({"type": ty, "rank_group": it.get("rank_group"), "rank_absolute": it.get("rank_absolute"), "title": it.get("title"), "alt_sayisi": len(it.get("items") or []), "alt": alt})
            ham[anahtar] = kayit
            json.dump(ham, open(yol, "w"), ensure_ascii=False)
            time.sleep(1)
    return ham
if __name__ == "__main__":
    ham = calistir()
    print(len(ham), round(sum(v["cost"] or 0 for v in ham.values()), 4))
