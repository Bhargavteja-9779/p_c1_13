import sys, json, urllib.request, urllib.parse, time
for q in sys.argv[1:]:
    u = 'https://api.crossref.org/works?' + urllib.parse.urlencode({'query.bibliographic': q, 'rows': 2, 'select': 'DOI,title,issued,container-title,author'})
    for _ in range(5):
        try: items = json.load(urllib.request.urlopen(u, timeout=60))['message']['items']; break
        except Exception: time.sleep(8)
    else: print(q, 'FAILED'); continue
    time.sleep(3)
    for it in items:
        a = (it.get('author') or [{}])[0].get('family', '')
        print(q[:40], '=>', it['DOI'], '|', a, it['issued']['date-parts'][0][0], '|', (it.get('title') or [''])[0][:90], '|', (it.get('container-title') or [''])[0][:40])
