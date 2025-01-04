#!/usr/bin/env python3

"""Christian lectionaries through a Python interface."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

import liturgical_calendar.liturgical
import pythonbible as bible
from pythonbible.versions import Version

import lectionaries.church_calendar
from lectionaries.lectionary_data import LECTIONARY_DATA as LECTIONARY_DATA
from lectionaries.lectionary_data import ALIASES as ALIASES

class ResultFormat(Enum):
    NAMES = 0
    PYBIBLE = 1
    VERSE_IDS = 2
    TEXT_LIST = 3
    TEXT = 4
    HTML = 5

class Lectionary(ABC):

    @abstractmethod
    def cyclic_year(self, year: int) -> Tuple[int, int]:
        """Return the Sunday and daily lectionary years for a given year.
        The results are 0-based, so 0, 0 in the Common Worship notation means year A, 1."""
        return None, None

    @abstractmethod
    def all_years_readings(self, date):
        return None

def format_reference(name, fmt=ResultFormat.NAMES, version=Version.KING_JAMES):
    if fmt == ResultFormat.NAMES:
        return name
    reference = bible.get_references(name)[0]
    if fmt == ResultFormat.PYBIBLE:
        return reference
    reference = bible.convert_references_to_verse_ids([reference])
    if fmt == ResultFormat.TEXT_LIST:
        return [name] + [bible.get_verse_text(vid, version) for vid in reference]
    if fmt == ResultFormat.TEXT:
        return name + ":\n" + "\n".join(bible.get_verse_text(vid, version) for vid in reference)
    if fmt == ResultFormat.HTML:
        return bible.format_scripture_text(reference)
    return reference

class CommonWorshipLectionary(Lectionary):

    def __init__(self):
        self.calendar = lectionaries.church_calendar.WesternChurchCalendar()

    def cyclic_year(self, year: int) -> Tuple[int, int]:
        return (year - 2001) % 3, (year - 2000) % 2

    def all_years_readings(self, date, fmt='name'):
        """Return the title for the day, and the readings for it for all years of the cycle."""
        lit_cal_data = liturgical_calendar.liturgical.liturgical_calendar(date)
        lit_cal_name = lit_cal_data['name']
        if lit_cal_name in LECTIONARY_DATA:
            return lit_cal_name, LECTIONARY_DATA[lit_cal_name]
        for suffix in (" the Apostle", " the Evangelist"):
            if lit_cal_name.endswith(suffix):
                lit_cal_alias = "St " + lit_cal_name.removesuffix(suffix)
                if lit_cal_alias in LECTIONARY_DATA:
                    return lit_cal_name, LECTIONARY_DATA[lit_cal_alias]
        if lit_cal_name in ALIASES:
            alias = ALIASES[lit_cal_name]
            if alias in LECTIONARY_DATA:
                return lit_cal_name, LECTIONARY_DATA[alias]
        lect_day_name = self.calendar.lectionary_day_name(date)
        if lect_day_name in LECTIONARY_DATA:
            return lect_day_name, LECTIONARY_DATA[lect_day_name]
        raise ValueError("Could not find readings for %s lit_cal_name=%s lect_day_name=%s", date.strftime("%Y-%m-%d (%a)"), lit_cal_name, lect_day_name)
        return lit_cal_name + "/" + lect_day_name, None

    def readings(self, date, fmt=ResultFormat.NAMES, version=Version.KING_JAMES):
        """Return the title for the day, and the readings for it for the current year of the cycle."""
        title, all_years = self.all_years_readings(date)
        if not all_years:
            return None, None
        sunday_year, daily_year = self.cyclic_year(date.year)
        readings = all_years[chr(ord('A') + sunday_year)]
        return title, {
            group: [format_reference(name, fmt, version) for name in names]
            for group, names in readings.items()
        }
