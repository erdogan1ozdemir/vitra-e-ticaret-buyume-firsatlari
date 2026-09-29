# -*- coding: utf-8 -*-
"""Sikayetvar ortak yardimcilar: curl ile sayfa cekme (istekler arasi 2-4 sn), marka sayfasi ayristirma.
Giris yapilmaz, form doldurulmaz. Yazar adi, telefon, siparis no ciktiya alinmaz."""
import json, random, re, subprocess, time, html as _h, base64
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
AYLAR = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}
BAZ = "https://www.sikayetvar.com"

def cek(yol, bekle=True):
    """yol: '/vitra?page=2'. (durum, html) dondurur."""
    if bekle:
        time.sleep(random.uniform(2.0, 4.0))
    for i in range(3):
        r = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, "-H", "Accept-Language: tr-TR,tr;q=0.9",
                            "-w", "\n__KOD__%{http_code}", BAZ + yol], capture_output=True)
        out = r.stdout.decode("utf-8", "replace")
        m = re.search(r"\n__KOD__(\d+)$", out)
        kod = int(m.group(1)) if m else 0
        body = out[:m.start()] if m else out
        if kod == 200 or kod in (301, 302, 308, 404):
            return kod, body
        time.sleep(10 * (i + 1))
    return kod, body

def _rsc(h):
    return h.replace('\\"', '"').replace("\\u0026", "&")

def _json_after(txt, anahtar, acilis):
    i = txt.find(anahtar)
    if i < 0:
        return None
    j = txt.find(acilis, i)
    try:
        return json.JSONDecoder().raw_decode(txt[j:])[0]
    except Exception:
        return None

def marka_bilgi(h):
    """Marka sayfasi ust bilgileri: baslik, puan, toplam sikayet, donem istatistikleri."""
    r = _rsc(h)
    b = {}
    m = re.search(r"<title>([^<]*)</title>", h); b["baslik"] = _h.unescape(m.group(1)) if m else None
    m = re.search(r'"aggregateRating":\{"@type":"AggregateRating","bestRating":(\d+),"worstRating":\d+,"ratingValue":(\d+),"ratingCount":(\d+)', r)
    if m: b["puan_100"], b["degerlendirme_sayisi"] = int(m.group(2)), int(m.group(3))
    m = re.search(r'"totalComplaintCount":(\d+),"title"', r)
    if m: b["toplam_sikayet"] = int(m.group(1))
    m = re.search(r'"maxCount":(\d+),"lastIndexedPage":(\d+)', r)
    if m: b["sayfa_sayisi"] = int(m.group(1))
    m = re.search(r'"companyId":(\d+)', r)
    if m: b["company_id"] = int(m.group(1))
    cs = _json_after(r, '"companyStats":', "[")
    if cs:
        b["donemler"] = {c["period"]: {k: c.get(k) for k in ("resolveRatio", "surveyCount", "resolvedCount", "complaintCount")} for c in cs}
        b["yildiz_dagilimi_tum"] = {str(x["point"]): x["count"] for x in cs[0].get("starDistribution", [])}
    m = re.search(r'Bu rapor, güncel şikayetler esas alınarak', h)
    # AiVar ozet metni (marka karnesi)
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", h, flags=re.S)
    t = _h.unescape(re.sub(r"<[^>]+>", "\n", t)); t = re.sub(r"\n\s*\n+", "\n", t)
    i = t.find("ile Marka Karnesi")
    if i >= 0:
        j = t.find("En Sık Karşılaşılan", i)
        b["aivar_ozet"] = t[i + len("ile Marka Karnesi"):j].strip().replace("\n", " ")
    return b

def _tarih(s, yil_yedek=2026):
    m = re.search(r"(\d{1,2}) (\w+?) (?:(\d{4}) )?(\d{2}):(\d{2})", s or "")
    if not m: return None
    g, ay, yil = int(m.group(1)), AYLAR.get(m.group(2)), int(m.group(3) or yil_yedek)
    return "%04d-%02d-%02d" % (yil, ay, g) if ay else None

def _rsc_harita(h):
    """baslik -> (sikayet_id, yol) : RSC yukunden."""
    r = _rsc(h); d = {}
    for m in re.finditer(r'"title":"([^"]*)","href":"[^"]*","encodedHref":"([A-Za-z0-9_-]+)","noIndexed":(?:true|false),"complaintId":(\d+)', r):
        try:
            yol = base64.urlsafe_b64decode(m.group(2) + "=" * (-len(m.group(2)) % 4)).decode()
        except Exception:
            yol = None
        d[_h.unescape(m.group(1))] = (int(m.group(3)), yol)
    return d

def sikayetler(h):
    """Sayfadaki sikayet kartlari."""
    hm = _rsc_harita(h)
    out = []
    for a in re.findall(r'<article[^>]*data-ga-element="Complaint_Card".*?</article>', h, re.S):
        d = {}
        m = re.search(r'<h3[^>]*>.*?title="([^"]*)"', a, re.S)
        d["baslik"] = _h.unescape(m.group(1)) if m else None
        m = re.search(r'<h3[^>]*><a[^>]*href="([^"]+)"', a)
        yol = m.group(1) if m else None
        sid = None
        if d["baslik"] in hm:
            sid, y2 = hm[d["baslik"]]; yol = yol or y2
        d["id"] = sid; d["url"] = (BAZ + yol) if yol else None
        m = re.search(r'aria-label="(\d{1,2} \w+ \d{4} \d{2}:\d{2})"', a)
        ts = m.group(1) if m else None
        if not ts:
            m = re.search(r'>(\d{1,2} \w+ (?:\d{4} )?\d{2}:\d{2})<', a); ts = m.group(1) if m else None
        d["tarih"] = _tarih(ts); d["tarih_ham"] = ts
        m = re.search(r'ic-view[^>]*></use></svg><span>([\d.]+)</span>', a)
        d["goruntulenme"] = int(m.group(1).replace(".", "")) if m else None
        d["cozuldu"] = "Complaint_Card_Solved" in a
        d["yayindan_kaldirildi"] = "yayından kaldırdı" in a
        m = re.search(r'Result_Stars.*?<div class="[^"]*">(\d)</div></div></span>', a, re.S)
        d["yildiz"] = int(m.group(1)) if m else None
        p = re.search(r"<p[^>]*>(.*?)</p>", a, re.S)
        txt = ""
        if p:
            s = re.sub(r"<span[^>]*>\.\.\.</span>", " ", p.group(1))
            txt = _h.unescape(re.sub(r"<[^>]+>", "", s))
            txt = re.sub(r"\s+", " ", txt).strip()
        d["metin"] = txt
        out.append(d)
    return out
