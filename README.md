## Overview
This project is about creating a budget management application using Python and SQLite. The goal of the system is to allow users to manage their finances based on the categories they choose and the budget they decide. This allows for users to generate budgets that are reliable, user friendly, and easy for consumers. 

SQLite was chosen due to its minimal setup, quick indexes, and ACID-compliancy. Since SQLite stores everything on a single local file, it is extremely portable, and it allows easy data transfer. It stores all its tables as B-Trees, which allows for extremely fast and efficient queries. It is the perfect relational database for this project. 

# How to run Budget Management Application 
If you do not have pip installed, please refer to this link and download pip based on your system: 

https://pip.pypa.io/en/stable/installation/

After installing pip, please follow the instructions:

From `dsci551_spring2026_final_project` directory run:

`pip install -r "requirements.txt"`

This first step will download all requirements required to run this application. Afterwards, run:

`python main.py`

This will run the budget management application! 