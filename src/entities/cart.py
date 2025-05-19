# id INT AUTO_INCREMENT PRIMARY KEY,
# =============================================================================
# TABLE carts_products
# quantity INT NOT NULL,
# product_id INT,
# cart_id INT,
# FOREIGN KEY (product_id) REFERENCES products(id),
# FOREIGN KEY (cart_id) REFERENCES carts(id)

import mysql.connector


class Cart:
    def __init__(self, id, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.connection = connection

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute("INSERT INTO carts () VALUES ()")
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE carts SET  WHERE id=%s", (self.id,))

        self.connection.commit()

    def load_carts_products(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM carts_products WHERE cart_id=%s", (self.id))
        rows = cursor.fetchall()
        return rows
