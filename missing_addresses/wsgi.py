from datetime import datetime
import os
from pathlib import Path
from flask import Flask, request
from urllib.parse import parse_qs
from missing_addresses import Address, IgnoredAddressInformation, IgnoredAddressesKeeper, compute_complete_address_diff
from typing import Dict

application = Flask(__name__)


@application.route("/")
def index():
    return "OSM Missing Addresses"


@application.route('/<city>/summary')
def serve_city(city):
    if city not in area_id_mapping:
        return "Unknown area", 404
    summary_file_path = Path(f'{city}/street_ordered_html_summary.html')
    if not summary_file_path.exists():
        recompute_diff(city)
        return "Summary was generated, please reload."
    return summary_file_path.read_text(encoding="UTF-8")


keepers: Dict[str, IgnoredAddressesKeeper] = {}


@application.route('/<city>/addresses_to_ignore', methods=['PUT', 'DELETE'])
def accept_ignored(city):
    if city not in area_id_mapping:
        return "Unknown area", 404
    if request.method == 'PUT':
        params: dict = parse_qs(request.query_string.decode("UTF-8"))
        if city not in keepers:
            keepers[city] = IgnoredAddressesKeeper(f'{city}/addresses_to_ignore.csv')
        keeper: IgnoredAddressesKeeper = keepers[city]
        keeper.add_ignored(Address(params['street'][0], params['housenumber'][0]),
                           IgnoredAddressInformation(params['exists'][0].lower() == 'true', params['reason'][0], datetime.now().date()))
        return "OK"


area_id_mapping = {'Leonberg': 722150,
                   'PaperTown': None}


@application.route('/<city>/recompute_summary', methods=['POST'])
def trigger_recompute_diff(city):
    if city not in area_id_mapping:
        return "Unknown area", 404
    if request.method == 'POST':
        recompute_diff(city)
        return "OK"


def recompute_diff(city):
    print(f'Recomputing diff for {city}')
    former: str = os.getcwd()
    os.chdir(city)
    try:
        compute_complete_address_diff(city, area_id_mapping[city])
    finally:
        os.chdir(former)
