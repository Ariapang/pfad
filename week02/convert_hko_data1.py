#!/usr/bin/env python3
"""Fetch HKO tide page and convert JavaScript `data1` variable to CSV.

Saves output to `week02/hko_data1.csv`.
"""
import re
import json
import csv
import sys
from urllib.request import urlopen

URL = 'https://www.hko.gov.hk/tide/eCLKtext2023.html'
OUT_CSV = 'week02/hko_data1.csv'


def js_array_to_python(js_text: str):
    """Try to convert a JS array literal to Python object.

    Strategy:
    - Remove JavaScript line comments
    - Replace single quotes with double quotes (simple but usually safe for this data)
    - Remove trailing commas before closing brackets
    - Try json.loads; if that fails, fall back to ast.literal_eval after replacements
    """
    # remove JS single-line comments
    js_text = re.sub(r"//.*?$", "", js_text, flags=re.M)
    # remove JS multi-line comments
    js_text = re.sub(r"/\*.*?\*/", "", js_text, flags=re.S)
    # remove trailing commas like [1,2,]
    js_text = re.sub(r",\s*(\]|})", r"\1", js_text)
    # normalize quotes: change single quotes to double quotes
    js_text = js_text.replace("'", '"')
    # replace JS undefined with null
    js_text = js_text.replace('undefined', 'null')

    try:
        return json.loads(js_text)
    except Exception:
        # fallback to Python literal eval
        import ast
        py_str = js_text.replace('null', 'None').replace('true', 'True').replace('false', 'False')
        return ast.literal_eval(py_str)


def main():
    print('Fetching', URL)
    try:
        raw = urlopen(URL, timeout=20).read().decode('utf-8')
    except Exception as e:
        print('Failed to fetch page:', e)
        sys.exit(1)

    # find var data1 = [ ... ];
    m = re.search(r"var\s+data1\s*=\s*(\[[\s\S]*?\]);", raw)
    if not m:
        print('Could not find data1 variable on page')
        sys.exit(1)

    js = m.group(1)
    data = js_array_to_python(js)

    # Ensure the output directory exists
    import os
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)

    # Write CSV
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in data:
            # Convert None to empty string and ensure simple types
            safe_row = [('' if v is None else v) for v in row]
            writer.writerow(safe_row)

    print(f'Wrote {OUT_CSV} with {len(data)} rows')


if __name__ == '__main__':
    main()
