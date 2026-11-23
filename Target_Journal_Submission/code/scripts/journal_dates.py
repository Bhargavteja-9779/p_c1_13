"""Collect Received/Accepted dates for recent articles of candidate journals from Crossref 'assertion' metadata.
Usage: python journal_dates.py ISSN [ISSN ...]   -> prints summary, writes per-journal CSV to journal_selection/dates_raw/
"""
import sys, json, csv, os, statistics, urllib.request, urllib.parse, datetime as dt, re, time
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'journal_selection', 'dates_raw')
os.makedirs(OUT, exist_ok=True)
def parse(s):
    s = s.strip()
    for f in ('%d %B %Y', '%d %b %Y', '%Y-%m-%d', '%B %d, %Y', '%d/%m/%Y'):
        try: return dt.datetime.strptime(s, f).date()
        except ValueError: pass
    return None
def fetch(issn, since='2025-06-01', rows=120):
    q = urllib.parse.urlencode({'filter': f'issn:{issn},from-pub-date:{since},type:journal-article', 'rows': rows,
        'select': 'DOI,title,assertion,container-title,publisher,issued', 'mailto': ''})
    q = q.replace('&mailto=', '')
    with urllib.request.urlopen('https://api.crossref.org/works?' + q, timeout=60) as r:
        return json.load(r)['message']['items']
def main():
    for issn in sys.argv[1:]:
        try: items = fetch(issn)
        except Exception as e: print(issn, 'ERR', e); continue
        rows = []
        jname = pub = ''
        for it in items:
            jname = (it.get('container-title') or [''])[0]; pub = it.get('publisher', '')
            a = {x.get('name', '').lower(): x.get('value', '') for x in it.get('assertion', []) or []}
            rec = a.get('received') or a.get('date_received'); acc = a.get('accepted') or a.get('date_accepted')
            if not rec or not acc: continue
            r, c = parse(rec), parse(acc)
            if not r or not c: continue
            rows.append({'title': (it.get('title') or [''])[0][:150], 'doi': it['DOI'], 'received': r, 'accepted': c, 'days': (c - r).days})
        name = re.sub(r'\W+', '_', jname)[:50] or issn
        with open(os.path.join(OUT, f'{issn}_{name}.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['title', 'doi', 'received', 'accepted', 'days']); w.writeheader(); w.writerows(rows)
        d = sorted(x['days'] for x in rows)
        if d:
            q = statistics.quantiles(d, n=4)
            print(f'{issn} | {jname} | {pub} | n_items={len(items)} n_dated={len(d)} | median={statistics.median(d)} p75={q[2]} max={max(d)}')
        else:
            print(f'{issn} | {jname} | {pub} | n_items={len(items)} no dates')
        time.sleep(2.5)
main()
