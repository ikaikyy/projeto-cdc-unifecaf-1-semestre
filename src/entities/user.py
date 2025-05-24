# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR (100) NOT NULL,
# email VARCHAR (255) NOT NULL UNIQUE,
# phone_number VARCHAR (20) NOT NULL UNIQUE,
# cpf VARCHAR (11) NOT NULL UNIQUE,

import mysql.connector

from entities.address import Address
from entities.cart import Cart


class User:
    def __init__(
        self,
        id,
        name,
        email,
        phone_number,
        cpf,
        connection: mysql.connector.connection.MySQLConnection,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.cpf = cpf
        self.connection = connection

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', phone_number='{self.phone_number}', cpf='{self.cpf}')"

    def as_dict(self, translate=False):
        if translate:
            return {
                "ID": self.id,
                "Nome": self.name,
                "Email": self.email,
                "Telefone": self.phone_number,
                "CPF": self.cpf,
            }

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "cpf": self.cpf,
        }

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        users = []
        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4], connection)
            users.append(user)

        return users

    @staticmethod
    def get_by_id(user_id, connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4], connection)
        else:
            return None

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO users (name, email, phone_number, cpf) VALUES (%s, %s, %s, %s)",
                (self.name, self.email, self.phone_number, self.cpf),
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE users SET name=%s, email=%s, phone_number=%s, cpf=%s WHERE id=%s",
                (self.name, self.email, self.phone_number, self.cpf, self.id),
            )

        self.connection.commit()

    def load_addresses(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE user_id=%s", (self.id,))
        rows = cursor.fetchall()
        self.addresses = []
        for row in rows:
            address = Address(
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
            self.addresses.append(address)

    def load_cart(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM carts WHERE user_id=%s", (self.id,))
        row = cursor.fetchone()
        if row is None:
            self.cart = Cart(0, self.id, self.connection)
            self.cart.save()
            return
        self.cart = Cart(row[0], row[1], self.connection)
        self.cart.load_products()
