# -*- coding: utf-8 -*-
"""YouTube derin arama (68 yeni arama) · TR · DataForSEO. Cikti: veri/ham/derin/youtube/arama.json"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__)); import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(P, "veri/ham/derin/youtube"); os.makedirs(OUT, exist_ok=True)
G = {
 "Seçim ve karşılaştırma": ["asma klozet mi yerden klozet mi", "gömme rezervuar mı normal rezervuar mı", "banyo dolabı nasıl seçilir", "lavabo nasıl seçilir", "batarya nasıl seçilir", "duşakabin nasıl seçilir", "akıllı klozet alınır mı", "banyo dolabı hangi malzeme", "pvc mi mdf mi banyo dolabı", "en iyi batarya markası", "en iyi banyo dolabı markası"],
 "Montaj": ["lavabo montajı", "çanak lavabo montajı", "gömme rezervuar kurulumu", "akıllı klozet montajı", "klozet kapağı takma", "duşakabin kurulumu", "küvet montajı", "duş teknesi montajı", "termostatik batarya montajı", "ankastre batarya montajı", "banyo aynası montajı", "çamaşır makinesi dolabı montajı", "havlupan montajı", "taharet musluğu takma", "sifon değiştirme"],
 "Tamir ve bakım": ["batarya damlatıyor", "musluk kartuşu değişimi", "rezervuar şamandıra ayarı", "gömme rezervuar su doldurmuyor", "klozet kapağı menteşe değişimi", "lavabo sifonu tıkandı", "duşakabin tekeri değişimi", "silikon çekme banyo", "kireç temizliği batarya", "gömme rezervuar kumanda paneli değişimi"],
 "İlham ve tadilat": ["küçük banyo yenileme", "banyo tadilatı öncesi sonrası", "banyo tadilatı maliyeti", "banyo tasarım fikirleri 2026", "banyo dekorasyonu", "kiralık ev banyo yenileme", "fayans üstüne fayans", "fayans boyama"],
 "Marka ve rakip": ["vitra", "artema", "vitra v-care", "vitra akıllı klozet kurulumu", "kale banyo", "creavit klozet", "serel klozet", "eca batarya", "grohe batarya", "geberit gömme rezervuar", "hansgrohe", "duravit", "bocchi lavabo", "ikea banyo", "koçtaş banyo", "trendyol banyo dolabı inceleme"],
 "Yeni kategoriler": ["granit evye montajı", "arıtmalı batarya", "su arıtma cihazı kurulumu", "elektrikli havlupan", "şofben montajı", "banyo lambası montajı", "engelli banyo düzenlemesi", "çocuk klozet adaptörü"],
}
KW = [(g, k) for g, ks in G.items() for k in ks]
print("toplam arama", len(KW))
def parse(t):
    res = (t.get("result") or [None])[0]
    if not res: return None
    return {"item_count": res.get("items_count"), "videolar": [
        {"baslik": it.get("title"), "kanal": it.get("channel_name"), "kanal_id": it.get("channel_id"), "kanal_url": it.get("channel_url"), "video_id": it.get("video_id"),
         "url": it.get("url"), "goruntulenme": it.get("views_count"), "yayin": it.get("publication_date"), "sure": it.get("duration_time"), "sira": it.get("rank_absolute"), "tip": it.get("type"), "dogrulanmis": it.get("is_verified")}
        for it in (res.get("items") or []) if it.get("type") in ("youtube_video", "youtube_shorts")]}
out = {}; maliyet = 0.0
def calistir(kws):
    global maliyet
    r = dfs.post("/v3/serp/youtube/organic/live/advanced", [{"keyword": k, "location_code": 2792, "language_code": "tr"} for k in kws])
    for t in r["tasks"]:
        maliyet += t.get("cost", 0) or 0
        k = t["data"]["keyword"]; p = parse(t)
        if p and p["videolar"]: out[k] = p
    return r["tasks"][0]["status_message"]
for i in range(0, len(KW), 10):
    print("batch", i, calistir([k for _, k in KW[i:i+10]])); time.sleep(3)
for tur in range(3):
    eksik = [k for _, k in KW if k not in out]
    if not eksik: break
    print("tekrar", tur + 1, len(eksik), "eksik")
    for k in eksik:
        try: calistir([k])
        except SystemExit as e: print("hata", k, str(e)[:100])
        time.sleep(2.5)
grup = {k: g for g, k in KW}
final = {"maliyet_usd": round(maliyet, 4), "aramalar": {k: {"grup": grup[k], **out[k]} for _, k in KW if k in out}, "bos": [k for _, k in KW if k not in out]}
json.dump(final, open(os.path.join(OUT, "arama.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("basarili", len(final["aramalar"]), "bos", final["bos"], "maliyet", final["maliyet_usd"])
