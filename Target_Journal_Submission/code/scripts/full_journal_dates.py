"""Pull ALL Crossref records of one journal in a date window (cursor paging), keep research articles,
write acceptance_time_evidence.csv and print summary by quarter."""
import json, urllib.request, urllib.parse, csv, sys, statistics, time, datetime as dt, re, os
sys.path.insert(0, os.path.dirname(__file__))
from research_only import oa_types, BAD
from journal_dates import parse
issn, since, until, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
items, cursor = [], '*'
while True:
    q = urllib.parse.urlencode({'filter': f'issn:{issn},from-pub-date:{since},until-pub-date:{until},type:journal-article',
                                'rows': 200, 'cursor': cursor, 'select': 'DOI,title,assertion,published,volume,issue'})
    for _ in range(4):
        try: m = json.load(urllib.request.urlopen('https://api.crossref.org/works?' + q, timeout=90))['message']; break
        except Exception as e: time.sleep(10)
    if not m['items']: break
    items += m['items']; cursor = m['next-cursor']; time.sleep(3)
    if len(items) >= m['total-results']: break
rows = []
for it in items:
    a = {x.get('name', '').lower(): x.get('value', '') for x in it.get('assertion', []) or []}
    r, c = parse(a.get('received', '') or 'x'), parse(a.get('accepted', '') or 'x')
    p = it.get('published', {}).get('date-parts', [[None]])[0]
    rows.append({'title': (it.get('title') or [''])[0], 'doi': it['DOI'], 'volume': it.get('volume', ''), 'issue': it.get('issue', ''),
                 'published': '-'.join(str(x) for x in p if x), 'received': r or '', 'accepted': c or '', 'days': (c - r).days if r and c else ''})
types = oa_types([r['doi'] for r in rows])
for r in rows:
    r['openalex_type'] = types.get(r['doi'].lower(), '')
    r['research_article'] = int(r['openalex_type'] == 'article' and not BAD.search(r['title']))
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
res = [r for r in rows if r['research_article'] and r['days'] != '']
d = sorted(r['days'] for r in res)
q = statistics.quantiles(d, n=4)
print(f'all records={len(rows)} research with dates={len(d)} median={statistics.median(d)} p25={q[0]} p75={q[2]} p90={statistics.quantiles(d, n=10)[8]} max={max(d)} share<=72={sum(x<=72 for x in d)/len(d):.2f}')
by = {}
for r in res: by.setdefault(str(r['published'])[:7], []).append(r['days'])
for k in sorted(by): print(k, len(by[k]), statistics.median(by[k]))
