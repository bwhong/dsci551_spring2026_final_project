import sqlite3
import os
from config import DATABASE

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    
