DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE ecommerce;
USE ecommerce;

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    email VARCHAR (255) NOT NULL UNIQUE,
    phone_number VARCHAR (20) NOT NULL UNIQUE,
    cpf VARCHAR (11) NOT NULL UNIQUE
);

CREATE TABLE addresses (
	id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR (30) NOT NULL,
    city VARCHAR (64) NOT NULL,
    cep VARCHAR (8) NOT NULL,
    1st_line VARCHAR (100) NOT NULL,
    2nd_line VARCHAR (100),
    3rd_line VARCHAR (100),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    description VARCHAR (255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    available_on_stock INT NOT NULL
);

CREATE TABLE carts (
	id INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE orders (
	id INT AUTO_INCREMENT PRIMARY KEY,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP,
    user_id INT,
    address_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);

CREATE TABLE orders_products (
	quantity INT NOT NULL,
    order_id INT,
    product_id INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE carts_products (
	quantity INT NOT NULL,
    product_id INT,
    cart_id INT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (cart_id) REFERENCES carts(id)
);

CREATE TABLE categories (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (30)
);

CREATE TABLE products_categories (
	product_id INT,
    category_id INT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
