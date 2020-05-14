import pytest
import selenium.webdriver
from pages import SummaryPage
import os
from pathlib import Path
import requests
from requests import Response

script_path = Path(__file__).parent.absolute()


@pytest.fixture
def summary_page():
    browser = selenium.webdriver.Chrome()
    browser.implicitly_wait(10)
    summary_page = SummaryPage(browser)
    summary_page.load()
    yield summary_page
    browser.quit()


@pytest.fixture
def clean_ignore_states():
    os.system(f'git checkout {script_path}/../PaperTown/addresses_to_ignore.csv')
    r: Response = requests.get('http://localhost/PaperTown/invalidate_ignores')
    assert r.status_code == 200
    yield None
    os.system(f'git checkout {script_path}/../PaperTown/addresses_to_ignore.csv')
