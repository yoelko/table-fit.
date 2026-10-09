import sys,time,json
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:8770/index.html"
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    c=b.new_context(viewport={'width':390,'height':844},service_workers="block",is_mobile=True,has_touch=True,device_scale_factor=3); pg=c.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    cdp=c.new_cdp_session(pg); cdp.send("Emulation.setCPUThrottlingRate",{"rate":4})
    t0=time.time(); pg.goto(url); pg.wait_for_load_state('load'); print('load %.0fms'%((time.time()-t0)*1000))
    pg.wait_for_timeout(2500)
    r=pg.evaluate("""()=>{const o={}; createProject('perf'); state.custom=null; state.L=4700; state.W=1500; P=roomPoints(); G=buildGrid(P);
      let t=performance.now(); fillRoom(items.find(i=>i.L===292)); o.fill=performance.now()-t; o.n=state.tables.length;
      for(const k of ['bar','backbar','sofa','tv','tv','stool','stool','plant']) addFurn(k);
      t=performance.now(); for(let i=0;i<5;i++) drawPlan(); o.drawPlan=(performance.now()-t)/5;
      o.nodes=document.getElementById('svg').querySelectorAll('*').length;
      t=performance.now(); for(const tb of ['room','tables','furn','gaps','tables']) setTab(tb); o.tabs5=performance.now()-t;
      t=performance.now(); select({type:'t',o:state.tables[3]}); o.select=performance.now()-t;
      t=performance.now(); for(let i=0;i<10;i++){ const tt=state.tables[3]; snapTable(tt,tt.cx+3,tt.cy); } o.snap10=performance.now()-t;
      return o;}""")
    print(json.dumps(r))
    # a real drag of a table, counting how long each frame takes
    bb=pg.locator('#svg [data-t="3"]').first.bounding_box(); x,y=bb['x']+bb['width']/2,bb['y']+bb['height']/2
    pg.evaluate("()=>{window.__f=[];let l=performance.now();(function q(t){__f.push(t-l);l=t;window.__r=requestAnimationFrame(q);})(l)}")
    t0=time.time()
    cdp.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":x,"y":y}]})
    for i in range(1,25): cdp.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":x+i*3,"y":y+i}]})
    cdp.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]})
    pg.wait_for_timeout(300); dt=time.time()-t0
    f=pg.evaluate("()=>{cancelAnimationFrame(__r);const a=__f.slice(2).sort((x,y)=>x-y);return [a.length,Math.round(a[Math.floor(a.length*.5)]),Math.round(a[Math.floor(a.length*.9)]),Math.round(a[a.length-1])]}")
    print('drag 24 moves: %.2fs, frames n/median/p90/max ms:'%dt, f)
    t0=time.time(); pg.evaluate("async()=>{ await openViz(); }"); print('open 3D: %.0fms'%((time.time()-t0)*1000))
    r=pg.evaluate("()=>{let t=performance.now(); buildScene(); const b=performance.now()-t; t=performance.now(); V.r.render(V.scene,V.cam); return [b, performance.now()-t]}")
    print('buildScene/render ms',r)
    b.close()
