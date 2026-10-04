# -*- coding: utf-8 -*-
"""Search Console verisi, 2. çekim (04.10.2026) · OAuth token (mcp-gsc-main/token.json) ile doğrudan API.
Dönemler: 12 ay = 1 Eki 2025 - 30 Eyl 2026 (son günler dataState=all ile ön veri), aylık seri Haz 2025 - Eyl 2026,
yapay zeka özellikleri karşılaştırması: 1 Haz - 29 Eyl 2026 ve 2025 (Search Console dışa aktarımı 29 Eylül'de bitiyor)."""
import json, os, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
G = "/Users/Erdo/Desktop/03_Geliştirme/API_Entegrasyonlar/google_search_console/mcp-gsc-main"
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(P, "veri/ham/gsc2"); os.makedirs(OUT, exist_ok=True)
cred = Credentials.from_authorized_user_file(os.path.join(G, "token.json"), ["https://www.googleapis.com/auth/webmasters.readonly"])
if cred.expired and cred.refresh_token: cred.refresh(Request())
svc = build("searchconsole", "v1", credentials=cred, cache_discovery=False)
SITE = "sc-domain:vitra.com.tr"
def sorgu(dims, start, end, limit=25000, filters=None):
    rows = []; startRow = 0
    while True:
        body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": min(25000, limit - len(rows)), "startRow": startRow, "type": "web", "dataState": "all"}
        if filters: body["dimensionFilterGroups"] = [{"filters": filters}]
        for dene in range(4):
            try: r = svc.searchanalytics().query(siteUrl=SITE, body=body).execute(); break
            except Exception as e: print("tekrar", e); time.sleep(5 * (dene + 1))
        rr = r.get("rows", []); rows += rr
        if len(rr) < body["rowLimit"] or len(rows) >= limit: break
        startRow += len(rr); time.sleep(0.3)
    return rows
def kaydet(ad, veri):
    json.dump(veri, open(os.path.join(OUT, ad + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(ad, len(veri) if isinstance(veri, list) else {k: len(v) for k, v in veri.items()}, flush=True)
BLOG = [{"dimension": "page", "operator": "contains", "expression": "ilham-veren-fikirler"}]
Y1, Y2 = "2025-10-01", "2026-09-30"
kaydet("gunluk_cihaz", sorgu(["date", "device"], "2025-06-01", Y2))
kaydet("ulke_12ay", sorgu(["country"], Y1, Y2, 200))
kaydet("sorgu_12ay", sorgu(["query"], Y1, Y2, 50000))
AYLAR = ["2025-%02d" % m for m in range(6, 13)] + ["2026-%02d" % m for m in range(1, 10)]
SON = {"02": 28, "04": 30, "06": 30, "09": 30, "11": 30}
sa = {}
for a in AYLAR:
    son = SON.get(a[5:], 31)
    sa[a] = sorgu(["page"], a + "-01", "%s-%02d" % (a, son), 100000)
    print(" ", a, len(sa[a]), flush=True)
kaydet("sayfa_aylik", sa)
# yapay zeka özellikleri karşılaştırması · blog sayfaları
kaydet("blog_sayfa_genai", sorgu(["page"], "2026-05-18", "2026-09-29", 25000, BLOG))
for etk, (a, b) in {"2026": ("2026-06-01", "2026-09-29"), "2025": ("2025-06-01", "2025-09-29")}.items():
    kaydet("blog_sayfa_%s" % etk, sorgu(["page"], a, b, 25000, BLOG))
    kaydet("blog_sorgu_sayfa_%s" % etk, sorgu(["query", "page"], a, b, 50000, BLOG))
    kaydet("sorgu_%s" % etk, sorgu(["query"], a, b, 50000))
    kaydet("blog_gunluk_%s" % etk, sorgu(["date"], a.replace("06-01", "05-18") if etk == "2026" else a, b, 500, BLOG))
print("bitti")
