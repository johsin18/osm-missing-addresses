import pandas
from missing_addresses import *
from typing import Dict


class ExcelAddressListImport:
    __projection: BadenWuerttembergProjection

    def read(self, file_path, projection, street_column, housenumber_columns) -> Dict[Address, Coordinate]:
        excel_file = pandas.read_excel(file_path)
        addresses = {}
        for index, row in excel_file.iterrows():
            x = ExcelAddressListImport.extract_coordinate(row['X'])
            y = ExcelAddressListImport.extract_coordinate(row['Y'])
            (lat, lon) = projection.project_to_latlon(x, y)
            addresses[Address(row[street_column], row[housenumber_columns])] = Coordinate(lat, lon)
        return addresses

    @staticmethod
    def extract_coordinate(coordinate):
        if isinstance(coordinate, str):
            return coordinate.replace(',', '.')
        else:
            return coordinate
