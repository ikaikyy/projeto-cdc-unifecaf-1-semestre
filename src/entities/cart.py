# id INT AUTO_INCREMENT PRIMARY KEY,
# user_id INT,
# FOREIGN KEY (user_id) REFERENCES users(id),
# =============================================================================
# TABLE carts_products
# quantity INT NOT NULL,
# product_id INT,
# cart_id INT,
# FOREIGN KEY (product_id) REFERENCES products(id),
# FOREIGN KEY (cart_id) REFERENCES carts(id)

import mysql.connector

from entities.product import Product


class Cart:
    def __init__(
        self, id, user_id, connection: mysql.connector.connection.MySQLConnection
    ):
        self.id = id
        self.user_id = user_id
        self.connection = connection

    def __str__(self):
        return f"Cart(id={self.id}, user_id={self.user_id})"

    def as_dict(self, translate=False):
        if translate:
            return {"ID": self.id, "ID do usuário": self.user_id}

        return {"id": self.id, "user_id": self.user_id}

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM carts")
        rows = cursor.fetchall()
        carts = []
        for row in rows:
            cart = Cart(row[0], row[1], connection)
            carts.append(cart)

        return carts

    @staticmethod
    def get_by_id(cart_id, connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM carts WHERE id=%s", (cart_id,))
        row = cursor.fetchone()
        if row:
            return Cart(row[0], row[1], connection)
        return None

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute("INSERT INTO carts (user_id) VALUES (%s)", (self.user_id,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE carts SET  WHERE id=%s", (self.id,))

        self.connection.commit()

    def clear(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM carts_products WHERE cart_id=%s", (self.id,))
        self.connection.commit()

        if hasattr(self, "products"):
            self.products = []

    def load_products(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT quantity, product_id FROM carts_products WHERE cart_id=%s",
            (self.id,),
        )
        rows = cursor.fetchall()
        self.products = []
        for row in rows:
            product_id = row[1]
            product = Product.get_by_id(product_id, self.connection)
            if product:
                product.quantity = row[0]
                self.products.append(product)

    def load_user(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (self.user_id))
        row = cursor.fetchone()
        self.user = row

    def has_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM carts_products WHERE cart_id=%s AND product_id=%s",
            (self.id, product_id),
        )
        row = cursor.fetchone()
        return row is not None

    def add_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO carts_products (cart_id, product_id, quantity) VALUES (%s, %s, 1)",
            (self.id, product_id),
        )
        self.connection.commit()

        if hasattr(self, "products"):
            product = Product.get_by_id(product_id, self.connection)
            product.quantity = 1
            self.products.append(product)
        else:
            self.load_products()

    def update_product_quantity(self, product_id, quantity):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE carts_products SET quantity=%s WHERE cart_id=%s AND product_id=%s",
            (quantity, self.id, product_id),
        )
        self.connection.commit()

        for product in self.products:
            if product.id == product_id:
                product.quantity = quantity
                break
