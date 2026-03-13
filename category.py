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
        print("You don't have any categories yet! Let's add some.")
    print('Please select an option!')
    while True:
        category_options_id = input("1: Add Category \n2: Delete Category \n")
        if category_options_id not in ("1","2"):
            print('Please enter a proper option.')
            continue
        category_options = int(category_options)
        return category_options

def add_category(user_id):
    ###




def category_main(user_id):
    if category_options(user_id) == 1:
        