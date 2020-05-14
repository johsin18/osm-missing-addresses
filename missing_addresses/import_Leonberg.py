from missing_addresses import ExcelAddressListImport, CsvAddressListExport

if __name__ == '__main__':
    reference = ExcelAddressListImport().read('200205_Adressen_Leonberg_ohne_Garagen.xls.xlsx')
    CsvAddressListExport('reference_addresses.csv').save_reference(reference)
