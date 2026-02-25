CREATE TABLE IF NOT EXISTS user (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL;
    budget_total DOUBLE NOT NULL;
    spent_total DOUBLE NOT NULL
)

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY,
    amount DOUBLE NOT NULL,
    transaction_date DATE NOT NULL,
    category_id INT NOT NULL,
    budget_id INT NOT NULL, 
    user_id INT NOT NULL,
    FOREIGN KEY user_id REFERENCES user(user_id),
    FOREIGN KEY category_id REFERENCES categories(category_id),
    FOREIGN KEY budget_id REFERENCES budget(budget_id)

);
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY user_id REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS budget (
    budget_id INT PRIMARY KEY,
    category_id INT,
    budget_amount double NOT NULL,
    month DATE NOT NULL
    user_id INT NOT NULL,
    FOREIGN KEY user_id REFERENCES user(user_id)
    FOREIGN KEY category_id REFERENCES categories(category_id)
)