CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    UNIQUE(user_id, category_name)
);

CREATE TABLE IF NOT EXISTS budgets (
    budget_id INTEGER PRIMARY KEY,
    category_id INTEGER REFERENCES categories(category_id),
    budget_amount double NOT NULL,
    month TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    UNIQUE(user_id, category_id, month)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    amount DOUBLE NOT NULL,
    transaction_date TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    budget_id INTEGER NOT NULL REFERENCES budgets(budget_id), 
    user_id INTEGER NOT NULL REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_transactions ON transactions(user_id, transaction_date)
