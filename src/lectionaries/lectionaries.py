#!/usr/bin/env python3

"""Christian lectionaries through a Python interface."""

from abc import ABC, abstractmethod
from typing import Tuple

import liturgical_calendar.liturgical

import lectionaries.church_calendar
from lectionaries.lectionary_data import LECTIONARY_DATA as LECTIONARY_DATA
from lectionaries.lectionary_data import ALIASES as ALIASES

class Lectionary(ABC):

    @abstractmethod
    def cyclic_year(self, year: int) -> Tuple[int, int]:
        """Return the Sunday and daily lectionary years for a given year.
        The results are 0-based, so 0, 0 in the Common Worship notation means year A, 1."""
        return None, None

    @abstractmethod
    def all_years_readings(self, date):
        return None

class CommonWorshipLectionary(Lectionary):

    def __init__(self):
        self.calendar = lectionaries.church_calendar.WesternChurchCalendar()

    def cyclic_year(self, year: int) -> Tuple[int, int]:
        return (year - 2001) % 3, (year - 2000) % 2

    def all_years_readings(self, date):
        lit_cal_name = liturgical_calendar.liturgical.liturgical_calendar(date)['name']
        if lit_cal_name in LECTIONARY_DATA:
            return LECTIONARY_DATA[lit_cal_name]
        for suffix in (" the Apostle", " the Evangelist"):
            if lit_cal_name.endswith(suffix):
                lit_cal_name = "St " + lit_cal_name.removesuffix(suffix)
                if lit_cal_name in LECTIONARY_DATA:
                    return LECTIONARY_DATA[lit_cal_name]
        if lit_cal_name in ALIASES:
            alias = ALIASES[lit_cal_name]
            if alias in LECTIONARY_DATA:
                return LECTIONARY_DATA[alias]
        lect_day_name = self.calendar.lectionary_day_name(date)
        if lect_day_name in LECTIONARY_DATA:
            return LECTIONARY_DATA[lect_day_name]
        raise ValueError("Could not find readings for %s lit_cal_name=%s lect_day_name=%s", date.strftime("%Y-%m-%d (%a)"), lit_cal_name, lect_day_name)
        return None

    def readings(self, date):
        all_years = self.all_years_readings(date)
        if not all_years:
            return None
        sunday_year, daily_year = self.cyclic_year(date.year)
        return all_years[chr(ord('A') + sunday_year)]
