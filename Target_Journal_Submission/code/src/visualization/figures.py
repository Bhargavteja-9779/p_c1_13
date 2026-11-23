"""Publication figures from results/metrics.json (no hand-typed numbers). Grayscale-readable: family = colour AND marker.
Usage: python -m src.visualization.figures"""
import os, json
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FIG = os.path.join(ROOT, 'figures')
FAM = {'D1': ('Classical trend', '#2a78d6', 'o'), 'D2': ('Classical trend', '#2a78d6', 'o'), 'D3': ('Classical trend', '#2a78d6', 'o'),
       'D4': ('Permutation / conformal', '#eb6834', 's'), 'D5': ('Permutation / conformal', '#eb6834', 's'),
       'D6': ('Permutation / conformal', '#eb6834', 's'), 'D7': ('Event analysis', '#1baf7a', '^'),
       'D8': ('Machine learning', '#6250d6', 'D'), 'D9': ('Machine learning', '#6250d6', 'D'), 'D10': ('Machine learning', '#6250d6', 'D')}
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#52514e',
                     'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e', 'savefig.dpi': 300})

def short(det): return det.split()[0]

def fig_validity_power(M):
    ks = sorted(M.k.unique()); fig, axs = plt.subplots(1, len(ks), figsize=(3.0 * len(ks), 3.2), sharey=True)
    axs = np.atleast_1d(axs)
    for ax, k in zip(axs, ks):
        m = M[M.k == k].dropna(subset=['sens', 'fpr_true_null'])
        ax.axvspan(0, 0.05, color='#e9e9e6', zorder=0); ax.axvline(0.05, color='#52514e', lw=0.8, ls='--', zorder=1)
        for _, r in m.iterrows():
            fam, col, mk = FAM[short(r.detector)]
            ax.errorbar(r.fpr_true_null, r.sens, xerr=[[r.fpr_true_null - r.fpr_true_null_lo], [r.fpr_true_null_hi - r.fpr_true_null]],
                        yerr=[[r.sens - r.sens_lo], [r.sens_hi - r.sens]], fmt=mk, ms=6, color=col, ecolor=col, elinewidth=0.8,
                        capsize=0, mec='white', mew=1.2, zorder=3)
            ax.annotate(short(r.detector), (r.fpr_true_null, r.sens), xytext=(4, 3), textcoords='offset points', fontsize=7, color='#0b0b0b')
        ax.set_title(f'{k} tests', fontsize=9); ax.set_xlabel('False-alarm rate, true no-change')
        ax.set_xlim(left=0); ax.set_ylim(0, 1); ax.grid(axis='y', color='#e9e9e6', lw=0.6)
    axs[0].set_ylabel('Sensitivity, future-confirmed progressors')
    hs = [plt.Line2D([], [], marker=v[2], ls='', color=v[1], label=v[0]) for v in {v[0]: v for v in FAM.values()}.values()]
    fig.legend(handles=hs, loc='upper center', ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig2_validity_vs_power.png'), bbox_inches='tight'); plt.close(fig)

def fig_audit(M):
    m = M.dropna(subset=['fpr_shuffle', 'fpr_true_null']); fig, ax = plt.subplots(figsize=(3.6, 3.4))
    lim = max(m.fpr_shuffle.max(), m.fpr_true_null_hi.max()) * 1.1
    ax.plot([0, lim], [0, lim], color='#52514e', lw=0.8, ls='--')
    for _, r in m.iterrows():
        fam, col, mk = FAM[short(r.detector)]
        ax.plot(r.fpr_shuffle, r.fpr_true_null, mk, color=col, ms=5, mec='white', mew=1)
    ax.set_xlabel('False-alarm rate, shuffle audit (UW clinic)'); ax.set_ylabel('False-alarm rate, true no-change (Halifax)')
    ax.set_xlim(0, lim); ax.set_ylim(0, lim); ax.grid(color='#e9e9e6', lw=0.6)
    hs = [plt.Line2D([], [], marker=v[2], ls='', color=v[1], label=v[0]) for v in {v[0]: v for v in FAM.values()}.values()]
    ax.legend(handles=hs, frameon=False, fontsize=7, loc='upper left')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig3_shuffle_audit_vs_true_null.png'), bbox_inches='tight'); plt.close(fig)

def fig_grape(M):
    m = M.dropna(subset=['grape_sens']); ks = sorted(m.k.unique())
    fig, axs = plt.subplots(1, len(ks), figsize=(3.4 * len(ks), 3.0), sharey=True); axs = np.atleast_1d(axs)
    for ax, k in zip(axs, ks):
        mm = m[m.k == k].sort_values('detector')
        for i, (_, r) in enumerate(mm.iterrows()):
            fam, col, mk = FAM[short(r.detector)]
            ax.errorbar(1 - r.grape_spec, r.grape_sens, xerr=[[r.grape_spec_hi - r.grape_spec], [r.grape_spec - r.grape_spec_lo]],
                        yerr=[[r.grape_sens - r.grape_sens_lo], [r.grape_sens_hi - r.grape_sens]], fmt=mk, color=col, ms=6,
                        elinewidth=0.8, mec='white', mew=1.2)
            ax.annotate(short(r.detector), (1 - r.grape_spec, r.grape_sens), xytext=(4, 3), textcoords='offset points', fontsize=7)
        ax.set_title(f'GRAPE, {k} tests', fontsize=9); ax.set_xlabel('1 - specificity (clinician label)'); ax.set_xlim(left=0); ax.set_ylim(0, 1)
        ax.grid(axis='y', color='#e9e9e6', lw=0.6)
    axs[0].set_ylabel('Sensitivity (clinician MD criterion)')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig4_grape_external.png'), bbox_inches='tight'); plt.close(fig)

def fig_design():
    fig, ax = plt.subplots(figsize=(7.2, 2.6)); ax.axis('off')
    boxes = [(0.02, 0.55, 'UWHVF (Seattle)\n24-2, 28,943 fields\npatient split 60/20/20'), (0.02, 0.08, 'Artes retest (Halifax)\n30 patients x 12 weekly\nfields: true no change'),
             (0.36, 0.55, '10 detectors\nclassical, permutation,\nconformal, event, ML'), (0.36, 0.08, 'GRAPE (Hangzhou)\n263 eyes, clinician\nprogression labels'),
             (0.70, 0.70, 'E1 sensitivity / specificity\nvs future reference'), (0.70, 0.40, 'E2 false alarms on\ntrue no-change series'),
             (0.70, 0.10, 'E3 shuffle audit (UWHVF)\nE4 external clinic (GRAPE)\nall: first 3-6 tests only')]
    for x, y, s in boxes:
        ax.add_patch(plt.Rectangle((x, y), 0.27, 0.3, fc='#f3f3f1', ec='#52514e', lw=0.8, transform=ax.transAxes))
        ax.text(x + 0.135, y + 0.15, s, ha='center', va='center', fontsize=7.5, transform=ax.transAxes)
    for (x0, y0, x1, y1) in [(0.29, 0.70, 0.36, 0.70), (0.29, 0.23, 0.36, 0.60), (0.63, 0.70, 0.70, 0.85), (0.63, 0.66, 0.70, 0.55),
                             (0.63, 0.62, 0.70, 0.25), (0.63, 0.23, 0.70, 0.22)]:
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0), xycoords='axes fraction', arrowprops=dict(arrowstyle='->', color='#52514e', lw=0.8))
    fig.savefig(os.path.join(FIG, 'fig1_study_design.png'), bbox_inches='tight'); plt.close(fig)

def main():
    os.makedirs(FIG, exist_ok=True)
    M = pd.DataFrame(json.load(open(os.path.join(ROOT, 'results', 'metrics.json'))))
    fig_design(); fig_validity_power(M); fig_audit(M)
    if 'grape_sens' in M: fig_grape(M)
    print('figures written to', FIG)

if __name__ == '__main__':
    main()
