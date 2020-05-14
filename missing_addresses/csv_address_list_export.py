from csv import writer
from missing_addresses import Address, Coordinate, IgnoredAddressInformation
from typing import Dict


class CsvAddressListExport:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_reference(self, addresses: Dict[Address, Coordinate]):
        with open(self.file_path, 'w', newline='', encoding='UTF-8') as csvfile:
            w = writer(csvfile)
            w.writerow(('addr:street', 'addr:housenumber', 'lat', 'lon'))
            for (a, c) in addresses.items():
                w.writerow([a.street, str(a.housenumber), c.lat, c.lon])

    def save_ignored(self, addresses: Dict[Address, IgnoredAddressInformation]):
        with open(self.file_path, 'w', newline='', encoding='UTF-8') as csvfile:
            w = writer(csvfile)
            w.writerow(('addr:street', 'addr:housenumber', 'exists', 'reason', 'ignore_date'))
            for (a, i) in addresses.items():
                w.writerow([a.street, str(a.housenumber), i.exists, i.reason, i.ignore_date.strftime(IgnoredAddressInformation.get_date_format())])
