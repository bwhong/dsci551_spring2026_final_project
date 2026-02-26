CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS category (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT NOT NULL REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS budget (
    budget_id INT PRIMARY KEY,
    category_id INT REFERENCES category(category_id),
    budget_amount double NOT NULL,
    month DATE NOT NULL
    user_id INT NOT NULL REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY,
    amount DOUBLE NOT NULL,
    transaction_date DATE NOT NULL,
    category_id INT NOT NULL REFERENCES category(category_id),
    budget_id INT NOT NULL REFERENCES budget(budget_id), 
    user_id INT NOT NULL REFERENCES users(user_id)
);