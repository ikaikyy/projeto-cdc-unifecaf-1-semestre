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

from entities.address import Address
from entities.product import Product
from entities.user import User


class Order:
    def __init__(
        self,
        id,
        total_price,
        user_id,
        address_id,
        connection: mysql.connector.connection.MySQLConnection,
        created_at=None,
    ):
        self.id = id
        self.total_price = total_price
        self.user_id = user_id
        self.address_id = address_id
        self.connection = connection
        self.created_at = created_at

    def __str__(self):
        return f"Order(id={self.id}, total_price={self.total_price}, created_at='{self.created_at}', user_id={self.user_id}, address_id={self.address_id})"

    def as_dict(self, translate=False):
        if translate:
            return {
                "ID": self.id,
                "Preço Total": self.total_price,
                "Criado em": self.created_at,
                "ID do usuário": self.user_id,
                "ID do endereço": self.address_id,
            }

        return {
            "id": self.id,
            "total_price": self.total_price,
            "created_at": self.created_at,
            "user_id": self.user_id,
            "address_id": self.address_id,
        }

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            order = Order(row[0], row[1], row[3], row[4], connection, row[2])
            orders.append(order)

        return orders

    @staticmethod
    def get_by_id(order_id, connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
        row = cursor.fetchone()
        if row:
            return Order(row[0], row[1], row[2], row[3], row[4], connection)
        else:
            return None

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO orders (total_price, created_at, user_id, address_id) VALUES (%s, NOW(), %s, %s)",
                (self.total_price, self.user_id, self.address_id),
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE orders SET total_price=%s, user_id=%s, address_id=%s WHERE id=%s",
                (
                    self.total_price,
                    self.user_id,
                    self.address_id,
                    self.id,
                ),
            )

        self.connection.commit()

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM orders WHERE id=%s", (self.id,))
        self.connection.commit()

    def add_product(self, product_id, quantity):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO orders_products (quantity, order_id, product_id) VALUES (%s, %s, %s)",
            (quantity, self.id, product_id),
        )
        self.connection.commit()

    def load_user(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (self.user_id,))
        row = cursor.fetchone()
        self.user = User(row[0], row[1], row[2], row[3], row[4], self.connection)

    def load_address(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE id=%s", (self.address_id,))
        row = cursor.fetchone()
        self.address = Address(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            self.connection,
        )

    def load_products(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT quantity, product_id FROM orders_products WHERE order_id=%s",
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
