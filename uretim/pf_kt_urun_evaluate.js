// Koctas SKU aramasi (sayfa ici fetch, koctas.com.tr sayfasindayken browser_evaluate ile calistirilir). Istek arasi 3-6 sn.
async (KODLAR) => {
  const uyku = ms => new Promise(r => setTimeout(r, ms));
  const rnd = () => 3000 + Math.floor(Math.random() * 3000);
  const norm = s => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const satirla = t => (t || '').split('\n').map(x => x.replace(/\s+/g, ' ').trim()).filter(Boolean);
  const temiz = d => { d.querySelectorAll('style,script,noscript').forEach(x => x.remove()); return satirla(d.body.textContent); };
  const sayi = s => { const m = (s || '').match(/([0-9][0-9.]*(,[0-9]+)?)\s*TL/); return m ? parseFloat(m[1].replace(/\./g, '').replace(',', '.')) : null; };
  const out = {ts: new Date().toISOString(), sonuc: {}};
  for (const kod of KODLAR) {
    const rec = {arama: [], listeler: [], hata: null};
    try {
      await uyku(rnd());
      const r = await fetch('/search?q=' + encodeURIComponent(kod), {credentials: 'include'});
      const html = await r.text(); rec.durum = r.status;
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const kartlar = [...doc.querySelectorAll('.prd-inner')].slice(0, 12);
      for (const c of kartlar) {
        const a = c.querySelector('a[title][href*="/p/"]'); if (!a) continue;
        const s = satirla(c.textContent);
        rec.arama.push([c.getAttribute('data-productid'), (a.getAttribute('title') || '').slice(0, 90), a.getAttribute('href'), s.filter(x => /TL/.test(x)).map(sayi), s.filter(x => /Sepette|Kargo|Taksit|indirim/i.test(x)).slice(0, 4)]);
      }
      const k = norm(kod);
      const esl = rec.arama.filter(a => norm(a[1]).includes(k));
      for (const a of esl.slice(0, 3)) {
        await uyku(rnd());
        const r2 = await fetch(a[2], {credentials: 'include'});
        const d2 = new DOMParser().parseFromString(await r2.text(), 'text/html');
        const ld = [...d2.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent).find(t => /"Product"/.test(t)) || '';
        const pm = ld.match(/"price"\s*:\s*"?([0-9.]+)/); const av = ld.match(/schema.org\/(InStock|OutOfStock|PreOrder|LimitedAvailability)/);
        const L = temiz(d2);
        const i = L.indexOf('Satıcı:');
        rec.listeler.push({id: a[0], ad: a[1], url: a[2], ldFiyat: pm ? parseFloat(pm[1]) : null, stok: av ? av[1] : null, satici: i >= 0 ? L.slice(i + 1, i + 3) : null, sepette: L.find(x => /Sepette %[0-9]+ İndirim/.test(x)) || null, taksit: L.find(x => /Aya Varan Taksit/.test(x)) || null, stokDurumu: L.find(x => /^Stok Durumu/.test(x)) || null, montajSatinAl: L.includes('Montaj Satın Al'), kargo: L.find(x => /Kargo Bedava|Ücretsiz Kargo/i.test(x)) || null});
      }
    } catch (e) { rec.hata = String(e).slice(0, 150); }
    out.sonuc[kod] = rec;
  }
  return out;
}
