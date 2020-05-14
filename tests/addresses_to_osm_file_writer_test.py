import os
from pathlib import Path
from missing_addresses import ExcelAddressListImport, AddressesToOsmFileWriter


script_path = Path(__file__).parent.absolute()


def test_write():
    target_file = 'addresses.osm'
    if os.path.exists(target_file):
        os.remove(target_file)

    addresses = ExcelAddressListImport().read(Path(script_path, 'some_reference_addresses.xlsx'))
    AddressesToOsmFileWriter().write(addresses, target_file)

    assert os.path.exists(target_file)
    with open(target_file, encoding='utf-8') as f:
        target_file_content: str = f.read()
        assert target_file_content.find('Albrecht-Dürer-Straße') >= 0
