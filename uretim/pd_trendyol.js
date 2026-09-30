// Trendyol kategori okuyucu (Control_Chrome execute_javascript; sayfa open_url ile acildiktan sonra calistirilir).
// Yan menu (Kategori / Marka / Urun Tipi / Fiyat...) canli DOM'dan, urunler ayni kokenli senkron XHR ile sr?...&pi=1,2 sayfalarindaki
// window["__single-search-result__PROPS"] gomulu JSON'undan okunur (36 urun/sayfa, sst=BEST_SELLER). Sayfalar arasi 3.2 sn.
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function TY(np){
  var out={u:location.pathname+location.search,ts:'2026-09-30'};
  var f={};[].slice.call(document.querySelectorAll('.aggregation')).forEach(function(a){var h=a.querySelector('h3');if(!h)return;var n=h.textContent.trim();
    if(/^(Kategori|Marka|Ürün Tipi|Fiyat$|Satıcı Tipi)/.test(n)){f[n]=[].slice.call(a.querySelectorAll('.checkbox-list-item,.radio-list-item')).map(function(i){return i.textContent.trim()}).slice(0,n=='Marka'?20:12)}});
  out.f=f;var rows=[],kt={};
  for(var p=1;p<=np;p++){
    var x=new XMLHttpRequest();x.open('GET','/sr'+location.search.replace(/[&?]pi=\d+/,'')+'&pi='+p,false);x.send();
    var m=x.responseText.match(/window\["__single-search-result__PROPS"\]=(\{[\s\S]*?\});?<\/script>/);
    if(!m){out['e'+p]=x.status;break}
    var P=JSON.parse(m[1]);if(p==1){out.total=P.data.total}
    P.data.products.forEach(function(q,i){var pr=q.price||{};var cur=pr.discountedPrice||pr.current;var old=pr.old||((pr.originalPrice>cur)?pr.originalPrice:0);var rs=q.ratingScore||{};var c=(q.category||{}).name||'';kt[c]=(kt[c]||0)+1;
      rows.push([(p-1)*36+i+1,q.id,q.brand,(q.name||'').slice(0,42),q.merchantId,cur,old||0,rs.averageRating?Math.round(rs.averageRating*10)/10:0,rs.totalCount||0].join('|'))});
    if(p<np)sleep(3200);
  }
  out.kat=Object.keys(kt).sort(function(a,b){return kt[b]-kt[a]}).slice(0,4).map(function(k){return k+':'+kt[k]}).join(', ');
  out.r=rows.join(';');return out;
}
