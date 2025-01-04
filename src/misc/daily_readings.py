#!/usr/bin/env python3

import datetime
import traceback

import liturgical_calendar.liturgical

import lectionaries.church_calendar
import lectionaries.lectionaries

def year_days_readings(year, fmt):
    print("")
    print("Getting readings")
    lect = lectionaries.lectionaries.CommonWorshipLectionary()
    missing = []
    for day in range(365):
        base = datetime.date(year, 1, 1)
        day_date = base + datetime.timedelta(days=day)
        try:
            title, readings = lect.readings(day_date, fmt=fmt)
            service = {"Readings": readings} | liturgical_calendar.liturgical.liturgical_calendar(day_date)
            print(day_date, day_date.strftime("%a"), service)
        except Exception as e:
            print("could not find reading for", day_date.isoformat(), e)
            traceback.print_exception(e)
            missing.append(day_date)
    print("Could not find readings for", len(missing), "days")
    ccal = lectionaries.church_calendar.WesternChurchCalendar()
    for day in missing:
        print(day, day.strftime("%a"), liturgical_calendar.liturgical.liturgical_calendar(day)['name'], ccal.lectionary_day_name(day))

year_days_readings(2025,
                   # lectionaries.lectionaries.ResultFormat.NAMES
                   # lectionaries.lectionaries.ResultFormat.PYBIBLE
                   # lectionaries.lectionaries.ResultFormat.VERSE_IDS
                   lectionaries.lectionaries.ResultFormat.TEXT_LIST
                   # lectionaries.lectionaries.ResultFormat.TEXT
                   # lectionaries.lectionaries.ResultFormat.HTML
                   )
