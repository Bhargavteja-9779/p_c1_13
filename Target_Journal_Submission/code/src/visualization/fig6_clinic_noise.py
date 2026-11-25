"""Fig. 6 (amendment C): A false alarms on held-out clinic-noise null by calibration source; B sensitivity at matched
clinic-noise false alarms, real eyes vs semi-synthetic truth; C cumulative false alarms vs progressors flagged by test 8
under three monitoring rules. Usage (from code/): python -m src.visualization.fig6_clinic_noise"""
import os, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
plt.rcParams.update({'font.size': 8.5, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#52514e',
                     'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e', 'savefig.dpi': 300})
STY = {'D1': ('D1 trend test', '#2a78d6', 'o'), 'D2c': ('D2c rate of change', '#eb6834', 's'),
       'D6s': ('D6s regional trend', '#1baf7a', '^'), 'D8c': ('D8c tree model', '#eda100', 'D'),
       'D11': ('D11 moderated trend (new)', '#7d52c7', 'P')}
SRC = {'RC': ('Weekly retests', '#c9c7c1'), 'SC': ('Shuffled clinic records', '#8f8d87'), 'CNN': ('Clinic-noise null', '#2a2925')}

def main():
    J = json.load(open(os.path.join(ROOT, 'results', 'amendC', 'amendC.json')))
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.4), gridspec_kw=dict(width_ratios=[1.15, 1, 1]))
    # A
    a = ax[0]; dets = list(STY); w = 0.26
    for i, (s, (lab, col)) in enumerate(SRC.items()):
        v = [np.mean([J['ho_cnn'][s][d][k][0] for k in '3456']) for d in dets]
        a.bar(np.arange(5) + (i - 1) * w, np.array(v) * 100, w, color=col, label=lab)
    a.axhline(5, ls='--', color='#52514e', lw=0.8); a.set_xticks(range(5)); a.set_xticklabels(dets)
    a.set_ylabel('False alarms on held-out clinic-noise\nnull series, % (mean of 3–6 tests)')
    a.set_title('A  Threshold source vs false alarms', loc='left', fontsize=9); a.legend(frameon=False, fontsize=7, loc='upper left'); a.set_ylim(0, 24)
    a.grid(axis='y', color='#e9e9e6', lw=0.6)
    # B
    b = ax[1]
    for d, (lab, col, mk) in STY.items():
        real = [J['real']['CNN'][k][d]['sens'][0] for k in '3456']; syn = [J['syn']['global_1.0'][d][k][0] for k in '3456']
        b.plot([3, 4, 5, 6], real, color=col, marker=mk, lw=2, ms=5, mec='white', label=lab)
        b.plot([3, 4, 5, 6], syn, color=col, marker=mk, lw=1, ls=':', ms=4, mec='white')
    b.set_xticks([3, 4, 5, 6]); b.set_xlabel('Number of tests'); b.set_ylim(0, 1)
    b.set_ylabel('Sensitivity at 5% clinic-noise false alarms'); b.grid(axis='y', color='#e9e9e6', lw=0.6)
    b.set_title('B  Real eyes (solid) vs synthetic 1 dB/yr (dotted)', loc='left', fontsize=9)
    # C
    c = ax[2]; mk_rule = {'naive': 'o', 'confirm': 's', 'budget': '*'}
    for d, (lab, col, _) in STY.items():
        pts = [(J['seq'][d][r]['ho_cnn_cum_fa'][0], J['seq'][d][r]['prog_by8'][0]) for r in mk_rule]
        c.plot([p[0] * 100 for p in pts], [p[1] for p in pts], color=col, lw=0.8, alpha=0.6)
        for (x, y), (r, m) in zip(pts, mk_rule.items()):
            c.scatter(x * 100, y, color=col, marker=m, s=60 if m == '*' else 30, edgecolor='white', lw=0.6, zorder=3)
    for r, m in mk_rule.items():
        c.scatter([], [], color='#52514e', marker=m, s=40, label={'naive': 'Every review at 5%', 'confirm': 'Confirm on next test',
                                                                   'budget': '5% budget over 6 reviews'}[r])
    c.axvline(5, ls='--', color='#52514e', lw=0.8); c.set_xlabel('Cumulative false alarms over reviews 3–8, %\n(held-out clinic-noise null)')
    c.set_ylabel('Reference progressors flagged by test 8'); c.set_ylim(0.3, 1); c.legend(frameon=False, fontsize=7, loc='lower right')
    c.set_title('C  Monitoring rules', loc='left', fontsize=9); c.grid(color='#e9e9e6', lw=0.6)
    h, l = b.get_legend_handles_labels()
    fig.legend(h, l, loc='upper center', ncol=5, frameon=False, fontsize=7.5, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(ROOT, 'figures', 'fig6_clinic_noise_calibration.png'))

if __name__ == '__main__':
    main()
