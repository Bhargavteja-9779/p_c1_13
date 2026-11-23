"""Re-compute received->accepted stats keeping only research articles (OpenAlex type 'article', excluding
letters/comments/editorials/corrections by title). Usage: python research_only.py dates_raw/<file>.csv ..."""
import csv, json, sys, re, statistics, urllib.request, urllib.parse, time
BAD = re.compile(r'\b(letter|reply|response to|comment|correspondence|editorial|correction|erratum|retraction|in memoriam|viewpoint|perspective|consensus|guideline|recommendation|review|meta-analysis|position statement|year in review)\b', re.I)
def oa_types(dois):
      out = {}
      for i in range(0, len(dois), 50):
          chunk = dois[i:i+50]
          f = '|'.join('https://doi.org/' + d.lower() for d in chunk)
          u = 'https://api.openalex.org/works?' + urllib.parse.urlencode({'filter': 'doi:' + f, 'per_page': 50, 'select': 'doi,type'})
          for _ in range(3):
              try:
                  r = json.load(urllib.request.urlopen(u, timeout=60)); break
              except Exception: time.sleep(3)
          else: continue
          for w in r['results']:
              out[(w['doi'] or '').replace('https://doi.org/', '').lower()] = w['type']
          time.sleep(0.3)
      return out
def main():
  for path in sys.argv[1:]:
      rows = list(csv.DictReader(open(path)))
      t = oa_types([r['doi'] for r in rows])
      keep = [r for r in rows if t.get(r['doi'].lower()) == 'article' and not BAD.search(r['title'])]
      for r in rows: r['openalex_type'] = t.get(r['doi'].lower(), ''); r['kept_research'] = int(r in keep)
      with open(path.replace('.csv', '_typed.csv'), 'w', newline='') as f:
          w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
      d = sorted(int(r['days']) for r in keep)
      if len(d) >= 4:
          q = statistics.quantiles(d, n=4)
          print(f"{path.split('/')[-1][:60]} | research n={len(d)}/{len(rows)} median={statistics.median(d)} p75={q[2]} max={max(d)}")
      else:
          print(path, 'too few', len(d))
if __name__ == '__main__':
    main()
