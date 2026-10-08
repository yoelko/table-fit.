from playwright.sync_api import sync_playwright
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    ctx=b.new_context(viewport={'width':1366,'height':860},service_workers="block",accept_downloads=True); pg=ctx.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(900)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    pg.evaluate("()=>{createProject('מועדון הגליל'); STYLE.title='מועדון הגליל'; const ps=makeProposals({L:1400,W:900,purpose:'pool',bar:true}); useProposal(ps[1]);}")
    pg.click('#vizOpen'); pg.wait_for_timeout(4500)
    with pg.expect_download(timeout=30000) as dl: pg.click('#vizOffer')
    dl.value.save_as('offer.png'); print(dl.value.suggested_filename,'errors',errs)
    b.close()
