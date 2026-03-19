from database_initialization import initialize_database
from user import ask_username, validate_user
from main_menu import main_menu_options
from category import category_main
from budget import budget_main

if __name__ == "__main__":
    initialize_database()
    print('Welcome to the Budget Management Application!\n')
    username = ask_username()
    user_id = validate_user(username)
    main_menu_id = main_menu_options()
    if main_menu_id == 1:
        category_main(user_id)
        # go to category and create categories -> create a default list (ex: press 1 to add/delete cateogires, press 2 to continue)
    elif main_menu_id == 2:
        budget_main(user_id)
    #elif main_menu_id == 3: 
        # go to transactions py file and add/delete/update a transation (display a list of transactions but filtered for x things)
    #elif main_menu_id == 4:    
        # show summary statistics 