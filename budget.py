import sqlite3
from config import DATABASE
from tabulate import tabulate

def budget_options(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT b.budget_id, c.name AS category, b.amount
    FROM budgets b
    JOIN categories c ON b.category_id = c.category_id
    WHERE b.user_id = ?
    """, (user_id,))

    data = cursor.fetchall()

    if data:
        print("Here are your Budgets")
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers = columns, tablefmt = "grid"))
    else:
        print("\nYou do not have any budgets yet! Let's add some.\n")

    conn.close()

    print("Select an option")
    while True:
        budget_option_id = input("1: Add Budget\n2: Delete Budget\n3: Exit\n")
        if budget_option_id not in ("1", "2", "3"):
            print("Please enter a proper option")
            continue
        return int(budget_option_id)

def add_budget(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    while True:
        category_name = input("\nEnter category name for budget (or 'exit'): ")
        if category_name == "exit":
            break

        cursor.execute(
            "SELECT category_id FROM categories WHERE name = ? AND user_id = ?",
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
                "INSERT INTO budgets(amount, category_id, user_id) VALUES (?, ?, ?)",
                (amount, category_id, user_id)
            )
            print("Budget added successfully")
        except:
            print("Budget already exists for this category")

    conn.commit()
    conn.close()
    return

def delete_budget(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    while True:
        category_name = input("\nEnter category name to remove budget (or 'exit'): ")
        if category_name == "exit":
            break

        cursor.execute(
            "SELECT category_id FROM categories WHERE name = ? AND user_id = ?",
            (category_name, user_id)
        )
        category = cursor.fetchone()

        if not category:
            print("Category not found")
            continue

        category_id = category[0]

        cursor.execute(
            "DELETE FROM budgets WHERE category_id = ? AND user_id = ?",
            (category_id, user_id)
        )

        if cursor.rowcount == 0:
            print("No budget exists for that category")
        else:
            print("Budget deleted successfully")
    conn.commit()
    conn.close()
    return

def budget_main(user_id):
    while True:
        budget_option_id = budget_options(user_id)

        if budget_option_id == 1:
            add_budget(user_id)
        elif budget_option_id == 2:
            delete_budget(user_id)
        else:
            return
            
