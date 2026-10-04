# -*- coding: utf-8 -*-
"""Rehber (blog, /ilham-veren-fikirler/) yazılarının adresteki konuya göre gruplanması · GEO ve Organik Kanal bölümleri ortak kullanır."""
GRUP = [("tamir", "Tamir, temizlik ve bakım", "Repair, cleaning and maintenance"), ("montaj", "Montaj ve kurulum", "Installation and fitting"),
        ("secim", "Seçim, ölçü ve \"nedir\" rehberleri", "Selection, size and \"what is\" guides"), ("plan", "Planlama ve tadilat", "Planning and renovation"),
        ("dekor", "Dekorasyon, trend ve karo modelleri", "Decoration, trends and tile designs"), ("surd", "Sürdürülebilirlik ve kurumsal", "Sustainability and corporate")]
GAD = {a: (b, c) for a, b, c in GRUP}
def grup(s_):
    if any(k_ in s_ for k_ in ("surdurul", "yesil-", "dongusel", "geri-donus", "cevre", "dunya-", "kuresel", "inovasyon-gunu", "temas-yoluyla", "herkes-icin")): return "surd"
    if any(k_ in s_ for k_ in ("temizl", "tamir", "hijyen")): return "tamir"
    if any(k_ in s_ for k_ in ("montaj", "takilir", "dosenir")): return "montaj"
    if any(k_ in s_ for k_ in ("tadilat", "yenile", "planlama", "mimari", "engelli")): return "plan"
    if any(k_ in s_ for k_ in ("secim", "secil", "secerken", "nedir", "nelerdir", "olculeri", "kullanisli", "saglikli", "quantumflush", "satin-alma", "kuvet-mi")): return "secim"
    return "dekor"
def grup_ad(s_): return GAD[grup(s_)]
