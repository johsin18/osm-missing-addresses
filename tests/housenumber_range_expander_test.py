from missing_addresses import Housenumber, HousenumberRangeExpander, InvalidHousenumber
import pytest


def test_expand():
    assert HousenumberRangeExpander.expand('26-28') == [Housenumber('26'), Housenumber('28')]
    assert HousenumberRangeExpander.expand('3-5') == [Housenumber('3'), Housenumber('5')]
    assert HousenumberRangeExpander.expand('98- 102') == [Housenumber('98'), Housenumber('100'), Housenumber('102')]
    assert HousenumberRangeExpander.expand('3a-5b') == []
    assert HousenumberRangeExpander.expand('123') == []
    assert HousenumberRangeExpander.expand('') == []
    with pytest.raises(InvalidHousenumber):
        HousenumberRangeExpander.expand('5-3')
    with pytest.raises(InvalidHousenumber):
        HousenumberRangeExpander.expand('3-6')
