import pandas
from missing_addresses import Address, Coordinate, BadenWuerttembergProjection
from typing import Dict

class ExcelAddressListImport:
    projection: BadenWuerttembergProjection

    def __init__(self):
        self.projection = BadenWuerttembergProjection()

    def read(self, file_path) -> Dict[Address, Coordinate]:
        excel_file = pandas.read_excel(file_path)
        addresses = {}
        for index, row in excel_file.iterrows():
            x = ExcelAddressListImport.extract_coordinate(row['X'])
            y = ExcelAddressListImport.extract_coordinate(row['Y'])
            (lat, lon) = self.projection.projected_to_latlon(x, y)
            addresses[Address(row['STR'], row['HAUSNUMMER'])] = Coordinate(lat, lon)
        return addresses

    @staticmethod
    def extract_coordinate(coordinate):
        if isinstance(coordinate, str):
            return coordinate.replace(',', '.')
        else:
            return coordinate
