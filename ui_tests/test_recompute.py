from pages import SummaryPage


def test_recompute(summary_page: SummaryPage):
    summary_page.recompute()
    assert summary_page.shows_recent_generation_time()
