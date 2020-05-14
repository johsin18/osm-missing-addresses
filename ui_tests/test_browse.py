from pages import SummaryPage


def test_open_tool_window_on_match(summary_page: SummaryPage):
    assert not summary_page.tool_window_visible()
    summary_page.click_address('Identical Street', '1')
    assert summary_page.tool_window_visible()


def test_close_tool_window(summary_page: SummaryPage):
    summary_page.click_address('Identical Street', '1')
    assert summary_page.tool_window_visible()
    summary_page.close_tool_window()
    assert not summary_page.tool_window_visible()


def test_show_on_osm_on_match(summary_page: SummaryPage):
    summary_page.click_address('Identical Street', '1')
    summary_page.show_on_osm()
    assert summary_page.osm_tab_opened_on_primitive('way', 1)


def test_show_on_osm_on_missing(summary_page: SummaryPage):
    summary_page.click_address('Missing Street', '2')
    summary_page.show_on_osm()
    assert summary_page.osm_tab_opened_on_location('2.10000/2.20000')


def test_show_on_osm_on_surplus(summary_page: SummaryPage):
    summary_page.click_address('Surplus Street', '4')
    summary_page.show_on_osm()
    assert summary_page.osm_tab_opened_on_primitive('node', 31)
