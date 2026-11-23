import sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.data.uwhvf import load_series, patient_split
S = load_series(); sp = patient_split(S)
out = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'split_assignment.csv')
with open(out, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['patient_id', 'split'])
    for p in sorted(sp): w.writerow([p, sp[p]])
print('wrote', out, len(sp))
