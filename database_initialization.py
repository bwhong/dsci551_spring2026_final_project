import sqlite3
import os
from config import DATABASE

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    conn.cursor()
    with open("schema.sql", "r") as f:
        table_sql_setup = f.read()
    conn.executescript(table_sql_setup)
    conn.commit()
    conn.close()
    
