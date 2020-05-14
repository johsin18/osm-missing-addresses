from missing_addresses import *
from pathlib import Path
import pytest
from .diff_ordered_by_street_test import create_diff_ordered_by_street
from AdvancedHTMLParser import AdvancedHTMLParser, AdvancedTag
from typing import List
from datetime import datetime

script_path = Path(__file__).parent.absolute()


def test_summary():
    diff, diff_ordered_by_streets = create_diff_ordered_by_street()
    metadata = AddressDiffMetaData("Test City", datetime.now(), datetime.now(), datetime.now())
    target_file = Path(script_path, 'street_ordered_html_summary.html')
    StreetOrderedHtmlSummary().write(diff_ordered_by_streets, diff, metadata, target_file)
    assert target_file.exists()

    summary = AdvancedHTMLParser()
    summary.parseFile(target_file)
    main_table = summary.getElementById('mainTable')

    matches: List[AdvancedTag] = summary.getElementsByTagName('a-i', main_table).all()
    assert len(matches) == 3
    street_row = matches[0].parentElement.parentElement
    assert street_row.getChildren()[0].textContent == 'Identical Street'
    assert street_row.getChildren()[1].getChildren()[0].textContent == '3: '
    assert matches[0].getAttribute('p') == "w1"
    assert matches[0].getAttribute('c') == "1.1,1.2"
    assert matches[1].getAttribute('p') == "w7"
    assert matches[1].getAttribute('c') == "7.1,7.2"
    assert matches[2].getAttribute('p') == "w13"
    assert matches[2].getAttribute('c') == "13.1,13.2"

    missing: List[AdvancedTag] = summary.getElementsByTagName('a-m', main_table).all()
    assert len(missing) == 2
    street_row = missing[0].parentElement.parentElement
    assert street_row.getChildren()[1].getChildren()[0].textContent == '0: '
    assert street_row.getChildren()[0].textContent == 'Missing Street'
    assert missing[0].getAttribute('c') == '2.1,2.2'
    assert missing[1].hasAttribute('ignored')
    assert missing[1].getAttribute('reason') == 'building does not exist'
    assert missing[1].getAttribute('c') == '3.1,3.2'

    surplus: List[AdvancedTag] = summary.getElementsByTagName('a-s', main_table).all()
    assert len(missing) == 2
    street_row = surplus[0].parentElement.parentElement
    assert surplus[0].parentElement.parentElement.getChildren()[0].textContent == 'Surplus Street'
    assert street_row.getChildren()[1].getChildren()[0].textContent == '0: '
    assert surplus[0].getAttribute('p') == 'w32'
    assert surplus[1].hasAttribute('ignored')
    assert surplus[1].getAttribute('reason') == 'building does exist'
    assert surplus[1].getAttribute('p') == 'n31'


@pytest.mark.skipif(True, reason="taking too long")
def test_summary_Leonberg():
    reference = ExcelAddressListImport().read(Path(script_path, '../Leonberg/200205_Adressen_Leonberg_ohne_Garagen.xls.xlsx'))
    actual = CsvAddressListImport.read_actual(Path(script_path, '20200522_Leonberg_actual.csv'))
    ignored = CsvAddressListImport.read_to_be_ignored(Path(script_path, '../Leonberg/addresses_to_ignore.csv'))
    diff = AddressDiffComputation().pretty_diff(reference, actual, ignored)
    diff_ordered_by_streets = DiffOrderedByStreet().create_view(diff)
    StreetOrderedHtmlSummary().write(diff_ordered_by_streets, diff, Path(script_path, 'street_ordered_html_summary.html'))
