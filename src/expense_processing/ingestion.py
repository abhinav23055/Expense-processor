import csv
import logging
from pathlib import Path

from pydantic import ValidationError

from expense_processing.models import Expense
from expense_processing.config import DATA_FOLDER
from expense_processing.db import get_connection

logger = logging.getLogger(__name__)

INSERT_SQL = """
    INSERT INTO expenses (expense_date, category, description, amount, payment_method)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
"""


def read_valid_rows(path: Path):
    valid = []
    invalid_count = 0

    with open(path, newline="", encoding="utf-8") as f:
        for line_number, row in enumerate(csv.DictReader(f), start=2):
            try:
                valid.append(Expense.model_validate(row))
            except ValidationError as error:
                first = error.errors()[0]
                logger.warning(
                    "%s line %d skipped (%s): %s",
                    path.name, line_number, first["loc"][0], first["msg"],
                )
                invalid_count += 1

    return valid, invalid_count

def insert_expenses(expenses, conn):
    inserted = 0
    for expense in expenses:
        cursor = conn.execute(INSERT_SQL, (
            expense.expense_date,
            expense.category,
            expense.description,
            expense.amount,
            expense.payment_method,
        ))
        inserted += cursor.rowcount
    conn.commit()
    return inserted

def ingest_folder(folder=DATA_FOLDER):
    files = sorted(Path(folder).glob("*.csv"))
    if not files:
        logger.warning("No CSV files found in %s", folder)
        return

    logger.info("Found %d CSV file(s) in %s", len(files), folder)
    totals = {"inserted": 0, "duplicates": 0, "invalid": 0}

    with get_connection() as conn:
        for path in files:
            logger.info("Processing %s", path.name)
            rows, invalid = read_valid_rows(path)
            inserted = insert_expenses(rows, conn)
            duplicates = len(rows) - inserted

            logger.info(
                "%s done: %d inserted, %d duplicates, %d invalid",
                path.name, inserted, duplicates, invalid,
            )
            totals["inserted"] += inserted
            totals["duplicates"] += duplicates
            totals["invalid"] += invalid

    logger.info("All files done: %s", totals)
    return totals