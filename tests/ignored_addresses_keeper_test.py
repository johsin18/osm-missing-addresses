import os
from pathlib import Path
from missing_addresses import IgnoredAddressesKeeper, Address, IgnoredAddressInformation, CsvAddressListImport

script_path = Path(__file__).parent.absolute()


def test_add():
    file_path = Path(script_path, 'keeper_addresses_to_be_ignored.csv')
    if os.path.exists(file_path):
        os.remove(file_path)
    keeper = IgnoredAddressesKeeper(file_path)
    ignore_date = IgnoredAddressInformation.parse_ignore_date('2020-05-13')
    keeper.add_ignored(Address('Ignored Street', '1'),
                       IgnoredAddressInformation(False, "building does not exist", ignore_date))

    ignored = CsvAddressListImport.read_to_be_ignored(file_path)
    assert len(ignored) == 1
    assert ignored[Address('Ignored Street', '1')] == IgnoredAddressInformation(False, "building does not exist", ignore_date)


def test_add_with_different_reason():
    file_path = 'keeper_addresses_to_be_ignored_different_reason.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
    keeper = IgnoredAddressesKeeper(file_path)
    ignore_date = IgnoredAddressInformation.parse_ignore_date('2020-05-13')
    keeper.add_ignored(Address('Ignored Street', '1'), IgnoredAddressInformation(False, "building does not exist", ignore_date))
    keeper.add_ignored(Address('Ignored Street', '1'), IgnoredAddressInformation(True, "building does exist", ignore_date))

    ignored = CsvAddressListImport.read_to_be_ignored(file_path)
    assert len(ignored) == 1
    assert ignored[Address('Ignored Street', '1')] == IgnoredAddressInformation(True, "building does exist", ignore_date)
