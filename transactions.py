import sqlite3
from config import DATABASE
from tabulate import tabulate
from datetime import datetime
from dateutil.relativedelta import relativedelta

def transaction_options(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;") 
    cursor = conn.cursor()

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
        print("\nHere are your last 10 transactions of the month")
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers = columns, tablefmt = "grid"))
    else:
        print("\nYou do not have any transactions yet! Let's add some.\n")

    conn.close()

    print("\nSelect an option")
    while True:
        transaction_option_id = input("1: Add Transaction\n2: Delete Transaction\n3: Exit\n")
        if transaction_option_id not in ("1", "2", "3"):
            print("Please enter a proper option")
            continue
        return int(transaction_option_id), month_year

def add_transaction(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;") 
    cursor = conn.cursor()

    while True:
        #show transactions
        cursor.execute("""
        SELECT t.transaction_id, t.amount, c.category_name, t.transaction_date
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = ? and t.transaction_date >= ? || '-01' AND t.transaction_date < date(? || '-01', '+1 month')
        ORDER BY t.transaction_date desc
        """, (user_id, month_year, month_year))
        data = cursor.fetchall()
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers=columns, tablefmt="grid"))

        print()

        #get category id
        cursor.execute("""
            SELECT category_name
            FROM categories
            where user_id = ?
            """, (user_id, ))
        data = cursor.fetchall()
        if not data:
            print('Please enter a category first!')
            break
        print('\nHere are your Categories!\n')
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers = columns, tablefmt = "grid"))
        print()
        try:
            category_name = input("Enter category name (or 'exit'): ")
            if category_name  == "exit":
                break
            else:
                cursor.execute("""
                    SELECT category_id
                    FROM categories
                    where user_id = ? and category_name = ?
                    """, (user_id, category_name))
                category_id = cursor.fetchall()[0][0]
        except:
            print('Please enter a valid category name!')
            continue

        #get budget id
        cursor.execute("""
            SELECT budget_id
            FROM budgets
            where user_id = ? and category_id = ? and month = ?
            """, (user_id, category_id, month_year))
        data = cursor.fetchall()
        if not data:
            print('Please enter a budget first!')
            continue
        else:
            budget_id = data[0][0]

        #get transaction amount
        try:
            transaction_amount = input("Enter transaction amount (or 'exit'): ")
            if transaction_amount == "exit":
                break
            else:
                transaction_amount = float(transaction_amount)
        except ValueError:
            print("Please enter a valid amount")
            continue

        #get transaction date
        try:
            transaction_date = datetime.strptime(input("Enter transaction date (YYYY-MM-DD): "), "%Y-%m-%d")
            if not (datetime.strptime(month_year, '%Y-%m') + relativedelta(months=1)) > transaction_date >= datetime.strptime(month_year, '%Y-%m'):
                raise ValueError
        except ValueError:
            print("Please enter a valid date")
            continue

        try:
            cursor.execute(
                f"INSERT INTO transactions(amount, transaction_date, category_id, budget_id, user_id) VALUES (?, ?, ?, ?, ?)",
                (transaction_amount, transaction_date, category_id, budget_id, user_id)
            )
            print("Transaction added successfully")
        except:
            print("Transaction already exists! ")

    conn.commit()
    conn.close()
    return

def delete_transaction(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;") 
    cursor = conn.cursor()
    while True:
        #show transactions
        cursor.execute("""
        SELECT t.transaction_id, t.amount, c.category_name, t.transaction_date
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = ? and t.transaction_date >= ? || '-01' AND t.transaction_date < date(? || '-01', '+1 month')
        ORDER BY t.transaction_date desc
        """, (user_id, month_year, month_year))
        data = cursor.fetchall()
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers=columns, tablefmt="grid"))
        try:
            transaction_id = input("\nEnter transaction id to delete (or 'exit'): ")
            if transaction_id == "exit":
                break
            else:
                transaction_id = int(transaction_id)
        except ValueError:
            print('Please enter a proper transaction id.')

        cursor.execute(
            "SELECT transaction_id FROM transactions WHERE transaction_id = ? AND user_id = ?",
            (transaction_id, user_id)
        )
        transaction = cursor.fetchone()

        if not transaction:
            print("Transaction not found")
            continue
        try:
            cursor.execute(
                "DELETE FROM transactions WHERE transaction_id = ?",
                (transaction_id,)
            )
            print('Transaction successfully deleted!')
        except:
            print('This transaction id does not exist.')
    conn.commit()
    conn.close()
    return

def transaction_main(user_id):
    while True:
        month_year = input("\nEnter Month and Year (YYYY-MM) for Transactions (or 'exit'):")
        if month_year == 'exit':
            print()
            break
        try:
            datetime.strptime(month_year, "%Y-%m")
        except ValueError:
            print('Please enter a valid date!')

        budget_option_id, month_year = transaction_options(user_id, month_year)

        if budget_option_id == 1:
            add_transaction(user_id, month_year)
        elif budget_option_id == 2:
            delete_transaction(user_id, month_year)
        else:
            return
            