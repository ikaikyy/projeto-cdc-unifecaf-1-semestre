CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
    is_admin BOOLEAN NOT NULL DEFAULT (FALSE),
    name VARCHAR (100) NOT NULL,
    email VARCHAR (255) NOT NULL UNIQUE,
    phone_number VARCHAR (20) NOT NULL UNIQUE,
    cpf VARCHAR (11) NOT NULL UNIQUE
);

CREATE TABLE carts (
	id INT AUTO_INCREMENT PRIMARY KEY
);

ALTER TABLE users ADD COLUMN cart_id INT;
ALTER TABLE users ADD CONSTRAINT FOREIGN KEY (cart_id) REFERENCES cart(id);

CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    description VARCHAR (255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    available_on_stock INT NOT NULL
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
