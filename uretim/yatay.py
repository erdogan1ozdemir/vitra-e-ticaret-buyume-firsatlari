# -*- coding: utf-8 -*-
"""Yatay ısı tablosu: aylar sütunda, yıllar satırda, altında Değişim satırı ve dönem toplamı. Hücre rengi satır içindeki görece büyüklüğü gösterir.
GSC (b_organik) ile aynı görünüm; GA4 bölümünde kullanılır."""
from ortak import *
from b_talep import AYA, YRENK


def isi_hucre(degerler, ters=False):
    vs = [v for v in degerler if v is not None]; lo, hi = (min(vs), max(vs)) if vs else (0, 1)
    out = []
    for v in degerler:
        if v is None: out.append(None); continue
        t = (v - lo) / (hi - lo) if hi > lo else 0.5
        if ters: t = 1 - t
        out.append(("var(--isi-a)", (t - 0.5) * 2 * 0.5) if t >= 0.5 else ("var(--isi-d)", (0.5 - t) * 2 * 0.5))
    return out


def yatay(m_tr, m_en, ac_tr, ac_en, satirlar, bicim, top_bas=("Oca-Eyl", "Jan-Sep"), top_ac=None, deg_tip="oran", ters=False, deg_sira=(0, 1)):
    """satirlar: [(yil_etiketi, renk, [12 deger | None], toplam | None)]; Değişim satırı deg_sira'daki iki satırın farkıdır.
    deg_tip: 'oran' (yüzde değişim), 'puan' (fark, iki ondalık), 'fark' (fark, bir ondalık; ters ise eksi iyidir)."""
    ta = top_ac or ("Ocak - Eylül toplamı ya da ortalaması; iki yılın kıyaslanabildiği dönem.", "January - September total or average; the period comparable across the two years.")
    bas = [th(m_tr, m_en, ac_tr, ac_en)] + [th(a_, b_, "%s ayının değeri; hücre rengi satır içindeki görece büyüklüğü gösterir." % a_, "Value for %s; the cell colour shows the relative size within the row." % b_, True) for a_, b_ in AYA] + [th(top_bas[0], top_bas[1], ta[0], ta[1], True)]
    rows = []
    for et, renk, v, tv in satirlar:
        hs = isi_hucre(v, ters)
        cells = ['<td class="yil"><i style="background:%s"></i>%s</td>' % (renk, et)]
        for val, h in zip(v, hs):
            cells.append('<td class="n">-</td>' if val is None else '<td class="n yh" style="--yr:%s;--a:%.2f">%s</td>' % (h[0], h[1], bicim(val)))
        cells.append('<td class="n top">%s</td>' % (bicim(tv) if tv is not None else "-"))
        rows.append("<tr>%s</tr>" % "".join(cells))
    a_, b_ = satirlar[deg_sira[0]], satirlar[deg_sira[1]]
    dc = ['<td>%s</td>' % x("Değişim", "Change")]
    for p, q in list(zip(a_[2], b_[2])) + [(a_[3], b_[3])]:
        if p is None or q is None or (deg_tip == "oran" and not p): dc.append('<td class="n">-</td>'); continue
        if deg_tip == "oran": dc.append('<td class="n">%s</td>' % yz((q / p - 1) * 100))
        else:
            d = q - p; t_ = ("+" if d > 0 else "") + (("%.2f" if deg_tip == "puan" else "%.1f") % d).replace(".", ","); x(t_, t_.replace(",", "."))
            iyi = (d < 0) if ters else (d > 0)
            dc.append('<td class="n"><span class="%s">%s</span></td>' % ("up" if iyi and d else ("dn" if d else ""), t_))
    rows.append('<tr class="deg">%s</tr>' % "".join(dc))
    return '<div class="tw yatay xl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % ("".join(bas), "".join(rows))
