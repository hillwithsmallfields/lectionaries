#!/usr/bin/env python3

import church_calendar
import lectionaries

import datetime

christmas = datetime.date(datetime.date.today().year, 12, 25)

def with_day(when):
    return when.strftime("%Y-%m-%d %a")

for countdown in range(40, -1, -1):
    full_date = christmas - datetime.timedelta(days=countdown)
    print(full_date, full_date.weekday(), full_date.strftime("%a"), "*" if full_date.weekday() == 6 else "", "<==" if countdown==28 else "")

cal = church_calendar.WesternChurchCalendar()

print("year christmas      sunbefore      advent sun     ash weds       easter       pentecost")
for year in range(2000, 2030):
    print(year,
          with_day(cal.christmas(year)),
          with_day(cal.sunday_before_christmas(year)),
          with_day(cal.advent_sunday(year)),
          with_day(cal.ash_wednesday(year)),
          with_day(cal.easter(year)),
          with_day(cal.pentecost(year)))

for day in range(365):
    base = datetime.date(2023, 1, 1)
    day_date = base + datetime.timedelta(days=day)
    print(day_date,
          "advent" if cal.is_advent(day_date) else "",
          "christmas" if cal.is_christmas(day_date) else "",
          "lent" if cal.is_lent(day_date) else "",
          "ordinary" if cal.is_ordinary(day_date) else "",
          cal.season(day_date))
