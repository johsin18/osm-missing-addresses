import pytest
import selenium.webdriver
from pages import SummaryPage


@pytest.fixture
def summary_page():
    browser = selenium.webdriver.Chrome()
    browser.implicitly_wait(10)
    summary_page = SummaryPage(browser)
    summary_page.load()
    yield summary_page
    browser.quit()
