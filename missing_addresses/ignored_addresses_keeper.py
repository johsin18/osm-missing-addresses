from missing_addresses import *
from typing import Dict


class IgnoredAddressesKeeper:
    """Keeper of the ignored addresses.  After each change, the ignored addresses are dumped to a file, with reason."""
    __addresses_to_be_ignored: Dict[Address, IgnoredAddressInformation]
    __export: CsvAddressListExport

    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            self.__addresses_to_be_ignored = CsvAddressListImport.read_to_be_ignored(file_path)
        except FileNotFoundError as e:
            print("No ignored addresses found so far, starting with an empty set")
            self.__addresses_to_be_ignored = {}
        self.__export = CsvAddressListExport(file_path)

    def add_ignored(self, a: Address, i: IgnoredAddressInformation):
        self.__addresses_to_be_ignored[a] = i
        self.__save()

    def remove_ignored(self, a: Address):
        del self.__addresses_to_be_ignored[a]
        self.__save()

    def __save(self):
        self.__export.save_ignored(self.__addresses_to_be_ignored)
