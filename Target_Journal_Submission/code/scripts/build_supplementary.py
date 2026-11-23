"""Build supplementary/ files from result tables (no hand-typed numbers) and TIFF copies of figures.
Usage (from code/): python scripts/build_supplementary.py"""
import os, json, shutil
import pandas as pd
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
S = os.path.join(ROOT, 'supplementary'); os.makedirs(S, exist_ok=True)
M = pd.read_csv(os.path.join(ROOT, 'tables', 'table_metrics_all.csv'))
M['valid_true_null'] = (M.fpr_true_null_hi <= 0.10) & (M.fpr_true_null_lo <= 0.05)
M.to_csv(os.path.join(S, 'Table_S1_all_metrics.csv'), index=False)
shutil.copy(os.path.join(ROOT, 'tables', 'table_paired_tests_vs_D1.csv'), os.path.join(S, 'Table_S2_paired_tests_vs_D1.csv'))
D = json.load(open(os.path.join(ROOT, 'results', 'descriptives.json')))
pd.DataFrame(D['tests_to_first_detection']).to_csv(os.path.join(S, 'Table_S3_tests_to_first_detection.csv'), index=False)
for n in ('table_S4_posthoc_later_reference.csv', 'table_S5_posthoc_later_reference_tests.csv'):
    shutil.copy(os.path.join(ROOT, 'tables', n), os.path.join(S, n.replace('table_', 'Table_')))
with pd.ExcelWriter(os.path.join(S, 'Supplementary_Tables_S1-S5.xlsx')) as w:
    M.to_excel(w, sheet_name='S1 all metrics', index=False)
    pd.read_csv(os.path.join(S, 'Table_S2_paired_tests_vs_D1.csv')).to_excel(w, sheet_name='S2 paired vs D1', index=False)
    pd.DataFrame(D['tests_to_first_detection']).to_excel(w, sheet_name='S3 tests to first flag', index=False)
    pd.read_csv(os.path.join(ROOT, 'tables', 'table_S4_posthoc_later_reference.csv')).to_excel(w, sheet_name='S4 post hoc later ref', index=False)
    pd.read_csv(os.path.join(ROOT, 'tables', 'table_S5_posthoc_later_reference_tests.csv')).to_excel(w, sheet_name='S5 post hoc tests', index=False)
F = os.path.join(ROOT, 'figures')
for f in sorted(os.listdir(F)):
    if f.endswith('.png'):
        Image.open(os.path.join(F, f)).convert('RGB').save(os.path.join(F, f[:-4] + '.tif'), compression='tiff_lzw', dpi=(300, 300))
print('supplementary and TIFF figures written')
