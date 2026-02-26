from database_initialization import initialize_database

if __name__ == "__main__":
    initialize_database()
    print('Welcome to the Budget Management Application!')
    input('Please enter your username! If your username does not exist, we will automatically create an account: \n')
    