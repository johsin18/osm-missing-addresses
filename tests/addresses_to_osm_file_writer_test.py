import os
from missing_addresses import *
from typing import Dict


def test_write():
    target_file = 'addresses.osm'
    if os.path.exists(target_file):
        os.remove(target_file)

    addresses: Dict[Address, MissingAddressInformation] = {
        Address('Albrecht-Dürer-Straße', '5'): MissingAddressInformation(Coordinate(5.0, 5.1), None)
    }
    AddressesToOsmFileWriter().write_missing(addresses, target_file)

    assert os.path.exists(target_file)
    with open(target_file, encoding='utf-8') as f:
        target_file_content: str = f.read()
        assert target_file_content.find('Albrecht-Dürer-Straße') >= 0
