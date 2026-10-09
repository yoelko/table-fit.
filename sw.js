const C="table-fit-v26";
const CORE=["./","index.html","manifest.webmanifest","icon-192.png","icon-512.png","apple-touch-icon.png"];
// Outside files the app uses (3D engine and fonts), kept so the app also works without internet.
const EXTRA=["https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"];
self.addEventListener("install",e=>{
  self.skipWaiting();
  e.waitUntil(caches.open(C).then(async c=>{
    await c.addAll(CORE);
    for(const u of EXTRA){ try{ const r=await fetch(u,{mode:"cors"}); if(r.ok) await c.put(u,r); }catch(err){} }
  }));
});
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{
  const req=e.request; if(req.method!=="GET") return;
  const url=new URL(req.url);
  if(url.origin===location.origin){
    // the app itself: newest from the network, saved copy when offline
    e.respondWith(fetch(req,{cache:"no-cache"}).then(r=>{const cp=r.clone(); caches.open(C).then(c=>c.put(req,cp)).catch(()=>{}); return r;}).catch(()=>caches.match(req,{ignoreSearch:true}).then(r=>r||caches.match("index.html"))));
    return;
  }
  if(/(^|\.)(cdnjs\.cloudflare\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)$/.test(url.hostname)){
    // libraries and fonts never change at the same address: saved copy first
    e.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(r=>{ if(r.ok||r.type==="opaque"){const cp=r.clone(); caches.open(C).then(c=>c.put(req,cp));} return r; })));
  }
});
