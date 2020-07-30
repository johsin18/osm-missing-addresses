from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time


class SummaryPage:

    URL = 'http://localhost/PaperTown/summary'
    browser: WebDriver

    def __init__(self, browser: WebDriver):
        self.browser = browser

    def load(self):
        self.browser.get(self.URL)

    def tool_window_visible(self) -> bool:
        return self.get_tool_window().is_displayed()

    def get_tool_window(self):
        tool_window: WebElement = self.browser.find_element(By.ID, 'toolWindow')
        return tool_window

    def click_address(self, street, housenumber):
        address_node = self.find_address_node(street, housenumber)
        address_node.click()

    def find_address_node(self, street, housenumber) -> WebElement:
        street_row: WebElement = self.browser.find_element(By.XPATH, f'//tr[@name="{street}"]')
        address_node = street_row.find_element(By.XPATH, f'//*[self::a-i or self::a-m or self::a-s][text()="{housenumber}"]')
        return address_node

    def show_on_osm(self):
        link_show_in_osm_org: WebElement = self.browser.find_element(By.ID, 'linkShowInOsmOrg')
        link_show_in_osm_org.click()

    def osm_tab_opened_on_primitive(self, primitive_type, primitive_id) -> bool:
        return self.tab_opened_with_url(f'https://www.openstreetmap.org/{primitive_type}/{primitive_id}')

    def osm_tab_opened_on_location(self, location) -> bool:
        return self.tab_opened_with_url(f'https://www.openstreetmap.org/#map=19/{location}')

    def tab_opened_with_url(self, url):
        window_handles = self.browser.window_handles
        self.browser.switch_to.window(window_handles[1])
        success: bool = self.browser.current_url.startswith(url)
        self.browser.close()  # close tab
        self.browser.switch_to.window(window_handles[0])
        return success

    def recompute(self):
        recompute_button = self.browser.find_element(By.ID, 'recomputeButton')
        assert recompute_button is not None
        recompute_button.click()
        time.sleep(2)
        self.browser.refresh()

    def shows_recent_generation_time(self) -> bool:
        generation_datetime_span: WebElement = self.browser.find_element(By.ID, 'generationDatetime')
        generation_datetime_text: str = generation_datetime_span.text
        print(generation_datetime_text)
        dt: datetime = datetime.strptime(generation_datetime_text, '%Y-%m-%d %H:%M:%S')
        delta = (datetime.now() - dt) / timedelta(seconds=1)
        return 0 <= delta < 5

    def toggle_column(self, column):
        toggle = self.browser.find_element(By.XPATH, f'//input[@id="{column}"]')
        toggle.click()

    def any_visible(self, column) -> bool:
        address = self.find_any_address_node(column)
        return address.is_displayed()

    def find_any_address_node(self, column) -> WebElement:
        address_type = {'matches': 'a-i', 'missing': 'a-m', 'surplus': 'a-s'}[column]
        address: WebElement = self.browser.find_element(By.XPATH, f'//{address_type}')
        return address

    def close_tool_window(self):
        link_show_in_osm_org: WebElement = self.browser.find_element(By.ID, 'closeToolWindowButton')
        link_show_in_osm_org.click()
