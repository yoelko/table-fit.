import json
from playwright.sync_api import sync_playwright
three=open('t3/build/three.min.js','rb').read()
JS="""async()=>{
  GAP.wall=140; GAP.table=120;
  const s=2.82, X=px=>Math.round((px-108)*s), Y=py=>Math.round((py-290)*s);
  createProject('ניסיון סרטוט 1'); STYLE.title='ניסיון סרטוט 1';
  state.custom=[[0,0],[X(1800),0],[X(1800),Y(822)],[0,Y(800)]];
  state.cols=[[365,520],[605,520],[1315,520],[1555,520]].map(([px,py])=>({x:X(px)-20,y:Y(py)-20,w:40,h:40})).concat([{x:X(840),y:0,w:X(1085)-X(840),h:Y(512)}]);
  P=roomPoints(); G=buildGrid(P);
  const L=G.maxX, stair=state.cols[4], colBot=Math.max(...state.cols.slice(0,4).map(c=>c.y+c.h));
  const it9=items.find(i=>i.L===292&&i.W===161), r10=PLAYON.find(r=>r[0]==='Regiis סנוקר 10 פיט'), it10={name:r10[0],kind:'cue',L:r10[3],W:r10[4]};
  const bad=[];
  const put=(it,x,y,rot)=>{ const t=newTable(it); t.rot=rot; const D=dims(t); t.cx=x+D.O[0]/2; t.cy=y+D.O[1]/2;
    const ok=gridFree(G,box(t.cx,t.cy,D.N))&&state.tables.every(o=>sep(box(o.cx,o.cy,dims(o).O),box(t.cx,t.cy,D.O))>=GAP.table-.5);
    if(ok) state.tables.push(t); else bad.push(it.L+'@'+x+','+y); return ok; };
  // row A (top band, tables turned): left of the stair block, then right of it; 10 ft except the two nearest the right lounge
  const rowA=[]; for(let x=140;x+176+140<=stair.x;x+=296) rowA.push(x);
  for(let x=stair.x+stair.w+140;x+176+140<=L;x+=296) rowA.push(x);
  rowA.pop(); // the last spot on the right becomes a seating corner
  rowA.forEach((x,i)=>put(i>=rowA.length-2?it9:it10,x,140,true));
  // rows B and C (bottom band): 9 ft, first spot on the left = lounge, last on the right = bar
  const yB=colBot+140, yC=yB+161+120, xs=[]; for(let x=140;x+292+140<=L;x+=412) xs.push(x);
  xs.slice(1,-1).forEach(x=>{ put(it9,x,yB,false); put(it9,x,yC,false); });
  const lastRight=140+(xs.length-2)*412+292+140, firstLeft=xs[1]-140;
  // furniture
  const F=(type,cx,cy,rot)=>{ const d=FURN[type]; state.furn.push({type,cx,cy,w:d.w,h:d.h,rot}); };
  // bar zone at the right end of the lower band
  const bzx=(lastRight+L)/2, bmid=(yB+Math.min(G.maxY-60,yC+161))/2;
  F('backbar',L-23,bmid,90); F('bar',L-23-45-75-33,bmid,90);
  for(let k=-2;k<=2;k++) F('stool',L-23-45-75-66-35,bmid+k*58,0);
  F('tv',L-6,bmid-230,90);
  // lounge at the left end of the lower band
  const lmid=(yB+yC+161)/2;
  F('sofa',45,lmid,270); F('coffee',90+60,lmid,0); F('armchair',150+60,lmid-150,0); F('armchair',150+60,lmid+150,180);
  const wallY=x=>P[3][1]+(P[2][1]-P[3][1])*x/L; { const tx=Math.min(firstLeft-80,260); F('tv',tx,wallY(tx)-6,180); }
  // second seating corner at the right end of the top band
  const rx=(rowA[rowA.length-1]+176+140+L)/2;
  F('sofa',L-45,300,90); F('coffee',L-90-60,300,0); F('armchair',L-150-60,170,0); F('armchair',L-150-60,430,180);
  F('tv',rx,6,0);
  // a screen on the stair block facing the lower rows, cue racks on its sides, plants in corners
  F('tv',stair.x+stair.w/2,stair.y+stair.h+6,180);
  F('cuerack',stair.x-8,stair.h/2,90); F('cuerack',stair.x+stair.w+8,stair.h/2,270);
  F('plant',30,30,0); F('plant',30,wallY(30)-32,0); F('plant',L-30,wallY(L-30)-32,0);
  G=buildGrid(P); select(null); drawPlan(); saveRoom(true);
  const n10=state.tables.filter(t=>t.L===320).length, n=state.tables.length;
  const link=(await packShare()).replace('https://yoelko.github.io/table-fit./preview/','https://yoelko.github.io/table-fit./');
  return {n,n10,n9:n-n10,pct:Math.round(n10/n*100),bad,furn:state.furn.length,link};
}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    ctx=b.new_context(viewport={'width':1440,'height':900},service_workers="block"); pg=ctx.new_page()
    pg.route("**/three.min.js",lambda r:r.fulfill(body=three,content_type="application/javascript"))
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(900)
    if pg.locator('#tipOk').is_visible(): pg.click('#tipOk')
    r=pg.evaluate(JS); print(json.dumps({k:v for k,v in r.items() if k!='link'},ensure_ascii=False)); open('sketch3_link.txt','w').write(r['link'])
    pg.wait_for_timeout(300); pg.screenshot(path='sketch3_plan.png')
    pg.click('#vizOpen'); pg.wait_for_timeout(8000); pg.screenshot(path='sketch3_3d.png',timeout=120000)
    b.close()
