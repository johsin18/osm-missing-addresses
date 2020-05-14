from dataclasses import dataclass
from missing_addresses import MatchInformation, Address, Coordinate, AddressDiff, MissingAddressInformation, SurplusInformation
from typing import Dict, List, Tuple


@dataclass()
class StreetDiff:
    matches: Dict[Address, MatchInformation]
    missing: Dict[Address, MissingAddressInformation]
    surplus: List[Tuple[Address, SurplusInformation]]
    num_missing_not_ignored: int
    num_surplus_not_ignored: int


class DiffOrderedByStreet:
    def create_view(self, diff: AddressDiff) -> Dict[str, StreetDiff]:
        """

        :param diff: diff to create view on
        :return: mapping from street to results per street
        """
        streets = {}

        a: Address
        for a, i in diff.matches.items():
            street_diff: StreetDiff = DiffOrderedByStreet.get_or_create_street_diff(a.street, streets)
            street_diff.matches[a] = i

        for a, m in diff.missing.items():
            street_diff: StreetDiff = DiffOrderedByStreet.get_or_create_street_diff(a.street, streets)
            street_diff.missing[a] = m

        c: Coordinate
        for (a, c) in diff.surplus:
            street_diff: StreetDiff = DiffOrderedByStreet.get_or_create_street_diff(a.street, streets)
            street_diff.surplus.append((a, c))

        sd: StreetDiff
        for sd in streets.values():
            m: MissingAddressInformation
            sd.num_missing_not_ignored = len([a for (a, m) in sd.missing.items() if m.ignore_information is None])
            s: SurplusInformation
            sd.num_surplus_not_ignored = len([a for (a, s) in sd.surplus if s.ignore_information is None])

        return streets

    @staticmethod
    def get_or_create_street_diff(street_name: str, streets):
        assert isinstance(street_name, str)
        if street_name not in streets:
            streets[street_name] = StreetDiff({}, {}, [], -1, -1)
        street_diff: StreetDiff = streets[street_name]
        return street_diff