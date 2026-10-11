import sys,time,json
from playwright.sync_api import sync_playwright
TXT0='מקום 70/20 מטר, עמוד כל 10 מטר לאורך ה70, דלפק בר בעומק 40 ס"מ במרחק 1.5 מטר מהקיר, ספות כורסאות טלוויזיות, 30% שולחנות 10 פיט, 70% שולחנות 9 פיט, סנוקר'
dev=sys.argv[1]; url=sys.argv[2] if len(sys.argv)>2 else "http://127.0.0.1:8770/preview/index.html"
TXT=sys.argv[3] if len(sys.argv)>3 else TXT0
with sync_playwright() as p:
    b=p.chromium.launch()
    vp={'width':390,'height':844} if dev=='m' else {'width':1440,'height':900}
    ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=dev=='m',has_touch=dev=='m',device_scale_factor=2 if dev=='m' else 1); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route("**/three.min.js",lambda r:r.fulfill(path="/tmp/claude-0/-home-claude/a2941520-6d34-5dd8-9a2f-962af0aae42b/scratchpad/t3/build/three.min.js"))
    pg.goto(url); pg.wait_for_timeout(1500)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    print(pg.evaluate("t=>JSON.stringify(parseRoom(t))",TXT))
    pg.evaluate("()=>{createProject('ריק');}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>openAdvisor()"); pg.wait_for_timeout(200)
    pg.fill('#advText',TXT); pg.wait_for_timeout(200)
    pg.screenshot(path=f'a70_1_{dev}.png')
    t=time.time(); pg.click('#advGo'); pg.wait_for_selector('.pcard',timeout=120000); print('proposals in %.1fs'%(time.time()-t), pg.locator('.pcard').count())
    print(pg.evaluate("()=>advProps.map(p=>{const r=p.room,c={};r.tables.forEach(t=>c[t.name]=(c[t.name]||0)+1);const f={};r.furn.forEach(x=>f[x.type]=(f[x.type]||0)+1);return p.title+' | '+p.note+' | '+JSON.stringify(c)+' furn '+JSON.stringify(f)+' cols '+r.cols.length+' L'+r.L+' W'+r.W}).join('\\n')"))
    pg.wait_for_timeout(400); pg.screenshot(path=f'a70_2_{dev}.png')
    pg.locator('[data-use]').first.click(); pg.wait_for_timeout(800); pg.screenshot(path=f'a70_3_{dev}.png')
    print('bad items:',pg.evaluate("()=>[state.tables.filter(t=>tableStatus(t)==='bad').length,state.furn.filter(f=>furnStatus(f)!=='ok').length,state.furn.filter(f=>f.aisle).length]"))
    print('errors',errs[:3]); b.close()
