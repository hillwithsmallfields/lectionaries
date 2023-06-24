#!/usr/bin/env python3

"""Church calendars through a Python interface."""

from abc import ABC, abstractmethod
from enum import Enum
import datetime
import dateutil.easter

class Season(Enum):
    ORDINARY = 0          # from Pentecost to Advent
    ADVENT = 1            # begins 4th Sunday before Christmas
    CHRISTMAS = 2         # begins -12-25
    EPIPHANY = 3          # begins -01-06
    LENT = 4              # begins 40 weekdays before Easter
    EASTER = 5            # lasts 50 days from Easter, up to Pentecost

class ChurchCalendar(ABC):

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
        return self.advent_sunday(date.year) <= date and date < self.christmas(date.year)

    def is_christmas(self, date):
        """Return whether a date is in the Christmas season."""
        return self.christmas(date.year) <= date or date <= self.epiphany(date.year)

    @abstractmethod
    def is_lent(self, date):
        """Return whether a date is in Lent."""
        return None

    def is_easter(self, date):
        """Return whether a date is in the Easter season."""
        return self.easter(date.year) <= date < self.pentecost(date.year)

    def is_ordinary(self, date):
        """Return whether a date is in ordinary time."""
        return not(self.is_advent(date) or self.is_christmas(date) or self.is_lent(date))

    def season_days(self, date):
        """Return the season for a given date, and the number of days into it."""
        return ((Season.ADVENT, (date - self.advent_sunday(date.year)).days)
                if self.is_advent(date)
                else ((Season.CHRISTMAS,
                       (date - self.christmas(date.year - (1 if date.month == 1 else 0))).days)
                      if self.is_christmas(date)
                      else ((Season.LENT, (date - self.ash_wednesday(date.year)).days)
                            if self.is_lent(date)
                            else ((Season.EASTER, (date - self.easter(date.year)).days)
                                  if self.is_easter(date)
                                  else (Season.ORDINARY,
                                        # TODO: not sure what to do here
                                        )))))

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
