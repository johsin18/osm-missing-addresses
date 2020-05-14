import re
from dataclasses import dataclass
from typing import Tuple

housenumber_splitting_regexp = re.compile('^([0-9]+)(/([0-9]+))?([a-zA-Z]?)$')


class Housenumber:
    """A housenumber, together with a street name forming the unique key of an address.

    A housenumber consists of a strictly positive number, optionally a slash and another number,
    and then optionally a single letter (case-insensitive).
    For example:  "42", "13b", "32/2", "50/3c"
    Any whitespace is ignored.
    """
    __normalized: str  # housenumber, without whitespace, and lower-case
    __primary_number: int  # primary number
    __secondary_number: int = 0  # optional secondary number, after the slash, 0 means not existent
    __letter: str = ""  # letter at the end

    def __init__(self, input_string: str):
        """:param input_string: String the housenumber is parsed from"""
        self.__normalized = input_string.replace(' ', '').lower()
        m: re.Match = housenumber_splitting_regexp.match(self.__normalized)
        if not m:
            raise InvalidHousenumber(input_string, "invalid structure")
        self.__primary_number = int(m.group(1))  # must be an integer, as the regexp matches
        if self.__primary_number <= 0:
            raise InvalidHousenumber(input_string, "primary number must be strictly positive")
        if m.group(3) is not None:
            self.__secondary_number = int(m.group(3))  # must be an integer, as the regexp matches
            if self.__secondary_number <= 0:
                raise InvalidHousenumber(input_string, "secondary number must be strictly positive")
        if m.group(4) is not None:
            self.__letter = m.group(4)

    def __str__(self) -> str:
        return self.__normalized

    def equality_key(self) -> str:
        return self.__normalized

    def __eq__(self, other) -> bool:
        if isinstance(other, Housenumber):
            return self.equality_key() == other.equality_key()
        return NotImplemented

    def sort_key(self) -> Tuple[int, int, str]:
        """:return: key housenumbers can be sorted by, to achieve the natural order"""
        return self.__primary_number, self.__secondary_number, self.__letter


@dataclass
class InvalidHousenumber(BaseException):
    input_string: str
    message: str
