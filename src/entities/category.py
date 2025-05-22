# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(30),
# =============================================================================
# TABLE products_categories
# product_id INT,
# category_id INT,
# FOREIGN KEY (product_id) REFERENCES products(id),
# FOREIGN KEY (category_id) REFERENCES categories(id),

import mysql.connector


class Category:
    def __init__(self, id, name, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.name = name
        self.connection = connection

    def __str__(self):
        return f"Category(id={self.id}, name='{self.name}')"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        categories = []
        for row in rows:
            category = Category(row[0], row[1], connection)
            categories.append(category)

        return categories

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO categories (name) VALUES (%s)",
                (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE categories SET name=%s WHERE id=%s",
                (self.name, self.id))

        self.connection.commit()

    def load_products_categories(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM products_categories WHERE category_id=%s", (self.id))
        rows = cursor.fetchall()
        self.products_categories = rows
