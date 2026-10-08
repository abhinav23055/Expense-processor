-- Total, count, and average spending per category
SELECT
    category,
    COUNT(*)              AS num_expenses,
    SUM(amount)           AS total_spent,
    ROUND(AVG(amount), 2) AS average_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;

-- Spending per month
SELECT
    DATE_TRUNC('month', expense_date)::date AS month,
    COUNT(*)                                AS num_expenses,
    SUM(amount)                             AS total_spent,
    ROUND(AVG(amount), 2)                   AS average_spent
FROM expenses
GROUP BY month
ORDER BY month;

-- Five largest single expenses
SELECT expense_date, category, description, amount
FROM expenses
ORDER BY amount DESC
LIMIT 5;