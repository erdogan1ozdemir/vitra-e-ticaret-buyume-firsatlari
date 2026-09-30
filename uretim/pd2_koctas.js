// Koctas (2. tur): /search?q=<ifade>&sort=bestseller-desc ilk sayfa (48 urun); marka/satici/fiyat li.prd icindeki gizli input'lardan.
window.__job=async function(k,q){
  var r=await fetch('/search?q='+encodeURIComponent(q)+'&sort=bestseller-desc',{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();
  var d=new DOMParser().parseFromString(t,'text/html');var res={k:k,q:q,st:r.status,h1:((d.querySelector('h1')||{}).textContent||'').trim().replace(/\s+/g,' ').slice(0,80)};
  var m=d.body.textContent.match(/(\d[\d\.]*)\s*Ürün/);res.total=m?parseInt(m[1].replace(/\./g,'')):null;
  res.rows=[].slice.call(d.querySelectorAll('li.prd')).map(function(l,i){var g=function(n){var e=l.querySelector('input[name="'+n+'"]');return e?e.value:''};var a=l.querySelector('a[href*="/p/"][title]');var ti=(a?a.getAttribute('title'):g('productNameForGTM'))||'';
    var cur=parseFloat(g('productPriceWithDiscountForGTM'))||parseFloat(g('productUnitPriceForGTM'))||null;var uni=parseFloat(g('productUnitPriceForGTM'))||0;var rt=(l.querySelector('.prd-rating')||{}).textContent||'';var rm=rt.replace(/\s+/g,'').match(/([\d\.]+)\((\d+)\)/);
    return [i+1,g('productBrandForGTM'),ti.slice(0,70),g('productSellerForGTM'),cur,uni>cur?uni:0,rm?parseFloat(rm[1]):0,rm?parseInt(rm[2]):0,g('productCategoryForGTM').slice(0,40)]});
  return res};
