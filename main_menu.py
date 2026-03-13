def main_menu_options():
    while True:
        print('Please select an option from the main menu!')
        menu_id = input("1: Category \n2: Budget \n3: Transactions \n4: Summary Statistics\n")
        if menu_id not in ("1","2","3","4"):
            print('Please enter a proper option.')
            continue
        menu_id = int(menu_id)
        return menu_id