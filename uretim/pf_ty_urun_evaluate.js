// Trendyol SKU aramasi (sayfa ici fetch): arama sonucu + urun sayfasindaki diger saticilar.
// Kullanim: browser_evaluate, trendyol.com sayfasindayken. KODLAR degistirilir. Yavas tempo: istek arasi 3-6 sn.
async () => {
  const KODLAR = __KODLAR__;
  const uyku = ms => new Promise(r => setTimeout(r, ms));
  const rnd = () => 3000 + Math.floor(Math.random() * 3000);
  const norm = s => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const state = async (url, anahtar) => {
    const r = await fetch(url, {credentials: 'include'});
    const html = await r.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    for (const s of doc.querySelectorAll('script')) {
      const t = s.textContent || '';
      const i = t.indexOf(anahtar);
      if (i < 0) continue;
      const bas = t.indexOf('{', i);
      let d = 0, ins = false, esc = false, son = -1;
      for (let j = bas; j < t.length; j++) {
        const c = t[j];
        if (ins) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === '"') ins = false; continue; }
        if (c === '"') ins = true; else if (c === '{') d++; else if (c === '}') { d--; if (d === 0) { son = j; break; } }
      }
      if (son > 0) return {status: r.status, veri: JSON.parse(t.slice(bas, son + 1))};
    }
    return {status: r.status, veri: null};
  };
  const out = {ts: new Date().toISOString(), sonuc: {}};
  for (const kod of KODLAR) {
    const rec = {toplam: null, listeler: [], hata: null};
    try {
      await uyku(rnd());
      const a = await state('/sr?q=' + encodeURIComponent(kod), '__single-search-result__PROPS');
      const d = a.veri && a.veri.data;
      rec.durum = a.status;
      if (!d) { rec.hata = 'arama verisi okunamadi'; out.sonuc[kod] = rec; continue; }
      rec.toplam = d.total;
      const k = norm(kod);
      const urunler = (d.products || []).slice(0, 10);
      rec.arama = urunler.map(p => [p.id, p.brand, (p.name || '').slice(0, 70), p.merchantId, p.price && p.price.current, p.price && p.price.discountedPrice, (p.priceLabels || []).map(x => x.name).join(';'), p.freeCargo ? 1 : 0, (p.rushDelivery || p.hasFastDeliveryTag) ? 1 : 0, p.hasOfficialSellerBadge ? 1 : 0]);
      const esl = urunler.filter(p => norm(p.name).includes(k) && !/set\b/i.test('') );
      for (const p of esl.slice(0, 4)) {
        await uyku(rnd());
        const b = await state((p.url || '').split('?')[0], '__envoy__SHARED_PROPS');
        const pr = b.veri && b.veri.product;
        if (!pr) { rec.listeler.push({id: p.id, hata: 'urun verisi okunamadi'}); continue; }
        const ml = pr.merchantListing || {}, m = ml.merchant || {}, w = ((ml.winnerVariant || {}).price) || {};
        rec.listeler.push({id: pr.id, ad: (pr.name || '').slice(0, 90), marka: (pr.brand || {}).name, stok: pr.inStock, satici: [m.id, m.name, m.sellerScore && m.sellerScore.value], guncel: w.sellingPrice && w.sellingPrice.value, indirimli: w.discountedPrice && w.discountedPrice.value, ind: w.discountPercentage, kargo: (ml.winnerVariant || {}).freeCargo, hizli: (ml.winnerVariant || {}).rushDeliveryDuration, taksit: pr.maxInstallment,
          diger: (ml.otherMerchants || []).map(x => { const v = (x.variants || [])[0] || {}, pp = v.price || {}; return [x.id, x.name, x.sellerScore && x.sellerScore.value, pp.sellingPrice && pp.sellingPrice.value, pp.discountedPrice && pp.discountedPrice.value, v.freeCargo ? 1 : 0]; })});
      }
    } catch (e) { rec.hata = String(e).slice(0, 150); }
    out.sonuc[kod] = rec;
  }
  return out;
}
