from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime

from missing_addresses import OverpassAddressListImport, CsvAddressListImport, AddressDiffComputation, AddressDiffMetaData, \
    AddressesToOsmFileWriter, DiffOrderedByStreet, StreetOrderedHtmlSummary


def compute_complete_address_diff(area_name: str, area_id):
    diff_metadata = AddressDiffMetaData(area_name, datetime.now(), None, None)

    reference_addresses_file_name = 'reference_addresses.csv'
    print(f'Reading reference addresses from {reference_addresses_file_name}...')
    reference = CsvAddressListImport.read_reference(reference_addresses_file_name)
    diff_metadata.reference_date = datetime.fromtimestamp(Path(reference_addresses_file_name).stat().st_mtime)

    if isinstance(area_id, int):
        print(f'Getting actual addresses of area {area_id} from Overpass...')
        actual = OverpassAddressListImport().read(area_id, print_query=True)
        diff_metadata.actual_date = datetime.now()
    else:
        actual = CsvAddressListImport().read_actual('actual_addresses.csv')
        diff_metadata.actual_date = datetime.fromtimestamp(Path('actual_addresses.csv').stat().st_mtime)

    addresses_to_ignore_file_name = 'addresses_to_ignore.csv'
    print(f'Reading addresses to ignore from {addresses_to_ignore_file_name}...')
    ignored = CsvAddressListImport.read_to_be_ignored(addresses_to_ignore_file_name)

    print("Computing diff...")
    diff = AddressDiffComputation().diff(reference, actual, ignored)

    missing_addresses_file_name = 'missing_addresses.osm'
    print(f'Writing missing addresses to {missing_addresses_file_name}')
    AddressesToOsmFileWriter().write(diff.missing, missing_addresses_file_name)
    diff_ordered_by_streets = DiffOrderedByStreet().create_view(diff)
    summary_html_file_name = 'street_ordered_html_summary.html'
    print(f'Writing summary ordered by street to {summary_html_file_name}')
    StreetOrderedHtmlSummary().write(diff_ordered_by_streets, diff, diff_metadata, summary_html_file_name)


if __name__ == '__main__':
    """
    Main program for computing the diff of the reference set of addresses, and the ones actually present in the current OpenStreetMap map. 
    """
    parser = ArgumentParser(
        description=
             """
             Find the difference of the reference and the actual address data sets.
             The data sets are expected in the current working directory,
             the reference data set as reference_addresses.csv,
             the addresses to ignore as addresses_to_ignore.csv.
             The set of missing addresses will as OSM file is written to missing_addresses.osm,
             the summary ordered by streets, is written to street_ordered_html_summary.html.
             """)
    parser.add_argument('area_id', type=int, help='OSM ID of area')
    args = parser.parse_args()

    compute_complete_address_diff('Unknown', args.area_id)
