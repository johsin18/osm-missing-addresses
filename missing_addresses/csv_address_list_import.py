from datetime import date
import pandas
from missing_addresses import Address, Housenumber, OsmPrimitive, Coordinate, IgnoredAddressInformation, InvalidHousenumber, \
    HousenumberRangeExpander
from typing import Dict, List, Tuple


class CsvAddressListImport:
    @staticmethod
    def read_reference(file_path_or_buffer) -> Dict[Address, Coordinate]:
        csv_file = pandas.read_csv(file_path_or_buffer)
        addresses = {}
        for index, row in csv_file.iterrows():
            try:
                addresses[CsvAddressListImport.get_address(row)] = Coordinate(row.get('lat'), row.get('lon'))
            except InvalidHousenumber as i:
                print(f'Invalid housenumber "{i.input_string}": {i.message}"')
                # skip this address, continue with others

        return addresses

    @staticmethod
    def read_actual(file_path_or_buffer) -> List[Tuple[Address, OsmPrimitive]]:
        csv_file = pandas.read_csv(file_path_or_buffer)
        addresses = []
        for index, row in csv_file.iterrows():
            try:
                addresses_for_housenumber = CsvAddressListImport.get_addresses(row)
                for a in addresses_for_housenumber:
                    addresses.append((a, OsmPrimitive(row.get('@type'), row.get('@id'))))
            except InvalidHousenumber as i:
                print(f'Invalid housenumber "{i.input_string}": {i.message}"')
                # skip this address, continue with others

        return addresses

    @staticmethod
    def read_to_be_ignored(file_path_or_buffer) -> Dict[Address, IgnoredAddressInformation]:
        csv_file = pandas.read_csv(file_path_or_buffer)
        addresses = {}
        for index, row in csv_file.iterrows():
            ignore_date_string: str = row.get('ignore_date')
            try:
                ignore_date = IgnoredAddressInformation.parse_ignore_date(ignore_date_string)
            except (ValueError, TypeError):
                print(f'To be ignored address has invalid ignore date "{ignore_date_string}", so we assume 2020-05-01')
                ignore_date = IgnoredAddressInformation.parse_ignore_date('2020-05-01')
            try:
                addresses[CsvAddressListImport.get_address(row)] = \
                    IgnoredAddressInformation(bool(row.get('exists')), row.get('reason'), ignore_date)
            except InvalidHousenumber as i:
                print(f'Invalid housenumber "{i.input_string}": {i.message}"')
                # skip this address, continue with others

        return addresses

    @staticmethod
    def get_address(row) -> Address:
        return CsvAddressListImport.get_addresses(row)[0]

    @staticmethod
    def get_addresses(row) -> list:
        street = row.get('addr:street')
        if not isinstance(street, str):
            street = row.get('addr:place', "")
        housenumber_string = str(row['addr:housenumber'])
        try:
            housenumber = Housenumber(housenumber_string)
            return [Address(street, housenumber)]

        except InvalidHousenumber as i:
            housenumbers = HousenumberRangeExpander.expand(housenumber_string)
            if len(housenumbers) == 0:
                raise i
            return [Address(street, h) for h in housenumbers]
