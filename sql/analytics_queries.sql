SELECT
    category,
    COUNT(*)              AS num_expenses,
    SUM(amount)           AS total_spent,
    ROUND(AVG(amount), 2) AS average_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;

SELECT
    DATE_TRUNC('month', expense_date)::date AS month,
    COUNT(*) AS num_expenses,
    SUM(amount) AS total_spent,
    ROUND(AVG(amount), 2) AS average_spent
FROM expenses
GROUP BY month
ORDER BY month;

SELECT expense_date, category, description, amount
FROM expenses
ORDER BY amount DESC
LIMIT 5;