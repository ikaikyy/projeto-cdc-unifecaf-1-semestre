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


class Cart:
    def __init__(self, id, user_id, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.user_id = user_id
        self.connection = connection

    def __str__(self):
        return f"Cart(id={self.id}, user_id={self.user_id})"

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

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

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute("INSERT INTO carts () VALUES ()")
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE carts SET  WHERE id=%s", (self.id,))

        self.connection.commit()

    def load_products(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM carts_products WHERE cart_id=%s", (self.id))
        rows = cursor.fetchall()
        self.products = rows

    def load_user(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id=%s", (self.user_id))
        row = cursor.fetchone()
        self.user = row
