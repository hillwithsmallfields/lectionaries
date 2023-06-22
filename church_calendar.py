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
        # TODO: I don't think this is right yet
        return self.christmas(date.year) <= date and date <= self.epiphany(date.year+1)

    def is_lent(self, date):
        """Return whether a date is in Lent."""
        return self.ash_wednesday(date.year) <= date and date < self.easter(date.year)

    def is_easter(self, date):
        """Return whether a date is in the Easter season."""
        return self.easter(date.year) <= date < self.pentecost(date.year)

    def is_ordinary(self, date):
        """Return whether a date is in ordinary time."""
        return not(self.is_advent(date) or self.is_christmas(date) or self.is_lent(date))

    def season(self, date):
        return (Season.ADVENT if self.is_advent(date)
                else (Season.CHRISTMAS if self.is_christmas(date)
                      else (Season.LENT if self.is_lent(date)
                            else (Season.EASTER if self.is_easter(date)
                                  else Season.ORDINARY))))

class WesternChurchCalendar(ChurchCalendar):

    def easter(self, year):
        return dateutil.easter.easter(year)

    def pentecost(self, year):
        return self.easter(year) + datetime.timedelta(days=49)

    def christmas(self, year):
        return datetime.date(year, 12, 25)

    def epiphany(self, year):
        return datetime.date(year, 1, 6)

    def ash_wednesday(self, year):
        return self.easter(year) - datetime.timedelta(days=46)
