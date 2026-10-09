from playwright.sync_api import sync_playwright
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    ctx=b.new_context(viewport={'width':1366,'height':860},service_workers="block"); pg=ctx.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(900)
    u=pg.evaluate("async()=>{createProject('מועדון הגליל'); STYLE.title='מועדון הגליל'; useProposal(makeProposals({L:1400,W:900,purpose:'pool',bar:true})[1]); return await packShare();}")
    u=u.replace('https://yoelko.github.io/table-fit./preview/','http://127.0.0.1:8770/preview/index.html')
    print(len(u))
    c2=b.new_context(viewport={'width':390,'height':844},service_workers="block",is_mobile=True,has_touch=True,device_scale_factor=2); p2=c2.new_page()
    p2.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    p2.goto(u); p2.wait_for_timeout(5000); p2.screenshot(path='viewer_m.png'); b.close()
