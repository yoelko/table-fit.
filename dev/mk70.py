import json,time
from playwright.sync_api import sync_playwright
TXT='מקום 70/20 מטר, עמוד כל 10 מטר לאורך ה70, דלפק בר בעומק 40 ס"מ במרחק 1.5 מטר מהקיר, ספות כורסאות טלוויזיות, 30% שולחנות 10 פיט, 70% שולחנות 9 פיט, סנוקר'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900})
    pg.goto("http://127.0.0.1:8770/preview/index.html"); pg.wait_for_timeout(1200)
    r=pg.evaluate("t=>{const ps=makeProposals(parseRoom(t)); return {room:ps[0].room,style:{...DEFAULT_STYLE(),title:'אולם סנוקר 70×20 עם ישיבה'}}}",TXT)
    b.close()
inb=json.load(open('/home/claude/table-fit./inbox.json'))
inb['projects']=[x for x in inb['projects'] if x['id']!='p-hall70b']
sizes=[{'name':'Regiis סנוקר 10 פיט','kind':'cue','L':320,'W':176},{'name':'Regiis Pro 9 פיט','kind':'cue','L':284,'W':155}]
inb['projects'].append({'id':'p-hall70b','name':'אולם סנוקר 70×20 עם ישיבה','updated':int(time.time()*1000),'room':r['room'],'style':r['style'],'gaps':{'wall':140,'table':120},'sizes':sizes})
for f in ['/home/claude/table-fit./inbox.json','/home/claude/table-fit./preview/inbox.json']: json.dump(inb,open(f,'w'),ensure_ascii=False)
print(len(r['room']['tables']),len(r['room']['furn']),len(r['room']['cols']))
