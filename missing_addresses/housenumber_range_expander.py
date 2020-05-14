import re
from missing_addresses import Housenumber, InvalidHousenumber
from typing import List

housenumber_range_regexp = re.compile('^ *([0-9]+) *-([0-9]+) *$')


class HousenumberRangeExpander:
    @staticmethod
    def expand(input_string: str) -> List[Housenumber]:
        normalized = input_string.replace(' ', '').lower()
        m: re.Match = housenumber_range_regexp.match(normalized)
        if not m:
            return []

        first_number = int(m.group(1))  # must be an integer, as the regexp matches
        second_number = int(m.group(2))  # must be an integer, as the regexp matches
        if first_number % 2 != second_number % 2:
            raise InvalidHousenumber(input_string, 'In housenumber range, one number odd, the other even')

        if first_number > second_number:
            raise InvalidHousenumber(input_string, 'In housenumber range, first number larger than second number')

        result = [Housenumber(str(n)) for n in range(first_number, second_number + 2, 2)]
        return result
