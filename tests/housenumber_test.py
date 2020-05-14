from missing_addresses import Housenumber, InvalidHousenumber
import pytest


def test_str():
    assert str(Housenumber('1')) == '1'
    assert str(Housenumber('2/13')) == '2/13'
    assert str(Housenumber('3 a')) == '3a'
    assert str(Housenumber('3A')) == '3a'
    assert str(Housenumber('50/3c')) == '50/3c'


def test_sort_key():
    assert Housenumber('1').sort_key() == (1, 0, '')
    assert Housenumber('2/13').sort_key() == (2, 13, '')
    assert Housenumber('50/3a').sort_key() == (50, 3, 'a')
    assert Housenumber('3 a').sort_key() == (3, 0, 'a')
    assert Housenumber('3A').sort_key() == (3, 0, 'a')


def test_equality_key():
    assert Housenumber('1').equality_key() == '1'
    assert Housenumber('2/13').equality_key() == '2/13'
    assert Housenumber('50/3a').equality_key() == '50/3a'
    assert Housenumber('3 a').equality_key() == '3a'
    assert Housenumber('3A').equality_key() == '3a'
    assert Housenumber('3A') == Housenumber('3 a')


def test_invalid():
    with pytest.raises(InvalidHousenumber):
        Housenumber("")
    with pytest.raises(InvalidHousenumber):
        Housenumber("0")
    with pytest.raises(InvalidHousenumber):
        Housenumber("-1")
    with pytest.raises(InvalidHousenumber):
        Housenumber("42/0")
    with pytest.raises(InvalidHousenumber):
        Housenumber("13abc")
    with pytest.raises(InvalidHousenumber):
        Housenumber("1/2/3")
    with pytest.raises(InvalidHousenumber):
        Housenumber("3a5")
