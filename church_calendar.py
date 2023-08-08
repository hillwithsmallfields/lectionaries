#!/usr/bin/env python3

"""Church calendars through a Python interface."""

from abc import ABC, abstractmethod
from enum import Enum
import datetime
import dateutil.easter
import inflect

class Season(Enum):
    ORDINARY = 0          # from Pentecost to Advent
    ADVENT = 1            # begins 4th Sunday before Christmas
    CHRISTMAS = 2         # begins -12-25
    EPIPHANY = 3          # begins -01-06
    LENT = 4              # begins 40 weekdays before Easter
    EASTER = 5            # lasts 50 days from Easter, up to Pentecost

SPECIAL_DAY_NAMES = {
    (Season.ADVENT, 0): "Advent Sunday",
    (Season.CHRISTMAS, 0): "Christmas Day",
    (Season.CHRISTMAS, 1): "St Stephen's Day",
    (Season.EPIPHANY, 0): "Epiphany",
    (Season.LENT, 0): "Ash Wednesday",
    (Season.LENT, 39): "Palm Sunday",
    (Season.LENT, 40): "Holy Monday",
    (Season.LENT, 41): "Holy Tuesday",
    (Season.LENT, 42): "Holy Wednesday",
    (Season.LENT, 43): "Maundy Thursday",
    (Season.LENT, 44): "Good Friday",
    (Season.LENT, 45): "Holy Saturday",
    (Season.EASTER, 0): "Easter Sunday",
    (Season.EASTER, 7): "First Sunday after Easter",
    (Season.EASTER, 14): "Second Sunday after Easter",
    (Season.EASTER, 21): "Third Sunday after Easter",
    (Season.EASTER, 28): "Fourth Sunday after Easter",
    (Season.EASTER, 28): "Fifth Sunday after Easter",
    (Season.EASTER, 35): "Sixth Sunday after Easter",
    (Season.EASTER, 42): "Seventh Sunday after Easter",
    (Season.EASTER, 7): "First Sunday after Easter",
    (Season.ORDINARY, 0): "Pentecost",
    (Season.ORDINARY, 7): "Trinity Sunday",
}

DAYS_TO_LENT_NAMES = {
    1: "Shrove Tuesday",
    3: "Quinquegesima Sunday",
    10: "Sexagesima Sunday",
    17: "Septuagesima Sunday"
}

class ChurchCalendar(ABC):

    def __init__(self):
        self._inflector = None

    def inflector(self):
        if self._inflector == None:
            self._inflector = inflect.engine()
        return self._inflector

    @staticmethod
    def season_name(season):
        return {
            Season.ORDINARY: "Ordinary time",
            Season.ADVENT: "Advent",
            Season.CHRISTMAS: "Christmas",
            Season.EPIPHANY: "Epiphany",
            Season.LENT: "Lent",
            Season.EASTER: "Easter",
        }.get(season, "Unknown")

    @abstractmethod
    def easter(self, year):
        """Return the date of Easter for a given year."""
        return None

    @abstractmethod
    def pentecost(self, year):
        """Return the date of Pentecost for a given year."""
        return None

    @abstractmethod
    def trinity_sunday(self, year):
        """Return the date of Trinity Sunday for a given year."""
        return None

    @abstractmethod
    def christmas(self, year):
        """Return the date of Christmas for a given year."""
        return None

    @abstractmethod
    def epiphany(self, year):
        """Return the date of Epiphany for a given year."""

    @abstractmethod
    def ash_wednesday(self, year):
        """Return the date of Ash Wednesday for a given year."""
        return None

    def shrove_tuesday(self, year):
        """Return the date of Shrove Tuesday for a given year."""
        return self.ash_wednesday(year) - datetime.timedelta(days=1)

    def passion_sunday(self, year):
        """Return the date of Passion Sunday for a given year."""
        return self.easter() - datetime.timedelta(days=14)

    def palm_sunday(self, year):
        """Return the date of Palm Sunday for a given year."""
        return self.easter() - datetime.timedelta(days=7)

    def sunday_before_christmas(self, year):
        christmas = self.christmas(year)
        return christmas - datetime.timedelta(days=christmas.isoweekday() or 7)

    def advent_sunday(self, year):
        """Return the date of Advent Sunday for a given year."""
        return self.sunday_before_christmas(year) - datetime.timedelta(days=28)

    def is_advent(self, date):
        """Return whether a date is in Advent."""
        return self.advent_sunday(date.year) <= date < self.christmas(date.year)

    def is_christmas(self, date):
        """Return whether a date is in the Christmas season."""
        return self.christmas(date.year) <= date or date < self.epiphany(date.year)

    def is_epiphany(self, date):
        """Return whether a date is in the Epiphany season.
        This counts the season as continuing to the start of Lent."""
        return self.epiphany(date.year) <= date < self.ash_wednesday(date.year)

    @abstractmethod
    def is_lent(self, date):
        """Return whether a date is in Lent."""
        return None

    def is_easter(self, date):
        """Return whether a date is in the Easter season."""
        return self.easter(date.year) <= date < self.pentecost(date.year)

    def is_ordinary(self, date):
        """Return whether a date is in ordinary time."""
        return not(self.is_advent(date)
                   or self.is_christmas(date)
                   or self.is_epiphany(date)
                   or self.is_lent(date)
                   or self.is_easter(date))

    def season_days(self, date):
        """Return the season for a given date, and the number of days into it.

        Note that the day number in the season is zero-based."""
        return ((Season.ADVENT, (date - self.advent_sunday(date.year)).days)
                if self.is_advent(date)
                else ((Season.CHRISTMAS,
                       (date - self.christmas(date.year - (1 if date.month == 1 else 0))).days)
                      if self.is_christmas(date)
                      else ((Season.EPIPHANY, (date - self.epiphany(date.year)).days)
                            if self.is_epiphany(date)
                            else ((Season.LENT, (date - self.ash_wednesday(date.year)).days)
                                  if self.is_lent(date)
                                  else ((Season.EASTER, (date - self.easter(date.year)).days)
                                        if self.is_easter(date)
                                        else (Season.ORDINARY, (date - self.pentecost(date.year)).days))))))

    def liturgical_week(self, date):
        """Return the liturgical name for a date."""
        season, days_into_season = self.season_days(date)
        if date == self.christmas(date.year) - datetime.timedelta(days=1):
            return "Christmas Eve"
        if season == Season.EPIPHANY:
            days_to_lent = (self.ash_wednesday(date.year) - date).days
            if days_to_lent in DAYS_TO_LENT_NAMES:
                return DAYS_TO_LENT_NAMES[days_to_lent]
        inflector = self.inflector()
        special = SPECIAL_DAY_NAMES.get((season, days_into_season))
        if special:
            return special
        week_in_season = (days_into_season // 7)+1
        preposition = (" of " if season in (Season.CHRISTMAS, Season.EASTER)
                       else " after the " if season == Season.EPIPHANY
                       else " in ")
        return (inflector.number_to_words(inflector.ordinal(week_in_season)).capitalize()
                + " " + date.strftime("%A")
                + preposition + self.season_name(season))

class WesternChurchCalendar(ChurchCalendar):

    def easter(self, year):
        return dateutil.easter.easter(year)

    def pentecost(self, year):
        return self.easter(year) + datetime.timedelta(days=49)

    def trinity_sunday(self, year):
        """Return the date of Trinity Sunday for a given year."""
        return self.pentecost(year) + datetime.timedelta(days=7)

    def christmas(self, year):
        return datetime.date(year, 12, 25)

    def epiphany(self, year):
        return datetime.date(year, 1, 6)

    def ash_wednesday(self, year):
        return self.easter(year) - datetime.timedelta(days=46)

    def is_lent(self, date):
        """Return whether a date is in Lent."""
        return self.ash_wednesday(date.year) <= date and date < self.easter(date.year)
