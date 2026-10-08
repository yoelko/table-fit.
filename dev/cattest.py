from playwright.sync_api import sync_playwright
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    for vp,tag in [({'width':390,'height':800},'m'),({'width':1366,'height':860},'d')]:
        ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=tag=='m',has_touch=tag=='m',device_scale_factor=2 if tag=='m' else 1); pg=ctx.new_page()
        pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript")); pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto("http://127.0.0.1:8770/index.html"); pg.wait_for_timeout(700)
        if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
        pg.click('#tab-room'); pg.fill('#rL','1400'); pg.fill('#rW','900'); pg.click('#tab-tables'); pg.click('#clearAll')
        pg.click('#catOpen'); pg.wait_for_timeout(200)
        pg.locator('#catTags button',has_text='פוקר').click(); pg.wait_for_timeout(100)
        pg.screenshot(path=f'cat_{tag}.png')
        pg.fill('#catQ','לבן 9'); pg.wait_for_timeout(100); print(tag,'search rows',pg.locator('#catList .prow').count())
        pg.locator('#catList [data-add]').first.click(); pg.wait_for_timeout(200)
        for q in ['פינג פונג חוץ','רגלי עץ','מתומן מקצועי','Heritage עגול 145','Gold Liberty 7']:
            pg.click('#catOpen'); pg.fill('#catQ',q); pg.wait_for_timeout(100); pg.locator('#catList [data-add]').first.click(); pg.wait_for_timeout(150)
        pg.click('#catOpen'); pg.fill('#catQ','כדורגל מקצועי'); pg.locator('#catList .popen').first.click(); pg.wait_for_timeout(150)
        pg.click('#tFill'); pg.wait_for_timeout(300)
        print(tag,'tables',pg.evaluate("()=>state.tables.map(t=>t.name+':'+t.kind+(t.fin?'/'+t.fin:'')+(t.sh?'/'+t.sh:'')).join(' | ')"))
        if tag=='m': pg.locator('#tab-tables').tap() if False else None
        pg.screenshot(path=f'plan_{tag}.png')
        if tag=='d':
            pg.click('#vizOpen'); pg.wait_for_timeout(5000); pg.locator('#vizStage').screenshot(path='cat3d_1.png')
            pg.click('#vizViews button[data-v="top"]'); pg.wait_for_timeout(1500); pg.locator('#vizStage').screenshot(path='cat3d_2.png')
            pg.evaluate("()=>{V.orbit.phi=1.2;V.orbit.r=V.size*.55;V.orbit.theta=1.2;markView(null);applyCam();}"); pg.wait_for_timeout(1500); pg.locator('#vizStage').screenshot(path='cat3d_3.png')
        print(tag,'errors',errs[:3]); ctx.close()
    b.close()
