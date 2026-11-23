import json, urllib.request, sys
out=[]
for pub in ['P4310319965','P4310320547']:
  for page in range(1,6):
    u=f'https://api.openalex.org/sources?filter=host_organization_lineage:{pub},type:journal,summary_stats.2yr_mean_citedness:>5,works_count:>300&per_page=200&page={page}&select=display_name,issn_l,issn,summary_stats,topics'
    try: r=json.load(urllib.request.urlopen(u,timeout=60))['results']
    except Exception as e: print(e,file=sys.stderr); break
    if not r: break
    for s in r:
      t=(s.get('topics') or [{}])[0].get('field',{}).get('display_name','') if s.get('topics') else ''
      out.append((s['issn_l'],s['display_name'],round(s['summary_stats']['2yr_mean_citedness'],1),t))
for o in out: print('\t'.join(map(str,o)))
