import base64
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    pg.route("**/three.min.js",lambda r:r.fulfill(body=open('t3/build/three.min.js','rb').read(),content_type="application/javascript"))
    pg.goto("http://127.0.0.1:8769/room-fit.html"); pg.wait_for_timeout(500)
    pg.evaluate("()=>loadThree().then(t=>{THREE=t})"); pg.wait_for_timeout(500)
    for mode in ["pool","snooker"]:
        pg.evaluate(f"()=>{{TVB.mode=null; tvTexture('{mode}'); TVB.cam=0; TVB.camKey=null; for(let i=0;i<70;i++) tvStep(1/30);}}")
        for k in range(3):
            pg.evaluate("()=>{ let n=0; while(n++<4000){ tvStep(1/30); if(TVB.phase==='roll'&&TVB.t>.25&&TVB.t<.3) break; } tvDraw(); }")
            open(f'tvs_{mode}{k}.png','wb').write(base64.b64decode(pg.evaluate("()=>TVB.c.toDataURL().split(',')[1]")))
    b.close()
