import sys,time
from playwright.sync_api import sync_playwright
page=sys.argv[1] if len(sys.argv)>1 else "room-fit.html"
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    ctx=b.new_context(viewport={'width':1366,'height':860},service_workers="block"); pg=ctx.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript")); pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto("http://127.0.0.1:8769/"+page); pg.wait_for_timeout(600)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    pg.click('#tab-room'); pg.fill('#rL','1100'); pg.fill('#rW','800'); pg.click('#tab-tables'); pg.click('#clearAll')
    pg.locator('.spick').nth(2).click(); pg.click('#tFill'); pg.wait_for_timeout(300)
    # fake 3 projects with ~450KB sketches
    pg.evaluate("""()=>{ const big='data:image/jpeg;base64,'+'A'.repeat(450000);
      cur.bg={src:big,show:true,op:.4}; for(let i=0;i<3;i++){const c=JSON.parse(JSON.stringify(cur)); c.id='x'+i; c.name='p'+i; PROJ.list.push(c);} saveProjects(); drawPlan(); }""")
    box=pg.locator('#svg [data-t="0"]').first.bounding_box() if pg.locator('#svg [data-t="0"]').count() else None
    print('table box',box)
    print(pg.evaluate("""()=>{const o={};let t=performance.now();for(let i=0;i<10;i++)drawPlan();o.draw=(performance.now()-t)/10;
      t=performance.now();for(let i=0;i<10;i++)saveProjects();o.save=(performance.now()-t)/10;
      t=performance.now();for(let i=0;i<10;i++)G=buildGrid(P);o.grid=(performance.now()-t)/10;
      t=performance.now();for(let i=0;i<10;i++)snapTable(state.tables[0],state.tables[0].cx+3,state.tables[0].cy);o.snap=(performance.now()-t)/10;
      o.bytes=JSON.stringify(PROJ).length; return o}"""))
    pg.evaluate("""()=>{window.__f=[];let last=performance.now();function loop(t){__f.push(t-last);last=t;window.__raf=requestAnimationFrame(loop);}requestAnimationFrame(loop);}""")
    x,y=box['x']+box['width']/2, box['y']+box['height']/2
    pg.mouse.move(x,y); pg.mouse.down(); t0=time.time()
    for i in range(60): pg.mouse.move(x+i*2,y+i)
    pg.mouse.up(); dt=time.time()-t0
    f=pg.evaluate("()=>{cancelAnimationFrame(__raf);const a=__f.slice(2);return [Math.max(...a),a.reduce((s,v)=>s+v,0)/a.length]}")
    print('drag 60 moves %.2fs  maxframe %.0fms avg %.0fms'%(dt,f[0],f[1]))
    t0=time.time(); pg.click('#vizOpen'); pg.wait_for_function("()=>typeof V!=='undefined'&&V&&V.scene&&$('vizMsg').hidden",timeout=90000); print('viz open %.2fs'%(time.time()-t0))
    r=pg.evaluate("()=>{const t=performance.now();for(let i=0;i<5;i++)V.r.render(V.scene,V.cam);return (performance.now()-t)/5}")
    print('render ms %.0f'%r)
    print('errors:',errs[:5]); b.close()
