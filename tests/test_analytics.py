from expense_processing.analytics import REPORTS


def test_expected_reports_exist():
    assert set(REPORTS) == {"by-category", "monthly", "top-expenses"}


def test_every_report_is_a_select_query():
    for name, sql in REPORTS.items():
        assert sql.strip().upper().startswith("SELECT"), name