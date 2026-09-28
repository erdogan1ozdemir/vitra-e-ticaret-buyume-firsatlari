# -*- coding: utf-8 -*-
"""Search Console verisi · OAuth token (mcp-gsc-main/token.json) ile dogrudan API · dosyaya yazar."""
import json, os, sys, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
G = "/Users/Erdo/Desktop/03_Geliştirme/API_Entegrasyonlar/google_search_console/mcp-gsc-main"
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(P, "veri/ham/gsc"); os.makedirs(OUT, exist_ok=True)
cred = Credentials.from_authorized_user_file(os.path.join(G, "token.json"), ["https://www.googleapis.com/auth/webmasters.readonly"])
if cred.expired and cred.refresh_token: cred.refresh(Request())
svc = build("searchconsole", "v1", credentials=cred, cache_discovery=False)
SITE = "sc-domain:vitra.com.tr"
def sorgu(dims, start, end, limit=25000, filters=None, tip="web"):
    rows = []; startRow = 0
    while True:
        body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": min(25000, limit - len(rows)), "startRow": startRow, "type": tip}
        if filters: body["dimensionFilterGroups"] = [{"filters": filters}]
        r = svc.searchanalytics().query(siteUrl=SITE, body=body).execute()
        rr = r.get("rows", []); rows += rr
        if len(rr) < body["rowLimit"] or len(rows) >= limit: break
        startRow += len(rr); time.sleep(0.3)
    return rows
def kaydet(ad, rows, dims):
    json.dump({"site": SITE, "dims": dims, "rows": rows}, open(os.path.join(OUT, ad + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(ad, len(rows))
S, E = "2025-06-01", "2026-09-25"
kaydet("gunluk_cihaz", sorgu(["date", "device"], S, E), ["date", "device"])
kaydet("sayfa_16ay", sorgu(["page"], S, E, 25000), ["page"])
kaydet("sorgu_16ay", sorgu(["query"], S, E, 25000), ["query"])
kaydet("sayfa_ay", sorgu(["page", "date"], S, E, 25000 * 4), ["page", "date"])  # gunluk sayfa · aylik toplanacak
kaydet("sorgu_sayfa", sorgu(["query", "page"], S, E, 25000), ["query", "page"])
kaydet("ulke", sorgu(["country"], S, E, 100), ["country"])
