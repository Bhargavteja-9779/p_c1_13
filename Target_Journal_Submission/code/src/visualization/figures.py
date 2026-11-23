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
    ks = sorted(M.k.unique()); fig, axs = plt.subplots(1, len(ks), figsize=(3.0 * len(ks), 3.2), sharey=True, sharex=True)
    xmax = float(M.fpr_true_null_hi.max()) * 1.05
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
        ax.set_xlim(0, xmax); ax.set_ylim(0, 1); ax.grid(axis='y', color='#e9e9e6', lw=0.6)
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
        ax.set_title(f'GRAPE, {k} tests', fontsize=9); ax.set_xlabel('1 - specificity (data-set MD label)'); ax.set_xlim(left=0); ax.set_ylim(0, 1)
        ax.grid(axis='y', color='#e9e9e6', lw=0.6)
    axs[0].set_ylabel('Sensitivity (data-set MD label)')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig4_grape_external.png'), bbox_inches='tight'); plt.close(fig)

def fig_design():
    fig, ax = plt.subplots(figsize=(7.2, 2.6)); ax.axis('off')
    boxes = [(0.02, 0.55, 'UWHVF (Seattle)\n24-2, 28,943 fields\npatient split 60/20/20'), (0.02, 0.08, 'Artes retest (Halifax)\n30 patients x 12 weekly\nfields: true no change'),
             (0.36, 0.55, '10 detectors\nclassical, permutation,\nconformal, event, ML'), (0.36, 0.08, 'GRAPE (Hangzhou)\nOctopus G1, 263 eyes,\nrule-based labels'),
             (0.70, 0.70, 'E1 sensitivity / specificity\nvs future reference'), (0.70, 0.40, 'E2 false alarms on\ntrue no-change series'),
             (0.70, 0.10, 'E3 shuffle audit & calibration\nE4 external (first 3-6 tests)')]
    for x, y, s in boxes:
        ax.add_patch(plt.Rectangle((x, y), 0.27, 0.3, fc='#f3f3f1', ec='#52514e', lw=0.8, transform=ax.transAxes))
        ax.text(x + 0.135, y + 0.15, s, ha='center', va='center', fontsize=7.5, transform=ax.transAxes)
    for (x0, y0, x1, y1) in [(0.29, 0.70, 0.36, 0.70), (0.29, 0.23, 0.36, 0.60), (0.63, 0.70, 0.70, 0.85), (0.63, 0.66, 0.70, 0.55),
                             (0.63, 0.62, 0.70, 0.25), (0.63, 0.23, 0.70, 0.22)]:
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0), xycoords='axes fraction', arrowprops=dict(arrowstyle='->', color='#52514e', lw=0.8))
    fig.savefig(os.path.join(FIG, 'fig1_study_design.png'), bbox_inches='tight'); plt.close(fig)

def fig_sct(M):
    """Fig. 5: nominal threshold -> shuffle-calibrated threshold (amendment A3a), true no-change FPR vs sensitivity,
    and GRAPE specificity with own-clinic calibration."""
    p = os.path.join(ROOT, 'results', 'a3_summary.json')
    if not os.path.exists(p): return
    S = pd.DataFrame(json.load(open(p))['A3a_sct']); ks = [3, 4, 5, 6]
    fig = plt.figure(figsize=(12.0, 3.4)); gs = fig.add_gridspec(1, 5, width_ratios=[1, 1, 1, 1, 1.25], wspace=0.45)
    for i, k in enumerate(ks):
        ax = fig.add_subplot(gs[0, i]); ax.axvspan(0, 0.05, color='#e9e9e6', zorder=0); ax.axvline(0.05, color='#52514e', lw=0.8, ls='--')
        d1 = M[(M.k == k) & (M.detector.str.startswith('D1 '))].iloc[0]
        ax.plot(d1.fpr_true_null, d1.sens, 'o', color='#2a78d6', ms=6, mec='white', mew=1.2, zorder=4)
        ax.annotate('D1', (d1.fpr_true_null, d1.sens), xytext=(4, -9), textcoords='offset points', fontsize=7)
        for _, r in S[S.k == k].iterrows():
            nm = r.detector.split()[0]; fam, col, mk = FAM[nm]
            o = M[(M.k == k) & (M.detector == r.detector)].iloc[0]
            ax.annotate('', xy=(r.fpr_true_null, r.sens), xytext=(o.fpr_true_null, o.sens),
                        arrowprops=dict(arrowstyle='->', color=col, lw=1.0, alpha=0.8))
            ax.plot(o.fpr_true_null, o.sens, mk, color=col, ms=5, mfc='white', mew=1.0, zorder=3)
            ax.plot(r.fpr_true_null, r.sens, mk, color=col, ms=6, mec='white', mew=1.0, zorder=4)
            ax.annotate(nm, (o.fpr_true_null, o.sens), xytext=(4, 3), textcoords='offset points', fontsize=7, color='#52514e')
        ax.set_title(f'{k} fields', fontsize=9); ax.set_ylim(0, 1); ax.set_xlim(0, 0.30); ax.grid(axis='y', color='#e9e9e6', lw=0.6)
        ax.set_xlabel('False-alarm rate, true no-change', fontsize=8)
        if i == 0: ax.set_ylabel('Sensitivity, future-confirmed progressors')
    ax = fig.add_subplot(gs[0, 4]); g3 = S[(S.k == 3) & S.grape_spec.notna()]
    d1g = M[(M.k == 3) & M.detector.str.startswith('D1 ')].iloc[0]
    items = [('D1', d1g.grape_sens, d1g.grape_spec, '#2a78d6', None)]
    for _, r in g3.iterrows():
        nm = r.detector.split()[0]; o = M[(M.k == 3) & (M.detector == r.detector)].iloc[0]; col = FAM[nm][1]
        items += [(f'{nm}\nnom.', o.grape_sens, o.grape_spec, col, '//'), (f'{nm}\ncal.', r.grape_sens, r.grape_spec, col, None)]
    for j2, (lab, se, sp, col, h) in enumerate(items):
        for off, v, a_ in ((-0.2, sp, 1.0), (0.2, se, 0.45)):
            ax.bar(j2 + off, v, width=0.38, color='white' if h else col, edgecolor=col, hatch=h, lw=1.0, alpha=a_ if not h else 1.0)
            ax.text(j2 + off, v + 0.015, f'{100 * v:.0f}', ha='center', fontsize=6)
    ax.set_xticks(range(len(items))); ax.set_xticklabels([b[0] for b in items], fontsize=7); ax.set_ylim(0, 1.1)
    ax.set_ylabel('GRAPE, 3 fields', labelpad=2); ax.set_title('External: specificity (left) / sensitivity (right)', fontsize=8)
    hs = [plt.Line2D([], [], marker='o', ls='', mfc='white', mec='#52514e', label='nominal threshold'),
          plt.Line2D([], [], marker='o', ls='', color='#52514e', label='shuffle-calibrated threshold')]
    fig.legend(handles=hs, loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.42, 1.06), fontsize=8)
    fig.savefig(os.path.join(FIG, 'fig5_shuffle_calibration.png'), bbox_inches='tight'); plt.close(fig)

def main():
    os.makedirs(FIG, exist_ok=True)
    M = pd.DataFrame(json.load(open(os.path.join(ROOT, 'results', 'metrics.json'))))
    fig_design(); fig_validity_power(M); fig_audit(M); fig_sct(M)
    if 'grape_sens' in M: fig_grape(M)
    print('figures written to', FIG)

if __name__ == '__main__':
    main()
