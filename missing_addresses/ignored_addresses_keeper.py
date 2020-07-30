from missing_addresses import CsvAddressListImport, Address, IgnoredAddressInformation, CsvAddressListExport
from typing import Dict


class IgnoredAddressesKeeper:
    addresses_to_be_ignored: Dict[Address, IgnoredAddressInformation]

    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            self.addresses_to_be_ignored = CsvAddressListImport.read_to_be_ignored(file_path)
        except FileNotFoundError as e:
            print("No ignored addresses found so far, starting with an empty set")
            self.addresses_to_be_ignored = {}
        self.export = CsvAddressListExport(file_path)

    def add_ignored(self, a: Address, i: IgnoredAddressInformation):
        self.addresses_to_be_ignored[a] = i
        self.save()

    def remove_ignored(self, a: Address):
        del self.addresses_to_be_ignored[a]
        self.save()

    def save(self):
        self.export.save_ignored(self.addresses_to_be_ignored)
