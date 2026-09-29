// Hepsiburada kategori / arama sayfasindan "cok satan" ilk 36 urunu okur (browser_evaluate; sayfa yuklendikten sonra calistirilir).
// Kullanim: hepsiburada.com/<kategori>?siralama=coksatan sayfasina git (3-6 sn arayla), sonra bu ifadeyi calistir; sonuc dosyaya kaydedilir.
() => {
  const st = Object.values(window.MORIA.PRODUCTLIST)[0].STATE.data;
  const rows = st.products.map((p, i) => {
    const v = (p.variantList || []).find(x => x.isDefault) || p.variantList[0];
    const l = v.listing || {}, pi = l.priceInfo || {}, cl = l.categorizedLabels || {};
    const tags = [];
    for (const g of Object.values(cl)) { if (Array.isArray(g)) g.forEach(t => { if (t && t.text) tags.push(String(t.text).replace(/<[^>]+>/g, '').slice(0, 60)); else if (t && t.tagName) tags.push(t.tagName); }); }
    return {sira: i + 1, id: p.productId, sku: v.sku, marka: p.brand, ad: v.name, url: v.url, satici: l.merchantName, buybox: v.buyboxOrder, coksatici: v.isMultiSeller,
      fiyat: pi.price, eski: pi.originalPrice, indirim: pi.discountRate, sepet: (l.campaignPriceInfo || {}).discountedPrice || null, sepetTip: (l.campaignPriceInfo || {}).labelText || null,
      puan: p.customerReviewRating, deg: p.customerReviewCount, jet: l.jetDelivery, express: l.expressDelivery, gun: l.shipmentDay, kargo: v.winnerFreight, etiket: tags.slice(0, 6), kat: (p.mainCategory || {}).name};
  });
  return {path: location.pathname + location.search, h1: document.querySelector('h1')?.textContent, title: document.title, total: st.totalProductCount, page: st.currentPage, last: st.lastPage, ts: new Date().toISOString(), rows};
}
