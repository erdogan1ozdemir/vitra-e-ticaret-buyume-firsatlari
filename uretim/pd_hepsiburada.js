// Hepsiburada kategori okuyucu (Control_Chrome execute_javascript; hepsiburada.com sekmesinde, senkron XHR, sayfalar arasi 3.2 sn).
// Sayfa HTML'indeki window.MORIA.PRODUCTLIST ... 'STATE' JSON'u (products, facets, totalProductCount, lastPage) dengeli suslu parantez taramasi ile ayrilir.
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function extract(t,marker){var i=t.indexOf(marker);if(i<0)return null;var s=t.indexOf('{',i);var d=0,inS=false,esc=false;for(var j=s;j<t.length;j++){var c=t[j];if(inS){if(esc)esc=false;else if(c=='\\')esc=true;else if(c=='"')inS=false}else{if(c=='"')inS=true;else if(c=='{')d++;else if(c=='}'){d--;if(d==0)return t.slice(s,j+1)}}}return null}
function pct(a,p){a=a.slice().sort(function(x,y){return x-y});if(!a.length)return null;var i=(a.length-1)*p,l=Math.floor(i),h=Math.ceil(i);return Math.round((a[l]+(a[h]-a[l])*(i-l))*100)/100}
function HB(key,path,np,mode){ // mode 'tam' (satirlar) veya 'ozet'
  var out={key:key,u:path,ts:'2026-09-30',mod:mode};var rows=[];
  for(var p=1;p<=np;p++){
    var x=new XMLHttpRequest();x.open('GET',path+(p>1?'&sayfa='+p:''),false);x.send();
    var m=x.responseText.match(/<script[^>]*>([^<]*?"products":\[\{"productId"[\s\S]*?)<\/script>/);var js=null;
    var re=/<script[^>]*>([\s\S]*?)<\/script>/g,q;while((q=re.exec(x.responseText))){if(q[1].indexOf('"products":[{"productId"')>=0){js=extract(q[1],"'STATE':");break}}
    if(!js){out['e'+p]=x.status;break}
    var S=JSON.parse(js),d=S.data;
    if(p==1){out.total=d.totalProductCount;out.last=d.lastPage;out.f={};d.facets.forEach(function(f){if(/^(Marka|Türü|Fiyat Aralığı|Satıcı)$/.test(f.name)||f.name=='Kategori'){var vs=f.values.map(function(v){return v.displayName});out.f[f.name+(f.name=='Kategori'?'@'+f.key.split('.').length:'')]=vs.slice(0,f.name=='Marka'?15:(f.name=='Satıcı'?10:10))}})}
    d.products.forEach(function(pr,i){var v=(pr.variantList||[]).filter(function(z){return z.isDefault})[0]||pr.variantList[0];var l=v.listing||{},pi=l.priceInfo||{};
      rows.push({s:(p-1)*36+i+1,id:pr.productId,b:pr.brand||'',n:(v.name||'').slice(0,32),m:l.merchantName||'',f:pi.price,o:pi.originalPrice,r:pr.customerReviewScore||0,d:pr.customerReviewCount||0,c:(pr.mainCategory||{}).name||''})});
    if(p<np)sleep(3200);
  }
  out.n=rows.length;
  if(mode=='tam'){out.r=rows.map(function(r){var v=/vitra|artema/i.test(r.b);return [r.s,r.id,r.b,(r.s<=36||v)?r.n:'',r.m,r.f,r.o==r.f?0:r.o,Math.round(r.r*10)/10,r.d].join('|')}).join(';')}
  else{var kt={};rows.forEach(function(r){kt[r.c]=(kt[r.c]||0)+1});out.kat=Object.keys(kt).sort(function(a,b){return kt[b]-kt[a]}).slice(0,4).map(function(k){return k+':'+kt[k]}).join(', ');
    var pr=rows.map(function(r){return r.f});out.p={min:Math.min.apply(null,pr),p25:pct(pr,.25),med:pct(pr,.5),p75:pct(pr,.75),max:Math.max.apply(null,pr)};
    var bt={},dt=0;rows.forEach(function(r){bt[r.b]=bt[r.b]||[0,0];bt[r.b][0]++;bt[r.b][1]+=r.d;dt+=r.d});out.deg=dt;out.nbrand=Object.keys(bt).length;out.marka=Object.keys(bt).sort(function(a,b){return bt[b][1]-bt[a][1]}).slice(0,6).map(function(b){return b+':'+bt[b][0]+'/'+bt[b][1]}).join(', ');
    var st={};rows.forEach(function(r){st[r.m]=(st[r.m]||0)+1});out.nsat=Object.keys(st).length;out.sat=Object.keys(st).sort(function(a,b){return st[b]-st[a]}).slice(0,6).map(function(k){return k+':'+st[k]}).join(', ');
    out.top=rows.slice().sort(function(a,b){return b.d-a.d}).slice(0,10).map(function(r){return [r.s,r.id,r.b,r.n,r.m,r.f,r.o==r.f?0:r.o,Math.round(r.r*10)/10,r.d].join('|')});
    out.vitra=rows.filter(function(r){return /vitra|artema/i.test(r.b)}).map(function(r){return [r.s,r.id,r.b,r.n,r.m,r.f,r.o==r.f?0:r.o,Math.round(r.r*10)/10,r.d].join('|')})}
  return out;
}
