# Overview
This project is about creating a budget management application that allows users to track transactions by category and generate personalizable budgets. 

# Features
There are 5 major features of this application.
- User Authentication
- Category Management
- Budget Management 
- Transaction Management
- Summary Statistics

# File Structure
- main.py - entry point that directs users to different features
- main_menu.py -  displays the main menu and allows users to navigate between application features
- config.py - contains all global configuration variables
- schema.sql - contains sql script that generates required tables and indexes if they do not exist already
- database_initalization.py - connects to the SQLite database and executes the SQL script to create database structure
- user.py - controls user authentication and generates new user_id in database if one does not exist
- category.py - handles category management, which includes viewing, adding, and deleting categories
- budget.py - handles budget management, which includes viewing, adding, and deleting budgets
- transactions.py - handles transactions management, which includes viewing, adding, and deleting transactions
- summary_statistics.py - generate monthly summar statistics for user spending

# Data Storage
All data is stored in a local budget_management_application.db SQLite database file that is automatically created when the application is first run. 

# How to run Budget Management Application 
If you do not have pip installed, please refer to this link and download pip based on your system: 

https://pip.pypa.io/en/stable/installation/

After installing pip, please follow the instructions:

Ensure that you are in the root project directory. From `dsci551_spring2026_final_project` directory run:

`pip install -r "requirements.txt"`

This first step will download all requirements required to run this application. Afterwards, run:

`python main.py`

This will run the budget management application! 