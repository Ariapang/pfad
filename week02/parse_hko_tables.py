#!/usr/bin/env python3
"""Parse tidal tables from HKO HTML and write CSV.

Output: week02/chek_lap_kok_e_2023.csv with columns:
  month,day,t1,h1,t2,h2,t3,h3,t4,h4

The script prefers a local copy at week02/hko_page.html (saved earlier). If not found,
it will fetch the page from the HKO site.
"""
import os
import csv
from urllib.request import urlopen
from lxml import html

URL = 'https://www.hko.gov.hk/tide/eCLKtext2023.html'
LOCAL_HTML = 'week02/hko_page.html'
OUT_CSV = 'week02/chek_lap_kok_e_2023.csv'


def get_html_text():
    if os.path.exists(LOCAL_HTML):
        with open(LOCAL_HTML, 'r', encoding='utf-8') as f:
            return f.read()
    # fetch live
    print('Local HTML not found; fetching from', URL)
    return urlopen(URL, timeout=20).read().decode('utf-8')


def normalize_text(s: str) -> str:
    if s is None:
        return ''
    t = s.strip()
    # replace non-breaking spaces and multiple spaces
    t = t.replace('\xa0', ' ').replace('\u00A0', ' ').strip()
    return ' '.join(t.split())


def parse_tables(html_text: str):
    tree = html.fromstring(html_text)
    rows_out = []

    # Find all tables on the page
    for table in tree.xpath('//table'):
        for tr in table.xpath('.//tr'):
            # skip header rows with TH
            ths = tr.xpath('.//th')
            if ths:
                continue

            tds = tr.xpath('.//td')
            if not tds:
                continue

            cells = [normalize_text(td.text_content()) for td in tds]

            # Expect rows like: [MM, DD, time1, height1, time2, height2, time3, height3, time4, height4]
            # Some rows may have fewer columns (missing trailing time/height). We'll pad to 10.
            if len(cells) < 2:
                continue

            # pad to 10 columns
            while len(cells) < 10:
                cells.append('')

            # take first 10 columns (ignore extras)
            row10 = cells[:10]
            # Ensure month/day are numeric if possible
            # leave as strings to preserve leading zeros
            rows_out.append(row10)

    return rows_out


def write_csv(rows):
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    header = ['month', 'day', 't1', 'h1', 't2', 'h2', 't3', 'h3', 't4', 'h4']
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def main():
    html_text = get_html_text()
    rows = parse_tables(html_text)
    if not rows:
        print('No table rows parsed')
        return
    write_csv(rows)
    print(f'Wrote {OUT_CSV} with {len(rows)} rows')


if __name__ == '__main__':
    main()
