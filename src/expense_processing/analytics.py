from expense_processing.db import get_connection
from typing import LiteralString

REPORTS: dict[str, LiteralString] = {
    "by-category": """
        SELECT category,
               COUNT(*)              AS num_expenses,
               SUM(amount)           AS total_spent,
               ROUND(AVG(amount), 2) AS average_spent
        FROM expenses
        GROUP BY category
        ORDER BY total_spent DESC
    """,
    "monthly": """
        SELECT DATE_TRUNC('month', expense_date)::date AS month,
               COUNT(*)                                AS num_expenses,
               SUM(amount)                             AS total_spent,
               ROUND(AVG(amount), 2)                   AS average_spent
        FROM expenses
        GROUP BY month
        ORDER BY month
    """,
    "top-expenses": """
        SELECT expense_date, category, description, amount
        FROM expenses
        ORDER BY amount DESC
        LIMIT 5
    """,
}


def run_report(name):
    with get_connection() as conn:
        cursor = conn.execute(REPORTS[name])
        headers = [column.name for column in cursor.description or []]
        rows = cursor.fetchall()

    table = [headers] + [[str(value) for value in row] for row in rows]
    widths = [max(len(row[i]) for row in table) for i in range(len(headers))]

    for index, row in enumerate(table):
        print(" | ".join(cell.ljust(width) for cell, width in zip(row, widths)))
        if index == 0:
            print("-+-".join("-" * width for width in widths))