from playwright.sync_api import sync_playwright
import sys
url=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(service_workers="block",viewport={'width':390,'height':780},is_mobile=True,has_touch=True,device_scale_factor=2)
    pg=ctx.new_page(); pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(700)
    if pg.locator('#tipOk').is_visible(): pg.locator('#tipOk').tap()
    cdp=ctx.new_cdp_session(pg)
    def drag(x0,y0,x1,y1,steps=12):
        cdp.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":x0,"y":y0}]})
        for i in range(1,steps+1): cdp.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":x0+(x1-x0)*i/steps,"y":y0+(y1-y0)*i/steps}]}); pg.wait_for_timeout(16)
        cdp.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]}); pg.wait_for_timeout(200)
    pg.evaluate("()=>{addFurn('armchair'); addTable(items[0]); select(null); drawPlan();}"); pg.wait_for_timeout(300)
    st=lambda: pg.evaluate("()=>({f:[state.furn[0].cx,state.furn[0].cy,state.furn[0].w], t:[state.tables[0].cx,state.tables[0].cy], z:VIEW.z, ptrs:ptrs.size})")
    print('start',st())
    for sel in ['[data-f="0"]','[data-t="0"]']:
        bb=pg.locator('#svg '+sel).first.bounding_box(); x,y=bb['x']+bb['width']/2,bb['y']+bb['height']/2
        drag(x,y,x+40,y+30); print('after drag',sel,st())
        drag(x+40,y+30,x+10,y+60); print('again',sel,st())
    pg.evaluate("()=>ptrs.set(999,{x:5,y:5})")  # a lift that was never reported
    bb=pg.locator('#svg [data-f="0"]').first.bounding_box(); x,y=bb['x']+bb['width']/2,bb['y']+bb['height']/2
    drag(x,y,x+30,y+30); print('stale pointer drag',st())
    print('fill', pg.evaluate("()=>{state.L=1200;state.W=800;P=roomPoints();G=buildGrid(P);state.tables=[]; addTable(items[2]); const a=state.tables[0], ax=a.cx; fillRoom(items[4]); return [state.tables.length, state.tables[0]===a&&a.cx===ax, state.tables.map(t=>t.name).join('|')]}"))
    # list scroll in the tables drawer
    pg.locator('#tab-tables').tap(); pg.wait_for_timeout(300)
    print('panel', pg.evaluate("()=>{const p=$('panel'),s=p.querySelector('.sizes');return {ph:p.clientHeight,psh:p.scrollHeight,sh:s.clientHeight,ssh:s.scrollHeight}}"))
    print('errors',errs); b.close()
