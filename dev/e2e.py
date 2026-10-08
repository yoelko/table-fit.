import sys, time, json
from playwright.sync_api import sync_playwright
dev=sys.argv[1]
three=open('t3/build/three.min.js','rb').read()
log=[]
def step(name,fn):
    try: fn(); log.append(('ok',name))
    except Exception as e: log.append(('FAIL',name,str(e)[:200]))
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    vp={'width':390,'height':844} if dev=='m' else {'width':1366,'height':860}
    ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=dev=='m',has_touch=dev=='m',device_scale_factor=2 if dev=='m' else 1,accept_downloads=True); pg=ctx.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    errs=[]; pg.on('pageerror',lambda e:errs.append('PAGE '+str(e))); pg.on('console',lambda m: m.type=='error' and 'Failed to load resource' not in m.text and errs.append('CONSOLE '+m.text))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(900)
    tap=(lambda sel: pg.locator(sel).first.tap()) if dev=='m' else (lambda sel: pg.locator(sel).first.click())
    def tab(t):
        if dev=='m':
            if not pg.evaluate("t=>document.querySelector('.tabs').classList.contains('open')&&tab===t",t): tap('#tab-'+t)
        else: tap('#tab-'+t)
        pg.wait_for_timeout(150)
    step('tip',lambda: pg.locator('#tipOk').is_visible() and tap('#tipOk'))
    step('new project',lambda:(tap('#projBtn'),pg.fill('#newProjName','בדיקה'),tap('#newProjBtn')))
    def shapes():
        tab('room')
        for i in range(pg.locator('.chips .chip').count()):
            pg.locator('.chips .chip').nth(i).click(); pg.wait_for_timeout(80)
        pg.locator('.chips .chip').first.click()
    step('shapes',shapes)
    def sizes():
        tab('room'); pg.fill('#rL','1000'); pg.fill('#rW','700'); pg.locator('#rL').press('Enter'); pg.wait_for_timeout(100)
        assert pg.evaluate("()=>state.L")==1000, pg.evaluate("()=>state.L")
    step('room size',sizes)
    step('column',lambda:(tab('room'),tap('#addCol')))
    step('sketch upload',lambda:(tab('room'),pg.set_input_files('#skFile','sketch.jpg'),pg.wait_for_timeout(800)))
    def sketchView():
        if pg.locator('#skView').is_visible(): pg.keyboard.press('Escape'); 
        if pg.locator('#skClose').count() and pg.locator('#skClose').is_visible(): pg.locator('#skClose').click()
    step('close sketch view',sketchView)
    step('sketch show',lambda:(tab('room'),pg.locator('#skShow').check(),pg.wait_for_timeout(100)))
    def tables():
        tab('tables'); tap('#tAdd'); pg.wait_for_timeout(100)
        for k in ['aRot','aDup']: pg.locator('#'+k).click(); pg.wait_for_timeout(80)
        pg.locator('#aDel').click(); pg.wait_for_timeout(80)
    step('table ops',tables)
    def sizeedit():
        tab('tables'); pg.locator('#sEditBtn').click(); pg.wait_for_timeout(100)
        tap('#addSize'); pg.wait_for_timeout(100)
    step('size edit/custom',sizeedit)
    def catalog():
        tab('tables'); tap('#catOpen'); pg.wait_for_timeout(100)
        for i in range(pg.locator('#catTags button').count()): pg.locator('#catTags button').nth(i).click(); pg.wait_for_timeout(50)
        pg.fill('#catQ','פינג'); pg.locator('#catList [data-add]').first.click(); pg.wait_for_timeout(150)
    step('catalog',catalog)
    step('fill',lambda:(tab('tables'),tap('#tFill'),pg.wait_for_timeout(200)))
    def furn():
        tab('furn')
        n=pg.locator('.fbtn').count()
        for i in range(n):
            if dev=='m': tab('furn')
            pg.locator('.fbtn').nth(i).click(); pg.wait_for_timeout(60)
        assert pg.evaluate("()=>state.furn.length")>=n
    step('furniture all',furn)
    step('gaps presets',lambda:(tab('gaps'),[pg.locator('.preset, .gp button, #panel button').nth(i).click() for i in range(2)]))
    step('undo x5',lambda:[pg.locator('#undo').click() for _ in range(5) if pg.locator('#undo').is_enabled()])
    step('dark mode',lambda:(pg.locator('#themeBtn').click(),pg.wait_for_timeout(200),pg.screenshot(path=f'e2e_dark_{dev}.png'),pg.locator('#themeBtn').click()))
    if dev=='d':
        def keys():
            pg.evaluate("()=>select({type:'t',o:state.tables[0]})")
            for k in ['ArrowLeft','Shift+ArrowUp','r','Control+d','Delete','Control+z','Escape']: pg.keyboard.press(k); pg.wait_for_timeout(50)
        step('keyboard',keys)
    def viz():
        tap('#vizOpen'); pg.wait_for_timeout(4000)
        for v in ['top','eye','angle']: pg.locator(f'#vizViews button[data-v="{v}"]').click(); pg.wait_for_timeout(400)
        if not pg.locator('.vizstyle').get_attribute('open') is not None: pg.locator('.vizstyle summary').click()
        n=pg.locator('.sw').count()
        for i in range(n): pg.locator('.sw').nth(i).click(); pg.wait_for_timeout(500)
        pg.locator('#dimToggle').click(); pg.wait_for_timeout(400)
    step('viz',viz)
    def save():
        with pg.expect_download(timeout=20000) as dl: pg.locator('#vizSave').click()
        dl.value.save_as(f'e2e_img_{dev}.png')
    step('save image',save)
    url={}
    def share():
        pg.locator('#vizShare').click(); pg.wait_for_timeout(700); url['u']=pg.input_value('#shareUrl'); assert '#' in url['u']
    step('share link',share)
    step('close viz',lambda:(pg.locator('#vizClose').click(),pg.wait_for_timeout(200)))
    def viewer():
        u=url['u'].replace('https://yoelko.github.io/table-fit./preview/','http://127.0.0.1:8770/preview/index.html')
        p2=ctx.new_page(); p2.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
        e2=[]; p2.on('pageerror',lambda e:e2.append(str(e)))
        p2.goto(u); p2.wait_for_timeout(4500); p2.screenshot(path=f'e2e_viewer_{dev}.png')
        assert not e2, e2
        print('viewer url',u[:80],p2.url[:80],p2.evaluate("()=>typeof VIEWER"))
        p2.locator('#vizImport').click(); p2.wait_for_timeout(800)
        assert not p2.evaluate("()=>VIEWER"); p2.close()
    step('viewer + import',viewer)
    def projects():
        tap('#projBtn'); pg.wait_for_timeout(150)
        pg.locator('.prow [data-a="dup"]').first.click(); pg.wait_for_timeout(100)
        pg.locator('.prow [data-a="ren"]').first.click(); pg.locator('.prow input').fill('שם חדש'); pg.locator('.prow [data-a="ok"]').click()
        pg.locator('.prow [data-a="del"]').last.click(); pg.locator('.prow [data-a="ok"]').click(); pg.wait_for_timeout(100)
        pg.locator('#plist .popen').last.click(); pg.wait_for_timeout(200)
    step('projects',projects)
    def adv():
        pg.evaluate("()=>openAdvisor()"); pg.fill('#advText','חדר 10 על 7 מטר בבית'); pg.locator('#advGo').click(); pg.wait_for_selector('.pcard',timeout=30000); pg.locator('[data-use]').first.click(); pg.wait_for_timeout(300)
    step('advisor',adv)
    step('reload persists',lambda:(pg.wait_for_timeout(600),pg.reload(),pg.wait_for_timeout(900)))
    print(dev, json.dumps(log,ensure_ascii=False,indent=0)); print('ERRORS',errs[:10]); b.close()
