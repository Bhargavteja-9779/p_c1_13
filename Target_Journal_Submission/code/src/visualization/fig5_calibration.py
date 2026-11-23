"""Fig. 5: sensitivity at matched (5%) false-alarm rates after retest calibration (RC) vs shuffle calibration (SC).
Usage (from code/): python -m src.visualization.fig5_calibration  -> ../figures/fig5_no_change_calibration.png"""
import os, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#52514e',
                     'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e', 'savefig.dpi': 300})
# fixed categorical order (validated palette, light mode); markers give a second, colour-free encoding
STY = {'D1': ('D1 trend test', '#2a78d6', 'o'), 'D2': ('D2 rate of change', '#eb6834', 's'),
       'D6': ('D6 pooled conformal', '#1baf7a', '^'), 'D8': ('D8 tree model', '#eda100', 'D'), 'D9': ('D9 sequence model', '#e87ba4', 'v')}

def main():
    B = json.load(open(os.path.join(ROOT, 'results', 'amendB', 'amendB.json')))['B1_metrics']
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), sharey=True)
    for ax, cal, title in zip(axes, ('RC', 'SC'), ('A  Calibrated on weekly retests', 'B  Calibrated on shuffled clinic records')):
        ends = []
        for code, (lab, col, mk) in STY.items():
            r = sorted([x for x in B if x['calibration'] == cal and x['detector'].split()[0] == code], key=lambda x: x['k'])
            ks = [x['k'] for x in r]; se = [x['sens'] for x in r]
            ax.plot(ks, se, color=col, lw=2, marker=mk, ms=6, mec='white', mew=1.2, label=lab, zorder=3 if code == 'D1' else 2)
            ends.append([se[-1], code])
        ends.sort(); gap = 0.05                       # de-overlap end labels
        for i in range(1, len(ends)):
            ends[i][0] = max(ends[i][0], ends[i - 1][0] + gap)
        for y, code in ends:
            ax.annotate(code, (6, y), xytext=(8, 0), textcoords='offset points', va='center', fontsize=7.5, color='#0b0b0b')
        ax.set_title(title, fontsize=9, loc='left'); ax.set_xticks([3, 4, 5, 6]); ax.set_xlim(2.8, 6.5)
        ax.set_xlabel('Number of tests'); ax.set_ylim(0, 1); ax.grid(axis='y', color='#e9e9e6', lw=0.6)
    axes[0].set_ylabel('Sensitivity at the calibrated threshold\n(future-confirmed progressors)')
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc='upper center', ncol=5, frameon=False, fontsize=7.5, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(ROOT, 'figures', 'fig5_no_change_calibration.png'))

if __name__ == '__main__':
    main()
