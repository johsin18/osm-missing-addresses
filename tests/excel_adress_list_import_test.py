from missing_addresses import ExcelAddressListImport, Address, Coordinate
from pathlib import Path

script_path = Path(__file__).parent.absolute()


def test_import():
    addresses = ExcelAddressListImport().read(Path(script_path, 'some_reference_addresses.xlsx'))
    assert isinstance(addresses, dict)
    assert len(addresses) == 3
    assert addresses[Address('Aalener Straße', '1')] == Coordinate(48.79120048603291, 8.99242822552413)
    assert addresses[Address('Albrecht-Dürer-Straße', '16/1')] == Coordinate(48.79599754936906, 9.006450776187728)
    assert addresses[Address('Am Schlossberg', '3')] == Coordinate(48.816561542901326, 9.01796943845542)
    assert Address('Am Schlossberg', '1') not in addresses
