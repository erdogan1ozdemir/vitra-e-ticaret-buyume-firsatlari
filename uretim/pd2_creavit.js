// Creavit e-magaza (2. tur, Shopify): /search?type=product&q=<ifade>; product-card (24 urun): baslik = ilk gorsel alt, fiyat = "N,NNN.NN TL" degerleri (indirimli / normal).
window.__job=async function(k,q){
  var r=await fetch('/search?type=product&q='+encodeURIComponent(q),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();var d=new DOMParser().parseFromString(t,'text/html');
  var m=d.body.innerText.match(/(\d+)\s*sonuç/);var res={k:k,q:q,st:r.status,total:m?parseInt(m[1]):null};
  res.rows=[].slice.call(d.querySelectorAll('product-list product-card')).map(function(c,i){var im=c.querySelector('img');var n=im?im.getAttribute('alt'):'';var tx=c.textContent.replace(/\s+/g,' ');var v=(tx.match(/([\d,]+\.\d\d)\s*TL/g)||[]).map(function(s){return parseFloat(s.replace(/[^\d\.]/g,'').replace(/,/g,''))});return [i+1,'Creavit',(n||'').slice(0,70),v.length?Math.min.apply(null,v):null,v.length>1?Math.max.apply(null,v):0,c.getAttribute('handle')]});
  return res};
