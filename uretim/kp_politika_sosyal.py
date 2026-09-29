# -*- coding: utf-8 -*-
"""Baslik 4: sosyal ve kesif kanallari (kamuya acik sayilar). YouTube ve Pinterest profil sayfalari curl ile, Instagram ve TikTok
girise kapali oldugu icin Google SERP snippet'inden ("~144K followers") alinir ve 'yaklasik, SERP'ten' diye isaretlenir.
Pinterest'te banyo temali icerikte marka gorunurlugu icin 8 'site:pinterest.com' sorgusu (DataForSEO organic, TR).
Cikti: kanal_politikalari/sosyal_ham.json ve sosyal.json"""
import json, os, re, time
import dfs
from kp_politika_ortak import *
MARKALAR = {
 "VitrA Türkiye": {"ig": "vitraturkiye", "yt": "https://www.youtube.com/user/VitrAglobal/about", "pin": "https://tr.pinterest.com/vitrabathrooms/", "tt": "vitraturkiye", "aramalar": ["vitra türkiye youtube kanalı"]},
 "Artema": {"ig": "artematurkiye", "yt": "https://www.youtube.com/user/ArtemATurkiye/about", "pin": "https://tr.pinterest.com/DesignStudioVitrA/", "tt": "artematurkiye"},
 "Kale (Çanakkale Seramik)": {"ig": "canakkaleseramik", "yt": "https://www.youtube.com/user/CanakkaleSrmk/about", "pin": "http://www.pinterest.com/canakkalesrmk/", "tt": "kaleseramik"},
 "Creavit": {"ig": "creavitturkiye", "yt": "https://www.youtube.com/user/creavitturkiye/about", "pin": "https://tr.pinterest.com/creavitturkiye/", "tt": "banyobutarafta"},
 "ECA (Elginkan)": {"ig": "elginkaneca", "yt": None, "pin": None, "tt": "ecaserel", "aramalar": ["E.C.A. SEREL youtube kanalı", "ECA Elginkan pinterest"]},
 "Geberit Türkiye": {"ig": "geberit.tr", "yt": None, "pin": None, "tt": "geberit", "aramalar": ["Geberit Türkiye youtube kanalı"]},
 "Grohe Türkiye": {"ig": "groheturkiye", "yt": "https://www.youtube.com/grohe/about", "pin": "https://www.pinterest.com/grohe/", "tt": "grohe"},
}
PIN_SORGULARI = ["vitra banyo pinterest", "site:pinterest.com vitra banyo", "site:pinterest.com vitra klozet", "site:pinterest.com vitra artema banyo", "site:pinterest.com banyo dolabı modelleri",
                 "site:pinterest.com modern banyo tasarımları", "site:pinterest.com banyo dekorasyon fikirleri", "site:pinterest.com küçük banyo dekorasyonu", "site:pinterest.com lavabo bataryası modelleri"]
HAM = os.path.join(KOK, "sosyal_ham.json")
def serp(kw):
    t = dfs.post("/v3/serp/google/organic/live/advanced", [{"keyword": kw, "location_code": 2792, "language_code": "tr", "device": "desktop", "depth": 30}])["tasks"][0]
    res = (t.get("result") or [{}])[0]
    return {"cost": t.get("cost"), "items": [{"sira": it.get("rank_group"), "url": it.get("url"), "baslik": it.get("title"), "aciklama": it.get("description"), "domain": it.get("domain")} for it in (res.get("items") or []) if it.get("type") == "organic"]}
def yt(url):
    k, h = cek(url)
    if k != 200: return {"durum": k}
    g = lambda p: (re.findall(p, h) or [None])[0]
    return {"durum": k, "kanal_url": g(r'"canonicalChannelUrl":"([^"]+)"'), "abone": (g(r'"subscriberCountText":"([^"]+)"') or "").replace("\xa0", " "),
            "video": g(r'"videoCountText":"([^"]+)"'), "goruntuleme": g(r'"viewCountText":"([^"]+)"'), "katilma": g(r'"joinedDateText":\{"content":"([^"]+)"'), "baslik": g(r'"channelMetadataRenderer":\{"title":"([^"]+)"')}
def pin(url):
    k, h = cek(url)
    if k != 200: return {"durum": k}
    handle = url.rstrip("/").split("/")[-1]
    import collections
    sayilar = []
    hd = re.escape(handle)
    sayilar += [int(x) for x in re.findall(r'"username":"%s"[^{}]*?"follower_count":(\d+)' % hd, h, re.I)]
    sayilar += [int(x) for x in re.findall(r'"follower_count":(\d+)[^{}]*?"username":"%s"' % hd, h, re.I)]
    sayilar += [int(x) for x in re.findall(r'"username":"%s"[^{}]*"follower_count":(\d+)' % hd, h, re.I)]
    baslik = (re.findall(r'<title[^>]*>([^<]+)', h) or [None])[0]
    if not sayilar and baslik:
        ad = re.escape(baslik.split(" (")[0].strip())
        sayilar += [int(x) for x in re.findall(r'"follower_count":(\d+)[^{}]{0,600}"full_name":"%s"' % ad, h)]
    if not sayilar: return {"durum": k, "takipci": None, "kullanici": handle, "baslik": baslik}
    c = collections.Counter(sayilar)
    return {"durum": k, "takipci": c.most_common(1)[0][0], "aralik": [min(sayilar), max(sayilar)], "kullanici": handle, "baslik": baslik}
def calistir():
    ham = json.load(open(HAM)) if os.path.exists(HAM) else {"markalar": {}, "pin_sorgulari": {}}
    for m, c in MARKALAR.items():
        r = ham["markalar"].setdefault(m, {})
        if c.get("yt") and "yt" not in r: r["yt"] = yt(c["yt"])
        if c.get("pin") and "pin" not in r: r["pin"] = pin(c["pin"])
        if "ig_serp" not in r: r["ig_serp"] = serp("instagram.com/%s" % c["ig"])
        if "tt_serp" not in r: r["tt_serp"] = serp("tiktok.com/@%s" % c["tt"])
        for a in c.get("aramalar", []):
            if a not in r: r[a] = serp(a)
        json.dump(ham, open(HAM, "w"), ensure_ascii=False); print("tamam", m, flush=True)
    for q in PIN_SORGULARI:
        if q not in ham["pin_sorgulari"]:
            ham["pin_sorgulari"][q] = serp(q); json.dump(ham, open(HAM, "w"), ensure_ascii=False); time.sleep(1)
    return ham
IG_EK = {"VitrA Türkiye": "vitraturkiye", "Artema": "artematurkiye", "Kale (Çanakkale Seramik)": "canakkaleseramik", "Creavit": "creavitturkiye", "ECA (Elginkan)": "elginkaneca", "Geberit Türkiye": "geberit.tr", "Grohe Türkiye": "groheturkiye"}
def sayi(x):
    """'144K' -> 144000; '1.8K+' -> 1800; '1,2 Mn' -> 1200000; '1486' -> 1486"""
    x = x.strip().lower().replace("+", "")
    m = re.match(r"([\d.,]+)\s*(k|b|m|mn|bin)?", x)
    if not m: return None
    n = float(m.group(1).replace(".", "").replace(",", ".")) if re.search(r",\d{1,2}$", m.group(1)) and not m.group(2) else float(m.group(1).replace(",", ""))
    return int(n * {"k": 1e3, "b": 1e3, "bin": 1e3, "m": 1e6, "mn": 1e6, None: 1}[m.group(2)])
def profil_snippet(items, platform, handle):
    """SERP oge listesinden profil snippet'i (takipci, gonderi) doner."""
    hd = handle.lower()
    for it in items:
        u = (it["url"] or "").lower().rstrip("/")
        if platform == "ig" and not re.search(r"instagram\.com/%s$" % re.escape(hd), u): continue
        if platform == "tt" and not re.search(r"tiktok\.com/@%s$" % re.escape(hd), u): continue
        a = it["aciklama"] or ""
        f = re.search(r"([\d.,]+\s?[KMB]?\+?)\s+(?:Followers|takipçi)", a, re.I)
        p = re.search(r"([\d.,]+\s?[KMB]?\+?)\s+(?:posts|gönderi)", a, re.I)
        return {"url": it["url"], "takipci_metin": f.group(1) if f else None, "takipci": sayi(f.group(1)) if f else None, "gonderi_metin": p.group(1) if p else None, "aciklama": a[:160]}
    return None
def tamamla():
    ham = json.load(open(HAM))
    for m, c in MARKALAR.items():
        r = ham["markalar"][m]
        if c.get("pin"): r["pin"] = pin(c["pin"])
        if profil_snippet(r["ig_serp"]["items"], "ig", c["ig"]) and (profil_snippet(r["ig_serp"]["items"], "ig", c["ig"]) or {}).get("takipci"): continue
        for kw in ("%s instagram" % c["ig"], "instagram.com/%s/" % c["ig"], "site:instagram.com %s" % c["ig"], "%s" % c["ig"], "%s instagram profili takipçi" % c["ig"], "%s official instagram followers" % c["ig"]):
            if profil_snippet(r["ig_serp"]["items"], "ig", c["ig"]) and (profil_snippet(r["ig_serp"]["items"], "ig", c["ig"]) or {}).get("takipci"): break
            r.setdefault("ig_ek", {})
            if kw not in r["ig_ek"]: r["ig_ek"][kw] = serp(kw)
            r["ig_serp"]["items"] = r["ig_serp"]["items"] + r["ig_ek"][kw]["items"]
        json.dump(ham, open(HAM, "w"), ensure_ascii=False)
    for q in PIN_SORGULARI:
        if q not in ham["pin_sorgulari"] or not ham["pin_sorgulari"][q]["items"]:
            ham["pin_sorgulari"][q] = serp(q)
    json.dump(ham, open(HAM, "w"), ensure_ascii=False)
    return ham
MARKA_DESEN = {"VitrA": r"vitra|vıtra", "Artema": r"artema", "Kale": r"\bkale\b|çanakkale seramik|kale seramik|kale banyo", "Creavit": r"creavit", "ECA": r"\beca\b|e\.c\.a|serel",
               "Geberit": r"geberit", "Grohe": r"grohe", "Duravit": r"duravit", "Ideal Standard": r"ideal standard", "Hansgrohe": r"hansgrohe", "Kütahya Seramik": r"kütahya seramik|kutahya seramik", "Villeroy & Boch": r"villeroy"}
def ozetle():
    ham = json.load(open(HAM))
    out = {"tarih": TARIH, "kaynak": "YouTube ve Pinterest profil sayfaları (curl, herkese açık HTML); Instagram ve TikTok girişe kapalı olduğundan Google TR SERP snippet'i (DataForSEO organic); yaklaşık değerler 'SERP'ten' işaretlidir",
           "markalar": [], "pinterest_gorunurluk": {"sorgular": [], "marka_toplam": {}}}
    for m, c in MARKALAR.items():
        r = ham["markalar"][m]
        ig = profil_snippet(r["ig_serp"]["items"], "ig", c["ig"])
        tt = profil_snippet(r["tt_serp"]["items"], "tt", c["tt"])
        y = r.get("yt") or {}
        p = r.get("pin") or {}
        # ek arama ile bulunan YouTube kanali
        row = {"marka": m,
               "instagram": {"hesap": "@" + c["ig"], "takipci_yaklasik": ig and ig["takipci"], "takipci_metin": ig and ig["takipci_metin"], "gonderi_metin": ig and ig["gonderi_metin"], "kaynak": "Google SERP snippet (yaklaşık)" if ig and ig["takipci"] else "alınamadı (girişe kapalı, SERP'te profil sayısı görünmedi)", "url": "https://www.instagram.com/%s/" % c["ig"]},
               "youtube": {"kanal": y.get("kanal_url"), "abone": y.get("abone"), "video": y.get("video"), "goruntuleme": y.get("goruntuleme"), "katilma": y.get("katilma"), "kaynak": "YouTube hakkında sayfası (curl)"} if y.get("durum") == 200 else None,
               "pinterest": {"kullanici": p.get("kullanici"), "takipci": p.get("takipci"), "kaynak": "Pinterest profil sayfası (curl)"} if p.get("durum") == 200 else None,
               "tiktok": {"hesap": "@" + c["tt"], "takipci_yaklasik": tt and tt["takipci"], "kaynak": "Google SERP snippet (yaklaşık)"} if tt and tt["takipci"] else None}
        out["markalar"].append(row)
    tum = {k: {"top10_sonuc": 0, "top30_sonuc": 0, "sorgu_sayisi": 0, "en_iyi_sira": None} for k in MARKA_DESEN}
    tum_nötr = {k: {"top30_sonuc": 0, "sorgu_sayisi": 0, "en_iyi_sira": None} for k in MARKA_DESEN}
    for q, v in ham["pin_sorgulari"].items():
        items = [i for i in v["items"] if "pinterest" in (i["domain"] or "")]
        marka_adli = bool(re.search(r"vitra|artema|kale|creavit|eca|geberit|grohe", q, re.I))
        satir = {"sorgu": q, "marka_adli_sorgu": marka_adli, "toplam_organik_sonuc": len(v["items"]), "pinterest_sonuc": len(items), "markalar": {}}
        for k, pat in MARKA_DESEN.items():
            eslesen = [i for i in items if re.search(pat, " ".join([i["baslik"] or "", i["aciklama"] or "", i["url"] or ""]), re.I)]
            if eslesen:
                satir["markalar"][k] = {"sonuc": len(eslesen), "en_iyi_sira": min(i["sira"] for i in eslesen), "ornek": [{"sira": i["sira"], "baslik": (i["baslik"] or "")[:80], "url": i["url"]} for i in eslesen[:2]]}
                t = tum[k]; t["top30_sonuc"] += len(eslesen); t["top10_sonuc"] += sum(1 for i in eslesen if i["sira"] <= 10); t["sorgu_sayisi"] += 1
                t["en_iyi_sira"] = min(t["en_iyi_sira"] or 99, min(i["sira"] for i in eslesen))
                if not marka_adli:
                    n = tum_nötr[k]; n["top30_sonuc"] += len(eslesen); n["sorgu_sayisi"] += 1; n["en_iyi_sira"] = min(n["en_iyi_sira"] or 99, min(i["sira"] for i in eslesen))
        out["pinterest_gorunurluk"]["sorgular"].append(satir)
    out["pinterest_gorunurluk"]["marka_toplam_tum_sorgular"] = tum
    out["pinterest_gorunurluk"]["marka_toplam_markasiz_sorgular"] = tum_nötr
    out["pinterest_gorunurluk"]["not"] = "Yalnızca pinterest alan adındaki sonuçlar sayıldı; eşleşme sonuç başlığı, açıklaması veya adresinde marka adının geçmesine göredir (pinin içindeki görsel okunmadı). Marka adlı sorgular ayrı gösterildi."
    json.dump(out, open(os.path.join(KOK, "sosyal.json"), "w"), ensure_ascii=False, indent=1)
    return out
if __name__ == "__main__":
    ham = calistir(); ham = tamamla(); o = ozetle(); print("bitti")
