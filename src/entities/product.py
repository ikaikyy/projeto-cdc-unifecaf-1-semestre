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

from entities.category import Category


class Product:
    def __init__(
        self,
        id,
        name,
        description,
        price,
        available_on_stock,
        connection: mysql.connector.connection.MySQLConnection,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.available_on_stock = available_on_stock
        self.connection = connection

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', description='{self.description}', price={self.price}, available_on_stock={self.available_on_stock})"

    def as_dict(self, translate=False):
        if translate:
            return {
                "ID": self.id,
                "Nome": self.name,
                "Descrição": self.description,
                "Preço": self.price,
                "Disponível em estoque": self.available_on_stock,
            }
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available_on_stock": self.available_on_stock,
        }

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        products = []
        for row in rows:
            product = Product(row[0], row[1], row[2], row[3], row[4], connection)
            products.append(product)

        return products

    @staticmethod
    def get_by_id(product_id, connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        row = cursor.fetchone()
        if row:
            return Product(row[0], row[1], row[2], row[3], row[4], connection)
        else:
            return None

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO products (name, description, price, available_on_stock) VALUES (%s, %s, %s, %s)",
                (self.name, self.description, self.price, self.available_on_stock),
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE products SET name=%s, description=%s, price=%s, available_on_stock=%s WHERE id=%s",
                (
                    self.name,
                    self.description,
                    self.price,
                    self.available_on_stock,
                    self.id,
                ),
            )

        self.connection.commit()

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (self.id,))
        self.connection.commit()

    def add_category(self, category_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO products_categories (product_id, category_id) VALUES (%s, %s)",
            (self.id, category_id),
        )
        self.connection.commit()

    def clear_categories(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM products_categories WHERE product_id = %s",
            (self.id,),
        )
        self.connection.commit()

    def load_categories(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM categories INNER JOIN products_categories ON categories.id = products_categories.category_id WHERE products_categories.product_id=%s",
            (self.id,),
        )
        rows = cursor.fetchall()
        self.categories = []
        for row in rows:
            category = Category(row[0], row[1], self.connection)
            self.categories.append(category)
