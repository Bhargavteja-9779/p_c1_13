"""Fill manuscript_template.md / cover_letter_template.md with numbers taken ONLY from result files.
Inputs : ../results/metrics.json, statistics.json, descriptives.json, run_meta_full.json, references.json
Outputs: manuscript_filled.md, cover_letter_filled.md, figure_legends.json, values.json (every substituted value),
         ../tables/table2_main.csv, ../tables/table3_grape.csv
Citations in the template are written as [n] / [n, m] / [n–m] where n indexes references.json (1-based);
they are renumbered in order of first appearance and the reference list is appended.
Usage: python fill_values.py   (fails loudly on any unfilled placeholder)"""
import os, re, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
R = lambda f: json.load(open(os.path.join(ROOT, 'results', f)))
M = pd.DataFrame(R('metrics.json')); ST = R('statistics.json'); DS = R('descriptives.json'); META = R('run_meta_full.json')
T = pd.DataFrame(ST['paired_tests'])
REFS = json.load(open(os.path.join(HERE, 'references.json')))
M['id'] = M.detector.str.split().str[0]; T['id'] = T.detector.str.split().str[0]
IDS = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10']
KS = [3, 4, 5, 6]
SHORT = {'D1': 'OLS-MD', 'D2': 'MD rate', 'D3': 'PLR-3', 'D4': 'PoPLR', 'D5': 'Pooled-shuffle conformal',
         'D6': 'Pooled-detrended conformal', 'D7': 'Event analysis', 'D8': 'ML tabular (LightGBM)',
         'D9': 'ML sequence (GRU)', 'D10': 'Self-supervised order net'}
V = {}


def pc(x, d=0):
    return '–' if x is None or (isinstance(x, float) and np.isnan(x)) else f'{100 * x:.{d}f}'


def ci(lo, hi, d=0):
    return f'{pc(lo, d)}–{pc(hi, d)}'


def pval(p):
    if p < 0.001: return '< 0.001'
    return f'= {p:.3f}' if p < 0.10 else f'= {p:.2f}'


def fmt_n(x): return f'{int(x):,}'


# validity rule (Methods): CI upper limit <= 10% AND point estimate not above 5% beyond sampling error (CI lower <= 5%)
M['valid'] = (M.fpr_true_null_hi <= 0.10) & (M.fpr_true_null_lo <= 0.05)

for _, r in M.iterrows():
    s = f"{r.id}_{int(r.k)}"
    V[f's_{s}'] = pc(r.sens); V[f'sci_{s}'] = ci(r.sens_lo, r.sens_hi)
    V[f'sp_{s}'] = pc(r.spec); V[f'spci_{s}'] = ci(r.spec_lo, r.spec_hi)
    V[f'f_{s}'] = pc(r.fpr_true_null, 1); V[f'fci_{s}'] = ci(r.fpr_true_null_lo, r.fpr_true_null_hi, 1)
    V[f'a_{s}'] = pc(r.fpr_shuffle, 1); V[f'aci_{s}'] = ci(r.fpr_shuffle_lo, r.fpr_shuffle_hi, 1)
    V[f'r2_{s}'] = pc(r.sens_ref2)
    V[f'ff_{s}'] = f'{1000 * r.fpr_true_null:.0f}'
    if not pd.isna(r.grape_sens):
        V[f'gs_{s}'] = pc(r.grape_sens); V[f'gsci_{s}'] = ci(r.grape_sens_lo, r.grape_sens_hi)
        V[f'gp_{s}'] = pc(r.grape_spec); V[f'gpci_{s}'] = ci(r.grape_spec_lo, r.grape_spec_hi)
for _, r in T.iterrows():
    tag = {'sensitivity': 'dS', 'false positives (1-spec)': 'dF', 'GRAPE sensitivity': 'dGS', 'GRAPE false positives': 'dGF'}[r.endpoint]
    s = f"{r.id}_{int(r.k)}"
    V[f'{tag}_{s}'] = f'{100 * r['diff']:+.0f}'; V[f'{tag}ci_{s}'] = f"{100 * r.diff_lo:.0f} to {100 * r.diff_hi:.0f}"
    V[f'{tag}p_{s}'] = pval(r.p_holm)
    V[f'{tag}a_{s}'] = f"{abs(100 * r['diff']):.0f}"

# seeds, sizes
st = M[M.id.isin(['D4', 'D5', 'D6', 'D8', 'D9', 'D10'])]
V['max_seed_det'] = SHORT[st.loc[st.sens_seed_sd.idxmax(), 'id']] + ', ' + str(int(st.loc[st.sens_seed_sd.idxmax(), 'k'])) + ' fields'; V['max_seed_sd_sens'] = pc(st.sens_seed_sd.max(), 1); V['max_seed_sd_fpr'] = pc(st.fpr_true_null_seed_sd.max(), 1)
V['n_seeds'] = str(len(META['seeds'])); V['runtime_min'] = f"{META['runtime_s'] / 60:.0f}"
u, a, g = DS['uwhvf'], DS['artes'], DS['grape']
V.update(n_uw_fields=fmt_n(u['n_fields']), n_uw_eyes=fmt_n(u['n_eyes']), n_uw_patients=fmt_n(u['n_patients']),
         n_train_eyes=fmt_n(u['train_eyes_ge3']), n_train_pat=fmt_n(u['train_patients_ge3']),
         n_val_eyes=fmt_n(u['val_eyes_ge3']), n_val_pat=fmt_n(u['val_patients_ge3']),
         n_test_eyes=fmt_n(u['test_eyes_ge3']), n_test_pat=fmt_n(u['test_patients_ge3']),
         n_test8=str(u['test_eyes_ge8']), n_prog=str(u['test_ref_prog']), n_stab=str(u['test_ref_stable']),
         n_indet=str(u['test_ref_indeterminate']), n_ref_pat=str(u['test_ref_patients']),
         ref_age=f"{u['ref_age_baseline']['median']:.0f}", ref_age_iqr=f"{u['ref_age_baseline']['q1']:.0f}–{u['ref_age_baseline']['q3']:.0f}",
         ref_md=f"{u['ref_md_baseline']['median']:.1f}", ref_md_iqr=f"{u['ref_md_baseline']['q1']:.1f} to {u['ref_md_baseline']['q3']:.1f}",
         ref_ntests=f"{u['ref_n_tests']['median']:.0f}", ref_fu=f"{u['ref_followup_yr']['median']:.1f}",
         ref_fu_iqr=f"{u['ref_followup_yr']['q1']:.1f}–{u['ref_followup_yr']['q3']:.1f}",
         ref_int=f"{u['ref_interval_first6_yr']['median']:.1f}", ref_int_iqr=f"{u['ref_interval_first6_yr']['q1']:.1f}–{u['ref_interval_first6_yr']['q3']:.1f}",
         ref_t6=f"{u['ref_time_to_test6_yr']['median']:.1f}", ref_t3=f"{u['ref_time_to_test3_yr']['median']:.1f}",
         n_artes=str(a['n_patients']), n_artes_fields=str(a['n_fields']), artes_span=f"{a['span_days']['median']:.0f}",
         **{f'artes_win_{k}': str(a['windows'][str(k)]) for k in KS},
         artes_win_draws=fmt_n(10 * sum(a['windows'][str(k)] for k in KS)),
         n_grape_eyes=str(g['n_eyes']), n_grape_pat=str(g['n_patients']), n_grape_records=fmt_n(g['n_records']),
         grape_visits=f"{g['visits_per_eye']['median']:.0f}", grape_fu=f"{g['followup_yr']['median']:.1f}",
         grape_age=f"{g['age']['median']:.0f}", grape_age_iqr=f"{g['age']['q1']:.0f}–{g['age']['q3']:.0f}",
         grape_pts=str(g['n_points']), grape_md=str(g['label_MD']), grape_plr2=str(g['label_PLR2']),
         grape_plr3=str(g['label_PLR3']), grape_ge4=str(g['eyes_ge4']),
         grape_md_pct=pc(g['label_MD'] / g['n_eyes']))
rq3 = ST['rq3_audit_concordance']
V.update(rq3_rho=f"{rq3['spearman_rho']:.2f}", rq3_p=pval(rq3['spearman_p']), rq3_cells=str(rq3['n_cells']),
         rq3_med=pc(rq3['median_abs_diff'], 1), rq3_within3=pc(rq3['share_within_3pp']), rq3_max=pc(rq3['max_abs_diff'], 1))
# tests to first detection
TT = {r['detector'].split()[0]: r for r in DS['tests_to_first_detection']}
for i in IDS:
    V[f'by6_{i}'] = pc(TT[i]['flagged_by6']); V[f'tfd_{i}'] = f"{TT[i]['median_first']:g}"
# validity summary
for k in KS:
    mk = M[M.k == k]
    V[f'nvalid_{k}'] = str(int(mk.valid.sum()))
    V[f'invalid_list_{k}'] = ', '.join(i for i in IDS if not bool(mk[mk.id == i].valid.iloc[0])) or 'none'
    vv = mk[mk.valid & (mk.id != 'D1')].sort_values('sens', ascending=False).iloc[0]
    V[f'bestvalid_{k}'] = vv.id
    V[f'bestvalid_name_{k}'] = SHORT[vv.id]
ml = M[M.id.isin(['D8', 'D9'])]
V['ml_cells_above5'] = str(int((ml.fpr_true_null_lo > 0.05).sum())); V['ml_cells'] = str(len(ml))
V['n_cells_invalid'] = str(int((~M.valid).sum())); V['n_cells'] = str(len(M))
# H2 decision (pre-registered): any valid detector with sens gain >= 10 pp AND Holm p < 0.05
h2 = []
for _, r in T[T.endpoint == 'sensitivity'].iterrows():
    v = bool(M[(M.id == r.id) & (M.k == r.k)].valid.iloc[0])
    if v and r['diff'] >= 0.10 and r.p_holm < 0.05: h2.append(f'{r.id}@{r.k}')
V['h2_falsified'] = 'was falsified' if h2 else 'was not falsified'
V['n_valid_gain10'] = str(int(sum(1 for _, r in T[T.endpoint == 'sensitivity'].iterrows()
                                  if r['diff'] >= 0.10 and bool(M[(M.id == r.id) & (M.k == r.k)].valid.iloc[0]))))
V['h3_status'] = ('met' if rq3['share_within_3pp'] > 0.5 and rq3['spearman_rho'] >= 0.7 else 'partly met')
# ---- additions after simulated peer review
V['dSpall_D6_3'] = pval(float(T[(T.id == 'D6') & (T.k == 3) & (T.endpoint == 'sensitivity')].p_holm_all_k.iloc[0]))
M['strict'] = M.fpr_true_null_hi <= 0.05; M['excess'] = M.fpr_true_null_lo > 0.05
V['n_cells_strict'] = str(int(M.strict.sum())); V['n_cells_excess'] = str(int(M.excess.sum()))
V['excess_list'] = ', '.join(f"{r.id} ({int(r.k)} fields)" for _, r in M[M.excess].sort_values(['k']).iterrows())
V['D1_hi_range'] = f"{pc(M[M.id == 'D1'].fpr_true_null_hi.min(), 1)}–{pc(M[M.id == 'D1'].fpr_true_null_hi.max(), 1)}"
sv = T[(T.endpoint == 'sensitivity')].merge(M[['id', 'k', 'valid']], on=['id', 'k'])
V['max_gain_hi'] = f"{100 * sv[sv.valid].diff_hi.max():.0f}"
rq3 = ST['rq3_audit_concordance']
V.update(rq3_lo=f"{rq3['spearman_lo']:.2f}", rq3_hi=f"{rq3['spearman_hi']:.2f}", rq3_rho_nz=f"{rq3['spearman_rho_nonzero']:.2f}",
         rq3_nz=str(rq3['n_cells_nonzero']), aud_inv=str(rq3['audit_invalid_true']), aud_det=str(rq3['audit_invalid_detected']),
         aud_fw=str(rq3['audit_false_warnings']), aud_nv=str(rq3['audit_n_valid_true']),
         aud_missed=', '.join(x.replace('@', ' at ') + ' fields' for x in rq3['audit_missed']) or 'none')
PH = json.load(open(os.path.join(ROOT, 'results', 'posthoc.json')))
for r in PH['P2_cumulative_false_alarms']:
    i = r['detector'].split()[0]; V[f'cum_{i}'] = pc(r['any_flag_3to6']); V[f'cumci_{i}'] = ci(r['lo'], r['hi'])
for r in PH['P3_ppv']:
    i = f"{r['detector'].split()[0]}_{r['k']}"
    if r['ppv_grape'] is not None: V[f'ppvg_{i}'] = pc(r['ppv_grape'])
    if r['ppv_uw_truenull_10'] is not None: V[f'ppv10_{i}'] = pc(r['ppv_uw_truenull_10'])
V['grape_prev'] = pc(PH['grape_prevalence_MD'])
P1 = pd.DataFrame(PH['P1_later_reference']); P1['id'] = P1.detector.str.split().str[0]
for _, r in P1.iterrows():
    V[f'lr_s_{r.id}_{r.k}'] = pc(r.sens); V[f'lr_np_{r.k}'] = str(r.n_prog); V[f'lr_ns_{r.k}'] = str(r.n_stable)
P5 = pd.DataFrame(PH['P5_later_reference_tests']); P5['id'] = P5.detector.str.split().str[0]
r5 = P5[(P5.id == 'D6') & (P5.k == 3)].iloc[0]
V['lr_d6_only'] = str(int(r5.only_det)); V['lr_d6_p'] = pval(r5.p_holm)
_n = int((P5.p_holm < 0.05).sum()); V['lr_nsig'] = 'none of the comparisons with D1 was' if _n == 0 else f'{_n} comparisons with D1 were'
P4 = PH['P4_grape_D1_k3_by_visits']
V.update(g3_f=str(P4['exactly3']['flagged']), g3_n=str(P4['exactly3']['n']), g4_f=str(P4['ge4']['flagged']), g4_n=str(P4['ge4']['n']),
         g_n3=str(P4['n_eyes_exactly3']), g_pts_min=str(P4['points_per_eye']['min']), g_pts_below=str(P4['points_per_eye']['n_below_max']))
for k in (3, 4):
    r = M[(M.id == 'D1') & (M.k == k)].iloc[0]
    V[f'g_np_{k}'] = str(int(r.grape_sens_n)); V[f'g_ns_{k}'] = str(int(r.grape_spec_n))
ab = DS['artes']['span_days']
V['artes_span_q'] = f"{ab['q1']:.0f}–{ab['q3']:.0f}"; V['artes_span_max'] = f"{ab['max']:.0f}"
# ---- amendment A3 (post-review, pre-specified before running)
A3 = json.load(open(os.path.join(ROOT, 'results', 'a3_summary.json')))
X = pd.DataFrame(A3['A3a_sct']); X['id'] = X.detector.str.split().str[0]
for _, r in X.iterrows():
    s_ = f"{r.id}_{int(r.k)}"
    V[f'xs_{s_}'] = pc(r.sens); V[f'xsci_{s_}'] = ci(r.sens_lo, r.sens_hi); V[f'xsp_{s_}'] = pc(r.spec)
    V[f'xf_{s_}'] = pc(r.fpr_true_null, 1); V[f'xfci_{s_}'] = ci(r.fpr_true_null_lo, r.fpr_true_null_hi, 1)
    if not pd.isna(r.get('grape_spec', np.nan)):
        V[f'xgp_{s_}'] = pc(r.grape_spec); V[f'xgpci_{s_}'] = ci(r.grape_spec_lo, r.grape_spec_hi); V[f'xgs_{s_}'] = pc(r.grape_sens)
V['x_nvalid'] = str(int(X.valid.sum())); V['x_ncells'] = str(len(X)); V['x_nexcess'] = str(int(X.excess.sum()))
V['x_invalid_list'] = ', '.join(f"{r.id} with {int(r.k)} fields" for _, r in X[~X.valid].iterrows()) or 'none'
XT = pd.DataFrame(A3['A3a_tests']); XT['id'] = XT.detector.str.split().str[0]
for _, r in XT.iterrows():
    tag = {'sensitivity': 'xdS', 'GRAPE sensitivity': 'xdGS', 'GRAPE false positives': 'xdGF'}[r.endpoint]; s_ = f"{r.id}_{int(r.k)}"
    V[f'{tag}_{s_}'] = f"{100 * r['diff']:+.0f}"; V[f'{tag}a_{s_}'] = f"{abs(100 * r['diff']):.0f}"
    V[f'{tag}ci_{s_}'] = f"{100 * r.diff_lo:.0f} to {100 * r.diff_hi:.0f}"; V[f'{tag}p_{s_}'] = pval(r.p_holm)
    V[f'{tag}pn_{s_}'] = pval(r.p_holm).replace('= ', '')
xs = XT[XT.endpoint == 'sensitivity']
V['x_max_gain_hi'] = f"{100 * xs.diff_hi.max():.0f}"; V['x_n_sig_gain'] = str(int(((xs['diff'] > 0) & (xs.p_holm < 0.05)).sum()))
V['H5'] = 'supported' if A3['H5_supported'] else 'not supported'; V['H6'] = 'was falsified' if A3['H6_falsified'] else 'was not falsified'
V['H8'] = 'supported' if A3['H8_supported'] else 'not supported'
CF = pd.DataFrame(A3['A3b_confirmation']); CF['id'] = CF.detector.str.split().str[0]
for _, r in CF.iterrows():
    tag = 'cfs' if r.measure.startswith('sens') else 'cff'; d_ = 0 if tag == 'cfs' else 1
    V[f'{tag}_{r.id}_{int(r.k)}'] = pc(r.est, d_); V[f'{tag}ci_{r.id}_{int(r.k)}'] = ci(r.lo, r.hi, d_)
EN = pd.DataFrame(A3['A3c_enlarged']); EN['id'] = EN.detector.str.split().str[0]
for _, r in EN.iterrows():
    s_ = f"{r.id}_{int(r.k)}"; V[f'ens_{s_}'] = pc(r.sens); V[f'ensci_{s_}'] = ci(r.sens_lo, r.sens_hi); V[f'ensp_{s_}'] = pc(r.spec)
V['en_np'] = str(int(EN.n_prog.iloc[0])); V['en_ns'] = str(int(EN.n_stable.iloc[0]))
ET = pd.DataFrame(A3['A3c_tests']); ET['id'] = ET.detector.str.split().str[0]
for _, r in ET.iterrows():
    tag = 'endS' if r.endpoint == 'sensitivity' else 'endF'; s_ = f"{r.id}_{int(r.k)}"
    V[f'{tag}_{s_}'] = f"{abs(100 * r['diff']):.0f}"; V[f'{tag}ci_{s_}'] = f"{100 * r.diff_lo:.0f} to {100 * r.diff_hi:.0f}"; V[f'{tag}p_{s_}'] = pval(r.p_holm)
V['a3_runtime'] = f"{A3['meta']['runtime_s'] / 60:.0f}"
# ---- round-2 editor fixes: plain names, clinical-implication table, consistent validity counts
PLAIN = {'D1': 'trend test (OLS-MD)', 'D2': 'MD-rate rule', 'D3': 'PLR-3', 'D4': 'PoPLR', 'D5': 'pooled conformal test',
         'D6': 'detrended conformal test', 'D7': 'event analysis', 'D8': 'gradient-boosted trees', 'D9': 'recurrent network',
         'D10': 'order network'}
V['ml_invalid'] = str(int((~ml.valid).sum()) if 'valid' in ml else int((~M[M.id.isin(['D8', 'D9'])].valid).sum()))
V['n_cells_invalid'] = str(int((~M.valid).sum()))
def ppv(se, fpr, pi=0.10): return se * pi / (se * pi + fpr * (1 - pi)) if se * pi + fpr * (1 - pi) > 0 else float('nan')
rows = [['Detector (threshold)', 'Sensitivity, 3 fields (%)', 'False flags per 1,000 stable eyes, 3 fields', 'True flags among all flags at 10% prevalence, 3 fields (%)',
         'Progressors flagged at any of fields 3–6 (%)', 'No-change series falsely flagged at any of fields 3–6 (%)']]
csv = []
CUM = {r['detector'].split()[0]: r['any_flag_3to6'] for r in PH['P2_cumulative_false_alarms']}
for i in IDS:
    r = M[(M.id == i) & (M.k == 3)].iloc[0]; p_ = ppv(r.sens, r.fpr_true_null)
    rows.append([f'{i} {PLAIN[i]}, nominal', pc(r.sens), f'{1000 * r.fpr_true_null:.0f}', pc(p_) if r.sens > 0 else '–',
                 pc(TT[i]['flagged_by6']), pc(CUM[i])])
    csv.append(dict(detector=i, threshold='nominal', sens3=r.sens, fpr3=r.fpr_true_null, ppv10_3=p_, flagged_by6=TT[i]['flagged_by6'], cum_false=CUM[i]))
for _, r in X[X.k == 3].iterrows():
    p_ = ppv(r.sens, r.fpr_true_null)
    rows.append([f'{r.id} {PLAIN[r.id]}, shuffle-calibrated', pc(r.sens), f'{1000 * r.fpr_true_null:.0f}', pc(p_), '–', '–'])
    csv.append(dict(detector=r.id, threshold='shuffle-calibrated', sens3=r.sens, fpr3=r.fpr_true_null, ppv10_3=p_))
    V[f'xppv_{r.id}_3'] = pc(p_)
pd.DataFrame(csv).to_csv(os.path.join(ROOT, 'tables', 'table3_clinical_implications.csv'), index=False)
CLIN_ROWS = rows
V['REFERENCES'] = '{{REFERENCES}}'  # replaced after renumbering

# ---------------- tables ----------------
def table1():
    rows = [['', 'UWHVF (Seattle, USA)', 'Artes retest (Halifax, Canada)', 'GRAPE (Hangzhou, China)'],
            ['Role', 'Development; future-reference test set', 'True no-change (false alarms)', 'External clinic'],
            ['Perimeter / pattern', 'Humphrey 24-2', 'Humphrey 24-2', f"Octopus 900 G1, {V['grape_pts']} analysable points"],
            ['Patients / eyes / fields', f"{V['n_uw_patients']} / {V['n_uw_eyes']} / {V['n_uw_fields']}",
             f"{V['n_artes']} / {V['n_artes']} / {V['n_artes_fields']}", f"{V['n_grape_pat']} / {V['n_grape_eyes']} / {V['n_grape_records']}"],
            ['Analysis sets', f"Train {V['n_train_eyes']} eyes; validation {V['n_val_eyes']}; test {V['n_test_eyes']} (≥3 fields)",
             f"Windows of 3/4/5/6 tests: {V['artes_win_3']}/{V['artes_win_4']}/{V['artes_win_5']}/{V['artes_win_6']}",
             f"{V['n_grape_eyes']} eyes (≥3 fields); {V['grape_ge4']} with ≥4"],
            ['Follow-up', f"Reference eyes: median {V['ref_ntests']} fields over {V['ref_fu']} years; interval {V['ref_int']} years",
             f"12 weekly fields over median {V['artes_span']} days", f"Median {V['grape_visits']} fields over {V['grape_fu']} years"],
            ['Age, years', f"Reference eyes: median {V['ref_age']} (IQR {V['ref_age_iqr']})", 'Not used', f"Median {V['grape_age']} (IQR {V['grape_age_iqr']})"],
            ['Progression label', f"Future reference (≥8 fields): {V['n_prog']} progressors, {V['n_stab']} stable, {V['n_indet']} indeterminate",
             'None (no change by design)', f"Rule-based MD label: {V['grape_md']} progressing ({V['grape_md_pct']}%); PLR2 {V['grape_plr2']}; PLR3 {V['grape_plr3']}"],
            ['Licence', 'BSD-3-Clause', 'Apache-2.0 (visualFields R package)', 'CC0']]
    return rows


def table2():
    rows = [['Detector'] + [f'{k} tests' for k in KS]]; csv = []
    for i in IDS:
        row = [f'{i} {SHORT[i]}']
        for k in KS:
            r = M[(M.id == i) & (M.k == k)].iloc[0]
            mark = '' if r.valid else ' †'
            row.append(f"{pc(r.sens)} / {pc(r.fpr_true_null, 1)}{mark}")
            csv.append(dict(detector=i, k=k, sens=r.sens, sens_lo=r.sens_lo, sens_hi=r.sens_hi, spec=r.spec,
                            fpr_true_null=r.fpr_true_null, fpr_lo=r.fpr_true_null_lo, fpr_hi=r.fpr_true_null_hi,
                            fpr_shuffle=r.fpr_shuffle, valid=bool(r.valid), sens_secondary_ref=r.sens_ref2))
        rows.append(row)
    pd.DataFrame(csv).to_csv(os.path.join(ROOT, 'tables', 'table2_main.csv'), index=False)
    return rows


def table3():
    rows = [['Detector', 'Sensitivity, 3 tests', 'Specificity, 3 tests', 'Sensitivity, 4 tests', 'Specificity, 4 tests']]; csv = []
    for i in ['D1', 'D2', 'D3', 'D4', 'D5', 'D7', 'D8']:
        row = [f'{i} {SHORT[i]}']
        for k in (3, 4):
            r = M[(M.id == i) & (M.k == k)].iloc[0]
            row += [f"{pc(r.grape_sens)} ({ci(r.grape_sens_lo, r.grape_sens_hi)})", f"{pc(r.grape_spec)} ({ci(r.grape_spec_lo, r.grape_spec_hi)})"]
            csv.append(dict(detector=i, k=k, sens=r.grape_sens, sens_lo=r.grape_sens_lo, sens_hi=r.grape_sens_hi,
                            spec=r.grape_spec, spec_lo=r.grape_spec_lo, spec_hi=r.grape_spec_hi, n_prog=r.grape_sens_n, n_stable=r.grape_spec_n))
        rows.append(row)
    pd.DataFrame(csv).to_csv(os.path.join(ROOT, 'tables', 'table3_grape.csv'), index=False)
    return rows


def md_table(rows):
    return '\n'.join(['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|' * len(rows[0])] + ['| ' + ' | '.join(r) + ' |' for r in rows[1:]])


V['TABLE_CLIN'] = md_table(CLIN_ROWS); V['TABLE1'] = md_table(table1()); V['TABLE2'] = md_table(table2()); V['TABLE3'] = md_table(table3())

# ---------------- substitution ----------------
def _minus(v):
    return re.sub(r'(?<![\w.])-(?=\d)', '−', v) if isinstance(v, str) else v


def substitute(text):
    missing = sorted(set(k for k in re.findall(r'\{\{(\w+)\}\}', text) if V.get(k) is None))
    if missing: raise SystemExit(f'UNFILLED placeholders: {missing}')
    return re.sub(r'\{\{(\w+)\}\}', lambda m: _minus(V[m.group(1)]) if not m.group(1).startswith('TABLE') else V[m.group(1)], text)


CIT = re.compile(r'\[(\d+(?:\s*[–,-]\s*\d+)*)\]')
def expand(s):
    out = []
    for part in re.split(r'\s*,\s*', s):
        if re.search(r'[–-]', part):
            a, b = [int(x) for x in re.split(r'\s*[–-]\s*', part)]; out += list(range(a, b + 1))
        else: out.append(int(part))
    return out


def compress(nums):
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(f'{nums[i]}–{nums[j]}' if j - i >= 2 else ', '.join(str(x) for x in nums[i:j + 1])); i = j + 1
    return ', '.join(out)


def renumber(text):
    order = []
    for m in CIT.finditer(text):
        for n in expand(m.group(1)):
            if n not in order: order.append(n)
    new = {old: i + 1 for i, old in enumerate(order)}
    text = CIT.sub(lambda m: '[' + compress([new[n] for n in expand(m.group(1))]) + ']', text)
    unused = [i + 1 for i in range(len(REFS)) if i + 1 not in new]
    reflist = '\n'.join(f'{new[o]}. {REFS[o - 1]["vancouver"].replace("&amp;", "&")}' for o in order)
    return text, reflist, order, unused


if __name__ == '__main__':
    tpl = open(os.path.join(HERE, 'manuscript_template.md')).read()
    tpl = tpl.replace('<<INTRO_METHODS>>', open(os.path.join(HERE, 'sections_intro_methods.md')).read().strip())
    body = substitute(tpl)
    head, sep, tail = body.partition('# Introduction')     # abstract/KSP must not cite references
    assert not CIT.search(head), 'citation found in title page/abstract/KSP'
    body2, reflist, order, unused = renumber(sep + tail)
    if unused: print('WARNING unused references (original indices):', unused)
    filled = head + body2.replace('{{REFERENCES}}', '\n\n'.join(reflist.split('\n')))
    open(os.path.join(HERE, 'manuscript_filled.md'), 'w').write(filled)
    open(os.path.join(HERE, 'cover_letter_filled.md'), 'w').write(substitute(open(os.path.join(HERE, 'cover_letter_template.md')).read()))
    legends = json.loads(substitute(open(os.path.join(HERE, 'figure_legends_template.json')).read()))
    json.dump(legends, open(os.path.join(HERE, 'figure_legends.json'), 'w'), indent=1)
    json.dump(dict(values={k: v for k, v in V.items() if not k.startswith('TABLE')}, citation_order=order),
              open(os.path.join(HERE, 'values.json'), 'w'), indent=1)
    abst = re.search(r'## Abstract\n(.*?)\n\*\*Keywords', filled, re.S).group(1)
    words = len(re.sub(r'\*\*[^*]+:\*\*', '', abst).split())
    main = re.search(r'# Introduction(.*?)# Declarations', filled, re.S).group(1)
    print(f'abstract words {words} (limit 300); main text words {len(main.split())}; refs {len(order)}')
