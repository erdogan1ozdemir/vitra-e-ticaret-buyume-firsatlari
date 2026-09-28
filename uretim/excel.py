# -*- coding: utf-8 -*-
"""HTML rapordaki tablolari Excel sekmelerine cevirir (TR). Kaynak: uretilen HTML."""
import os, sys, re, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veri
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
INK = "10332F"; BAS = "434343"; YES = "2E7D32"; KIR = "D32F2F"; COR = "FF7B52"; GOLD = "F5A623"; CT = "FFE3D8"; CD = "E85F36"; GRI = "F0EDE8"
CIZ = Border(top=Side(style="thin", color="E0E0E0"))
def F(b=False, c=INK, sz=10): return Font(name="Calibri", bold=b, color=c, size=sz)
def AL(h="left", w=True): return Alignment(horizontal=h, vertical="center", wrap_text=w)
AD = "VitrA_E-Ticaret_Buyume_Firsatlari"
H = open(os.path.join(veri.KOK, AD + ".html"), encoding="utf-8").read()
S = BeautifulSoup(H, "html.parser")
wb = Workbook(); wb.remove(wb.active)
_num = re.compile(r"^[+\-]?%?\d[\d.]*(,\d+)?%?$")
def deger(t):
    t = " ".join(t.split())
    if not t or t == "-": return t
    if _num.match(t):
        s = t.replace("%", "").replace(".", "").replace(",", ".")
        try:
            v = float(s)
            return int(v) if v.is_integer() and "," not in t else v
        except ValueError: return t
    return t
def yaz(ws, r, c, v, bold=False, renk=INK, h="left", fill=None):
    cell = ws.cell(row=r, column=c, value=v); cell.font = F(bold, renk); cell.alignment = AL(h); cell.border = CIZ
    if fill: cell.fill = PatternFill("solid", fgColor=fill)
    return cell
def sekme(ad, baslik, notlar, basliklar, satirlar, genislik=None):
    ws = wb.create_sheet(re.sub(r"[\[\]:*?/\\]", "", ad)[:31])
    yaz(ws, 1, 1, baslik, True); ws.row_dimensions[1].height = 22
    n_ = len(basliklar)
    c = ws.cell(row=2, column=1, value="\n".join(notlar)); c.font = F(); c.alignment = Alignment(vertical="top", wrap_text=True); c.border = CIZ
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max(n_, 2))
    ws.row_dimensions[2].height = 14 * max(1, sum(math.ceil(len(x_) / 110) for x_ in notlar)) + 6
    hr = 4
    for i, b in enumerate(basliklar, 1):
        cc = ws.cell(row=hr, column=i, value=b); cc.font = F(True, "FFFFFF"); cc.fill = PatternFill("solid", fgColor=BAS); cc.alignment = AL("center"); cc.border = CIZ
    ws.row_dimensions[hr].height = 30
    w = genislik or [max(12, min(60, max([len(str(b))] + [len(str(s[i])) for s in satirlar if i < len(s)]) + 2)) for i, b in enumerate(basliklar)]
    for i, ww in enumerate(w, 1): ws.column_dimensions[get_column_letter(i)].width = ww
    for j, sat in enumerate(satirlar):
        rr = hr + 1 + j; yuk = 15
        for i, dv in enumerate(sat, 1):
            v = deger(dv) if isinstance(dv, str) else dv
            sayisal = isinstance(v, (int, float))
            cell = yaz(ws, rr, i, v, h="center" if sayisal else "left")
            if isinstance(dv, str) and dv.strip().startswith(("+", "-")) and sayisal and ("%" in dv):
                cell.font = F(True, YES if v > 0 else KIR); cell.number_format = '+0.0"%";-0.0"%"'
            elif sayisal and "%" in str(dv): cell.number_format = '0.0"%"'
            elif isinstance(v, int): cell.number_format = "#,##0"
            elif isinstance(v, float): cell.number_format = "#,##0.0"
            if isinstance(dv, str) and dv.startswith("Öncelik"):
                p = {"Öncelik 1": (GOLD, INK), "Öncelik 2": (CT, CD), "Öncelik 3": (GRI, "4A4A4A")}[dv]
                cell.fill = PatternFill("solid", fgColor=p[0]); cell.font = F(True, p[1])
            if isinstance(v, str) and v: yuk = max(yuk, 13 * math.ceil(len(v) / max(8, w[i - 1] - 2)) + 4)
        ws.row_dimensions[rr].height = min(yuk, 300)
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    return ws
def metin(el):
    for s in el.select("span.t"): s.replace_with(s.get_text())   # dil katmani
    return " ".join(el.get_text(" ").split())
# --- bolumler -> sekmeler ---
say = 0
for sec in S.select("main section"):
    sid = sec.get("id"); h2 = sec.find("h2"); bas = metin(h2).split(" ", 1)[1] if h2 else sid
    if sid in ("kaynakca", "sozluk"): continue
    tablolar = sec.select("div.tw table")
    if not tablolar: continue
    src = sec.select_one("p.src"); kaynak = metin(src) if src else ""
    lede = sec.select_one("p.lede"); lede_t = metin(lede) if lede else ""
    for ti, t in enumerate(tablolar, 1):
        h3 = t.find_parent("div").find_previous("h3"); alt = metin(h3) if h3 and h3.find_parent("section") is sec else ""
        thead = [metin(th) for th in t.select("thead th")]
        aciklama = ["%s: %s" % (metin(th), th.get("data-t", "")) for th in t.select("thead th") if th.get("data-t")]
        rows = []
        for tr in t.select("tbody tr"):
            rows.append([metin(td) for td in tr.select("td")])
        notlar = ["Bölüm: %s%s" % (bas, (" · " + alt) if alt else "")]
        if lede_t: notlar.append("Kapsam: " + lede_t)
        if kaynak: notlar.append(kaynak)
        notlar += ["Sütun açıklamaları: " + " | ".join(aciklama)] if aciklama else []
        say += 1
        ad = "%02d %s" % (say, (alt or bas)[:26].replace("/", "-").replace(":", ""))
        sekme(ad, "%s · %s" % (bas, alt or ("Tablo %d" % ti)), notlar, thead, rows)
# kaynakca
rows = []
for li in S.select("ol.kaynakca li"):
    kb = li.select_one(".kb"); a = li.select("a.u"); kt = li.select_one(".kt")
    rows.append([metin(li.select_one(".kn")), metin(kb) if kb else "", " · ".join(x_.get("href") for x_ in a), metin(kt) if kt else ""])
sekme("Kaynakça", "Kaynakça", ["Raporun metnindeki üst simge numaraları bu listeye bağlanmaktadır."], ["No", "Kaynak", "Adres", "Erişim"], rows, [6, 90, 60, 18])
yol = os.path.join(veri.KOK, AD + ".xlsx"); wb.save(yol)
print("kaydedildi:", yol, len(wb.sheetnames), "sekme"); print(wb.sheetnames)
