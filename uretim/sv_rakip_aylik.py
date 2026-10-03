# -*- coding: utf-8 -*-
"""Sikayetvar rakip marka sayfalarindan son 24 ayin aylik sikayet sayisi (VitrA serisiyle ayni yontem: marka sayfasindaki tum sikayetler).
Yalniz tarih sayilir; sikayet sahibi adi ya da metni kaydedilmez. Istekler arasinda 1,5 sn beklenir; 429'da beklenir, tekrarda vazgecilir."""
import re, json, time, os, collections, urllib.request
import veri
AY = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
BAS, SON = "2024-10", "2026-09"
DT = re.compile(r'(?:aria-label="|>)(\d{1,2}) (' + "|".join(AY) + r') (\d{4}) \d{2}:\d{2}["<]')
def sayfa(slug, n):
    import subprocess
    for deneme in range(3):
        r = subprocess.run(["curl", "-s", "-L", "-A", UA, "-H", "Accept-Language: tr", "-w", "\n%{http_code}", "https://www.sikayetvar.com/%s?page=%d" % (slug, n)], capture_output=True, text=True, timeout=60)
        govde, _, kod = r.stdout.rpartition("\n")
        if kod == "429": time.sleep(30); continue
        if kod == "404": return ""
        if kod != "200": return None
        return govde
    return None
out = {}
for marka, slug in [("Kale", "kale"), ("Creavit", "creavit"), ("Geberit", "geberit"), ("Bocchi", "bocchi"), ("E.C.A. (Serel dahil)", "eca")]:
    say = collections.Counter(); n = 1; dur = None
    while True:
        h = sayfa(slug, n)
        if h is None: dur = "hata"; break
        kartlar = h.split('data-ga-element="Complaint_Card"')[1:]
        if not kartlar: dur = "bitti"; break
        en_eski = None
        for k_ in kartlar:
            m = DT.search(k_)
            if not m: continue
            a = "%s-%02d" % (m.group(3), AY[m.group(2)])
            en_eski = a if en_eski is None or a < en_eski else en_eski
            if BAS <= a <= SON: say[a] += 1
        print(marka, n, len(kartlar), en_eski, flush=True)
        if en_eski and en_eski < BAS: dur = "pencere"; break
        n += 1; time.sleep(1.5)
        if n > 120: dur = "sinir"; break
    out[marka] = {"aylik": dict(sorted(say.items())), "sayfa": n, "durus": dur, "toplam": sum(say.values())}
    print(marka, out[marka]["toplam"], dur, flush=True)
json.dump({"kaynak": "Şikayetvar marka sayfaları · %s - %s · 03.10.2026" % (BAS, SON), "markalar": out},
          open(os.path.join(veri.V, "ham", "derin", "sikayetvar", "rakip_aylik.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("kaydedildi")
