async (page) => {
  const fs = require('fs');
  const OUT = '/Users/Erdo/Desktop/Claude Projects/Vitra/11_e-ticaret-buyume/veri/ham/derin/pazaryeri_fiyat/hb/';
  const JOBS = [["banyo_dolabi", "/ara?q=banyo%20dolab%C4%B1&siralama=coksatan"], ["camasir_makinesi_dolabi", "/ara?q=%C3%A7ama%C5%9F%C4%B1r%20makinesi%20dolab%C4%B1&siralama=coksatan"], ["dusakabin", "/dusakabinler-c-18021979?siralama=coksatan"], ["banyo_bataryasi", "/banyo-bataryalari-c-18021947?siralama=coksatan"]];
  const res = [];
  for (const [key, path] of JOBS) {
    const wait = 3000 + Math.floor(Math.random()*3000);
    await page.waitForTimeout(wait);
    let status = null, err = null, data = null;
    try {
      const r = await page.goto('https://www.hepsiburada.com' + path, {waitUntil: 'domcontentloaded', timeout: 45000});
      status = r ? r.status() : null;
      await page.waitForFunction(() => window.MORIA && window.MORIA.PRODUCTLIST && Object.values(window.MORIA.PRODUCTLIST)[0] && Object.values(window.MORIA.PRODUCTLIST)[0].STATE, null, {timeout: 20000});
      data = await page.evaluate(() => {
        const st=Object.values(window.MORIA.PRODUCTLIST)[0].STATE.data;
        const rows=st.products.map((p,i)=>{const v=(p.variantList||[]).find(x=>x.isDefault)||p.variantList[0]; const l=v.listing||{}; const pi=l.priceInfo||{}; const cl=l.categorizedLabels||{}; const tags=[]; for(const g of Object.values(cl)){ if(Array.isArray(g)) g.forEach(t=>{ if(t&&t.text) tags.push(String(t.text).replace(/<[^>]+>/g,'').slice(0,60)); else if(t&&t.tagName) tags.push(t.tagName)}) } return {sira:i+1,id:p.productId,sku:v.sku,marka:p.brand,ad:v.name,url:v.url,satici:l.merchantName,buybox:v.buyboxOrder,coksatici:v.isMultiSeller,fiyat:pi.price,eski:pi.originalPrice,indirim:pi.discountRate,sepet:(l.campaignPriceInfo||{}).discountedPrice||null,sepetTip:(l.campaignPriceInfo||{}).labelText||null,puan:p.customerReviewRating,deg:p.customerReviewCount,jet:l.jetDelivery,express:l.expressDelivery,gun:l.shipmentDay,kargo:v.winnerFreight,etiket:tags.slice(0,6),kat:(p.mainCategory||{}).name}});
        return {path:location.pathname+location.search,h1:document.querySelector('h1')?.textContent,title:document.title,total:st.totalProductCount,page:st.currentPage,last:st.lastPage,rows};
      });
      data.status = status; data.ts = new Date().toISOString();
      fs.writeFileSync(OUT + key + '.json', JSON.stringify(data));
    } catch (e) { err = String(e).slice(0,200); }
    const blocked = await page.evaluate(() => /captcha|robot|erişim engellendi|access denied/i.test(document.title + ' ' + (document.body ? document.body.innerText.slice(0,300) : ''))).catch(()=>false);
    res.push({key, status, n: data ? data.rows.length : 0, total: data ? data.total : null, err, blocked});
    if (blocked) break;
  }
  return res;
}
