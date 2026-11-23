"""Supplementary Fig. S1: participant flow (numbers from results/descriptives.json). Usage: python -m src.visualization.flow"""
import os, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = json.load(open(os.path.join(ROOT, 'results', 'descriptives.json'))); u = D['uwhvf']; a = D['artes']; g = D['grape']
f = lambda x: f"{x:,}"
boxes = [
    (0.35, 0.86, f"UWHVF: {f(u['n_fields'])} fields, {f(u['n_eyes'])} eyes, {f(u['n_patients'])} patients"),
    (0.05, 0.64, f"Training: {f(u['train']['n_patients'])} patients\n{f(u['train']['n_eyes_ge3'])} eyes with >= 3 tests"),
    (0.35, 0.64, f"Validation: {f(u['val']['n_patients'])} patients\n{f(u['val']['n_eyes_ge3'])} eyes with >= 3 tests"),
    (0.65, 0.64, f"Test (locked): {f(u['test']['n_patients'])} patients\n{f(u['test']['n_eyes_ge3'])} eyes with >= 3 tests\n(shuffle audit, E3)"),
    (0.65, 0.40, f"Test eyes with >= 8 tests: {u['test_ge8']['n_eyes']}\nexcluded (indeterminate): {u['test_ge8']['n_excluded']}"),
    (0.65, 0.16, f"Reference eyes (E1): {u['test_ge8']['n_prog']} progressors\n{u['test_ge8']['n_stable']} stable; {u['test_ge8']['n_ref_patients']} patients"),
    (0.02, 0.28, f"Artes retest (E2, no change)\n{a['n_patients']} patients, {a['n_eyes']} eyes\nwindows k=3-6: {a['windows']['3']}/{a['windows']['4']}/{a['windows']['5']}/{a['windows']['6']}"),
    (0.36, 0.28, f"GRAPE (E4, external)\n{g['n_eyes']} eyes, {g['n_patients']} patients\n>= 4 tests: {g['n_ge4']}\nMD-label progressing: {g['n_md_prog']}"),
]
fig, ax = plt.subplots(figsize=(8, 5)); ax.axis('off')
for x, y, s in boxes:
    ax.text(x + 0.14, y + 0.05, s, ha='center', va='center', fontsize=7.5, transform=ax.transAxes,
            bbox=dict(boxstyle='square,pad=0.5', fc='#f3f3f1', ec='#52514e', lw=0.8))
for (x0, y0, x1, y1) in [(0.49, 0.86, 0.19, 0.76), (0.49, 0.86, 0.49, 0.76), (0.49, 0.86, 0.79, 0.76), (0.79, 0.59, 0.79, 0.50), (0.79, 0.35, 0.79, 0.26)]:
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), xycoords='axes fraction', arrowprops=dict(arrowstyle='->', color='#52514e', lw=0.8))
os.makedirs(os.path.join(ROOT, 'figures'), exist_ok=True)
fig.savefig(os.path.join(ROOT, 'figures', 'figS1_flow.png'), dpi=200, bbox_inches='tight'); print('ok')
