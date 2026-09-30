// Banyomega (2. tur): /arama?q=<ifade>; ilk HTML'de 24'e kadar urun; [data-toggle=product], marka [data-qa=product-brand], fiyat [data-toggle=price-sell-vat].
function pn(s){return parseFloat((s||'').replace(/[^\d,\.]/g,'').replace(/\./g,'').replace(',','.'))}
window.__job=async function(k,q){
  var r=await fetch('/arama?q='+encodeURIComponent(q),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();var d=new DOMParser().parseFromString(t,'text/html');
  var res={k:k,q:q,st:r.status};
  res.rows=[].slice.call(d.querySelectorAll('[data-toggle=product]')).map(function(e,i){var b=((e.querySelector('[data-qa=product-brand]')||{}).textContent||'').replace(/ /g,'').trim();var n=((e.querySelector('[data-toggle=product-title]')||{}).textContent||'').trim();var f=pn((e.querySelector('[data-toggle=price-sell-vat]')||{}).textContent);var ol=e.querySelector('.line-through');var o2=ol?pn(ol.textContent):0;return [i+1,b||'?',n.slice(0,70),f,o2>f?o2:0]});
  return res};
