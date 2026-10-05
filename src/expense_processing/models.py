from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class Expense(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    expense_date : date
    category : str = Field(max_length=50)
    description : str = ""
    amount : Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    payment_method : str = Field(default="", max_length=30)


    @field_validator("category")
    @classmethod
    def category_must_not_be_empty(cls, value : str) -> str:
        if not value:
            raise ValueError("Category cannot be empty")
        return value.title()