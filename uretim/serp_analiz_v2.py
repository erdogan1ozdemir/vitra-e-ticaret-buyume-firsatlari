# -*- coding: utf-8 -*-
"""Genisletilmis SERP seti (set_v2) kayit duzeyi analiz: ilk 20 organik, sayfa tipi, VitrA sirasi, SERP ozellikleri, AI Overview kaynaklari.
Yardimci fonksiyonlar serp_analiz.py'nin ust bolumunden alinir. Cikti: veri/ham/derin/serp/kelime_sonuc_v2.json"""
import json, os, re, collections
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "serp_analiz.py"), encoding="utf-8").read()
_src = _src[:_src.index("# ---------- hacim eslemesi")].replace("from serp_kelimeler import LISTE, KEL", "")
exec(_src)
SET = json.load(open(os.path.join(S, "set_v2.json"), encoding="utf-8"))
GSC = json.load(open(os.path.join(S, "gsc_v2.json"), encoding="utf-8"))["kelime"]
# VitrA sirasi icin birincil kaynak: SEOmonitor gunluk mobil takip (03.10.2026); takipte olmayan kelimelerde SERP gozlemlerinin ortancasi
SM = {k_["keyword"]: k_ for k_ in json.load(open(os.path.join(S, "..", "..", "seomonitor", "kelimeler_2026-10-03.json"), encoding="utf-8"))}
# Takipteki kelimelerde tum siralar (VitrA ve rakipler) SEOmonitor'un ayni gunku mobil ilk 20 sonucundan alinir: iki kaynagin
# karistirilmasi ayni kelimede iki alan adinin birden 1. sirada sayilmasina yol aciyordu. SERP ozellikleri gozlemlerden gelir.
SMT = {r["keyword"]: r["top_100_results"] for r in json.load(open(os.path.join(S, "..", "..", "seomonitor", "top_results_2026-10-03.json"), encoding="utf-8"))["kelimeler"]}
kayit, eksik = [], []
for s in SET["kelimeler"]:
    kw = s["kw"]
    # Ayni gun uc gozlem (ham_v2, ham_v2b, ham_v2c): Google mobilde ayni aramaya farkli sonuc varyantlari donebildigi icin
    # sira bilgisi gozlemlerin ortancasi (medyan) ile, sayfa listesi en eksiksiz gozlemden alinir. 10'dan az organik sonuc donen gozlem eksik sayilir.
    gz = []
    for kl in ("ham_v2", "ham_v2b", "ham_v2c"):
        f = os.path.join(S, kl, ad(kw) + ".json")
        if os.path.exists(f):
            r_ = json.load(open(f))["tasks"][0]["result"][0]
            gz.append((r_, [i for i in (r_.get("items") or []) if i["type"] == "organic"]))
    if not gz: eksik.append(kw); continue
    tam = [(r_, o_) for r_, o_ in gz if len(o_) >= 10] or gz
    res, org = max(tam, key=lambda t: len(t[1])); it = res.get("items") or []
    def _med(L_):
        L_ = sorted(L_); return L_[len(L_) // 2] if L_ else None
    alan_med = {}
    for r_, o_ in tam:
        enb = {}
        for i in o_:
            if i["rank_group"] <= 20: enb[kok(i["domain"])] = min(enb.get(kok(i["domain"]), 99), i["rank_group"])
        for d_ in set(enb) | set(alan_med): alan_med.setdefault(d_, []).append(enb.get(d_, 99))
    alan_med = {d_: _med(v_ + [99] * (len(tam) - len(v_))) for d_, v_ in alan_med.items()}
    vmed = alan_med.get("vitra.com.tr"); vmed = vmed if vmed and vmed <= 20 else None
    sm = ((SM.get(kw) or {}).get("ranking_data") or {}).get("mobile") or {}
    vkay = "serp"
    if kw in SM and sm.get("rank") is not None:
        vkay = "seomonitor"; vmed = sm["rank"] if sm["rank"] and sm["rank"] <= 20 else None
        alan_med.pop("vitra.com.tr", None)
        if vmed and vmed <= 10: alan_med["vitra.com.tr"] = vmed
    skay = "gozlem"
    if SMT.get(kw):
        skay = vkay = "seomonitor"; L_ = sorted(SMT[kw], key=lambda x: x["rank"])
        top = [{"sira": x["rank"], "alan": kok(x["domain"]), "url": x["landing_page"], "tip": tip(x["domain"], x["landing_page"] or "", x.get("title")), "baslik": x.get("title")} for x in L_ if x["rank"] <= 10]
        t20 = [{"sira": x["rank"], "alan": kok(x["domain"]), "url": x["landing_page"], "tip": tip(x["domain"], x["landing_page"] or "", x.get("title"))} for x in L_]
        alan_med = {}
        for x in t20: alan_med[x["alan"]] = min(alan_med.get(x["alan"], 99), x["sira"])
        vmed = alan_med.get("vitra.com.tr")
    else:
        top = [{"sira": i["rank_group"], "alan": kok(i["domain"]), "url": i["url"], "tip": tip(i["domain"], i["url"], i.get("title")), "baslik": i.get("title")} for i in org if i["rank_group"] <= 10]
        t20 = [{"sira": i["rank_group"], "alan": kok(i["domain"]), "url": i["url"], "tip": tip(i["domain"], i["url"], i.get("title"))} for i in org]
    amed = alan_med.get("artema.com.tr"); amed = amed if amed and amed <= 20 else None
    vit = [x for x in t20 if x["alan"] == "vitra.com.tr"]; art = [x for x in t20 if x["alan"] == "artema.com.tr"]
    tur = collections.Counter(i["type"] for i in it)
    paa = [e["title"] for i in it if i["type"] == "people_also_ask" for e in (i.get("items") or []) if e.get("title")]
    vids = [{"kaynak": e.get("source"), "baslik": e.get("title"), "url": e.get("url")} for i in it if i["type"] == "video" for e in (i.get("items") or [])]
    sv = [{"kaynak": e.get("source"), "alan": e.get("domain")} for i in it if i["type"] == "short_videos" for e in (i.get("items") or [])]
    lp = [{"baslik": i.get("title")} for i in it if i["type"] == "local_pack"]
    cs = [kok(e.get("domain")) for i in it if i["type"] == "compare_sites" for e in (i.get("items") or [])]
    _ilk = gz[0][0] if os.path.exists(os.path.join(S, "ham_v2", ad(kw) + ".json")) else res   # AI Overview icerigi ilk gozleme gore cekildi
    ai_var = any(i["type"] == "ai_overview" for i in (_ilk.get("items") or [])); ai = None
    fa = os.path.join(S, "ham_ai_v2", ad(kw) + ".json")
    if ai_var and os.path.exists(fa):
        ra = json.load(open(fa))["tasks"][0]["result"][0]
        a = [i for i in (ra.get("items") or []) if i["type"] == "ai_overview"]
        if a:
            a = a[0]; refs = a.get("references") or []; md = a.get("markdown") or ""
            ai = {"ref_alanlar": [kok(x.get("domain")) for x in refs], "ref_url": [x.get("url") for x in refs],
                  "vitra_ref": any(kok(x.get("domain")) == "vitra.com.tr" for x in refs), "vitra_metin": bool(re.search(r"vitra", md, re.I)), "metin_uzun": len(md)}
    kayit.append({"kelime": kw, "grup": s["grup"], "tema": s["tema"], "alt": s.get("alt"), "hacim": s["hacim"], "top10": top,
                  "vitra_sira": vmed, "vitra_kaynak": vkay, "sira_kaynak": skay, "vitra_url": vit[0]["url"] if vit else None, "vitra_tip": vit[0]["tip"] if vit else None,
                  "artema_sira": amed, "alan_med": {d_: v_ for d_, v_ in alan_med.items() if v_ <= 10}, "gozlem": len(gz), "tam_gozlem": len([1 for _, o_ in gz if len(o_) >= 10]),
                  "vitra_gozlem": [next((i["rank_group"] for i in o_ if kok(i["domain"]) == "vitra.com.tr"), None) for _, o_ in gz], "ai_ilk_cekim": ai_var, "ai": ai, "paa": paa, "video": vids, "short_video": sv,
                  "local_pack": lp, "compare_sites": cs, "ozellik_sayim": dict(tur), "gsc": GSC.get(kw)})
json.dump({"tarih": "2026-10-04", "kelimeler": kayit}, open(os.path.join(S, "kelime_sonuc_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("kayit", len(kayit), "eksik", len(eksik), eksik[:10])
