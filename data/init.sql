DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS secrets;

CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE secrets (
    id INTEGER PRIMARY KEY,
    secret_name TEXT NOT NULL,
    secret_value TEXT NOT NULL
);

INSERT INTO clients (id, name, email) VALUES
(1, 'Alice Johnson', 'alice@example.test'),
(2, 'Bob Smith', 'bob@example.test'),
(3, 'Carol White', 'carol@example.test');

INSERT INTO orders (id, client_id, product, amount) VALUES
(101, 1, 'Laptop', 1500.00),
(102, 1, 'Mouse', 50.00),
(103, 2, 'Monitor', 700.00),
(104, 3, 'Keyboard', 120.00);

INSERT INTO secrets (id, secret_name, secret_value) VALUES
(1, 'INTERNAL_API_KEY', 'demo_api_key_12345'),
(2, 'ADMIN_TOKEN', 'demo_admin_token_67890'),
(3, 'DB_PASSWORD', 'demo_db_password_abcde');