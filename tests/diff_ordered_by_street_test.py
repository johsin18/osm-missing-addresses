from missing_addresses import DiffOrderedByStreet, AddressDiff, StreetDiff, Address, MatchInformation, OsmPrimitive, Coordinate, \
    MissingAddressInformation, IgnoredAddressInformation, SurplusInformation
from typing import Dict
from .address_diff_computation_test import create_diff

ignore_date = IgnoredAddressInformation.parse_ignore_date('2020-05-13')


def create_diff_ordered_by_street() -> (AddressDiff, Dict[str, StreetDiff]):
    diff: AddressDiff = create_diff()
    diff_ordered_by_streets: Dict[str, StreetDiff] = DiffOrderedByStreet().create_view(diff)
    assert len(diff_ordered_by_streets) == 3

    assert diff_ordered_by_streets['Identical Street'].matches == {
        Address('Identical Street', '1'): MatchInformation(OsmPrimitive('way', 1), Coordinate(1.1, 1.2)),
        Address('Identical Street', '7'): MatchInformation(OsmPrimitive('way', 7), Coordinate(7.1, 7.2)),
        Address('Identical Street', '13'): MatchInformation(OsmPrimitive('way', 13), Coordinate(13.1, 13.2))
    }
    assert diff_ordered_by_streets['Identical Street'].missing == {}
    assert diff_ordered_by_streets['Identical Street'].surplus == []

    assert diff_ordered_by_streets['Missing Street'].matches == {}
    assert diff_ordered_by_streets['Missing Street'].missing == {
        Address('Missing Street', '2'): MissingAddressInformation(Coordinate(2.1, 2.2), None),
        Address('Missing Street', '3'): MissingAddressInformation(Coordinate(3.1, 3.2),
                                                                  IgnoredAddressInformation(False, 'building does not exist', ignore_date)),
    }
    assert diff_ordered_by_streets['Missing Street'].surplus == []

    assert diff_ordered_by_streets['Surplus Street'].matches == {}
    assert diff_ordered_by_streets['Surplus Street'].missing == {}
    assert diff_ordered_by_streets['Surplus Street'].surplus == [
        (Address('Surplus Street', '4'), SurplusInformation(OsmPrimitive('node', 31),
                                                            IgnoredAddressInformation(True, 'building does exist', ignore_date))),
        (Address('Surplus Street', '3'), SurplusInformation(OsmPrimitive('way', 32), None))
    ]

    return diff, diff_ordered_by_streets


def test_diff_ordered_by_street():
    diff, diff_ordered_by_streets = create_diff_ordered_by_street()
    print(diff_ordered_by_streets)
