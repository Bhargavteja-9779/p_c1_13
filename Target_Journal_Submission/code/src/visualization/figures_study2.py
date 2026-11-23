"""Study 2 figures from results/study2_metrics.json. Usage: python -m src.visualization.figures_study2"""
import os, json
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FIG = os.path.join(ROOT, 'figures')
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#52514e',
                     'xtick.color': '#52514e', 'ytick.color': '#52514e', 'savefig.dpi': 300})
STYLE = {'D1 OLS-MD': ('#0b0b0b', 'o', 'D1 trend (p<0.05)'), 'D7 Event': ('#1baf7a', '^', 'D7 event'),
         'S1 SC-Trend': ('#2a78d6', 'o', 'S1 SC trend'), 'S2 SC-Rate': ('#5fa0e8', 'v', 'S2 SC rate'),
         'S3 SC-PoPLR': ('#eb6834', 's', 'S3 SC PoPLR'), 'S4 SC-Event': ('#0f7d55', '^', 'S4 SC event'),
         'S5 SC-LightGBM': ('#6250d6', 'D', 'S5 SC LightGBM'), 'S6 Order-LightGBM': ('#a78bfa', 'P', 'S6 order LightGBM'),
         'S7 SC-GRU': ('#9e5bd6', 'X', 'S7 SC GRU'), 'B8 LightGBM-95spec': ('#c8102e', 'D', 'B8 LightGBM, 95% spec threshold')}
CSTYLE = {'D1-repeated': ('#0b0b0b', 'o'), 'D7-repeated': ('#1baf7a', '^'), 'Q1 Sequential trend': ('#2a78d6', 'o'),
          'Q2 Confirmed trend': ('#5fa0e8', 's'), 'Q3 Confirmed SC-Event': ('#0f7d55', '^'), 'Q4 Sequential Order-LightGBM': ('#a78bfa', 'P')}

def fig_matched(M):
    ks = sorted(M.k.unique()); fig, axs = plt.subplots(1, len(ks), figsize=(3.0 * len(ks), 3.4), sharey=True)
    for ax, k in zip(axs, ks):
        m = M[M.k == k]
        ax.axvspan(0, 0.05, color='#e9e9e6', zorder=0); ax.axvline(0.05, color='#52514e', lw=0.8, ls='--')
        for _, r in m.iterrows():
            c, mk, _ = STYLE[r.detector]
            ax.errorbar(r.fa, r.sens, xerr=[[r.fa - r.fa_lo], [r.fa_hi - r.fa]], yerr=[[r.sens - r.sens_lo], [r.sens_hi - r.sens]],
                        fmt=mk, color=c, ms=5.5, elinewidth=0.7, mec='white', mew=1)
        ax.set_title(f'{k} tests'); ax.set_xlabel('False-alarm rate, true no-change'); ax.set_xlim(left=0); ax.set_ylim(0, 1)
        ax.grid(axis='y', color='#e9e9e6', lw=0.6)
    axs[0].set_ylabel('Sensitivity (R1 progressors, cross-fitted)')
    hs = [plt.Line2D([], [], marker=v[1], ls='', color=v[0], label=v[2]) for v in STYLE.values()]
    fig.legend(handles=hs, loc='upper center', ncol=5, frameon=False, bbox_to_anchor=(0.5, 1.1), fontsize=7.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig5_matched_false_alarms.png'), bbox_inches='tight'); plt.close(fig)

def fig_cum(C):
    c6 = C[C.k == 6]; fig, ax = plt.subplots(figsize=(4.6, 3.6))
    ax.axvspan(0, 0.05, color='#e9e9e6', zorder=0); ax.axvline(0.05, color='#52514e', lw=0.8, ls='--')
    for _, r in c6.iterrows():
        c, mk = CSTYLE[r.detector]
        ax.errorbar(r.fa, r.sens, xerr=[[r.fa - r.fa_lo], [r.fa_hi - r.fa]], yerr=[[r.sens - r.sens_lo], [r.sens_hi - r.sens]],
                    fmt=mk, color=c, ms=6, elinewidth=0.7, mec='white', mew=1, label=r.detector)
    ax.set_xlabel('Flagged at least once by test 6, true no-change'); ax.set_ylabel('Progressors flagged by test 6')
    ax.set_xlim(left=0); ax.set_ylim(0, 1); ax.grid(color='#e9e9e6', lw=0.6); ax.legend(frameon=False, fontsize=7, loc='lower right')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig6_repeated_looks.png'), bbox_inches='tight'); plt.close(fig)

def main():
    J = json.load(open(os.path.join(ROOT, 'results', 'study2_metrics.json')))
    fig_matched(pd.DataFrame(J['metrics'])); fig_cum(pd.DataFrame(J['cumulative'])); print('study2 figures written')

if __name__ == '__main__':
    main()
