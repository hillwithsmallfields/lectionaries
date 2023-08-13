#!/usr/bin/env python3

import collections
import csv
import os.path
import re
from bs4 import BeautifulSoup

def day_years(date):
    m = re.match("(.+ [0-9]+)([,ABC]+)$", date)
    if m:
        return m.group(1), tuple(m.group(2).split(','))
    m = re.match("(.+) ([,ABC]+)$", date)
    if m:
        return m.group(1), tuple(m.group(2).split(','))
    return date, ('A', 'B', 'C')

def entries_by_date(downloaded_filename):

    """Parse a file saved from
    http://www.lectionarypage.net/ReverseLectionary.html.

    The result is a dictionary indexed by day, containing dictionaries
    indexed by lectionary year, containing lists of readings.
    """

    by_date = collections.defaultdict(lambda: collections.defaultdict(list))

    for row in BeautifulSoup(open(os.path.expanduser(downloaded_filename),
                                  'rb').read(),
                             "lxml").body.contents[25].find_all('tr'):
        cells = [[' '.join(text.replace('\n', ' ').split())
                  for text in list(cell.stripped_strings)]
                 for cell in list(row.find_all('td'))]
        readings = cells[0]
        dates = cells[1]
        for date in dates:
            day, years = day_years(date)
            for year in years:
                for reading in readings:
                    by_date[day][year].append(reading)

    return by_date

def print_lectionary(lectionary):
    """Print the lectionary, for debugging."""
    for dk in sorted(lectionary.keys()):
        ys = by_date[dk]
        for yk in sorted(ys.keys()):
            print(dk, yk, "; ".join(ys[yk]))

# print_lectionary(entries_by_date("~/Downloads/Reverse Lectionary.html"))

def write_lectionary(filename, lectionary):
    with open(filename, 'w') as outstream:
        writer = csv.DictWriter(outstream, ['Day', 'A', 'B', 'C'])
        writer.writeheader()
        for date in sorted(lectionary.keys()):
            readings = lectionary[date]
            row = {year: ";".join(readings.get(year, [])) for year in ['A', 'B', 'C']}
            row['Day'] = date
            writer.writerow(row)

write_lectionary("/tmp/lectionary.csv", entries_by_date("~/Downloads/Reverse Lectionary.html"))
