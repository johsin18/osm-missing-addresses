from dataclasses import dataclass
from missing_addresses import Address, MatchInformation, MissingAddressInformation, IgnoredAddressInformation, SurplusInformation, Coordinate, \
    OsmPrimitive
from typing import Dict, Tuple, List
from datetime import datetime


@dataclass
class AddressDiff:
    matches: Dict[Address, MatchInformation]
    missing: Dict[Address, MissingAddressInformation]
    surplus: List[Tuple[Address, SurplusInformation]] # can be multiple surplus for an address, e.g. a building outline and an office
    num_reference: int
    num_matches: int
    num_missing_not_ignored: int
    num_surplus_not_ignored: int
    coverage_in_percent: float


@dataclass
class AddressDiffMetaData:
    area_name: str
    generation_date: datetime
    actual_date: datetime
    reference_date: datetime


class AddressDiffComputation:
    def diff(self, reference: Dict[Address, Coordinate], actual: List[Tuple[Address, OsmPrimitive]],
             ignored: Dict[Address, IgnoredAddressInformation]) -> AddressDiff:
        """
        :param reference: reference set of addresses
        :param actual: addresses actually contained in OpenStreetMap
        :param ignored: addresses to be ignored
        :return: address diff
        """
        assert isinstance(reference, dict)
        assert isinstance(actual, list)
        assert isinstance(ignored, dict)

        matches = {}
        surplus = []
        for (a, p) in actual:
            if a in reference:
                matches[a] = MatchInformation(p, reference[a])
            else:
                ignore_information = ignored.get(a, None)
                surplus.append((a, SurplusInformation(p, ignore_information)))

        actual_set = set()
        for (a, c) in actual:
            actual_set.add(a)

        missing = {}
        for a, c in reference.items():
            if a not in actual_set:
                ignore_information = ignored.get(a, None)
                missing[a] = MissingAddressInformation(c, ignore_information)

        num_matches: int = len(matches)
        num_missing_not_ignored: int = len([a for a in missing.values() if a.ignore_information is None])
        s: SurplusInformation
        num_surplus_not_ignored: int = len([a for (a, s) in surplus if s.ignore_information is None])
        num_reference_without_ignored = len(matches) + num_missing_not_ignored

        return AddressDiff(matches,  missing, surplus,
                           len(reference), num_matches, num_missing_not_ignored, num_surplus_not_ignored,
                           num_matches / num_reference_without_ignored * 100)

    def pretty_diff(self, reference, actual, ignored) -> AddressDiff:
        print(f"reference       {len(reference):>6} addresses")
        print(f"actual          {len(actual):>6} addresses")
        diff = self.diff(reference, actual, ignored)
        print(f"missing         {len(diff.missing):>6} addresses")
        print(f"ign missing     {diff.num_missing_not_ignored:>6} addresses")
        print(f"surplus         {len(diff.surplus):>6} addresses")
        print(f"identical       {diff.num_matches:>6} addresses")
        print(f"coverage        {diff.coverage_in_percent: 3.1f}%")
        return diff
