// Trendyol satici adi cozumleme: cozulmemis merchantId icin, o saticinin listede gorulen ilk urun sayfasindan yalniz mağaza adi okunur:
//   fetch('/x/x-p-'+urunId+'?merchantId='+mid) -> /"merchant":\{"id":(\d+),"name":"([^"]+)"/  (id eslesmesi dogrulanir; vergi no, adres vb. alinmaz). Istekler arasi 3.3 sn.
