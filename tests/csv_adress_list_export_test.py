from missing_addresses import *
from pathlib import Path


script_path = Path(__file__).parent.absolute()


def test_save_reference():
    addresses = {Address('Hauptstraße', '23'): Coordinate(48.5, 8.5)}
    target_file = Path(script_path, 'reference_addresses.csv')
    CsvAddressListExport(target_file).save_reference(addresses)

    assert target_file.exists()
    with open(target_file, encoding='utf-8') as f:
        target_file_content: str = f.read()
        assert target_file_content == \
'''\
addr:street,addr:housenumber,lat,lon
Hauptstraße,23,48.5,8.5
'''
