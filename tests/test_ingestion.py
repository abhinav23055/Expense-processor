from pathlib import Path

from expense_processing.ingestion import read_valid_rows

HEADER = "expense_date,category,description,amount,payment_method\n"


def write_csv(tmp_path: Path, rows: list[str]) -> Path:
    path = tmp_path / "sample.csv"
    path.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_valid_rows_are_returned(tmp_path):
    path = write_csv(tmp_path, [
        "2026-01-03,Food,Lunch,250.00,UPI",
        "2026-01-05,Transport,Metro,500.00,Card",
    ])
    valid, invalid = read_valid_rows(path)
    assert len(valid) == 2
    assert invalid == 0


def test_invalid_rows_are_skipped_and_counted(tmp_path):
    path = write_csv(tmp_path, [
        "2026-01-03,Food,Lunch,250.00,UPI",
        "2026-01-12,Food,Dinner,-300.00,UPI",
        "2026-01-15,,Movie,400.00,Card",
        "2026-31-02,Shopping,Headphones,1999.00,Card",
    ])
    valid, invalid = read_valid_rows(path)
    assert len(valid) == 1
    assert invalid == 3