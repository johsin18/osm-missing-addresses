from pages import SummaryPage


def test_hide_and_show(summary_page: SummaryPage):
    assert summary_page.any_visible('matches')
    summary_page.toggle_column('matches')
    assert not summary_page.any_visible('matches')
    summary_page.toggle_column('matches')
    assert summary_page.any_visible('matches')

    assert summary_page.any_visible('missing')
    summary_page.toggle_column('missing')
    assert not summary_page.any_visible('missing')
    summary_page.toggle_column('missing')
    assert summary_page.any_visible('missing')

    assert summary_page.any_visible('surplus')
    summary_page.toggle_column('surplus')
    assert not summary_page.any_visible('surplus')
    summary_page.toggle_column('surplus')
    assert summary_page.any_visible('surplus')
