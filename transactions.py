import sqlite3
from config import DATABASE
from tabulate import tabulate
from datetime import datetime

def transaction_options(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    while True:
        month_year = input("\nEnter Month and Year (YYYY-MM) for Transactions (or 'exit'):")
        if month_year == 'exit':
            break
        try:
            print(datetime.strptime(month_year, "%Y-%m"))
            break
        except ValueError:
            print('Please enter a valid date!')
            
    cursor.execute("""
    SELECT t.transaction_id, t.amount, c.category_name, t.transaction_date
    FROM transactions t
    JOIN categories c ON t.category_id = c.category_id
    WHERE t.user_id = ? and t.transaction_date >= ? || '-01' AND t.transaction_date < date(? || '-01', '+1 month')
    ORDER BY t.transaction_date desc
    LIMIT 10
    """, (user_id, month_year, month_year))

    data = cursor.fetchall()

    if data:
        print("Here are your last 10 transactions of the month")
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers = columns, tablefmt = "grid"))
    else:
        print("\nYou do not have any transactions yet! Let's add some.\n")

    conn.close()

    print("Select an option")
    while True:
        transaction_option_id = input("1: Add Transaction\n2: Delete Transaction\n3: Exit\n")
        if transaction_option_id not in ("1", "2", "3"):
            print("Please enter a proper option")
            continue
        return int(transaction_option_id), month_year

def add_transaction(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    while True:

        #show categories
        cursor.execute("""
            SELECT c.category_name AS category, b.budget_amount
            FROM categories c
            LEFT JOIN budgets b ON c.category_id = b.category_id and b.month = ?
            WHERE c.user_id = ? 
            """, (month_year, user_id))
        data = cursor.fetchall()
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers=columns, tablefmt="grid"))

        category_name = input("\nEnter category name for budget (or 'exit'): ")
        if category_name == "exit":
            break

        cursor.execute(
            "SELECT category_id FROM categories WHERE category_name = ? AND user_id = ?",
            (category_name, user_id)
        )
        category = cursor.fetchone()

        if not category:
            print("Category does not exist")
            continue 

        category_id = category[0]

        try:
            amount = float(input("Enter budget amount: "))
        except ValueError:
            print("Please enter a valid number")
            continue

        try:
            cursor.execute(
                f"INSERT INTO budgets(budget_amount, category_id, user_id, month) VALUES (?, ?, ?, ?)",
                (amount, category_id, user_id, month_year)
            )
            print("Budget added successfully")
        except:
            print("Budget already exists for this category")

    conn.commit()
    conn.close()
    return


def transaction_main(user_id):
    while True:
        budget_option_id, month_year = transaction_options(user_id)

        if budget_option_id == 1:
            add_transaction(user_id, month_year)
        elif budget_option_id == 2:
            delete_budget(user_id, month_year)
        else:
            return
            