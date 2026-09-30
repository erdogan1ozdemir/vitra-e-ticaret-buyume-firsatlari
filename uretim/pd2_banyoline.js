// Banyoline (2. tur, Ticimax): /Arama?1&kelime=<ifade>; .productItem (24 urun): .productMarka, .productName, .productPrice.
function pn(s){return parseFloat((s||'').replace(/[^\d,\.]/g,'').replace(/\./g,'').replace(',','.'))}
window.__job=async function(k,q){
  var r=await fetch('/Arama?1&kelime='+encodeURIComponent(q).replace(/%20/g,'+'),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();var d=new DOMParser().parseFromString(t,'text/html');
  var pgs=(t.match(/[?&]sayfa=(\d+)/g)||[]).map(function(s){return parseInt(s.replace(/\D/g,''))});var res={k:k,q:q,st:r.status,sayfa:pgs.length?Math.max.apply(null,pgs):1};
  res.rows=[].slice.call(d.querySelectorAll('.productItem')).map(function(e,i){var b=((e.querySelector('.productMarka')||{}).textContent||'').trim();var n=((e.querySelector('.productName')||{}).textContent||'').trim();var pp=e.querySelector('.productPrice');if(!pp)return null;var ds=pp.querySelector('.discountPriceSpan');var all=(pp.textContent.match(/₺\s?[\d\.]+,\d{2}/g)||[]).map(pn);var f=ds?pn(ds.textContent):all[0];var old=Math.max.apply(null,all.concat([0]));return [i+1,b||'?',n.slice(0,70),f,old>f?old:0]}).filter(function(x){return x});
  return res};
