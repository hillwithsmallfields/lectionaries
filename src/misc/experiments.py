#!/usr/bin/env python3

import liturgical_calendar.liturgical

import lectionaries.church_calendar
import lectionaries.lectionary_data
import lectionaries.lectionaries

import datetime

christmas = datetime.date(datetime.date.today().year, 12, 25)

def with_day(when):
    return when.strftime("%Y-%m-%d %a")

def days_to_christmas(countdown_from=40):
    print("days before Christmas")
    print("=====================")
    for countdown in range(countdown_from, -1, -1):
        full_date = christmas - datetime.timedelta(days=countdown)
        print(full_date, full_date.weekday(), full_date.strftime("%a"), "*" if full_date.weekday() == 6 else "", "<==" if countdown==28 else "")
    print("")

def years_between(cal, start=2000, end=2030):
    print("Festival dates by year, between", start, "and", end)
    print("===========================")
    print("| year | christmas      | sunbefore      | advent sun     | ash weds       | easter         | pentecost      |")
    for year in range(start, end):
        print("| "
              + " | ".join([str(year),
                            with_day(cal.christmas(year)),
                            with_day(cal.sunday_before_christmas(year)),
                            with_day(cal.advent_sunday(year)),
                            with_day(cal.ash_wednesday(year)),
                            with_day(cal.easter(year)),
                            with_day(cal.pentecost(year))])
              + " |")
    print("")

def describe_year_days(cal, year):
    print("Days of", year, "with flags")
    for day in range(365):
        base = datetime.date(year, 1, 1)
        day_date = base + datetime.timedelta(days=day)
        litcal = liturgical_calendar.liturgical.liturgical_calendar(day_date)
        print(with_day(day_date),
              "advent" if cal.is_advent(day_date) else "------",
              "christmas" if cal.is_christmas(day_date) else "---------",
              "epiphany" if cal.is_epiphany(day_date) else "--------",
              "lent" if cal.is_lent(day_date) else "----",
              "easter" if cal.is_easter(day_date) else "------",
              "ordinary" if cal.is_ordinary(day_date) else "--------",
              "% 30s % 4d" % cal.season_days(day_date),
              "%- 42s" % cal.liturgical_day_name(day_date),
              "/",
              "name is", litcal['name'],
              "and week is", litcal['week'],
              "and proper is", cal.proper(day_date))

cal = lectionaries.church_calendar.WesternChurchCalendar()

days_to_christmas(40)
years_between(cal, 2000, 2030)
describe_year_days(cal, 2025)
