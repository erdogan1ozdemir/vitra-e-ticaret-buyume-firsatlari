// vitra.com.tr (2. tur): her kategori icin 4 ayri sayfa istegi (varsayilan En Cok Satanlar, fiyat artan, fiyat azalan, sadece stoklu), istekler arasi 3.3 sn.
// Toplam: "<Kategori> icin N sonuc listeleniyor"; kartlar .js-plp-card (data-insider-plp-product: unit_price, unit_sale_price, stock). Ozel sayfalarda (/c-ucretsiz-montaj vb.) /ajax/c-...?q=:bestSelling&page=N ile tum sayfalar.
window.__pg=async function(u){var ac=new AbortController();var to=setTimeout(function(){ac.abort()},20000);try{var r=await fetch(u,{credentials:'include',signal:ac.signal});if(r.status==429)return{status:429};var t=await r.text();var d=new DOMParser().parseFromString(t,'text/html');var tx=d.body.innerText.replace(/\s+/g,' ');var m=tx.match(/için (\d+) sonuç/);
  var cs=[].slice.call(d.querySelectorAll('.js-plp-card')).map(function(c){var a=c.querySelector('a[data-insider-plp-product]');var ip={},g={};try{ip=JSON.parse(a.getAttribute('data-insider-plp-product'))}catch(e){}try{g=JSON.parse(c.querySelector('a[data-gtm-product]').getAttribute('data-gtm-product'))}catch(e){}var x=c.textContent.replace(/\s+/g,' ');
    return [g.id||ip.id,(ip.name||g.name||'').slice(0,60),ip.unit_price,ip.unit_sale_price,ip.stock,/Ücretsiz Montaj/i.test(x)?1:0,/stok(ta)? yok|tükendi|haber ver/i.test(x)?1:0,(x.match(/% ?(\d+) indirim/)||[])[1]||0,(g.category||'').slice(0,80)]});
  return{status:r.status,total:m?+m[1]:null,h1:((d.querySelector('h1')||{}).textContent||'').trim(),cards:cs,len:t.length,blocked:(r.status!=200&&r.status!=404)?1:0}}finally{clearTimeout(to)}};
window.__pg2=async function(u){try{return await window.__pg(u)}catch(e){return {status:0,fail:String(e),cards:[],total:null}}};
window.__job=async function(k,paths){
  var res={k:k,paths:paths,items:[]};
  for(var pi=0;pi<paths.length;pi++){var p=paths[pi];var it={p:p};
    var a=await window.__pg(p);if(a.status==429||a.blocked)return a;if(a.status==404){it.st=404;res.items.push(it);continue}
    it.total=a.total;it.h1=a.h1;it.cards=a.cards;
    if(a.total&&a.total>a.cards.length){
      await window.__sleep(3300);var b=await window.__pg2(p+'?q=%3Aprice-asc');if(b.status==429)return b;it.asc=b.cards.slice(0,2);if(b.fail)it.asc_fail=b.fail;
      await window.__sleep(3300);var c=await window.__pg2(p+'?q=%3Aprice-desc');if(c.status==429)return c;it.desc=c.cards.slice(0,2);if(c.fail)it.desc_fail=c.fail}
    if(a.total){await window.__sleep(3300);var d=await window.__pg2(p+'?q=%3AbestSelling%3AinStockFlag%3Atrue');if(d.status==429)return d;if(d.fail){it.instock=null;it.instock_fail=d.fail}else if(d.total===null){it.instock=0;it.instock_bos=1}else it.instock=d.total}
    if(paths.length>1)await window.__sleep(3300);
    res.items.push(it)}
  return res};
window.__jobOzel=async function(k,paths){
  var p=paths[0];var res={k:k,paths:paths,items:[]};var a=await window.__pg(p);if(a.status==429||a.blocked)return a;var it={p:p,total:a.total,h1:a.h1,cards:a.cards.slice()};
  var np=Math.min(12,Math.ceil((a.total||0)/20));
  for(var n=1;n<np;n++){await window.__sleep(3300);var b=await window.__pg('/ajax'+p+'?q=%3AbestSelling&page='+n);if(b.status==429)return b;it.cards=it.cards.concat(b.cards)}
  res.items.push(it);return res};
// Not: sifir sonuclu stoklu suzgeci (inStockFlag:true) bazi kategorilerde yanit vermez; 20 sn zaman asimi ile it.instock=null, instock_fail kaydedilir.
// /c-online-ozel yonlendirme dongusune girer (ERR_TOO_MANY_REDIRECTS); fetch 'Failed to fetch' doner.
