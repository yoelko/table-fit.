import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(service_workers="block",accept_downloads=True); pg=ctx.new_page(); pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto("http://127.0.0.1:8770/index.html"); pg.wait_for_timeout(600)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    pg.evaluate("()=>{createProject('לקוח א'); addTable(items[1]); createProject('לקוח ב'); addTable(items[2]); addTable(items[2]);}")
    pg.click('#projBtn'); pg.wait_for_timeout(200)
    with pg.expect_download() as dl: pg.click('#bkSave')
    path='backup_test.json'; dl.value.save_as(path); d=json.load(open(path))
    print('file',dl.value.suggested_filename,len(d['projects']),'projects; hint:',pg.inner_text('#bkHint')[:40])
    # wipe and restore in a fresh browser profile
    ctx2=b.new_context(service_workers="block"); pg2=ctx2.new_page(); pg2.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    pg2.goto("http://127.0.0.1:8770/index.html"); pg2.wait_for_timeout(600)
    pg2.evaluate("()=>{$('proj').hidden=false}"); pg2.set_input_files('#bkFile',path); pg2.wait_for_timeout(500)
    print('restored:',pg2.evaluate("()=>PROJ.list.map(p=>p.name+':'+(p.room.tables||[]).length).join(', ')"), '|', pg2.inner_text('#toast'))
    pg2.set_input_files('#bkFile',path); pg2.wait_for_timeout(400); print('again:',pg2.inner_text('#toast'))
    print('errors',errs); b.close()
