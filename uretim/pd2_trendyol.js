// Trendyol (2. tur): once alaka sirasinda arama (cozumlenen WebCategory adaylari), sonra secilen web kategorisi + arama ifadesi ile Cok Satan (BEST_SELLER) ilk sayfa (36 urun).
window.__BATH=/lavabo|klozet|batarya|armat|du[sş]|k[uü]vet|banyo|rezervuar|pisuvar|vitrifiye|aksesuar|sabun|f[ıi]r[cç]a|as[ıi]|kova|havlu|ayna|dolap|tezgah|sifon|musluk|vana|kulp|ayak|panel|kabin|kanal/i;
window.__job=async function(k,q){
  async function g(u){var r=await fetch(u,{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();var m=t.match(/window\["__single-search-result__PROPS"\]=(\{[\s\S]*?\});?<\/script>/);if(!m)return{status:r.status,blocked:1,title:(t.match(/<title>([^<]*)/)||[])[1]};return{status:r.status,d:JSON.parse(m[1]).data}}
  var a=await g('/sr?q='+encodeURIComponent(q));if(!a.d)return a.status==429||a.blocked?a:{k:k,err:'rel'+a.status};
  var wl=[];((a.d.resolvedQuery||{}).filters||[]).forEach(function(f){if(f.type=='WebCategory')(f.filters||[]).forEach(function(c){wl.push([c.key,c.name])})});
  var pick=wl.filter(function(c){return window.__BATH.test(c[1])})[0];
  var res={k:k,q:q,rel_total:a.d.total,cands:wl.map(function(c){return c.join(':')}).join(','),wc:pick?pick[0]+':'+pick[1]:null};
  await window.__sleep(3300);
  var u='/sr?q='+encodeURIComponent(q)+(pick?'&wc='+pick[0]:'')+'&sst=BEST_SELLER';res.u=u;
  var b=await g(u);if(!b.d)return b.status==429||b.blocked?b:{k:k,err:'bs'+b.status};
  res.total=b.d.total;
  res.rows=b.d.products.map(function(p,i){var pr=p.price||{};var cur=pr.discountedPrice||pr.current;var old=pr.old||((pr.originalPrice>cur)?pr.originalPrice:0);var rs=p.ratingScore||{};
    return [i+1,p.id,p.brand,(p.name||'').slice(0,70),p.merchantId,cur,old||0,rs.averageRating?Math.round(rs.averageRating*10)/10:0,rs.totalCount||0,(p.category||{}).name||'',/vitra|artema/i.test(p.brand||'')?(p.url||'').slice(0,110):'']});
  return res};
