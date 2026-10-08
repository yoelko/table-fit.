import sys
from playwright.sync_api import sync_playwright
dev=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch()
    vp={'width':390,'height':844} if dev=='m' else {'width':1440,'height':900}
    ctx=b.new_context(viewport=vp,service_workers="block",is_mobile=dev=='m',has_touch=dev=='m',device_scale_factor=2 if dev=='m' else 1); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(900)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    pg.evaluate("()=>{createProject('ריק');}"); pg.wait_for_timeout(300)
    pg.screenshot(path=f'adv0_{dev}.png')
    for txt in ["חדר 12 על 8 מטר, מועדון סנוקר עם בר","מרתף שבע על חמש מטר בבית עם ספה וטלוויזיה","אולם 1500 על 1000 ס\"מ מועדון ביליארד 9 פיט","חדר 6 על 5 מטר לערבי פוקר","חדר בצורת L עשר על שמונה"]:
        print(txt,'=>',pg.evaluate("t=>JSON.stringify(parseRoom(t))",txt))
    pg.click('#advFromEmpty'); pg.wait_for_timeout(200)
    pg.fill('#advText','חדר 12 על 8 מטר, מועדון סנוקר עם בר'); pg.wait_for_timeout(100)
    pg.screenshot(path=f'adv1_{dev}.png')
    import time; t=time.time(); pg.click('#advGo'); pg.wait_for_selector('.pcard',timeout=60000); print('proposals in %.1fs'%(time.time()-t), pg.locator('.pcard').count())
    pg.wait_for_timeout(500); pg.screenshot(path=f'adv2_{dev}.png',full_page=False)
    pg.locator('[data-use]').first.click(); pg.wait_for_timeout(500); pg.screenshot(path=f'adv3_{dev}.png')
    print('project:',pg.evaluate("()=>cur.name+' tables '+state.tables.length+' furn '+state.furn.length"))
    for txt in ["מרתף 7 על 5 מטר בבית, עם ספה וטלוויזיה","חדר 6 על 5 מטר לערבי פוקר","אולם 15 על 10 מטר, מועדון ביליארד 9 פיט"]:
        r=pg.evaluate("t=>{const q=parseRoom(t); const ps=makeProposals(q); return ps.map(p=>p.title+':'+p.room.tables.length+'/'+p.room.furn.length).join(' | ')}",txt); print(txt,'->',r)
    print('errors',errs[:3]); b.close()
