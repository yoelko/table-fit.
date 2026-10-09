from playwright.sync_api import sync_playwright
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    for name,vp,mob in [('se',{'width':360,'height':640},True),('land',{'width':844,'height':390},True),('ipad',{'width':820,'height':1180},True)]:
        ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=mob,has_touch=mob,device_scale_factor=2); pg=ctx.new_page()
        pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(900)
        if pg.locator('#tipOk').is_visible(): pg.locator('#tipOk').tap()
        pg.evaluate("()=>{createProject('מועדון הגליל'); useProposal(makeProposals({L:1300,W:900,purpose:'pool',bar:true})[1]);}"); pg.wait_for_timeout(300)
        pg.screenshot(path=f'sz_{name}_1.png')
        pg.locator('#tab-tables').tap(); pg.wait_for_timeout(300); pg.screenshot(path=f'sz_{name}_2.png')
        pg.evaluate("()=>openAdvisor()"); pg.wait_for_timeout(200); pg.screenshot(path=f'sz_{name}_3.png'); pg.evaluate("()=>$('adv').hidden=true")
        pg.locator('#vizOpen').tap(); pg.wait_for_timeout(4500); pg.screenshot(path=f'sz_{name}_4.png')
        print(name,errs); ctx.close()
    b.close()
