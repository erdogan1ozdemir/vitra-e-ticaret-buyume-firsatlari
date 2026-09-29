// Hepsiburada SKU aramasi (sayfa ici fetch, hepsiburada.com sayfasindayken browser_evaluate ile calistirilir).
// Kullanim: (bu fonksiyon)(["7041B003-0090", ...]) ; sonuc dosyaya kaydedilir. Istek arasi 3-6 sn.
async (KODLAR) => {
  const uyku = ms => new Promise(r => setTimeout(r, ms));
  const rnd = () => 3000 + Math.floor(Math.random() * 3000);
  const norm = s => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const dizi = (t, anahtar) => {
    const i = t.indexOf(anahtar); if (i < 0) return null;
    const bas = t.indexOf('[', i);
    let d = 0, ins = false, esc = false, son = -1;
    for (let j = bas; j < t.length; j++) {
      const c = t[j];
      if (ins) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === '"') ins = false; continue; }
      if (c === '"') ins = true; else if (c === '[') d++; else if (c === ']') { d--; if (d === 0) { son = j; break; } }
    }
    return son > 0 ? JSON.parse(t.slice(bas, son + 1)) : null;
  };
  const bul = (o, dep) => { if (dep > 9 || o == null) return null; if (typeof o === 'string') return (o.indexOf('MORIA.PRODUCTLIST') >= 0 && o.indexOf('"products":[') >= 0) ? o : null; if (typeof o === 'object') { for (const k of Object.keys(o)) { const x = bul(o[k], dep + 1); if (x) return x; } } return null; };
  const out = {ts: new Date().toISOString(), sonuc: {}};
  for (const kod of KODLAR) {
    const rec = {arama: [], listeler: [], hata: null};
    try {
      await uyku(rnd());
      const r = await fetch('/ara?q=' + encodeURIComponent(kod), {credentials: 'include'});
      const html = await r.text(); rec.durum = r.status;
      const doc = new DOMParser().parseFromString(html, 'text/html');
      let prods = null;
      const el0 = doc.getElementById('reduxStore');
      if (el0) { const hs = bul(JSON.parse(el0.textContent), 0); if (hs) prods = dizi(hs, '"products":['); }
      if (!prods) { rec.hata = 'arama verisi okunamadi'; out.sonuc[kod] = rec; continue; }
      const k = norm(kod);
      rec.arama = prods.slice(0, 10).map(p => { const v = (p.variantList || []).find(x => x.isDefault) || p.variantList[0]; const l = v.listing || {}, pi = l.priceInfo || {}; return [p.productId, p.brand, (v.name || '').slice(0, 90), l.merchantName, pi.price, pi.originalPrice, (l.campaignPriceInfo || {}).discountedPrice || null, v.isMultiSeller ? 1 : 0, v.url, p.customerReviewRating, p.customerReviewCount, (l.jetDelivery || l.expressDelivery) ? 1 : 0, v.winnerFreight, l.shipmentDay]; });
      const esl = rec.arama.filter(a => norm(a[2]).includes(k));
      for (const a of esl.slice(0, 4)) {
        await uyku(rnd());
        const r2 = await fetch(a[8], {credentials: 'include'});
        const d2 = new DOMParser().parseFromString(await r2.text(), 'text/html');
        const el = d2.getElementById('reduxStore');
        if (!el) { rec.listeler.push({id: a[0], hata: 'urun verisi okunamadi'}); continue; }
        const ps = JSON.parse(el.textContent).productState || {}; const pr = ps.product || {};
        rec.listeler.push({id: pr.productId, sku: pr.sku, ad: (pr.name || '').slice(0, 90), marka: (pr.brand || pr.brandName), satici: pr.merchantName, fiyat: pr.prices && pr.prices[0] && pr.prices[0].value, indirimOrani: pr.prices && pr.prices[0] && pr.prices[0].discountRate, stok: pr.isInStock, kargo: pr.winnerFreight, gun: pr.shipmentDay, saticiPuan: pr.merchant && pr.merchant.lifetimeRating,
          diger: (pr.listings || []).map(x => [x.merchantName, x.originalPrice, (x.minimumPrices || []).filter(m => m.name === 'non-segmented-price').map(m => m.value)[0], x.buyboxOrder, x.freeShipping ? 1 : 0, x.fastShipping ? 1 : 0, x.ratingSummary && x.ratingSummary.lifetimeRating])});
      }
    } catch (e) { rec.hata = String(e).slice(0, 150); }
    out.sonuc[kod] = rec;
  }
  return out;
}
