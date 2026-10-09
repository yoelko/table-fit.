import sys
from playwright.sync_api import sync_playwright
js=sys.argv[1]; out=sys.argv[2]; dev=sys.argv[3] if len(sys.argv)>3 else 'd'
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    vp={'width':390,'height':844} if dev=='m' else {'width':1440,'height':900}
    ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=dev=='m',has_touch=dev=='m',device_scale_factor=2 if dev=='m' else 1); pg=ctx.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(2300)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    r=pg.evaluate("async()=>{"+js+"}"); pg.wait_for_timeout(int(sys.argv[4]) if len(sys.argv)>4 else 500)
    pg.screenshot(path=out); print('result',r,'errors',errs[:3]); b.close()
