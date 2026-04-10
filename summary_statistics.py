import sqlite3
from config import DATABASE
from tabulate import tabulate
from datetime import datetime

def summary_statistics_main(user_id):
    while True:
        month_year = input("\nEnter month (YYYY-MM) for summary statistics (or 'exit'): ")
        if month_year == 'exit':
            print()
            break
        try:
            datetime.strptime(month_year, "%Y-%m")
            summary_stats(user_id, month_year)
        except ValueError:
            print('Please enter a valid date!')
    
def summary_stats(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    start_date = f"{month_year}-01"

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = ?
        AND transaction_date >= ?
        AND transaction_date < date(?, '+1 month')
    """, (user_id, start_date, start_date))
    total_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND transaction_date >= ?
        AND transaction_date < date(?, '+1 month')
    """, (user_id, start_date, start_date))
    total_spent = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(budget_amount), 0)
        FROM budgets
        WHERE user_id = ?
        AND month = ?
    """, (user_id, month_year))
    total_budget = cursor.fetchone()[0]

    net = total_budget - total_spent

    cursor.execute("""
        SELECT AVG(total_spent) FROM (
        SELECT SUM(amount) as total_spent, strftime('%Y-%m', transaction_date) as month
        FROM transactions 
        WHERE user_id = ?
        GROUP BY month)
    """, (user_id,))

    average_spent = cursor.fetchone()[0]

    print(f"\nMonth: {month_year}")
    print(f"Total Transactions: {total_transactions}")
    print(f"Total Budget: ${total_budget:.2f}")
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Net (Budget - Spent): ${net:.2f}")
    print(f"Average Monthly Spend: ${average_spent:.2f}")

    cursor.execute("""
        SELECT
            c.category_name,
            COALESCE(b.budget_amount, 0) AS budget,
            COALESCE(SUM(t.amount), 0) AS spent,
            COALESCE(b.budget_amount, 0) - COALESCE(SUM(t.amount), 0) AS difference
        FROM categories c
        LEFT JOIN budgets b
            ON c.category_id = b.category_id AND b.month = ?
        LEFT JOIN transactions t
            ON c.category_id = t.category_id
            AND t.transaction_date >= ?
            AND t.transaction_date < date(?, '+1 month')
        WHERE c.user_id = ?
        GROUP BY c.category_name
        ORDER BY c.category_name
    """, (month_year, start_date, start_date, user_id))
    data = cursor.fetchall()

    print(tabulate(data, headers = ["Category", "Budget", "Spent", "Diff"], tablefmt = "grid"))

    conn.close()

    return
