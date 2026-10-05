CREATE TABLE IF NOT EXISTS expenses (
    id             SERIAL PRIMARY KEY,
    expense_date   DATE           NOT NULL,
    category       VARCHAR(50)    NOT NULL,
    description    TEXT           NOT NULL DEFAULT '',
    amount         NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    payment_method VARCHAR(30)    NOT NULL DEFAULT '',
    created_at     TIMESTAMP      NOT NULL DEFAULT NOW(),
    UNIQUE (expense_date, category, description, amount, payment_method)
);