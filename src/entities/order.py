# id INT AUTO_INCREMENT PRIMARY KEY,
# total_price DECIMAL(10,2) NOT NULL,
# created_at TIMESTAMP,
# user_id INT,
# address_id INT,
# FOREIGN KEY (user_id) REFERENCES users(id),
# FOREIGN KEY (address_id) REFERENCES addresses(id),
# ==============================================================================
# TABLE orders_products
# quantity INT NOT NULL,
# order_id INT,
# product_id INT,
# FOREIGN KEY (order_id) REFERENCES orders(id),
# FOREIGN KEY (product_id) REFERENCES products(id),

import mysql.connector


class Order:
    def __init__(self, id, total_price, created_at, user_id, address_id, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.total_price = total_price
        self.created_at = created_at
        self.user_id = user_id
        self.address_id = address_id
        self.connection = connection

    def __str__(self):
        return f"Order(id={self.id}, total_price={self.total_price}, created_at='{self.created_at}', user_id={self.user_id}, address_id={self.address_id})"

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        return rows

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO orders (total_price, created_at, user_id, address_id) VALUES (%s, %s, %s, %s)",
                (self.total_price, self.created_at, self.user_id, self.address_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE orders SET total_price=%s, created_at=%s, user_id=%s, address_id=%s WHERE id=%s",
                (self.total_price, self.created_at, self.user_id, self.address_id, self.id))

        self.connection.commit()

    def load_user(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id=%s", (self.user_id))
        row = cursor.fetchone()
        self.user = row

    def load_address(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM addresses WHERE id=%s", (self.address_id))
        row = cursor.fetchone()
        self.address = row

    def load_orders_products(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders_products WHERE order_id=%s", (self.id))
        rows = cursor.fetchall()
        self.orders_products = rows
