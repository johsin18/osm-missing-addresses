from missing_addresses import *

if __name__ == '__main__':
    reference = ExcelAddressListImport().read(
        '200205_Adressen_Leonberg_ohne_Garagen.xls.xlsx', BadenWuerttembergProjection(), 'STR', 'HAUSNUMMER')
    CsvAddressListExport('reference_addresses.csv').save_reference(reference)
