# -*- coding: utf-8 -*-
"""Kelime evreninden çıkarılan aramaların ortak kuralı (kelime_niyet.py ve ssg_bm.py aynı kuralı kullanır).
Kaynak kategori listesinde banyo alt kategorisine eşlenmiş, ancak Google sonuçlarında banyo dışı niyete kayan genel ifadeler (04.10.2026 SERP kontrolü,
veri/ham/derin/serp/genel_kelime_kontrol_2026-10-04.json) ile mutfak ve genel tezgah aramaları ve marka adı geçen aramalar."""
import re
MARKA = r"vitra|artema|creavit|kale|ece\b|serel|duravit|geberit|grohe|hansgrohe|roca|ideal standard|bien|kütahya|kutahya|çanakkale|canakkale|ege seramik|yurtbay|turkuaz|bocchi|newarc|isvea|toto|eca\b|nsk|ferro|penta|fixet|orka|nemo|dilara|tema\b|koçtaş|koctas|bauhaus|ikea|tekzen|trendyol|hepsiburada|n11|amazon"
BANYO = r"banyo|wc|tuvalet|lavabo|klozet|duş|rezervuar"
GRUP_AD = {"tezgah": ("mutfak ve genel tezgah", "kitchen and general countertop"),
           "kulp_konsol": ("mobilya kulpu ve salon konsolu", "furniture handles and living-room consoles"),
           "cop_kovasi": ("genel çöp kovası", "general waste bins"),
           "pecetelik": ("masa peçeteliği", "table napkin dispensers"),
           "panel": ("elektronik ve uygulama paneli", "electronic and app panels"),
           "dogal_tas": ("doğal taş traverten", "natural travertine stone"),
           "markali": ("marka adı geçen arama", "searches containing a brand name")}


def grup(kw, k2, marka_rx=None):
    """Kelime çıkarılıyorsa grup adını, kalıyorsa None döndürür."""
    if k2 == "Banyo Tezgahları" and not re.search(r"banyo|lavabo", kw): return "tezgah"
    if k2 in ("Banyo Mobilya Tamamlayıcıları", "Banyo Dolabı Kulpları") and re.search(r"kulp|kolu\b|tutacağı|konsol", kw) and not re.search(BANYO, kw): return "kulp_konsol"
    if k2 == "Banyo Çöp Kovaları" and not re.search(BANYO, kw): return "cop_kovasi"
    if kw == "dispenser peçetelik": return "pecetelik"
    if kw in ("smart panel", "akıllı panel"): return "panel"
    if re.fullmatch(r"(kırmızı|gri) traverten", kw): return "dogal_tas"
    if re.search(marka_rx or MARKA, kw): return "markali"
    return None
