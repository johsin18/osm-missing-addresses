from missing_addresses import *
from pathlib import Path


script_path = Path(__file__).parent.absolute()


def test_read_reference():
    addresses = CsvAddressListImport.read_reference(Path(script_path, 'reference_addresses.csv'))
    assert len(addresses) == 1
    for (a, c) in addresses.items():
        assert a.street != ""
        assert isinstance(a.housenumber, Housenumber)
        assert c is not None


def test_read_actual():
    addresses = CsvAddressListImport.read_actual(Path(script_path, 'actual_addresses.csv'))
    assert len(addresses) == 4
    for (a, p) in addresses:
        assert a.street != ""
        assert isinstance(a.housenumber, Housenumber)
        assert p.type in ['node', 'way', 'relation']
        assert isinstance(p.id, int)


def test_read_actual_with_housenumber_ranges():
    addresses = CsvAddressListImport.read_actual(Path(script_path, 'addresses_with_housenumber_ranges.csv'))
    assert len(addresses) == 8  # from 3 valid ranges and a single housenumber


def test_read_to_be_ignored():
    addresses = CsvAddressListImport.read_to_be_ignored(Path(script_path, 'addresses_to_be_ignored.csv'))
    assert len(addresses) == 2
    assert addresses[Address('Heumahden', '2')] == \
           IgnoredAddressInformation(False, "building does not exist", IgnoredAddressInformation.parse_ignore_date('2020-05-07'))
    assert addresses[Address('Hauptstraße', '4')] == \
           IgnoredAddressInformation(True, "custom reason", IgnoredAddressInformation.parse_ignore_date('2020-05-01'))
