import sqlite3
import os
from config import DATABASE
from tabulate import tabulate

def category_options(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories where user_id = (?)", (user_id,))
    data = cursor.fetchall()
    if data:
        print('Here are your Categories!')
        columns = [name[0] for name in cursor.description]
        print(tabulate(data, headers=columns, tablefmt="grid"))
    else:
        print("\nYou don't have any categories yet! Let's add some.\n")
    print('Please select an option!')
    while True:
        category_options_id = input("1: Add Category \n2: Delete Category \n")
        if category_options_id not in ("1","2"):
            print('Please enter a proper option.')
            continue
        category_options_id = int(category_options_id)
        return category_options_id

def add_category(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    category_name = input("\nPlease input a category name!\n")
    try:
        cursor.execute("INSERT INTO categories(name, user_id) values(?,?)", (category_name, user_id))
    except:
        print('test')
    conn.commit()
    conn.close()
    return

def delete_category(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

def category_main(user_id):
    category_options_id = category_options(user_id)
    if category_options_id == 1:
        add_category(user_id)
    elif category_options_id == 2:
        delete_category(user_id)