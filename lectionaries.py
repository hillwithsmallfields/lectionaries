#!/usr/bin/env python3

"""Christian lectionaries through a Python interface."""

from abc import ABC, abstractmethod
from typing import Tuple

class Lectionary(ABC):

    @abstractmethod
    def cyclic_year(self, year: int) -> Tuple[int, int]:
        """Return the Sunday and daily lectionary years for a given year.
        The results are 0-based, so 0, 0 in the Common Worship notation means year A, 1."""
        return None, None

class CommonWorshipLectionary(Lectionary):

    def cyclic_year(self, year: int) -> Tuple[int, int]:
        return (year - 2001) % 3, (year - 2000) % 2
