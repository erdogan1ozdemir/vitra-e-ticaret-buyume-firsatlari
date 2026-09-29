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
SHOP_TIPLERI = ("shopping", "popular_products", "product_considerations", "google_shopping", "paid", "commercial_units", "refine_products")
def kontrol_calistir():
    """Ayni tespit yolunu genel urun sorgularinda dener (kontrol): Shopping bloklari TR SERP'te genel olarak var mi."""
    yol = os.path.join(KOK, "shopping_kontrol.json")
    out = json.load(open(yol)) if os.path.exists(yol) else {}
    for kw in ["iphone 15", "samsung televizyon 55 inç", "kablosuz kulaklık", "nike air max", "buzdolabı"]:
        for cihaz in ("mobile", "desktop"):
            if cihaz + "|" + kw in out: continue
            g = {"keyword": kw, "location_code": 2792, "language_code": "tr", "device": cihaz, "depth": 20}
            if cihaz == "mobile": g["os"] = "android"
            t = dfs.post("/v3/serp/google/organic/live/advanced", [g])["tasks"][0]
            res = (t.get("result") or [{}])[0]
            out[cihaz + "|" + kw] = {"item_types": res.get("item_types"), "cost": t.get("cost")}
            json.dump(out, open(yol, "w"), ensure_ascii=False); time.sleep(1)
    return out
def ozetle():
    ham = json.load(open(os.path.join(KOK, "shopping_ham.json")))
    kon = json.load(open(os.path.join(KOK, "shopping_kontrol.json")))
    sonuc = {"tarih": TARIH, "kaynak": "DataForSEO serp/google/organic/live/advanced · Google TR · location_code 2792 · dil tr · derinlik 20", "kategori": [], "kontrol": [], "ozet": {}}
    def satir(cihaz, kw):
        v = ham.get(cihaz + "|" + kw)
        if not v: return None
        tipler = v["item_types"] or []
        vs = [o["sira"] for o in v["organik"] if "vitra.com.tr" in (o["domain"] or "")]
        return {"kelime": kw, "cihaz": cihaz, "blok_tipleri": tipler,
                "shopping_urun_blogu": any(t in tipler for t in SHOP_TIPLERI),
                "local_pack": "local_pack" in tipler, "images": "images" in tipler, "ai_overview": "ai_overview" in tipler,
                "video": "video" in tipler, "paa": "people_also_ask" in tipler,
                "vitra_organik_sira_top10": vs[0] if vs else None,
                "top10_domain": [o["domain"] for o in v["organik"]][:10]}
    for kw in KATEGORI + MARKA:
        m = satir("mobile", kw); d = satir("desktop", kw)
        sonuc["kategori"].append({"kelime": kw, "tur": "marka" if kw in MARKA else "kategori", "mobil": m, "masaustu": d})
    for k, v in kon.items():
        cihaz, kw = k.split("|", 1)
        sonuc["kontrol"].append({"kelime": kw, "cihaz": cihaz, "blok_tipleri": v["item_types"], "shopping_urun_blogu": any(t in (v["item_types"] or []) for t in SHOP_TIPLERI)})
    kat = [r for r in sonuc["kategori"] if r["tur"] == "kategori"]
    def say(cihaz, f): return sum(1 for r in kat if r[cihaz] and f(r[cihaz]))
    sonuc["ozet"] = {"kategori_kelime_sayisi": len(kat),
        "mobil_shopping_urun_blogu": say("mobil", lambda x: x["shopping_urun_blogu"]), "masaustu_shopping_urun_blogu": say("masaustu", lambda x: x["shopping_urun_blogu"]),
        "mobil_local_pack": say("mobil", lambda x: x["local_pack"]), "masaustu_local_pack": say("masaustu", lambda x: x["local_pack"]),
        "mobil_images": say("mobil", lambda x: x["images"]), "mobil_ai_overview": say("mobil", lambda x: x["ai_overview"]), "masaustu_ai_overview": say("masaustu", lambda x: x["ai_overview"]),
        "mobil_paa": say("mobil", lambda x: x["paa"]), "mobil_video": say("mobil", lambda x: x["video"]),
        "mobil_vitra_top10": say("mobil", lambda x: x["vitra_organik_sira_top10"] is not None),
        "kontrol_sorgu_sayisi": len(sonuc["kontrol"]), "kontrol_shopping_blogu": sum(1 for r in sonuc["kontrol"] if r["shopping_urun_blogu"]),
        "maliyet_usd": round(sum(v["cost"] or 0 for v in ham.values()) + sum(v["cost"] or 0 for v in kon.values()), 4)}
    json.dump(sonuc, open(os.path.join(KOK, "shopping_blok.json"), "w"), ensure_ascii=False, indent=1)
    return sonuc
if __name__ == "__main__":
    calistir(); kontrol_calistir(); o = ozetle(); print(json.dumps(o["ozet"], ensure_ascii=False))
