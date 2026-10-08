from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(service_workers="block"); pg=ctx.new_page(); pg.route("**/fonts.googleapis.com/**",lambda r:r.abort())
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    # old format: sketch stored inline in the project list
    pg.add_init_script("""if(!sessionStorage.getItem('seeded')){sessionStorage.setItem('seeded',1);const id='old1'; localStorage.setItem('tf-projects-v1',JSON.stringify({current:id,list:[{id,name:'ישן',updated:1,room:{shape:'rect',L:600,W:400,a:0,b:0,custom:null,cols:[],tables:[],furn:[]},style:{},bg:{src:'data:image/jpeg;base64,'+btoa('x'.repeat(3000)),show:true,op:.4}}]}));}""")
    pg.goto("http://127.0.0.1:8769/room-fit.html"); pg.wait_for_timeout(500)
    print('migrated:',pg.evaluate("()=>({inList:localStorage.getItem('tf-projects-v1').includes('base64'), own:(localStorage.getItem('tf-bg-old1')||'').length, mem:cur.bg&&cur.bg.src.length})"))
    pg.evaluate("()=>{state.L=777; drawPlan();}"); pg.wait_for_timeout(700)
    pg.reload(); pg.wait_for_timeout(500)
    print('after reload:',pg.evaluate("()=>({L:state.L, bg:cur.bg&&cur.bg.src.length, svgImg:document.querySelector('#svg image')?.getAttribute('href').slice(0,5)})"))
    pg.evaluate("()=>{state.L=555; drawPlan(); dispatchEvent(new Event('pagehide'));}")
    pg.reload(); pg.wait_for_timeout(500); print('pagehide flush L:',pg.evaluate("()=>state.L"))
    pg.evaluate("()=>{deleteProject('old1')}"); print('bg key removed:',pg.evaluate("()=>localStorage.getItem('tf-bg-old1')"))
    print('errors',errs); b.close()
