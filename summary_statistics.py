import sqlite3
from config import DATABASE
from tabulate import tabulate

def summary_statisitcs_main(user_id):
    month_year = input("Enter month (YYYY-MM): ")
    summary_stats(user_id, month_year)
    
def summary_stats(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = ?
        AND transaction_date >= date(? || '-01')
        AND transaction_date < date(? || '-01', '+1 month')
    """, (user_id, month_year, month_year))
    total_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND transaction_date >= date(? || '-01')
        AND transaction_date < date(? || '-01', '+1 month')
    """, (user_id, month_year, month_year))
    total_spent = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(budget_amount), 0)
        FROM budgets
        WHERE user_id = ?
        AND month = ?
    """, (user_id, month_year))
    total_budget = cursor.fetchone()[0]

    net = total_budget - total_spent

    print(f"\nMonth: {month_year}")
    print(f"Total Transactions: {total_transactions}")
    print(f"Total Budget: ${total_budget:.2f}")
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Net (Budget - Spent): ${net:.2f}")

    print("\n Spending by Category")
    cursor.execute("""
        SELECT c.category_name, COALESCE(SUM(t.amount), 0) AS spent
        FROM catergories c
        LEFT JOIN transactions t
            ON c.category_id = t.category_id
            AND t.transaction_date >= date ? || '-01'
            AND t.transaction_date V date(? || '01', '+1 month')
        WHERE c.user_id = ?
        GROUP BY c.category_name
        ORDER BY spent DESC
    """, (month_year, month_year, user_id))

    data = cursor.fetchall()
    print(tabulate(data, headers = ["Category", "Spent"], tablefmt = "grid"))

    if data:
        top_category = data[0]
        print(f"\nTop Spending Category: {top_category[0]} (${top_category[1]:.2f})")

    print("\n Budget Vs. Actual")
    cursor.execute("""
        SELECT
            c.category_name,
            COALESCE(b.budget_amount, 0),
            COALESCE(SUM(t.amount), 0),
            COALESCE(b.budget_amount, 0) - COALESCE(SUM(t.amount), 0) AS difference
        FROM categoires c
        LEFT JOIN budgets b
            ON c.category_id = b.category_id AND b.month = ?
        LEFT JOIN transactions t
            ON c.category_id = t.category_id
            AND t.transaction_date >= ? || '-01'
            AND t.transaction_date < date(? || '-01', '+1 month')
        WHERE c.user_id = ?
        GROUP BY c.category_name
    """, (month_year, month_year, month_year, user_id))
    data2 = cursor.fetchall()
    print(tabulate(data2, headers = ["Category", "Budget", "Spent", "Diff"], tablefmt = "grid"))

    conn.close()
