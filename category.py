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
        category_options_id = input("1: Add Category \n2: Delete Category\n3: Exit\n")
        if category_options_id not in ("1","2","3"):
            print('Please enter a proper option.')
            continue
        category_options_id = int(category_options_id)
        return category_options_id

def add_category(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    while True:
        category_name = input("\nPlease input a category name to add! Input 'exit' if you want to leave. \n")
        if category_name == 'exit':
            break
        try:
            cursor.execute("INSERT INTO categories(category_name, user_id) values(?,?)", (category_name, user_id))
        except:
            print(f'{category_name} already exists.')
    #commit changes        
    conn.commit()
    conn.close()
    return

def delete_category(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    while True:
        category_name = input("\nPlease input a category name to delete! Input 'exit' if you want to leave. \n")
        if category_name == 'exit':
            break
        try:
            cursor.execute("DELETE FROM categories where category_name = ? and user_id = ?", (category_name, user_id))
        except:
            print(f'{category_name} is referenced in other tables. {category_name} cannot be removed.')
    #commit changes        
    conn.commit()
    conn.close()
    return

def category_main(user_id):
    while True:
        category_options_id = category_options(user_id)
        if category_options_id == 1:
            add_category(user_id)
        elif category_options_id == 2:
            delete_category(user_id)
        else:
            return
    