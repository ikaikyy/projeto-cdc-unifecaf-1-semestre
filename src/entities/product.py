# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(100) NOT NULL,
# description VARCHAR(255) NOT NULL,
# price DECIMAL(10,2) NOT NULL,
# available_on_stock INT NOT NULL,
# =============================================================================
# TABLE products_categories
# product_id INT,
# category_id INT,
# FOREIGN KEY (product_id) REFERENCES products(id),
# FOREIGN KEY (category_id) REFERENCES categories(id),
# ==============================================================================
# TABLE orders_products
# quantity INT NOT NULL,
# order_id INT,
# product_id INT,
# FOREIGN KEY (order_id) REFERENCES orders(id),
# FOREIGN KEY (product_id) REFERENCES products(id),

import mysql.connector


class Product:
    def __init__(self, id, name, description, price, available_on_stock, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.available_on_stock = available_on_stock
        self.connection = connection

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', description='{self.description}', price={self.price}, available_on_stock={self.available_on_stock})"

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        products = []
        for row in rows:
            product = Product(row[0], row[1], row[2],
                              row[3], row[4], connection)
            products.append(product)

        return rows

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO products (name, description, price, available_on_stock) VALUES (%s, %s, %s, %s)",
                (self.name, self.description, self.price, self.available_on_stock))
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE products SET name=%s, description=%s, price=%s, available_on_stock=%s WHERE id=%s",
                (self.name, self.description, self.price, self.available_on_stock, self.id))

        self.connection.commit()

    def load_products_categories(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM products_categories WHERE product_id=%s", (self.id))
        rows = cursor.fetchall()
        self.products_categories = rows
