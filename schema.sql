CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY,
    amount DOUBLE NOT NULL,
    transaction_date DATE NOT NULL,
    category_id INT
);
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);