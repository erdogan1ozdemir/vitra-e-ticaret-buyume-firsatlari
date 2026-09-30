// Hepsiburada (2. tur): /ara?q=<ifade>&siralama=coksatan ilk sayfa (36 urun). Arama sayfasinda STATE JSON'u kacisli (\") govde icinde gelir; bir kat kacis acilarak okunur.
function extract(t,marker){var i=t.indexOf(marker);if(i<0)return null;var s=t.indexOf('{',i);var d=0,inS=false,esc=false;for(var j=s;j<t.length;j++){var c=t[j];if(inS){if(esc)esc=false;else if(c=='\\')esc=true;else if(c=='"')inS=false}else{if(c=='"')inS=true;else if(c=='{')d++;else if(c=='}'){d--;if(d==0)return t.slice(s,j+1)}}}return null}
window.__job=async function(k,q){
  var u='/ara?q='+encodeURIComponent(q)+'&siralama=coksatan';
  var r=await fetch(u,{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();
  var i=t.indexOf('window.MORIA.PRODUCTLIST');if(i<0)return{status:r.status,blocked:1,title:(t.match(/<title>([^<]*)/)||[])[1],len:t.length};
  var tail=t.slice(i,i+1500000);if(tail.indexOf("'STATE': {\\\"")>0)tail=tail.replace(/\\(.)/g,function(m,c){return c=='n'?'\n':c=='t'?'\t':c});
  var js=extract(tail,"'STATE':");if(!js)return{k:k,err:'state',len:t.length,title:(t.match(/<title>([^<]*)/)||[])[1]};
  var d=JSON.parse(js).data;var res={k:k,q:q,u:u,total:d.totalProductCount,last:d.lastPage,f:{}};
  (d.facets||[]).forEach(function(f){if(/^(Marka|Ürün Çeşidi|Kategori)$/.test(f.name)){res.f[f.name+'@'+String(f.key).split('.').length]=f.values.slice(0,12).map(function(v){return v.displayName+(v.count?'='+v.count:'')})}});
  res.rows=d.products.map(function(pr,i){var v=(pr.variantList||[]).filter(function(z){return z.isDefault})[0]||pr.variantList[0]||{};var l=v.listing||{},pi=l.priceInfo||{};
    return [i+1,pr.productId,pr.brand||'',(v.name||'').slice(0,70),l.merchantName||'',pi.price,pi.originalPrice==pi.price?0:(pi.originalPrice||0),Math.round((pr.customerReviewRating||pr.customerReviewScore||0)*10)/10,pr.customerReviewCount||0,(pr.mainCategory||{}).name||'',/vitra|artema/i.test(pr.brand||'')?(v.url||'').slice(0,110):'']});
  return res};
