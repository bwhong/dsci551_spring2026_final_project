from database_initialization import initialize_database
from user import ask_username, validate_user
from main_menu import main_menu_options
from category import category_main
from budget import budget_main
from transactions import transaction_main

if __name__ == "__main__":
    initialize_database()
    print('Welcome to the Budget Management Application!\n')
    username = ask_username()
    user_id = validate_user(username)
    while True:
        main_menu_id = main_menu_options()
        if main_menu_id == 1:
            category_main(user_id)
        elif main_menu_id == 2:
            budget_main(user_id)
        elif main_menu_id == 3: 
            transaction_main(user_id)
        elif main_menu_id == 4:
            break
            # show summary statistics 
        elif main_menu_id == 5:
            break