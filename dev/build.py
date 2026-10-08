import json, sys
VER=sys.argv[1]
PREVIEW=len(sys.argv)>2 and sys.argv[2]=='preview'
body=open('room-fit.html',encoding='utf-8').read()
head='''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2b120d">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="mobile-web-app-capable" content="yes">
<meta name="description" content="תכנון חדר משחקים: כמה שולחנות ביליארד וסנוקר נכנסים, איפה, והדמיה בתלת מימד.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="שולחן לחדר">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
<style>html{background:#2b120d}body{margin:0}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style>
'''
upd=open('updater.html',encoding='utf-8').read().replace('@@VER@@',VER)
R='/home/claude/table-fit./'
if PREVIEW:
    # test address: own saved data (separate storage keys), links that open the test version, no offline worker, visible badge
    R+='preview/'
    import os; os.makedirs(R,exist_ok=True)
    body=body.replace('"tf-','"tfp-').replace('https://yoelko.github.io/table-fit./','https://yoelko.github.io/table-fit./preview/')
    body=body.replace('<title>','<title>ניסיון · ')
    upd=upd.replace('if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js").catch(()=>{});}','')
    upd+='<div style="position:fixed;left:8px;bottom:calc(env(safe-area-inset-bottom,0px) + 8px);z-index:99;background:#c9a24d;color:#1b120c;font:700 11px Heebo,Arial,sans-serif;padding:3px 8px;border-radius:99px;pointer-events:none;opacity:.9">גרסת ניסיון '+VER+'</div>'
    head=head.replace('<link rel="manifest" href="manifest.webmanifest">\n','').replace('href="apple-touch-icon.png"','href="../apple-touch-icon.png"').replace('href="icon-192.png"','href="../icon-192.png"')
idx=body.index('<div class="app"')
open(R+'index.html','w',encoding='utf-8').write(head+body[:idx]+'</head>\n<body>\n'+body[idx:]+'\n'+upd+'\n</body>\n</html>\n')
json.dump({"version":VER},open(R+'version.json','w'))
if not PREVIEW:
    sw=open(R+'sw.js').read(); import re
    open(R+'sw.js','w').write(re.sub(r'table-fit-v\d+','table-fit-v'+VER,sw))
