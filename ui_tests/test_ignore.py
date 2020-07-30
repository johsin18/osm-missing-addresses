from pages import SummaryPage


def test_ignore_missing(summary_page: SummaryPage):
    summary_page.click_address('Missing Street', '2')
    summary_page.ignore('building does not exist')
    summary_page.click_address('Identical Street', '7')
    summary_page.close_tool_window()  # otherwise Missing Street 2 would be hidden, and could not be clicked
    summary_page.click_address('Missing Street', '2')
    assert summary_page.ignore_reason_selected('building does not exist')
