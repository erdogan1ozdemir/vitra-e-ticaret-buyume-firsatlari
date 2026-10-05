# -*- coding: utf-8 -*-
"""Site içi arama testi değerlendirmeleri (04.10.2026): b_yolculuk ve b_ga4 ortak kullanır; dil kaydı yapmaz."""
# degerlendirme kurali (04.10.2026): her yolda ilk uc kartin en az ikisi aranan urun tipindeyse o yol uyumlu sayilir; sonuc sayisi 0 ise bos
DEG = {"U": ("Uyumlu", "Consistent"), "T": ("Anlık sonuç uyumlu, sonuç sayfası boş veya ilgisiz", "Instant results fine, results page empty or off-target"),
       "S": ("Anlık sonuç boş ya da ilgisiz, sonuç sayfası uyumlu", "Instant results empty or off-target, results page fine"), "Y": ("İki yolda da ilgili ürün yok", "No relevant product on either path"),
       "D": ("Destek sayfasına yönlendirme yok", "No route to the support page"), "P": ("Kısmen uyumlu: ilk kartlar karışık", "Partly consistent: mixed first cards"), "G": ("VitrA gamı dışında", "Outside VitrA's range")}
DEGK = {"klozet": "P", "asma klozet": "U", "lavabo": "T", "banyo dolabı": "U", "duşakabin": "U", "banyo bataryası": "U", "gömme rezervuar": "P", "havlupan": "P", "evye": "G",
        "duş seti": "U", "klozet kapağı": "U", "iç takım": "U", "rezervuar iç takımı": "P", "şamandıra": "T", "klozet kapağı menteşesi": "S", "kartuş": "Y", "conta": "Y",
        "kumanda paneli": "U", "taharet musluğu": "S", "lavabo sifonu": "U", "klozet kapagi": "P", "dusakabin": "T", "banyo dolabi": "T", "rezarvuar": "T", "klozed": "T",
        "batarya": "T", "80 cm banyo dolabı": "S", "kanalsız klozet": "P", "akıllı klozet": "P", "siyah klozet": "P", "metropole": "U", "sento": "U", "integra": "T",
        "7906B483-0090": "T", "montaj": "U", "yedek parça": "Y", "garanti": "D", "servis": "D"}
