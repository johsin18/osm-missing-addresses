import os
from pathlib import Path
from missing_addresses import IgnoredAddressesKeeper, Address, IgnoredAddressInformation, CsvAddressListImport

script_path = Path(__file__).parent.absolute()
ignore_date = IgnoredAddressInformation.parse_ignore_date('2020-05-13')


def test_add():
    file_path, keeper = create_keeper('keeper_addresses_to_be_ignored.csv')
    keeper.add_ignored(Address('Ignored Street', '1'),
                       IgnoredAddressInformation(False, "building does not exist", ignore_date))

    ignored = CsvAddressListImport.read_to_be_ignored(file_path)
    assert len(ignored) == 1
    assert ignored[Address('Ignored Street', '1')] == IgnoredAddressInformation(False, "building does not exist", ignore_date)


def create_keeper(file_name: str):
    file_path = Path(script_path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    keeper = IgnoredAddressesKeeper(file_path)
    return file_path, keeper


def test_add_with_different_reason():
    file_path, keeper = create_keeper('keeper_addresses_to_be_ignored_different_reason.csv')
    keeper.add_ignored(Address('Ignored Street', '1'), IgnoredAddressInformation(False, "building does not exist", ignore_date))
    keeper.add_ignored(Address('Ignored Street', '1'), IgnoredAddressInformation(True, "building does exist", ignore_date))

    ignored = CsvAddressListImport.read_to_be_ignored(file_path)
    assert len(ignored) == 1
    assert ignored[Address('Ignored Street', '1')] == IgnoredAddressInformation(True, "building does exist", ignore_date)


def test_remove():
    file_path, keeper = create_keeper('keeper_addresses_to_be_ignored_not_anymore.csv')
    address = Address('Ignored Street', '1')
    keeper.add_ignored(address, IgnoredAddressInformation(False, "building does not exist", ignore_date))
    keeper.remove_ignored(address)

    ignored = CsvAddressListImport.read_to_be_ignored(file_path)
    assert len(ignored) == 0
