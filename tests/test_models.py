from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from expense_processing.models import Expense

VALID_ROW = {
    "expense_date" : "2026-01-03",
    "category" : "food",
    "description" : "Lunch at cafe",
    "amount" : "250.00",
    "payment_method" : "UPI"
}

def test_valid_row_is_accepted():
    expense = Expense.model_validate(VALID_ROW)
    assert expense.expense_date == date(2026, 1, 3)
    assert expense.amount == Decimal("250.00")
    assert expense.category == "Food"


def test_negative_amount_is_rejected():
    with pytest.raises(ValidationError):
        Expense.model_validate({**VALID_ROW, "amount": "-300.00"})


def test_non_numeric_amount_is_rejected():
    with pytest.raises(ValidationError):
        Expense.model_validate({**VALID_ROW, "amount": "abc"})


def test_empty_category_is_rejected():
    with pytest.raises(ValidationError):
        Expense.model_validate({**VALID_ROW, "category": ""})


def test_impossible_date_is_rejected():
    with pytest.raises(ValidationError):
        Expense.model_validate({**VALID_ROW, "expense_date": "2026-31-02"})


def test_missing_optional_fields_default_to_empty_string():
    row = {k: v for k, v in VALID_ROW.items() if k not in ("description", "payment_method")}
    expense = Expense.model_validate(row)
    assert expense.description == ""
    assert expense.payment_method == ""