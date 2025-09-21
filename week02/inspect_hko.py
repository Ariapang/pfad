"""Inspect HKO tide page for JS variable names and save a local copy for debugging."""
import re
from urllib.request import urlopen

URL = 'https://www.hko.gov.hk/tide/eCLKtext2023.html'
OUT = 'week02/hko_page.html'

print('Fetching', URL)
raw = urlopen(URL, timeout=20).read().decode('utf-8')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(raw)

print('Saved page to', OUT)

# look for data1-like variable assignments
for var in ['data1', 'data2', 'data', 'var data1', 'var data2']:
    if var in raw:
        print(f"Found literal '{var}' in page")

# search for patterns var <name> = [ ... ]
matches = re.findall(r"var\s+(\w+)\s*=\s*\[", raw)
if matches:
    print('JS array variables found (first 20):', matches[:20])
else:
    print('No JS array variable declarations found with simple regex')

# print a small snippet around 'data1' if present
idx = raw.find('data1')
if idx != -1:
    start = max(0, idx-200)
    end = idx+200
    print('\n...snippet around data1...\n')
    print(raw[start:end])
else:
    print('\ndata1 not found in page content')
