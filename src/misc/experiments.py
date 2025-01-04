#!/usr/bin/env python3

import liturgical_calendar.liturgical

import lectionaries.church_calendar
import lectionaries.lectionary_data
import lectionaries.lectionaries

import datetime

christmas = datetime.date(datetime.date.today().year, 12, 25)

def with_day(when):
    return when.strftime("%Y-%m-%d %a")

print("")
print("countdown to Christmas", christmas)
for countdown in range(40, -1, -1):
    full_date = christmas - datetime.timedelta(days=countdown)
    print(full_date, full_date.weekday(), full_date.strftime("%a"), "*" if full_date.weekday() == 6 else "", "<==" if countdown==28 else "")

cal = lectionaries.church_calendar.WesternChurchCalendar()

print("")
print("Festival dates by year")
print("year christmas      sunbefore      advent sun     ash weds       easter         pentecost     properP2")
for year in range(2000, 2030):
    print(year,
          with_day(cal.christmas(year)),
          with_day(cal.sunday_before_christmas(year)),
          with_day(cal.advent_sunday(year)),
          with_day(cal.ash_wednesday(year)),
          with_day(cal.easter(year)),
          with_day(cal.pentecost(year)),
          cal._proper_of_pentecost_2(year))

def describe_year_days(year):
    print("")
    print("days of year", year)
    for day in range(365):
        base = datetime.date(year, 1, 1)
        day_date = base + datetime.timedelta(days=day)
        litcal = liturgical_calendar.liturgical.liturgical_calendar(day_date)
        print(with_day(day_date),
              "adv" if cal.is_advent(day_date) else "---",
              "chr" if cal.is_christmas(day_date) else "---",
              "epi" if cal.is_epiphany(day_date) else "---",
              "len" if cal.is_lent(day_date) else "---",
              "eas" if cal.is_easter(day_date) else "---",
              "ord" if cal.is_ordinary(day_date) else "---",
              cal.season_days(day_date),
              cal.liturgical_day_name(day_date),
              "/",
              cal.lectionary_day_name(day_date),
              "name is", litcal['name'],
              "and week is", litcal['week'],
              "and proper is", cal.proper(day_date)
              )

describe_year_days(2025)

def litcal_day_names(year):
    print("")
    print("litcal day names of year", year)
    for day in range(365):
        base = datetime.date(year, 1, 1)
        day_date = base + datetime.timedelta(days=day)
        litcal = liturgical_calendar.liturgical.liturgical_calendar(day_date)
        print(litcal['name'])

litcal_day_names(2025)

print("")
print("lectionary entry names")
for name in sorted(lectionaries.lectionary_data.LECTIONARY_DATA.keys()):
    print(name)

def year_days_readings(year):
    print("")
    print("Getting readings")
    lect = lectionaries.lectionaries.CommonWorshipLectionary()
    for day in range(365):
        base = datetime.date(year, 1, 1)
        day_date = base + datetime.timedelta(days=day)
        readings = lect.all_years_readings(day_date)
        print(day_date, readings)

year_days_readings(2025)
