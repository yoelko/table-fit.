from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1366,'height':860},service_workers="block"); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(800)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    pg.evaluate("()=>{createProject('i'); state.L=800; state.W=600; refreshRoom(); addTable(items[1]); addFurn('sofa'); select(null);}")
    # select furniture and drag the resize handle
    bb=pg.locator('#svg [data-f="0"]').first.bounding_box(); pg.mouse.click(bb['x']+bb['width']/2,bb['y']+bb['height']/2); pg.wait_for_timeout(200)
    h=pg.locator('#svg [data-h]').first.bounding_box(); w0=pg.evaluate("()=>state.furn[0].w")
    pg.mouse.move(h['x']+h['width']/2,h['y']+h['height']/2); pg.mouse.down(); pg.mouse.move(h['x']+40,h['y']+10,steps=6); pg.mouse.up(); pg.wait_for_timeout(200)
    print('resize w',w0,'->',pg.evaluate("()=>JSON.stringify(state.furn[0])+' cmpx '+cmPerPx()"))
    # table position fields
    pg.evaluate("()=>select({type:'t',o:state.tables[0]})"); pg.wait_for_timeout(200)
    print('pos fields', pg.locator('#posX').count(), pg.locator('#posY').count())
    if pg.locator('#posX').count():
        pg.fill('#posX','150'); pg.locator('#posX').press('Enter'); pg.wait_for_timeout(150)
        print('table x edge', pg.evaluate("()=>{const t=state.tables[0];return box(t.cx,t.cy,dims(t).O).x}"))
    # column add and drag
    pg.evaluate("()=>{select(null); state.cols.push({x:600,y:100,w:40,h:40}); refreshRoom();}")
    c=pg.locator('#svg [data-col="0"]').first.bounding_box(); pg.mouse.move(c['x']+5,c['y']+5); pg.mouse.down(); pg.mouse.move(c['x']+60,c['y']+40,steps=6); pg.mouse.up(); pg.wait_for_timeout(200)
    print('col', pg.evaluate("()=>JSON.stringify(state.cols[0])"))
    pg.screenshot(path='interact.png'); print('errors',errs); b.close()
