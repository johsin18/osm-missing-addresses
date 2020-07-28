from behave import *
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time


@given('summary is loaded')
def step_impl(context):
    browser: WebDriver = webdriver.Chrome()
    browser.get("http://localhost/PaperTown/summary")
    context.browser = browser
    tool_window = get_tool_window(browser)
    assert not tool_window.is_displayed()


@when(u'user opened toolbox for {address}')
def step_impl(context, address):
    browser: WebDriver = context.browser
    housenumber, street = split_address(address)
    street_row: WebElement = browser.find_element(By.XPATH, f'//tr[@name="{street}"]')
    address_widget = street_row.find_element(By.XPATH, f'//*[self::a-i or self::a-m or self::a-s][text()="{housenumber}"]')
    address_widget.click()


def split_address(address):
    street, _, housenumber = address.rpartition(' ')
    return housenumber, street


@when('user clicked Recompute')
def step_impl(context):
    browser: WebDriver = context.browser
    recompute_button = browser.find_element(By.ID, 'recomputeButton')
    assert recompute_button is not None
    recompute_button.click()
    time.sleep(2)
    browser.refresh()


@when('user toggles {column}')
def step_impl(context, column):
    browser: WebDriver = context.browser
    toggle = browser.find_element(By.XPATH, f'//input[@id="{column}"]')
    toggle.click()


@when('user clicked Show in openstreetmap.org')
def step_impl(context):
    browser: WebDriver = context.browser
    link_show_in_osm_org: WebElement = browser.find_element(By.ID, 'linkShowInOsmOrg')
    link_show_in_osm_org.click()


@then('toolbox opens for {address}')
def step_impl(context, address):
    browser: WebDriver = context.browser
    tool_window = get_tool_window(browser)
    assert tool_window.is_displayed()


def get_tool_window(browser):
    tool_window: WebElement = browser.find_element(By.ID, 'toolWindow')
    return tool_window


@then('page will show a late datetime as Generation time')
def step_impl(context):
    browser: WebDriver = context.browser
    generation_datetime_span: WebElement = browser.find_element(By.ID, 'generationDatetime')
    generation_datetime_text: str = generation_datetime_span.text
    print(generation_datetime_text)
    dt: datetime = datetime.strptime(generation_datetime_text, '%Y-%m-%d %H:%M:%S')
    delta = (datetime.now() - dt) / timedelta(seconds=1)
    assert delta >= 0
    assert delta < 5


@then('{column} are shown')
def step_impl(context, column):
    address = find_address_node(context.browser, column)
    assert address.is_displayed()


@then('{column} are hidden')
def step_impl(context, column):
    address = find_address_node(context.browser, column)
    assert not address.is_displayed()


def find_address_node(browser, column) -> WebElement:
    address_type = {'matches': 'a-i', 'missing': 'a-m', 'surplus': 'a-s'}[column]
    address: WebElement = browser.find_element(By.XPATH, f'//{address_type}')
    return address


@then('new tab showing OSM {primitive_type} with ID {primitive_id} will open')
def step_impl(context, primitive_type, primitive_id):
    browser: WebDriver = context.browser
    window_handles = browser.window_handles
    browser.switch_to.window(window_handles[1])
    assert browser.current_url.startswith(f'https://www.openstreetmap.org/{primitive_type}/{primitive_id}')
    browser.close()  # close tab
    browser.switch_to.window(window_handles[0])


@then('new tab showing OSM at location {location}')
def step_impl(context, location):
    browser: WebDriver = context.browser
    window_handles = browser.window_handles
    browser.switch_to.window(window_handles[1])
    assert browser.current_url.startswith(f'https://www.openstreetmap.org/#map=19/{location}')
    browser.close()  # close tab
    browser.switch_to.window(window_handles[0])
