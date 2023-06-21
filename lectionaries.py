#!/usr/bin/env python3

"""Christian lectionaries through a Python interface."""

from abc import ABC, abstractmethod
from enum import Enum
import datetime
import dateutil.easter
from typing import Tuple

class Season(Enum):
    ORDINARY = 0          # from Pentecost to Advent
    ADVENT = 1            # begins 4th Sunday before Christmas
    CHRISTMAS = 2         # begins -12-25
    EPIPHANY = 3          # begins -01-06
    LENT = 4              # begins 40 weekdays before Easter
    EASTER = 5            # lasts 50 days from Easter, up to Pentecost

class Lectionary(ABC):

    @abstractmethod
    def cyclic_year(self, year: int) -> Tuple[int, int]:
        """Return the Sunday and daily lectionary years for a given year.
        The results are 0-based, so 0, 0 in the Common Worship notation means year A, 1."""
        return None, None

class CommonWorshipLectionary(Lectionary):

    def cyclic_year(self, year: int) -> Tuple[int, int]:
        return (year - 2001) % 3, (year - 2000) % 2

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
    def ash_wednesday(self, year):
        """Return the date of Ash Wednesday for a given year."""
        return None

    def sunday_before_christmas(self, year):
        christmas = self.christmas(year)
        return christmas - datetime.timedelta(days=christmas.isoweekday() or 7)

    def advent_sunday(self, year):
        """Return the date of Advent Sunday for a given year."""
        return self.sunday_before_christmas(year) - datetime.timedelta(days=28)

class WesternChurchCalendar(ChurchCalendar):

    def easter(self, year):
        return dateutil.easter.easter(year)

    def pentecost(self, year):
        return self.easter(year) + datetime.timedelta(days=49)

    def christmas(self, year):
        return datetime.date(year, 12, 25)

    def ash_wednesday(self, year):
        return self.easter(year) - datetime.timedelta(days=46)
