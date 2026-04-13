#Imports
import sqlite3
from config import DATABASE
from tabulate import tabulate
from datetime import datetime

def budget_options(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;") 
    cursor = conn.cursor()

    cursor.execute("""
    SELECT b.budget_id, c.category_name AS category, b.budget_amount
    FROM budgets b
    JOIN categories c ON b.category_id = c.category_id
    WHERE b.user_id = ? and b.month =?
    """, (user_id, month_year))

    data = cursor.fetchall()

    if data:
        print("\nHere are your set budgets for the month")
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers = columns, tablefmt = "grid"))
    else:
        print("\nYou do not have any budgets yet! Let's add some.")

    conn.close()

    print("\nSelect an option")
    while True:
        budget_option_id = input("1: Add Budget\n2: Delete Budget\n3: Exit\n")
        if budget_option_id not in ("1", "2", "3"):
            print("Please enter a proper option")
            continue
        return int(budget_option_id), month_year

def add_budget(user_id, month_year):
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
            print("\nCategory does not exist")
            continue 

        category_id = category[0]

        try:
            amount = float(input("Enter budget amount: "))
            if amount < 0:
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid number")
            continue

        try:
            cursor.execute(
                f"INSERT INTO budgets(budget_amount, category_id, user_id, month) VALUES (?, ?, ?, ?)",
                (amount, category_id, user_id, month_year)
            )
            print("Budget added successfully")
        except:
            print("\nBudget already exists.")

    conn.commit()
    conn.close()
    return

def delete_budget(user_id, month_year):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;") 
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
        
        category_name = input("\nEnter category name to remove budget (or 'exit'): ")
        if category_name == "exit":
            break

        cursor.execute(
            "SELECT category_id FROM categories WHERE category_name = ? AND user_id = ?",
            (category_name, user_id)
        )
        category = cursor.fetchone()
        
        if not category:
            print("\nCategory does not exist")
            continue

        category_id = category[0]

        try:
            cursor.execute(
                "DELETE FROM budgets WHERE category_id = ? AND user_id = ? and month = ?",
                (category_id, user_id, month_year)
            )
            if cursor.rowcount == 0:
                print("\nNo budget exists for that category")
            else:
                print("Budget deleted successfully")
        except:
            print(f'{category_name} is referenced in other tables. {category_name} cannot be removed.')

    conn.commit()
    conn.close()
    return

def budget_main(user_id):
    while True:
        month_year = input("\nEnter Month and Year (YYYY-MM) for Budgets (or 'exit'):")
        if month_year == 'exit':
            print()
            break
        try:
            datetime.strptime(month_year, "%Y-%m")
        except ValueError:
            print('Please enter a valid date!')
            continue

        budget_option_id, month_year = budget_options(user_id, month_year)

        if budget_option_id == 1:
            add_budget(user_id, month_year)
        elif budget_option_id == 2:
            delete_budget(user_id, month_year)
        else:
            return
            
