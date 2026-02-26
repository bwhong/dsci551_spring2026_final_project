from database_initialization import initialize_database

if __name__ == "__main__":
    initialize_database()
    print('Welcome to the Budget Management Application!')
    input('Please enter your username! If your username does not exist, we will automatically create an account: \n')
    # check if username exists (lowercase and remove white space). if not, insert it into users table
    # press 1 to go to cateogry, press 2 to go to budget, press 3 to go to transactions, press 4 to go to summary statistics 
    # go to category and create categoryes -> create a default list (ex: press 1 to add/delete cateogires, press 2 to continue)
    # go to budget py file and create a budget based on categories for the month (ex: press 1 to add/delete budget, press 2 to continue)
    # go to transactions py file and add/delete/update a transation (display a list of transactions but filtered for x things)
    # show summary statistics 