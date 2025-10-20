#!/usr/bin/env python3

import argparse
import datetime
import traceback

import liturgical_calendar.liturgical

import lectionaries.church_calendar
import lectionaries.lectionaries

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fmt",
                        default="names",
                        choices=[rf.value
                                 for rf in lectionaries.lectionaries.ResultFormat])
    parser.add_argument("--year", "-y",
                        type=int, default=0)
    parser.add_argument("--quiet", "-q",
                        action='store_true')
    parser.add_argument("--list-missing",
                        action='store_true')
    return vars(parser.parse_args())

def service_details(lect, day_date, fmt):
    title, readings = lect.readings(day_date, fmt=fmt)
    return (({'Date': day_date.isoformat(),
              'Weekday': day_date.strftime("%A"),
              'Title': title,
              'Readings': readings}
             | liturgical_calendar.liturgical.liturgical_calendar(day_date))
            if title
            else None)

def year_days_readings(year: int,
                       fmt: lectionaries.lectionaries.ResultFormat,
                       quiet:bool=False,
                       list_missing=False):
    """Print the readings for a year."""
    if year == 0:
        year = datetime.date.today().year
    lect = lectionaries.lectionaries.CommonWorshipLectionary()
    missing = []
    for day in range(365):
        base = datetime.date(year, 1, 1)
        day_date = base + datetime.timedelta(days=day)
        service = service_details(lect, day_date, fmt)
        if service and service.get('Readings'):
            print(day_date, day_date.strftime("%a"), service)
        else:
            missing.append(day_date)
            if not quiet:
                print(("Warning: could not find reading for"
                       if day_date.weekday() == 6 else
                       "could not find reading for"),
                      day_date.isoformat(), day_date.strftime("(%A)"))
    if list_missing:
        print("Could not find readings for", len(missing), "days")
        ccal = lectionaries.church_calendar.WesternChurchCalendar()
        for day in missing:
            print("no reading for",
                  day, day.strftime("%a"),
                  liturgical_calendar.liturgical.liturgical_calendar(day)['name'],
                  ccal.lectionary_day_name(day))

if __name__ == "__main__":
    year_days_readings(**get_args())
