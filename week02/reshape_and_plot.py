"""Reshape HKO tide CSV (wide) into long form and create plots.

Outputs:
- week02/chek_lap_kok_e_2023_long.csv
- week02/plots/tide_timeseries.png
- week02/plots/tide_boxplot_by_month.png
- week02/plots/tide_histogram.png

Run with the workspace Python.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
CSV_IN = BASE / "chek_lap_kok_e_2023.csv"
CSV_OUT = BASE / "chek_lap_kok_e_2023_long.csv"
PLOTS_DIR = BASE / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# Read wide CSV
df = pd.read_csv(CSV_IN, dtype=str)
# Ensure columns exist
expected = ['month','day','t1','h1','t2','h2','t3','h3','t4','h4']
for c in expected:
    if c not in df.columns:
        df[c] = np.nan

# Melt into long form: for each t/h pair create a row
rows = []
for _, r in df.iterrows():
    month = int(r['month'])
    day = int(r['day'])
    for i in range(1,5):
        t_col = f't{i}'
        h_col = f'h{i}'
        t = r.get(t_col, '')
        h = r.get(h_col, '')
        if pd.isna(t) or str(t).strip() == '':
            continue
        if pd.isna(h) or str(h).strip() == '':
            continue
        t_str = str(t).zfill(4)  # times like 0531
        # parse hour/minute
        try:
            hour = int(t_str[:2])
            minute = int(t_str[2:])
        except Exception:
            # skip malformed times
            continue
        # construct datetime in 2023
        dt = pd.Timestamp(year=2023, month=month, day=day, hour=hour, minute=minute)
        try:
            h_val = float(str(h).strip())
        except Exception:
            continue
        rows.append({
            'datetime': dt,
            'tide_m': h_val,
            'pair': i,
            'month': month,
            'day': day,
        })

long = pd.DataFrame(rows)
long = long.sort_values('datetime').reset_index(drop=True)
long.to_csv(CSV_OUT, index=False)
print(f'Wrote {CSV_OUT} with {len(long)} rows')

# Plot 1: timeseries
plt.figure(figsize=(14,4))
plt.plot(long['datetime'], long['tide_m'], '.', markersize=3, alpha=0.6)
plt.title('Chek Lap Kok (E) 2023 Tide Levels')
plt.xlabel('Date')
plt.ylabel('Tide height (m)')
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'tide_timeseries.png', dpi=150)
plt.close()

# Plot 2: boxplot by month
plt.figure(figsize=(10,5))
sns.boxplot(x='month', y='tide_m', data=long)
plt.title('Monthly distribution of tide heights (2023)')
plt.xlabel('Month')
plt.ylabel('Tide height (m)')
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'tide_boxplot_by_month.png', dpi=150)
plt.close()

# Plot 3: histogram
plt.figure(figsize=(8,4))
sns.histplot(long['tide_m'], bins=30, kde=True)
plt.title('Distribution of tide heights (2023)')
plt.xlabel('Tide height (m)')
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'tide_histogram.png', dpi=150)
plt.close()

print('Saved 3 plots to', PLOTS_DIR)
