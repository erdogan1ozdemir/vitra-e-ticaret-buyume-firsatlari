// pd2 ortak kosucu: sekmede arka planda kesitleri sirayla okur (kesitler arasi 3.3 sn), sonuc window.__R[anahtar] altinda birikir.
// 429 ya da dogrulama sayfasinda 60 sn bekler, ikinci denemede de olmazsa siteyi birakir (window.__ST.blocked).
window.__R=window.__R||{};window.__ST={done:0,err:[],blocked:false,running:true,t0:Date.now(),last:''};
window.__sleep=function(ms){return new Promise(function(r){setTimeout(r,ms)})};
window.__run=async function(delay){
  for(var i=0;i<window.__SEGS.length;i++){var s=window.__SEGS[i];if(window.__R[s[0]])continue;
    var res=null;
    for(var a=0;a<2;a++){
      try{res=await window.__job(s[0],s[1])}catch(e){res={k:s[0],err:String(e)}}
      if(res&&(res.status==429||res.blocked)){window.__ST.err.push(s[0]+':'+(res.status||'blk'));res=null;await window.__sleep(60000);continue}
      break}
    if(!res){window.__ST.blocked=true;window.__ST.last=s[0];break}
    window.__R[s[0]]=res;window.__ST.done++;window.__ST.last=s[0];
    await window.__sleep(delay)}
  window.__ST.running=false};
