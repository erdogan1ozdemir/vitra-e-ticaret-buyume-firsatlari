# -*- coding: utf-8 -*-
"""Kelime evrenini genisletme · Google Ads keywords_for_keywords · TR · tohum gruplari."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOHUM = {
 "ssg": ["klozet", "asma klozet", "lavabo", "çanak lavabo", "pisuvar", "bide", "gömme rezervuar", "klozet kapağı", "akıllı klozet", "hela taşı",
         "rezervuar iç takımı", "taharet musluğu", "klozet takımı", "lavabo sifonu", "tezgah üstü lavabo", "kanalsız klozet", "yerden klozet", "tuvalet taşı", "klozet fiyatları", "lavabo modelleri"],
 "bm": ["banyo dolabı", "lavabo dolabı", "banyo boy dolabı", "aynalı banyo dolabı", "banyo aynası", "çamaşır makinesi dolabı", "banyo rafı", "banyo tezgahı",
        "banyo mobilyası", "banyo dolap takımı", "banyo dolabı modelleri", "banyo dolabı fiyatları", "pvc banyo dolabı", "suya dayanıklı banyo dolabı", "köşe banyo dolabı", "klozet üstü dolap"],
 "yeni_isitma_su": ["şofben", "termosifon", "anında su ısıtıcı", "elektrikli şofben", "su arıtma cihazı", "havlupan", "banyo radyatörü", "elektrikli havlupan", "banyo ısıtıcı",
                    "su yumuşatma cihazı", "hidrofor", "basınç düşürücü", "su kaçak dedektörü"],
 "yeni_tekstil_aksesuar": ["duş perdesi", "banyo paspası", "bornoz", "havlu seti", "banyo taburesi", "banyo düzenleyici", "ecza dolabı", "banyo tartısı", "banyo halısı", "duş rafı",
                           "banyo çöp kovası", "çamaşır sepeti", "banyo organizer", "sıvı sabunluk", "banyo aydınlatma", "aydınlatmalı ayna", "akıllı ayna", "led ayna"],
 "yeni_ozel": ["klozet adaptörü", "çocuk klozeti", "bebek küveti", "engelli banyo", "engelli klozet", "tutunma barı", "duş oturağı", "yaşlı banyo", "küvet tutamağı",
               "taharet aparatı", "bide makinesi", "klozet taharet aparatı", "elektrikli klozet kapağı", "fotoselli batarya", "el kurutma makinesi", "kağıt havlu dispenseri"],
 "yeni_yapi": ["seramik yapıştırıcı", "derz dolgu", "su yalıtımı", "banyo su izolasyonu", "banyo silikonu", "yer süzgeci", "mozaik", "banyo lambri", "pvc banyo paneli",
               "fayans boyası", "banyo boyası", "fayans üstü kaplama", "seramik yapıştırma", "banyo zemin kaplama", "duvar paneli banyo", "süpürgelik"],
 "yeni_mutfak": ["eviye", "granit eviye", "mutfak evyesi", "mutfak tezgahı", "filtreli batarya", "mutfak lavabosu", "çöp öğütücü", "ankastre evye", "çelik evye",
                 "mutfak bataryası", "mutfak tezgahı fiyatları", "mutfak dolabı"],
 "yeni_wellness": ["jakuzi", "sauna", "buhar odası", "duş paneli", "yağmurlama duş", "termostatik batarya", "bahçe jakuzisi", "hidromasaj", "ev tipi sauna", "duş kabini hamam", "masaj duşu"],
 "hizmet_set": ["banyo tadilatı", "banyo yenileme", "banyo tadilat fiyatları", "komple banyo", "banyo takımı", "banyo seti", "hazır banyo", "prefabrik banyo", "banyo tasarım",
                "3d banyo tasarım", "küçük banyo tasarımı", "banyo dekorasyonu", "tesisatçı", "klozet montajı", "anahtar teslim banyo", "banyo yenileme fiyatı", "banyo ustası", "fayans ustası"],
 "dis_mekan_diger": ["bahçe musluğu", "bahçe duşu", "havuz duşu", "çamaşır musluğu", "sifon", "mutfak sifonu", "tuvalet kağıdı", "klozet temizleyici", "kireç çözücü", "lavabo açıcı"],
}
out = {}
for g, seeds in TOHUM.items():
    r = dfs.post("/v3/keywords_data/google_ads/keywords_for_keywords/live",
                 [{"location_code": 2792, "language_code": "tr", "keywords": seeds, "search_partners": False, "date_from": "2022-09-01", "date_to": "2026-08-31", "sort_by": "search_volume"}])
    t = r["tasks"][0]; res = t.get("result") or []
    print(g, t["status_message"], t.get("cost"), len(res))
    for x in res:
        k = x["keyword"]
        if k in out: out[k]["grup"].add(g); continue
        ms = x.get("monthly_searches") or []
        out[k] = {"grup": {g}, "hacim": x.get("search_volume"), "cpc": x.get("cpc"), "rekabet": x.get("competition"),
                  "seri": {"%04d-%02d" % (m["year"], m["month"]): m["search_volume"] for m in ms}}
for v in out.values(): v["grup"] = sorted(v["grup"])
json.dump({"kaynak": "Google Ads keywords_for_keywords (DataForSEO) · TR 2792 · tr · 2022-09 - 2026-08 · cekim 29.09.2026", "tohum": TOHUM, "kelimeler": out},
          open(os.path.join(P, "veri/ham/kfk_evren.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("toplam", len(out))
