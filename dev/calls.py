import sys,json
from playwright.sync_api import sync_playwright
three=open('t3/build/three.min.js','rb').read()
url=sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:8770/index.html"
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_context(viewport={'width':1366,'height':860},service_workers="block").new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    pg.goto(url); pg.wait_for_timeout(2500)
    r=pg.evaluate("""async()=>{ createProject('perf'); state.L=4700; state.W=1500; P=roomPoints(); G=buildGrid(P); fillRoom(items.find(i=>i.L===292)); for(const k of ['bar','backbar','sofa','tv','plant']) addFurn(k);
      await openViz(); let t=performance.now(); buildScene(); const bs=performance.now()-t; V.r.info.reset(); V.r.render(V.scene,V.cam);
      let meshes=0, mats=new Set(), geos=new Set(); V.scene.traverse(o=>{ if(o.isMesh){ meshes++; [].concat(o.material).forEach(m=>mats.add(m)); geos.add(o.geometry);} });
      return {tables:state.tables.length, build:Math.round(bs), calls:V.r.info.render.calls, tris:V.r.info.render.triangles, meshes, mats:mats.size, geos:geos.size}; }""")
    print(json.dumps(r)); b.close()
