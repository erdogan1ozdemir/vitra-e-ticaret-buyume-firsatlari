# -*- coding: utf-8 -*-
"""Alt sayfa: Yorum ve Soru Seti (marka ve pazaryeri kirilimi, pain point kumeleri, yorum ve soru gezgini).
Ana raporun icindekilerinde yer almaz; rapordaki dugmelerle yeni sekmede acilir.
Cikti: <KOK>/yorum-soru-seti.html"""
import json, os, html, re
import veri
from rapor_parca1 import VITRA, INBOUND
from yorum_tema import YAD, SAD, YORUM, SORU
import yorum_analiz

AD = "yorum-soru-seti.html"
ANA = "VitrA_E-Ticaret_Buyume_Firsatlari.html"
E = html.escape


def T(tr, en):
    return '<span data-l="tr">%s</span><span data-l="en">%s</span>' % (tr, en)


def tr_s(v, ond=1):
    s = ("%." + str(ond) + "f") % v
    a, _, b = s.partition(".")
    a = "{:,}".format(int(a)).replace(",", ".")
    return a + ("," + b if b else "")


def en_s(v, ond=1):
    return ("{:,.%df}" % ond).format(v)


def P(v, ond=1):
    """yuzde: TR %12,5 / EN 12.5%"""
    if v is None: return "-"
    return T("%" + tr_s(v, ond), en_s(v, ond) + "%")


def N(v):
    return T(tr_s(v, 0), en_s(v, 0))


def F(v, ond=2):
    if v is None: return "-"
    return T(tr_s(v, ond), en_s(v, ond))


def saat(v):
    if v is None: return "-"
    if v < 1: return T("%d dk" % round(v * 60), "%d min" % round(v * 60))
    if v < 48: return T("%s sa" % tr_s(v, 1), "%s h" % en_s(v, 1))
    return T("%s gün" % tr_s(v / 24, 1), "%s days" % en_s(v / 24, 1))


def tema_ad(k, soru=False):
    t, e = (SAD if soru else YAD)[k]
    return T(t, e)


KANAL_EN = {"Trendyol": "Trendyol", "Hepsiburada": "Hepsiburada"}


def main():
    A = yorum_analiz.main()
    ALT = json.load(open(os.path.join(veri.V, "islenmis", "yorum_alt.json"), encoding="utf-8"))
    K = A["kumeler"]; M = A["marka"]; S = A["soru"]; TOP = A["toplam"]

    # ------------------------------------------------ marka x pazaryeri ozet tablosu
    def dv(v): return "" if v is None else ("%.4f" % v)
    def satir(m, kanal=None):
        p = M[m] if kanal is None else M[m]["kanal_profil"][kanal]
        s = S[m] if kanal is None else S[m]["kanal_profil"][kanal]
        if not p["n"] and not s["n"]: return ""
        pk = p["olumsuz_metinli"] >= 15 and p["pain"]
        pain = (", ".join('%s <small>%s</small>' % (tema_ad(t), P(r, 0)) for t, _, r in p["pain"][:3] if r) or "-") if pk else "-"
        guc = ", ".join('%s <small>%s</small>' % (tema_ad(t), P(r, 0)) for t, _, r in p["guclu"][:2] if r) or "-"
        ad = m if m != "Diğer markalar" else T("Diğer markalar", "Other brands")
        kn = T(kanal, KANAL_EN[kanal]) if kanal else T("İki pazaryeri", "Both marketplaces")
        grp = "vg" if m in ("VitrA", "Artema") else ("diger" if m == "Diğer markalar" else "rakip")
        vurgu = ' class="vg"' if grp == "vg" else ""
        return ('<tr%s data-g="%s"><td><b>%s</b></td><td>%s</td><td class="n" data-v="%s">%s</td><td class="n" data-v="%s">%s</td><td class="n" data-v="%s">%s</td>'
                '<td class="n pos" data-v="%s">%s</td><td class="n neg" data-v="%s">%s</td><td data-v="%s">%s</td><td data-v="%s">%s</td>'
                '<td class="n c" data-v="%s">%s</td><td class="n c" data-v="%s">%s</td></tr>') % (
            vurgu, grp, ad, kn, dv(p["n"]), N(p["n"]), dv(p["metinli"]), N(p["metinli"]), dv(p["ort_puan"]), F(p["ort_puan"]),
            dv(p["olumlu"]), P(p["olumlu"]), dv(p["olumsuz"]), P(p["olumsuz"]), dv(p["pain"][0][2]) if pk else "", pain,
            dv(p["guclu"][0][2]) if p["guclu"] else "", guc, dv(s["n"]), N(s["n"]), dv(s["medyan_saat"]), saat(s["medyan_saat"]))
    bas = ('<thead><tr><th>%s</th><th>%s</th><th class="n">%s</th><th class="n">%s</th><th class="n">%s</th><th class="n">%s</th><th class="n">%s</th><th>%s</th><th>%s</th><th class="n c">%s</th><th class="n c">%s</th></tr></thead>'
           % (T("Marka", "Brand"), T("Pazaryeri", "Marketplace"), T("Yorum", "Reviews"), T("Metinli", "With text"), T("Ort. puan", "Avg. rating"),
              T("Olumlu", "Positive"), T("Olumsuz", "Negative"), T("En sık pain point'ler", "Top pain points"), T("Öne çıkan güçlü yönler", "Top strengths"),
              T("Soru", "Questions"), T("Medyan cevap süresi", "Median answer time")))
    OZ = {}
    for anah, kanal in (("tum", None), ("ty", "Trendyol"), ("hb", "Hepsiburada")):
        OZ[anah] = '<div class="tw"><table class="tb srt ozt">%s<tbody>%s</tbody></table></div>' % (bas, "".join(satir(m, kanal) for m in K))

    # ------------------------------------------------ pain point matrisi
    mat_bas = "<thead><tr><th>%s</th>%s</tr></thead>" % (T("Tema", "Theme"), "".join('<th class="n c">%s</th>' % (m if m != "Diğer markalar" else T("Diğer", "Other")) for m in K))
    def hucre(v):
        if v is None: return '<td class="n c" data-v="">-</td>'
        a = min(1, v / 45)
        return '<td class="n c hm" style="--a:%.2f" data-v="%.4f">%s</td>' % (a, v, P(v, 0))
    mat = "".join("<tr><td>%s</td>%s</tr>" % (tema_ad(t), "".join(hucre(M[m]["tema_neg"].get(t) if M[m]["olumsuz_metinli"] >= 15 else None) for m in K)) for t, _, _, _ in YORUM)
    mat_alt = "<tr class='alt'><td>%s</td>%s</tr>" % (T("Olumsuz metinli yorum sayısı", "Negative text reviews"), "".join('<td class="n c">%s</td>' % N(M[m]["olumsuz_metinli"]) for m in K))
    MAT = '<div class="tw"><table class="tb mx srt">%s<tbody>%s</tbody><tfoot>%s</tfoot></table></div>' % (mat_bas, mat, mat_alt)

    # ------------------------------------------------ soru kumeleri matrisi
    sm_bas = "<thead><tr><th>%s</th>%s</tr></thead>" % (T("Soru teması", "Question theme"), "".join('<th class="n c">%s</th>' % (m if m != "Diğer markalar" else T("Diğer", "Other")) for m in K if S[m]["n"]))
    def stema(m, t):
        d = {k: r for k, _, r in S[m]["tema"]}
        return d.get(t)
    sm = "".join("<tr><td>%s</td>%s</tr>" % (tema_ad(t, True), "".join(hucre(stema(m, t)) for m in K if S[m]["n"])) for t in [k for k, _, _, _ in SORU] + ["diger"])
    sm_alt = "<tr class='alt'><td>%s</td>%s</tr>" % (T("Soru sayısı", "Number of questions"), "".join('<td class="n c">%s</td>' % N(S[m]["n"]) for m in K if S[m]["n"]))
    sm_alt += "<tr class='alt'><td>%s</td>%s</tr>" % (T("Medyan cevap süresi", "Median answer time"), "".join('<td class="n c">%s</td>' % saat(S[m]["medyan_saat"]) for m in K if S[m]["n"]))
    SMAT = '<div class="tw"><table class="tb mx srt">%s<tbody>%s</tbody><tfoot>%s</tfoot></table></div>' % (sm_bas, sm, sm_alt)

    # ------------------------------------------------ ozet tablosu suzgeci
    OZF = ('<div class="filtre"><input id="ozAra" type="search" aria-label="Ara" data-ph-tr="Marka veya tema ara" data-ph-en="Search brand or theme">'
           '<select id="ozGrup" aria-label="Grup">%s</select><span class="say" id="ozSay" style="margin:0"></span></div>') % "".join(
        '<option value="%s" data-tr="%s" data-en="%s">%s</option>' % (v, a, b, a) for v, a, b in (("", "Tüm markalar", "All brands"), ("vg", "VitrA ve Artema", "VitrA and Artema"), ("rakip", "Rakip markalar", "Competitor brands"), ("diger", "Diğer markalar", "Other brands")))

    # ------------------------------------------------ marka notlari
    vg_neg = A["vg"]["olumsuz"]; rk_neg = A["rakip"]["olumsuz"]
    def kart(m):
        p = M[m]; s = S[m]
        guc = [(t, r) for t, _, r in p["guclu"] if r and r >= 12][:3]
        pain = [(t, r) for t, _, r in p["pain"] if r and r >= 12 and p["olumsuz_metinli"] >= 15][:3]
        li = []
        for t, r in guc:
            li.append('<li><span class="mk up">✓</span>%s</li>' % T("%s: olumlu yorumların %s'inde" % (YAD[t][0], "%" + tr_s(r, 0)), "%s: in %s of positive reviews" % (YAD[t][1], en_s(r, 0) + "%")))
        for t, r in pain:
            li.append('<li><span class="mk at">▲</span>%s</li>' % T("%s: olumsuz yorumların %s'inde" % (YAD[t][0], "%" + tr_s(r, 0)), "%s: in %s of negative reviews" % (YAD[t][1], en_s(r, 0) + "%")))
        if s["n"]:
            st = [(t, r) for t, _, r in s["tema"] if t != "diger"][:2]
            if st:
                li.append('<li><span class="mk q">?</span>%s</li>' % T("En sık soru: %s" % " ve ".join("%s (%s)" % (SAD[t][0].lower(), "%" + tr_s(r, 0)) for t, r in st),
                                                                      "Most frequent questions: %s" % " and ".join("%s (%s)" % (SAD[t][1].lower(), en_s(r, 0) + "%") for t, r in st)))
        ad = m if m != "Diğer markalar" else T("Diğer markalar", "Other brands")
        ek = ""
        if m == "Diğer markalar" and p["markalar"]:
            ek = '<p class="kucuk">%s %s</p>' % (T("Kapsanan başlıca markalar:", "Main brands covered:"), ", ".join(E(b) for b, _ in p["markalar"][:10]))
        return ('<article class="kart%s"><header><h4>%s</h4><span class="rozet">%s · %s · %s</span></header>'
                '<p class="kucuk">%s</p><ul class="marks">%s</ul>%s</article>') % (
            " vg" if m in ("VitrA", "Artema") else "", ad, T("%s yorum" % tr_s(p["n"], 0), "%s reviews" % en_s(p["n"], 0)),
            T("ort. %s" % tr_s(p["ort_puan"], 2), "avg. %s" % en_s(p["ort_puan"], 2)), T("olumsuz %s" % ("%" + tr_s(p["olumsuz"])), "negative %s" % (en_s(p["olumsuz"]) + "%")),
            T("Trendyol %s · Hepsiburada %s yorum" % (tr_s(p["kanal"].get("Trendyol", 0), 0), tr_s(p["kanal"].get("Hepsiburada", 0), 0)),
              "Trendyol %s · Hepsiburada %s reviews" % (en_s(p["kanal"].get("Trendyol", 0), 0), en_s(p["kanal"].get("Hepsiburada", 0), 0))),
            "".join(li), ek)
    KART = '<div class="kartlar">%s</div>' % "".join(kart(m) for m in K)

    # ------------------------------------------------ kayit verisi (yalniz metinli yorumlar)
    yor = [[y["kanal"][0], y["marka"], y["kume"], y["grup"], y["urun"], y.get("url") or "", 1 if y.get("resmi") else 0, y.get("satici") or "",
            y["puan"], y["tarih"] or "", y["metin"], y["tema"]] for y in ALT["yorum"] if y["metin"]]
    yor.sort(key=lambda r: r[9], reverse=True)
    sor = [[s["kanal"][0], s["marka"], s["kume"], s["grup"], s["urun"], s.get("url") or "", s["soru"], s["tarih"] or "", s.get("cevap") or "",
            s.get("cevaplayan") or "", 1 if s.get("resmi") else 0, s.get("cevap_saat"), s["tema"]] for s in ALT["soru"] if s["soru"] and s["soru"] != "[ad]"]
    sor.sort(key=lambda r: r[7], reverse=True)
    VERI = {"y": yor, "s": sor, "k": K,
            "yt": {k: list(v) for k, v in YAD.items()}, "st": {k: list(v) for k, v in SAD.items()},
            "g": sorted({r[3] for r in yor} | {r[3] for r in sor})}
    VJ = json.dumps(VERI, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    d0, d1 = TOP["donem"]
    ay_tr = {"01": "Oca", "02": "Şub", "03": "Mar", "04": "Nis", "05": "May", "06": "Haz", "07": "Tem", "08": "Ağu", "09": "Eyl", "10": "Eki", "11": "Kas", "12": "Ara"}
    ay_en = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    son12 = sum(1 for y in ALT["yorum"] if (y["tarih"] or "") >= "2025-10-01")

    KPI = "".join('<div class="kpi"><div class="v">%s</div><div class="k">%s</div></div>' % (v, k) for v, k in (
        (N(TOP["yorum"]), T("yorum · %s metinli" % tr_s(TOP["metinli"], 0), "reviews · %s with text" % en_s(TOP["metinli"], 0))),
        (N(TOP["soru"]), T("soru ve cevap", "questions and answers")),
        (N(TOP["urun"]), T("ürün sayfası · Trendyol ve Hepsiburada", "product pages · Trendyol and Hepsiburada")),
        (N(len(K) - 1), T("marka ayrı izlendi · küçük markalar tek kümede", "brands tracked separately · small brands in one cluster")),
        (P(A["vg"]["olumsuz"]), T("VitrA ve Artema olumsuz yorum payı · rakipler %s" % ("%" + tr_s(A["rakip"]["olumsuz"])), "VitrA and Artema negative review share · competitors %s" % (en_s(A["rakip"]["olumsuz"]) + "%"))),
    ))

    CSS = r"""
:root{--ink:#10332F;--ink-2:#2F4E4A;--muted:#5C6B69;--line:#E0DCD5;--bg:#FBFAF8;--card:#FFFFFF;--teal:#10332F;--coral:#FF7B52;
--coral-deep:#E85F36;--coral-tint:#FFE3D8;--green:#2E7D32;--green-wash:#C8E6C9;--red:#D32F2F;--red-wash:#FFCDD2;--neutral:#F0EDE8;--hm:255,123,82;
--f:"Segoe UI",Arial,Helvetica,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#EDEAE4;--ink-2:#CFD8D5;--muted:#9AA8A5;--line:#2A3E3B;--bg:#0C1917;--card:#12211F;--teal:#0B2523;--neutral:#1A2A28;--coral-tint:#3A241D;--green-wash:#1E3A24;--red-wash:#3E1F1F}}
:root[data-theme="dark"]{--ink:#EDEAE4;--ink-2:#CFD8D5;--muted:#9AA8A5;--line:#2A3E3B;--bg:#0C1917;--card:#12211F;--teal:#0B2523;--neutral:#1A2A28;--coral-tint:#3A241D;--green-wash:#1E3A24;--red-wash:#3E1F1F}
*{box-sizing:border-box}
html[lang="tr"] [data-l="en"],html[lang="en"] [data-l="tr"]{display:none}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 var(--f);-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:var(--coral-deep)}
.appbar{position:sticky;top:0;z-index:40;background:var(--teal);border-bottom:1px solid rgba(255,255,255,.1)}
.appbar .in{max-width:1400px;margin:0 auto;padding:12px 22px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.bb{display:flex;align-items:center;gap:11px;min-width:0}
.lbl{font-size:9.5px;letter-spacing:.13em;color:rgba(255,255,255,.55);white-space:nowrap}
.logo-card{background:#fff;border-radius:5px;padding:5px 10px;display:flex;align-items:center}
.logo-card img{height:22px;width:auto;display:block}
.ib img{height:22px;width:auto;display:block;filter:brightness(0) invert(1)}
.geri{color:#fff;text-decoration:none;font-size:12.5px;font-weight:600;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.10);border-radius:6px;padding:6px 10px;white-space:nowrap}
.geri:hover,.geri:focus-visible{background:rgba(255,255,255,.2)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:5px;height:32px;min-width:32px;padding:0 9px;border-radius:6px;cursor:pointer;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.10);color:#fff;font:650 11.5px/1 var(--f);letter-spacing:.04em}
.btn:hover{background:rgba(255,255,255,.2)}
.btn:focus-visible,.geri:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.btn svg{width:15px;height:15px}
#tema .ay{display:none}:root[data-theme="dark"] #tema .ay{display:block}:root[data-theme="dark"] #tema .gunes{display:none}
main{max-width:1240px;margin:0 auto;padding:26px 22px 60px}
.eyebrow{font-size:11px;letter-spacing:.14em;color:var(--coral-deep);font-weight:700;margin:0 0 6px}
h1{font-size:clamp(23px,3.4vw,32px);line-height:1.2;margin:0 0 10px;text-wrap:balance}
.lede{color:var(--ink-2);max-width:92ch;margin:0 0 18px}
h2{font-size:20px;margin:38px 0 6px;padding-bottom:8px;border-bottom:1px solid var(--line);position:relative}
h2::after{content:"";position:absolute;left:0;bottom:-1px;width:72px;height:3px;border-radius:2px;background:var(--coral)}
.h2n{color:var(--muted);font-size:13px;margin:6px 0 14px;max-width:100ch}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:8px 0 6px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kpi .v{font-size:24px;font-weight:700;font-variant-numeric:tabular-nums}
.kpi .k{font-size:12.5px;color:var(--muted);line-height:1.4}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 10px}
.tabs button,.chip{font:inherit;font-size:12.5px;padding:5px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer}
.tabs button[aria-selected="true"],.chip.on{background:var(--teal);border-color:var(--teal);color:#fff}
:root[data-theme="dark"] .tabs button[aria-selected="true"],:root[data-theme="dark"] .chip.on{background:var(--coral-deep);border-color:var(--coral-deep)}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
.tb{width:100%;border-collapse:collapse;font-size:13px;min-width:880px}
.tb th{position:sticky;top:0;background:var(--teal);color:#fff;font-weight:600;font-size:12px;text-align:left;padding:9px 10px;white-space:nowrap}
.tb td{padding:8px 10px;border-top:1px solid var(--line);vertical-align:top}
.tb .n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tb tr.vg td{background:var(--coral-tint)}
.tb td small{color:var(--muted)}
.tb .pos{color:var(--green)}.tb .neg{color:var(--red)}
.tb.mx td.hm{background:rgba(var(--hm),calc(var(--a)*.55))}
.tb tr.alt td{background:var(--neutral);font-weight:600}
.tb td.c,.tb th.c{text-align:center;vertical-align:middle}
.tb.mx td{vertical-align:middle}
.tb.srt thead th{cursor:pointer;user-select:none}
.tb.srt thead th::after{content:" \2195";opacity:.45;font-size:10px}
.tb.srt thead th[aria-sort="ascending"]::after{content:" \25B2";opacity:1;color:var(--coral)}
.tb.srt thead th[aria-sort="descending"]::after{content:" \25BC";opacity:1;color:var(--coral)}
.tb.srt thead th:focus-visible{outline:2px solid var(--coral);outline-offset:-2px}
.tb tbody tr.gizli{display:none}
.note{background:var(--neutral);border-radius:10px;padding:12px 14px;margin:12px 0;font-size:13.5px}
.note b{color:var(--coral-deep)}
.ins{border:1px solid var(--line);background:var(--card);border-radius:10px;padding:12px 14px;margin:12px 0;font-size:14px}
.ins::before{content:"➔ ";color:var(--coral-deep);font-weight:700}
.kartlar{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.kart{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kart.vg{border-color:var(--coral)}
.kart header{display:flex;justify-content:space-between;gap:8px;align-items:baseline;flex-wrap:wrap}
.kart h4{margin:0;font-size:16px}
.rozet{font-size:11.5px;color:var(--muted)}
.kucuk{font-size:12.5px;color:var(--muted);margin:4px 0 8px}
ul.marks{list-style:none;padding-left:0;margin:0}
ul.marks li{position:relative;padding-left:23px;margin:0 0 5px;font-size:13.5px}
.mk{position:absolute;left:0;font-weight:700}.mk.up{color:var(--green)}.mk.at{color:var(--coral)}.mk.q{color:var(--muted)}
.filtre{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 12px}
.filtre select,.filtre input{font:inherit;font-size:13px;padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.filtre input{min-width:220px;flex:1 1 220px}
.say{font-size:12.5px;color:var(--muted);margin:0 0 8px}
.liste{display:grid;gap:8px}
.oge{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px}
.meta{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:12px;color:var(--muted);align-items:center}
.pz{font-weight:700;color:var(--ink-2)}
.yildiz{color:#F5A623;letter-spacing:1px}
.res{background:var(--green-wash);color:var(--green);border-radius:999px;padding:1px 8px;font-weight:600}
.urun{font-size:12.5px;margin:3px 0}.urun a{text-decoration:none}.urun a:hover{text-decoration:underline}
.metin{margin:4px 0 6px;font-size:14px}
.tm{display:inline-block;font-size:11px;padding:1px 8px;border-radius:999px;background:var(--neutral);color:var(--ink-2);margin:0 4px 2px 0}
.tm.n{background:var(--red-wash);color:var(--red)}
.cev{border-left:2px solid var(--line);padding:4px 0 2px 10px;margin:6px 0 0;font-size:13.5px;color:var(--ink-2)}
.dahafazla{font:inherit;font-size:13px;margin:12px auto 0;display:block;padding:8px 16px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
footer{max-width:1240px;margin:0 auto;padding:10px 22px 40px;font-size:12px;color:var(--muted)}
@media(max-width:720px){.lbl,.ib{display:none}.appbar .in{padding:10px 16px;gap:8px}main{padding:18px 16px 50px}.filtre input{min-width:0}}
@media(max-width:520px){.geri .uzun{display:none}.kpi .v{font-size:20px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
@media print{.appbar,.filtre,.dahafazla,.tabs{display:none}.tw{overflow:visible}}
"""
    JS = r"""
(function(){
var V=JSON.parse(document.getElementById('veri').textContent), kok=document.documentElement;
function dil(){return kok.lang==='en'?'en':'tr'}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function T(tr,en){return dil()==='en'?en:tr}
function num(v){return dil()==='en'?v.toLocaleString('en-US'):v.toLocaleString('tr-TR')}
function tad(k,s){var d=(s?V.st:V.yt)[k];return d?(dil()==='en'?d[1]:d[0]):k}
var AYTR=['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara'],AYEN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function tarih(t){if(!t)return '';var p=t.split('-');return (dil()==='en'?AYEN:AYTR)[+p[1]-1]+' '+p[0]}
function sure(h){if(h==null)return '';if(h<1)return Math.round(h*60)+T(' dk',' min');if(h<48)return (dil()==='en'?h.toFixed(1):h.toFixed(1).replace('.',','))+T(' sa',' h');var g=h/24;return (dil()==='en'?g.toFixed(1):g.toFixed(1).replace('.',','))+T(' gün',' days')}
function pzad(c){return c==='T'?'Trendyol':'Hepsiburada'}
/* ---- secim kutulari */
function doldur(id,list,hepsi,fn){var s=document.getElementById(id),v=s.value;s.innerHTML='<option value="">'+hepsi+'</option>'+list.map(function(k){return '<option value="'+esc(k)+'">'+esc(fn?fn(k):k)+'</option>'}).join('');s.value=v}
function kumeAd(k){return k==='Diğer markalar'?T('Diğer markalar','Other brands'):k}
function secimler(){
 doldur('yMarka',V.k,T('Tüm markalar','All brands'),kumeAd);doldur('sMarka',V.k,T('Tüm markalar','All brands'),kumeAd);
 doldur('yGrup',V.g,T('Tüm ürün grupları','All product groups'),gad);doldur('sGrup',V.g,T('Tüm ürün grupları','All product groups'),gad);
 doldur('yTema',Object.keys(V.yt),T('Tüm temalar','All themes'),function(k){return tad(k)});
 doldur('sTema',Object.keys(V.st),T('Tüm soru temaları','All question themes'),function(k){return tad(k,1)});
 document.getElementById('yAra').placeholder=T('Yorumlarda ara','Search reviews');document.getElementById('sAra').placeholder=T('Sorularda ve cevaplarda ara','Search questions and answers');
}
var GEN={'Klozet kapağı':'Toilet seat','Rezervuar ve iç takım':'Cistern and inner mechanism','Banyo dolabı':'Bathroom cabinet','Duşakabin':'Shower enclosure','Lavabo bataryası':'Basin tap','Banyo ve duş bataryası':'Bath and shower mixer','Eviye bataryası':'Kitchen sink mixer','Duş seti ve sistemi':'Shower set and system','Klozet':'WC','Lavabo':'Washbasin','Ara musluk ve tesisat':'Angle valve and plumbing','Banyo aksesuarı':'Bathroom accessories','Diğer':'Other'};
function gad(g){return dil()==='en'?(GEN[g]||g):g}
/* ---- yorum gezgini */
var yS=40,sS=40;
function pz(id){var b=document.querySelector('#'+id+' .chip.on');return b?b.dataset.v:''}
function yFiltre(){
 var m=document.getElementById('yMarka').value,g=document.getElementById('yGrup').value,t=document.getElementById('yTema').value,q=document.getElementById('yAra').value.toLocaleLowerCase('tr'),p=pz('yPz'),d=pz('yDu');
 return V.y.filter(function(r){
  if(p&&r[0]!==p)return false;if(m&&r[2]!==m)return false;if(g&&r[3]!==g)return false;if(t&&r[11].indexOf(t)<0)return false;
  if(d){var u=r[8]==null?'':(r[8]>=4?'p':(r[8]<=2?'n':'o'));if(u!==d)return false}
  if(q&&(r[10]+' '+r[4]).toLocaleLowerCase('tr').indexOf(q)<0)return false;return true})}
function yCiz(){
 var L=yFiltre(),h=L.slice(0,yS).map(function(r){
  var neg=r[8]!=null&&r[8]<=2;
  var urun=r[5]?'<a href="'+esc(r[5])+'" target="_blank" rel="noopener">'+esc(r[4])+'</a>':esc(r[4]);
  return '<article class="oge"><div class="meta"><span class="pz">'+pzad(r[0])+'</span><span>'+esc(r[1])+'</span><span>'+esc(gad(r[3]))+'</span><span>'+tarih(r[9])+'</span>'+
  (r[8]!=null?'<span class="yildiz" aria-label="'+r[8]+'/5">'+'★★★★★'.slice(0,r[8])+'<span style="opacity:.25">'+'★★★★★'.slice(0,5-r[8])+'</span></span>':'')+
  (r[6]?'<span class="res">'+T('VitrA resmi mağaza','VitrA official store')+'</span>':(r[7]?'<span>'+T('Satıcı: ','Seller: ')+esc(r[7])+'</span>':''))+
  '</div><div class="urun">'+urun+'</div><p class="metin">'+esc(r[10])+'</p><div>'+r[11].map(function(k){return '<span class="tm'+(neg?' n':'')+'">'+esc(tad(k))+'</span>'}).join('')+'</div></article>'}).join('');
 document.getElementById('yListe').innerHTML=h||'<p class="say">'+T('Bu filtrelerle eşleşen yorum bulunmuyor.','No reviews match these filters.')+'</p>';
 document.getElementById('ySay').textContent=T(num(L.length)+' yorum · en yeni üstte',num(L.length)+' reviews · newest first');
 document.getElementById('yDaha').hidden=L.length<=yS}
function sFiltre(){
 var m=document.getElementById('sMarka').value,g=document.getElementById('sGrup').value,t=document.getElementById('sTema').value,q=document.getElementById('sAra').value.toLocaleLowerCase('tr'),p=pz('sPz');
 return V.s.filter(function(r){if(p&&r[0]!==p)return false;if(m&&r[2]!==m)return false;if(g&&r[3]!==g)return false;if(t&&r[12].indexOf(t)<0)return false;
  if(q&&(r[6]+' '+r[8]+' '+r[4]).toLocaleLowerCase('tr').indexOf(q)<0)return false;return true})}
function sCiz(){
 var L=sFiltre(),h=L.slice(0,sS).map(function(r){
  var urun=r[5]?'<a href="'+esc(r[5])+'" target="_blank" rel="noopener">'+esc(r[4])+'</a>':esc(r[4]);
  var kim=r[10]?'<span class="res">'+T('VitrA resmi mağaza','VitrA official store')+'</span>':(r[9]?esc(r[9]):'');
  return '<article class="oge"><div class="meta"><span class="pz">'+pzad(r[0])+'</span><span>'+esc(r[1])+'</span><span>'+esc(gad(r[3]))+'</span><span>'+tarih(r[7])+'</span></div><div class="urun">'+urun+'</div>'+
  '<p class="metin"><b>'+T('Soru: ','Question: ')+'</b>'+esc(r[6])+'</p>'+
  (r[8]?'<div class="cev"><b>'+T('Cevap','Answer')+'</b>'+(kim?' · '+kim:'')+(r[11]!=null?' · '+sure(r[11]):'')+'<br>'+esc(r[8])+'</div>':'<div class="cev">'+T('Cevap bulunmuyor.','No answer.')+'</div>')+
  '<div style="margin-top:6px">'+r[12].map(function(k){return '<span class="tm">'+esc(tad(k,1))+'</span>'}).join('')+'</div></article>'}).join('');
 document.getElementById('sListe').innerHTML=h||'<p class="say">'+T('Bu filtrelerle eşleşen soru bulunmuyor.','No questions match these filters.')+'</p>';
 document.getElementById('sSay').textContent=T(num(L.length)+' soru · en yeni üstte',num(L.length)+' questions · newest first');
 document.getElementById('sDaha').hidden=L.length<=sS}
['yMarka','yGrup','yTema','yAra'].forEach(function(id){document.getElementById(id).addEventListener('input',function(){yS=40;yCiz()})});
['sMarka','sGrup','sTema','sAra'].forEach(function(id){document.getElementById(id).addEventListener('input',function(){sS=40;sCiz()})});
document.querySelectorAll('.chips').forEach(function(g){g.addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;g.querySelectorAll('.chip').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});if(g.id[0]==='y'){yS=40;yCiz()}else{sS=40;sCiz()}})});
document.getElementById('yDaha').addEventListener('click',function(){yS+=40;yCiz()});
document.getElementById('sDaha').addEventListener('click',function(){sS+=40;sCiz()});
/* ---- sekmeler */
document.querySelectorAll('.tabs').forEach(function(t){t.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
 t.querySelectorAll('button').forEach(function(x){var on=x===b;x.setAttribute('aria-selected',on);var p=document.getElementById(x.getAttribute('aria-controls'));if(p)p.hidden=!on})})});

/* ---- tablo siralama */
function hucreDeger(td){var v=td.getAttribute('data-v');if(v!==null){return v===''?null:+v}var t=(td.innerText||'').trim();return t===''||t==='-'?null:t}
function sirala(t,ci,th){
 var yon=th.getAttribute('aria-sort')==='descending'?'ascending':'descending';
 [].forEach.call(t.tHead.rows[0].cells,function(c){c.removeAttribute('aria-sort')});th.setAttribute('aria-sort',yon);
 var tb=t.tBodies[0],rows=[].slice.call(tb.rows);
 rows.sort(function(a,b){var x=hucreDeger(a.cells[ci]),y=hucreDeger(b.cells[ci]);if(x===null&&y===null)return 0;if(x===null)return 1;if(y===null)return -1;
  var r=(typeof x==='number'&&typeof y==='number')?x-y:String(x).localeCompare(String(y),dil());return yon==='ascending'?r:-r});
 rows.forEach(function(r){tb.appendChild(r)})}
document.querySelectorAll('table.srt').forEach(function(t){[].forEach.call(t.tHead.rows[0].cells,function(th,ci){th.tabIndex=0;th.setAttribute('role','columnheader');
 th.addEventListener('click',function(){sirala(t,ci,th)});th.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sirala(t,ci,th)}})})});
/* ---- ozet tablosu suzgeci */
function ozSuz(){var q=document.getElementById('ozAra').value.toLocaleLowerCase(dil()==='en'?'en':'tr'),g=document.getElementById('ozGrup').value,gor=0,top=0;
 var panel=[].slice.call(document.querySelectorAll('table.ozt')).filter(function(t){return !t.closest('[hidden]')})[0];
 document.querySelectorAll('table.ozt').forEach(function(t){[].forEach.call(t.tBodies[0].rows,function(r){
  var ok=(!g||r.dataset.g===g)&&(!q||(r.innerText||r.textContent).toLocaleLowerCase(dil()==='en'?'en':'tr').indexOf(q)>=0);
  r.classList.toggle('gizli',!ok);if(t===panel){top++;if(ok)gor++}})});
 document.getElementById('ozSay').textContent=T(gor+' / '+top+' satır',gor+' / '+top+' rows')}
['ozAra','ozGrup'].forEach(function(id){document.getElementById(id).addEventListener('input',ozSuz)});
document.querySelectorAll('.tabs').forEach(function(t){t.addEventListener('click',function(){setTimeout(ozSuz,0)})});
/* ---- yaninda gelen derin baglanti: #yorumlar?marka=VitrA */
function derin(){var h=location.hash||'';var m=h.match(/marka=([^&]+)/);if(m){var v=decodeURIComponent(m[1]);['yMarka','sMarka'].forEach(function(id){document.getElementById(id).value=v})}}
/* ---- dil ve tema */
function dilKur(l){kok.lang=l;document.getElementById('dil').querySelector('b').textContent=l==='en'?'TR':'EN';document.title=l==='en'?'VitrA | Reviews and Q&A Set':'VitrA | Yorum ve Soru Seti';secimler();derin();yCiz();sCiz();document.querySelectorAll('#ozGrup option').forEach(function(o){o.textContent=o.getAttribute(l==='en'?'data-en':'data-tr')});var oa=document.getElementById('ozAra');oa.placeholder=oa.getAttribute(l==='en'?'data-ph-en':'data-ph-tr');ozSuz()}
document.getElementById('dil').addEventListener('click',function(){var l=dil()==='en'?'tr':'en';try{localStorage.setItem('vitra-dil',l)}catch(e){}dilKur(l)});
document.getElementById('tema').addEventListener('click',function(){kok.setAttribute('data-theme',kok.getAttribute('data-theme')==='dark'?'light':'dark')});
var l0='tr';try{l0=localStorage.getItem('vitra-dil')||'tr'}catch(e){}
dilKur(l0==='en'?'en':'tr');
})();
"""
    TEMA_BTN = ('<button class="btn" type="button" id="tema" aria-label="Tema değiştir" title="Tema değiştir"><svg class="gunes" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/>'
                '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="ay" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>')
    DIL_BTN = '<button class="btn" type="button" id="dil" aria-label="Dil / Language"><b>EN</b></button>'

    def sekme(anah, parcalar):
        b = "".join('<button type="button" role="tab" aria-selected="%s" aria-controls="%s-%d">%s</button>' % ("true" if i == 0 else "false", anah, i, ad) for i, (ad, _) in enumerate(parcalar))
        p = "".join('<div role="tabpanel" id="%s-%d"%s>%s</div>' % (anah, i, "" if i == 0 else " hidden", h) for i, (_, h) in enumerate(parcalar))
        return '<div class="tabs" role="tablist">%s</div>%s' % (b, p)

    def chips(id_, ogeler):
        return '<div class="chips" id="%s" role="group">%s</div>' % (id_, "".join('<button type="button" class="chip%s" data-v="%s" aria-pressed="%s">%s</button>' % (" on" if i == 0 else "", v, "true" if i == 0 else "false", ad) for i, (v, ad) in enumerate(ogeler)))

    PZ = [("", T("Tümü", "All")), ("T", "Trendyol"), ("H", "Hepsiburada")]
    DU = [("", T("Tüm puanlar", "All ratings")), ("p", T("Olumlu (4-5)", "Positive (4-5)")), ("o", T("Nötr (3)", "Neutral (3)")), ("n", T("Olumsuz (1-2)", "Negative (1-2)"))]

    vg, rk = A["vg"], A["rakip"]
    DOC = """<!doctype html>
<html lang="tr" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>VitrA | Yorum ve Soru Seti</title><style>%(css)s</style></head><body>
<header class="appbar"><div class="in">
 <div class="bb"><span class="lbl">%(marka)s</span><span class="logo-card"><img src="%(vitra)s" alt="VitrA"></span>
  <a class="geri" href="%(ana)s">← <span class="uzun">%(geri)s</span></a></div>
 <div class="bb">%(dilb)s%(temab)s<span class="lbl">%(haz)s</span><span class="ib"><img src="%(inb)s" alt="Inbound"></span></div>
</div></header>
<main>
<p class="eyebrow">%(eyebrow)s</p>
<h1>%(h1)s</h1>
<p class="lede">%(lede)s</p>
<div class="kpis">%(kpi)s</div>

<h2 id="ozet">%(h_oz)s</h2>
<p class="h2n">%(n_oz)s</p>
%(oz)s
<p class="ins">%(i_oz)s</p>

<h2 id="pain">%(h_pa)s</h2>
<p class="h2n">%(n_pa)s</p>
%(mat)s
<p class="ins">%(i_pa)s</p>

<h2 id="notlar">%(h_no)s</h2>
<p class="h2n">%(n_no)s</p>
%(kart)s

<h2 id="sorukume">%(h_sk)s</h2>
<p class="h2n">%(n_sk)s</p>
%(smat)s
<p class="ins">%(i_sk)s</p>

<h2 id="yorumlar">%(h_y)s</h2>
<p class="h2n">%(n_y)s</p>
<div class="filtre">%(ypz)s%(ydu)s</div>
<div class="filtre"><select id="yMarka" aria-label="Marka"></select><select id="yGrup" aria-label="Ürün grubu"></select><select id="yTema" aria-label="Tema"></select><input id="yAra" type="search" aria-label="Ara"></div>
<p class="say" id="ySay"></p><div class="liste" id="yListe"></div><button class="dahafazla" id="yDaha" type="button">%(daha)s</button>

<h2 id="sorular">%(h_s)s</h2>
<p class="h2n">%(n_s)s</p>
<div class="filtre">%(spz)s</div>
<div class="filtre"><select id="sMarka" aria-label="Marka"></select><select id="sGrup" aria-label="Ürün grubu"></select><select id="sTema" aria-label="Tema"></select><input id="sAra" type="search" aria-label="Ara"></div>
<p class="say" id="sSay"></p><div class="liste" id="sListe"></div><button class="dahafazla" id="sDaha" type="button">%(daha)s</button>

<div class="note"><b>%(yontem_b)s</b> %(yontem)s</div>
</main>
<footer>%(kaynak)s</footer>
<script type="application/json" id="veri">%(veri)s</script>
<script>%(js)s</script>
</body></html>""" % {
        "css": CSS, "marka": T("Marka", "Brand"), "vitra": VITRA, "ana": ANA, "geri": T("Rapora dön", "Back to the report"), "dilb": DIL_BTN, "temab": TEMA_BTN,
        "haz": T("Hazırlayan", "Prepared by"), "inb": INBOUND,
        "eyebrow": T("VitrA TÜRKİYE · PAZARYERİ YORUMLARI VE SORU-CEVAP", "VitrA TURKEY · MARKETPLACE REVIEWS AND Q&amp;A"),
        "h1": T("Yorum ve Soru Seti: Marka ve Pazaryeri Kırılımı", "Reviews and Q&amp;A Set: Brand and Marketplace Breakdown"),
        "lede": T("Trendyol ve Hepsiburada'da VitrA, Artema ve rakip markaların ürün sayfalarındaki %s yorum ve %s soru-cevap kaydı; yorumlar puana göre olumlu, nötr ve olumsuz olarak ayrılmış, metinler pain point ve güçlü yön temalarına kümelenmiştir. VitrA resmi mağazasının Trendyol panel kayıtları da kapsama dahildir. Dönem: %s - %s; yorumların %s'i son 12 aya (Eki 2025 - Eki 2026) aittir."
                  % (tr_s(TOP["yorum"], 0), tr_s(TOP["soru"], 0), "%s %s" % (ay_tr[d0[5:7]], d0[:4]), "%s %s" % (ay_tr[d1[5:7]], d1[:4]), "%" + tr_s(TOP["son12"], 0)),
                  "%s reviews and %s Q&amp;A records from the product pages of VitrA, Artema and competitor brands on Trendyol and Hepsiburada; reviews are split into positive, neutral and negative by rating, and texts are clustered into pain point and strength themes. Trendyol panel records of the VitrA official store are also included. Period: %s - %s; %s of reviews are from the last 12 months (Oct 2025 - Oct 2026)."
                  % (en_s(TOP["yorum"], 0), en_s(TOP["soru"], 0), "%s %s" % (ay_en[d0[5:7]], d0[:4]), "%s %s" % (ay_en[d1[5:7]], d1[:4]), en_s(TOP["son12"], 0) + "%")),
        "kpi": KPI,
        "h_oz": T("Marka ve pazaryeri özeti", "Brand and marketplace summary"),
        "n_oz": T("Sütun başlığına tıklayarak sıralayabilir, marka veya tema adıyla ve marka grubuyla süzebilirsiniz. Ortalama puan ve duygu dağılımı tüm yorumlardan, tema payları metinli yorumlardan hesaplanmıştır. Pain point payı: olumsuz (1-2 puan) metinli yorumların ilgili temaya değinen oranı (olumsuz metinli yorumu 15'in altındaki satırlarda gösterilmemiştir); güçlü yön payı: olumlu (4-5 puan) metinli yorumlardaki oran. VitrA ve Artema satırları vurgulanmıştır.",
                  "Click a column header to sort, and filter by brand or theme name and by brand group. Average rating and sentiment split are calculated from all reviews, theme shares from reviews with text. Pain point share: the share of negative (1-2 star) text reviews mentioning the theme (not shown for rows with fewer than 15 negative text reviews); strength share: the share among positive (4-5 star) text reviews. VitrA and Artema rows are highlighted."),
        "oz": OZF + sekme("oz", [(T("İki pazaryeri", "Both marketplaces"), OZ["tum"]), ("Trendyol", OZ["ty"]), ("Hepsiburada", OZ["hb"])]),
        "i_oz": T("VitrA ve Artema yorumlarında olumsuz pay %s, rakip markalarda %s'tir. Ortalama puan VitrA'da %s, Artema'da %s düzeyindedir."
                  % ("%" + tr_s(vg["olumsuz"]), "%" + tr_s(rk["olumsuz"]), tr_s(M["VitrA"]["ort_puan"], 2), tr_s(M["Artema"]["ort_puan"], 2)),
                  "The negative share is %s in VitrA and Artema reviews and %s for competitor brands. The average rating is %s for VitrA and %s for Artema."
                  % (en_s(vg["olumsuz"]) + "%", en_s(rk["olumsuz"]) + "%", en_s(M["VitrA"]["ort_puan"], 2), en_s(M["Artema"]["ort_puan"], 2))),
        "h_pa": T("Pain point matrisi", "Pain point matrix"),
        "n_pa": T("Her hücre, markanın olumsuz metinli yorumlarından ilgili temaya değinenlerin payıdır; bir yorum birden fazla temaya girebilir. Olumsuz metinli yorumu 15'in altında kalan markalarda hücre boş bırakılmıştır. Renk yoğunluğu payla artar.",
                  "Each cell is the share of the brand's negative text reviews that mention the theme; a review may fall into more than one theme. Cells are left blank for brands with fewer than 15 negative text reviews. Colour intensity rises with the share."),
        "mat": MAT,
        "i_pa": T("Rakiplerin tamamında olumsuz yorumların en sık değindiği konular iade ve satıcı iletişimi, malzeme ve sağlamlık ile kırık veya hasarlı ürün teslimatıdır; bu üç tema kategori genelindeki ortak pain point'lerdir. VitrA'da kırık veya hasarlı ürün payı (%s) rakip ortalamasının (%s) üzerindedir."
                  % ("%" + tr_s(M["VitrA"]["tema_neg"]["kirik"]), "%" + tr_s(rk["tema_neg"]["kirik"])),
                  "Across all competitors, the topics most often raised in negative reviews are returns and seller contact, material and sturdiness, and broken or damaged deliveries; these three themes are category-wide pain points. At VitrA the broken or damaged product share (%s) is above the competitor average (%s)."
                  % (en_s(M["VitrA"]["tema_neg"]["kirik"]) + "%", en_s(rk["tema_neg"]["kirik"]) + "%")),
        "h_no": T("Marka notları", "Brand notes"),
        "n_no": T("✓ olumlu yorumlarda en sık geçen güçlü yönler, ▲ olumsuz yorumlarda en sık geçen pain point'ler (yalnız %12 ve üzeri), ? en sık soru temaları.",
                  "✓ strengths most often mentioned in positive reviews, ▲ pain points most often mentioned in negative reviews (12% and above only), ? most frequent question themes."),
        "kart": KART,
        "h_sk": T("Soru kümeleri: marka bazında", "Question clusters by brand"),
        "n_sk": T("Her hücre, markanın sorularından ilgili temaya giren payıdır; bir soru birden fazla temaya girebilir. Cevap süresi Hepsiburada'da soru ve cevap zaman damgasından, Trendyol'da sayfadaki cevap süresi ifadesinden ve VitrA resmi mağaza panelinden hesaplanmıştır. Herkese açık sayfalarda yalnız cevaplanmış sorular listelendiği için cevaplanma oranı karşılaştırılmamıştır.",
                  "Each cell is the share of the brand's questions falling into the theme; a question may fall into more than one theme. Answer time is calculated from question and answer timestamps on Hepsiburada, from the answer time phrase on the page and the VitrA official store panel on Trendyol. Since public pages list only answered questions, answer rates are not compared."),
        "smat": SMAT,
        "i_sk": T("VitrA sorularında uyumluluk ve kullanım yeri (%s), kutu içeriği (%s) ve ölçü (%s) öne çıkmaktadır. Hepsiburada'da VitrA ürünlerine gelen soruların %s'i VitrA resmi mağazası tarafından cevaplanmış, kalan bölüm aynı ürünü satan diğer satıcılarca yanıtlanmıştır."
                  % ("%" + tr_s(dict((t, r) for t, _, r in S["VitrA"]["tema"]).get("uyum", 0)), "%" + tr_s(dict((t, r) for t, _, r in S["VitrA"]["tema"]).get("icerik", 0)),
                     "%" + tr_s(dict((t, r) for t, _, r in S["VitrA"]["tema"]).get("olcu", 0)), "%" + tr_s(S["VitrA"]["kanal_profil"]["Hepsiburada"]["resmi_cevap"] or 0)),
                  "Compatibility and place of use (%s), box contents (%s) and size (%s) stand out in VitrA questions. On Hepsiburada, %s of questions on VitrA products were answered by the VitrA official store, the rest by other sellers of the same product."
                  % (en_s(dict((t, r) for t, _, r in S["VitrA"]["tema"]).get("uyum", 0)) + "%", en_s(dict((t, r) for t, _, r in S["VitrA"]["tema"]).get("icerik", 0)) + "%",
                     en_s(dict((t, r) for t, _, r in S["VitrA"]["tema"]).get("olcu", 0)) + "%", en_s(S["VitrA"]["kanal_profil"]["Hepsiburada"]["resmi_cevap"] or 0) + "%")),
        "h_y": T("Yorumlar", "Reviews"),
        "n_y": T("Metinli yorumların tamamı; pazaryeri, marka, ürün grubu, puan ve temaya göre süzülebilir. Yorum metinleri kullanıcının yazdığı gibidir; kişisel bilgi içeren ifadeler maskelenmiştir.",
                 "All reviews with text; filter by marketplace, brand, product group, rating and theme. Review texts are as written by users; expressions containing personal information are masked."),
        "ypz": chips("yPz", PZ), "ydu": chips("yDu", DU), "spz": chips("sPz", PZ), "daha": T("Daha fazla göster", "Show more"),
        "h_s": T("Sorular ve cevaplar", "Questions and answers"),
        "n_s": T("Ürün sayfalarındaki soru-cevap kayıtları; cevabı veren satıcı ve cevap süresi ile birlikte.", "Q&amp;A records on product pages, with the answering seller and answer time."),
        "yontem_b": T("Yöntem:", "Method:"),
        "yontem": T("Duygu sınıfı puandan türetilmiştir (4-5 olumlu, 3 nötr, 1-2 olumsuz). Temalar Türkçe anahtar ifade kurallarıyla atanmıştır; bir metin birden fazla temaya girebilir ve kısa övgü cümleleri (\"güzel\", \"teşekkürler\") temasız kalabilir. Rakip örneklemi, iki pazaryerinde çok satan ve en çok değerlendirilen ürünlerden seçilmiştir; ürün başına en fazla 50-100 yorum ve 20 soru alınmıştır. Yorumcu ve soru soran adları kayda alınmamıştır.",
                    "The sentiment class is derived from the rating (4-5 positive, 3 neutral, 1-2 negative). Themes are assigned with Turkish key phrase rules; a text may fall into more than one theme and short praise sentences (\"nice\", \"thanks\") may remain without a theme. The competitor sample was selected from best-selling and most-reviewed products on both marketplaces; at most 50-100 reviews and 20 questions were collected per product. Reviewer and asker names were not recorded."),
        "kaynak": T("Kaynak: Trendyol ve Hepsiburada ürün sayfaları (herkese açık değerlendirme ve soru-cevap kayıtları) · VitrA resmi mağaza Trendyol paneli (ürün değerlendirmeleri ve ürün soruları) · 03.10.2026",
                    "Source: Trendyol and Hepsiburada product pages (public reviews and Q&amp;A records) · VitrA official store Trendyol panel (product reviews and product questions) · 03.10.2026"),
        "veri": VJ, "js": JS}
    if "—" in DOC: raise SystemExit("alt sayfada em dash var")
    yol = os.path.join(veri.KOK, AD)
    open(yol, "w", encoding="utf-8").write(DOC)
    print("kaydedildi:", yol, len(DOC), "karakter ·", len(yor), "yorum ·", len(sor), "soru")


if __name__ == "__main__":
    main()
