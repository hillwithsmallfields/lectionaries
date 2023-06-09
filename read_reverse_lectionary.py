#!/usr/bin/env python3

import collections
import os.path
import re
from bs4 import BeautifulSoup

def day_years(date):
    m = re.match("(.+ [0-9]+)([,ABC]+)", date)
    if m:
        return m.group(1), tuple(m.group(2).split(','))
    m = re.match("(.+) ([,ABC]+)", date)
    if m:
        return m.group(1), tuple(m.group(2).split(','))
    return date, ('A', 'B', 'C')

by_date = collections.defaultdict(list)

for row in BeautifulSoup(open(os.path.expanduser("~/Downloads/Reverse Lectionary.html"),
                              'rb').read(),
                         "lxml").body.contents[25].find_all('tr'):
    cells = [[' '.join(text.replace('\n', ' ').split()) for text in list(cell.stripped_strings)] for cell in list(row.find_all('td'))]
    readings = cells[0]
    dates = cells[1]
    for date in dates:
        for reading in readings:
            by_date[day_years(date)].append(reading)

for k in sorted(by_date.keys()):
    print(k, by_date[k])
