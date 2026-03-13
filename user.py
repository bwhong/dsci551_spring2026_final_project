import sqlite3
import os
from config import DATABASE

def ask_username():
    while True:
        username = input('Please enter your username! If your username does not exist, we will automatically create an account (Alphanumeric Characters and uppercase only!): \n')
        if not username.isalnum():
            print("\nPlease only use Alphanumeric Characters! \n")
            continue
        cleaned_username = str(username).strip().upper()
        return cleaned_username

def validate_user(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users where user_name = (?)", (username,))
    data = cursor.fetchall()
    if data:
        print(f'Welcome back {username}!')
    else:
        print(f"Creating a new user account. Welcome {username}!")
        cursor.execute("INSERT INTO users(user_name) values(?)", (username,))
    conn.commit()
    conn.close()
    return data
