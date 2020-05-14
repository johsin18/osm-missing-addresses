from missing_addresses import Address, MissingAddressInformation, SurplusInformation, Coordinate, IgnoredAddressInformation, MatchInformation, \
    OsmPrimitive, AddressDiffComputation, AddressDiff

ignore_date = IgnoredAddressInformation.parse_ignore_date('2020-05-13')


def create_diff():
    address_diff = AddressDiffComputation()
    reference = {Address('Identical Street', '1'): Coordinate(1.1, 1.2),
                 Address('Identical Street', '7'): Coordinate(7.1, 7.2),
                 Address('Identical Street', '13'): Coordinate(13.1, 13.2),
                 Address('Missing Street', '2'): Coordinate(2.1, 2.2),
                 Address('Missing Street', '2'): Coordinate(2.1, 2.2),  # duplicate in reference set
                 Address('Missing Street', '3'): Coordinate(3.1, 3.2)}
    actual = [(Address('Identical Street', '1'), OsmPrimitive('way', 1)),
              (Address('Identical Street', '7'), OsmPrimitive('way', 7)),
              (Address('Identical Street', '13'), OsmPrimitive('way', 13)),
              (Address('Surplus Street', '4'), OsmPrimitive('node', 31)),
              (Address('Surplus Street', '3'), OsmPrimitive('way', 32))]  # way and node with same address, to be reported twice
    ignored = {Address('Missing Street', '3'): IgnoredAddressInformation(False, 'building does not exist', ignore_date),
               Address('Surplus Street', '4'): IgnoredAddressInformation(True, 'building does exist', ignore_date)}

    diff: AddressDiff = address_diff.compute(reference, actual, ignored)
    return diff


def test_diff():
    diff: AddressDiff = create_diff()

    assert len(diff.matches) == 3
    assert len(diff.missing) == 2
    assert len(diff.surplus) == 2
    assert diff.num_matches == 3
    assert diff.num_missing_not_ignored == 1
    assert diff.num_surplus_not_ignored == 1
    assert round(abs(diff.coverage_in_percent - 75.0), 1) == 0

    assert diff.matches[Address('Identical Street', '1')] == MatchInformation(OsmPrimitive('way', 1), Coordinate(1.1, 1.2))
    assert diff.matches[Address('Identical Street', '7')] == MatchInformation(OsmPrimitive('way', 7), Coordinate(7.1, 7.2))
    assert diff.matches[Address('Identical Street', '13')] == MatchInformation(OsmPrimitive('way', 13), Coordinate(13.1, 13.2))
    assert diff.missing[Address('Missing Street', '2')] == MissingAddressInformation(Coordinate(2.1, 2.2), None)
    assert diff.missing[Address('Missing Street', '3')] == \
           MissingAddressInformation(Coordinate(3.1, 3.2), IgnoredAddressInformation(False, 'building does not exist', ignore_date))
    assert diff.surplus[0] == (Address('Surplus Street', '4'), SurplusInformation(OsmPrimitive('node', 31), IgnoredAddressInformation(True, 'building does exist', ignore_date)))
    assert diff.surplus[1] == (Address('Surplus Street', '3'), SurplusInformation(OsmPrimitive('way', 32), None))

    return diff
