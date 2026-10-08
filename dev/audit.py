import sys
from playwright.sync_api import sync_playwright
tag=sys.argv[1] if len(sys.argv)>1 else 'a'
three=open('t3/build/three.min.js','rb').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    for vp,dev in [({'width':390,'height':844},'m'),({'width':1440,'height':900},'d')]:
        ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=dev=='m',has_touch=dev=='m',device_scale_factor=2 if dev=='m' else 1); pg=ctx.new_page()
        pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(1200)
        pg.screenshot(path=f'audit/{tag}_{dev}_01_first.png')
        if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
        pg.evaluate("()=>{createProject('מועדון הגליל'); state.L=1500; state.W=1000; P=roomPoints(); G=buildGrid(P); fillRoom(items[2]); addFurn('sofa'); addFurn('bar'); addFurn('tv'); select(null); drawPlan(); renderPanel();}")
        pg.wait_for_timeout(400); pg.screenshot(path=f'audit/{tag}_{dev}_02_plan.png')
        for t in ['tables','furn','room','gaps']:
            pg.click('#tab-'+t); pg.wait_for_timeout(300); pg.screenshot(path=f'audit/{tag}_{dev}_03_tab_{t}.png')
            if dev=='m': pg.click('#tab-'+t); pg.wait_for_timeout(200)
        pg.evaluate("()=>select({type:'t',o:state.tables[0]})"); pg.wait_for_timeout(300); pg.screenshot(path=f'audit/{tag}_{dev}_04_selected.png')
        pg.evaluate("()=>select(null)")
        pg.click('#projBtn'); pg.wait_for_timeout(300); pg.screenshot(path=f'audit/{tag}_{dev}_05_projects.png'); pg.click('#projClose')
        pg.click('#vizOpen'); pg.wait_for_timeout(5000); pg.screenshot(path=f'audit/{tag}_{dev}_06_viz.png')
        pg.click('#dimToggle'); pg.wait_for_timeout(1200); pg.screenshot(path=f'audit/{tag}_{dev}_07_vizdims.png')
        pg.click('#vizShare'); pg.wait_for_timeout(800); pg.screenshot(path=f'audit/{tag}_{dev}_08_share.png')
        print(dev,'errors',errs[:3]); ctx.close()
    b.close()
