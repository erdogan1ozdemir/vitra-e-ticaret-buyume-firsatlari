# -*- coding: utf-8 -*-
"""Similarweb (Apify trakk/similarweb) ham verisinden site trafigi ve kanal kirilimi ozeti.
Girdi : veri/ham/similarweb/trakk_2026-10.json (31 alan adi, Haz - Agu 2026)
Cikti : veri/islenmis/similarweb.json"""
import json, os
import veri

HAM = os.path.join(veri.V, "ham", "similarweb", "trakk_2026-10.json")
GRUP = {
    "marka": ["vitra.com.tr", "artema.com.tr", "kale.com.tr", "creavit.com.tr", "eca.com.tr", "egeseramik.com", "seramiksan.com.tr",
              "turkuazseramik.com.tr", "geberit.com.tr", "grohe.com.tr", "hansgrohe.com.tr", "roca.com.tr", "duravit.com.tr",
              "serelseramik.com.tr", "bien.com.tr"],
    "uzman": ["banyomarka.com", "banyomega.com", "banyome.com", "banyoline.com", "evidea.com", "vivense.com"],
    "yapi": ["koctas.com.tr", "bauhaus.com.tr", "tekzen.com.tr", "ikea.com.tr"],
    "pazar": ["trendyol.com", "hepsiburada.com", "amazon.com.tr", "n11.com", "akakce.com", "cimri.com"],
}
KANAL = [("direct", "directPercent"), ("organik", "organicSearchPercent"), ("ucretli", "paidSearchPercent"),
         ("sosyal_org", "organicSocialPercent"), ("sosyal_ucretli", "paidSocialPercent"), ("referans", "referralsPercent"),
         ("eposta", "mailPercent"), ("display", "displayAdsPercent"), ("affiliate", "affiliatePercent"), ("ai", "aiTrafficPercent")]


def modellenmis(d, ort):
    """Dusuk trafikli sitelerde Similarweb kanal dagilimini benzer sitelerden modeller; bu siteler ayni kaliba oturur
    (e-posta, display ve affiliate paylari birlikte dolu, ziyaret 35 binin altinda)."""
    return ort < 35000 and (d.get("mailPercent") or 0) >= 1.5 and (d.get("affiliatePercent") or 0) >= 0.3


def main():
    D = json.load(open(HAM, encoding="utf-8"))
    grup = {dm: g for g, l in GRUP.items() for dm in l}
    out = []
    for d in D:
        dm = d["domain"]
        aylar = d.get("estimatedMonthlyVisits") or {}
        seri = [{"ay": k_[:7], "ziyaret": round(v)} for k_, v in sorted(aylar.items())]
        ort = sum(s["ziyaret"] for s in seri) / len(seri) if seri else 0
        tr = next((c["visitsShare"] for c in d.get("trafficByCountry") or [] if c.get("countryCode") == "TR"), None)
        if tr is None:
            tr = next((c["share"] for c in d.get("topCountryShares") or [] if c.get("countryCode") == "TR"), None)
        kan = {ad: round(d.get(alan) or 0, 2) for ad, alan in KANAL}
        e = d.get("engagement") or {}
        out.append({
            "alan": dm, "grup": grup.get(dm, "diger"), "seri": seri, "ort_ziyaret": round(ort),
            "son_ay": seri[-1]["ay"] if seri else None, "son_ziyaret": seri[-1]["ziyaret"] if seri else None,
            "tr_pay": round(100 * tr, 2) if tr is not None else None,
            "ilk_ulke": d.get("topCountryCode"), "ilk_ulke_pay": d.get("topCountrySharePercent"),
            "kanal": kan, "modellenmis": modellenmis(d, ort), "kucuk": bool(d.get("isSmall")),
            "hemen_cikma": round(100 * e["bounceRate"], 1) if e.get("bounceRate") is not None else None,
            "sayfa_ziyaret": round(e["pagesPerVisit"], 2) if e.get("pagesPerVisit") is not None else None,
            "sure_sn": round(e["timeOnSite"]) if e.get("timeOnSite") is not None else None,
            "organik_kelime": d.get("organicKeywordCount"),
            "ai_ziyaret": round(d.get("estimatedAiVisits") or 0),
            "ulkeler": [{"ulke": c["countryCode"], "pay": round(100 * c["visitsShare"], 2)} for c in (d.get("trafficByCountry") or [])[:5]],
            "rakipler": [c["domain"] for c in (d.get("similarwebCompetitors") or [])[:10]],
            "ayrica_ziyaret": d.get("audienceAlsoVisits") or [],
            "sosyal_ag": [{"ad": s["name"], "pay": round(100 * s["visitsShare"], 1)} for s in (d.get("topSocialNetworks") or [])],
            "kelimeler": [{"kelime": t["name"], "hacim": t.get("volume")} for t in (d.get("topKeywords") or [])[:10]],
        })
    out.sort(key=lambda r: -r["ort_ziyaret"])
    yol = os.path.join(veri.V, "islenmis", "similarweb.json")
    json.dump({"kaynak": "Similarweb (Apify) · Haz - Ağu 2026 · tüm ülkeler", "siteler": out}, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("kaydedildi:", yol, len(out), "site ·", sum(r["modellenmis"] for r in out), "modellenmiş kanal dağılımı")


if __name__ == "__main__":
    main()
