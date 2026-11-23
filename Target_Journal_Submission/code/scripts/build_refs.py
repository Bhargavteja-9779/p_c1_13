"""Fetch Crossref metadata for every DOI cited and write manuscript/references.json (Vancouver strings)."""
import json, urllib.request, time, os, sys
DOIS = """10.1016/j.ophtha.2014.05.013 10.1001/jama.2014.3192 10.1001/archopht.120.10.1268 10.1136/bjo.2007.135012 10.1038/eye.2017.1
10.1167/iovs.12-10049 10.1016/j.ophtha.2014.04.015 10.1016/j.ophtha.2014.01.020 10.1167/iovs.15-16957 10.1167/tvst.10.14.13
10.1167/tvst.7.4.20 10.1016/j.ajo.2007.09.038 10.1016/j.ophtha.2008.02.005 10.1167/tvst.11.1.1 10.1038/s41597-023-02424-4
10.1167/tvst.10.7.27 10.1016/j.ophtha.2020.12.020 10.1167/iovs.18-25568 10.1371/journal.pone.0214875 10.1038/s41598-019-54653-6
10.1167/tvst.5.3.2 10.1371/journal.pone.0357179 10.64898/2026.11.16.26368187 10.1007/978-3-032-05182-0_53 10.1016/j.ophtha.2017.01.027
10.1167/iovs.12-9476 10.1016/j.ogla.2025.11.004 10.1167/tvst.10.13.21 10.2202/1544-6115.1585 10.1080/07350015.1983.10509354
10.1561/2200000101 10.1136/bmj.q902 10.1214/19-aoas1241 10.1016/j.ophtha.2014.02.021 10.1167/tvst.10.12.4 10.1016/j.xops.2023.100423 10.1167/13.4.10""".split()
out = []
for doi in DOIS:
    for _ in range(5):
        try:
            m = json.load(urllib.request.urlopen('https://api.crossref.org/works/' + doi, timeout=60))['message']; break
        except Exception as e:
            time.sleep(6)
    else:
        out.append(dict(doi=doi, verified=False)); print('FAILED', doi); continue
    au = m.get('author', [])
    names = [f"{a.get('family','')} {''.join(x[0] for x in a.get('given','').replace('-', ' ').split() if x)}".strip() for a in au]
    names = names[:6] + (['et al'] if len(names) > 6 else [])
    yr = (m.get('issued', {}).get('date-parts') or [[None]])[0][0]
    ct = (m.get('short-container-title') or m.get('container-title') or [''])[0] or (m.get('institution', [{}])[0].get('name', '') if m.get('institution') else 'Preprint')
    s = f"{', '.join(names) if names else m.get('group-title','')}. {(m.get('title') or [''])[0]}. {ct}. {yr}"
    if m.get('volume'): s += f";{m['volume']}"
    if m.get('issue'): s += f"({m['issue']})"
    if m.get('page'): s += f":{m['page']}"
    s += f". https://doi.org/{doi}"
    out.append(dict(doi=doi, verified=True, title=(m.get('title') or [''])[0], year=yr, venue=ct, type=m.get('type'), vancouver=s))
    time.sleep(1.5)
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'manuscript', 'references.json'), 'w'), indent=1)
print(sum(o['verified'] for o in out), 'verified of', len(out))
