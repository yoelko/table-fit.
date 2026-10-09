from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for mob in [True,False]:
        c=b.new_context(viewport={'width':390,'height':844} if mob else {'width':1366,'height':860},service_workers="block",is_mobile=mob,has_touch=mob); pg=c.new_page()
        e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
        pg.add_init_script("""if(!sessionStorage.getItem('s')){sessionStorage.setItem('s',1); localStorage.setItem('tf-projects-v1',JSON.stringify({current:'old',list:[{id:'old',name:'לקוח ישן',updated:1,room:{shape:'rect',L:700,W:500,a:0,b:0,custom:null,cols:[],tables:[{name:'ביליארד 8 פיט',kind:'cue',L:244,W:137,cx:350,cy:250,rot:false}],furn:[]},style:{},bg:{src:'data:image/jpeg;base64,'+btoa('x'.repeat(2000)),show:true,op:.4}}]}));}""")
        pg.goto("http://127.0.0.1:8770/index.html"); pg.wait_for_timeout(1800)
        r1=pg.evaluate("()=>[cur.name,state.tables.length,state.furn.length,GAP.table,PROJ.list.map(p=>p.name).join('|'),!!PROJ.list.find(p=>p.id==='old').bg]")
        pg.reload(); pg.wait_for_timeout(1500)
        r2=pg.evaluate("()=>[cur.name,PROJ.list.length]")
        print('mobile' if mob else 'desktop','first load:',r1,'| after reload:',r2,'errors',e)
        pg.screenshot(path=f'inbox_{"m" if mob else "d"}.png'); c.close()
    b.close()
