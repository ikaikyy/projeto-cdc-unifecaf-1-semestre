# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR (100) NOT NULL,
# email VARCHAR (255) NOT NULL UNIQUE,
# phone_number VARCHAR (20) NOT NULL UNIQUE,
# cpf VARCHAR (11) NOT NULL UNIQUE,

import mysql.connector


class User:
    def __init__(self, id, name, email, phone_number, cpf, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.cpf = cpf
        self.connection = connection

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', phone_number='{self.phone_number}', cpf='{self.cpf}')"

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO users (name, email, phone_number, cpf) VALUES (%s, %s, %s, %s)",
                (self.name, self.email, self.phone_number, self.cpf))
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE users SET name=%s, email=%s, phone_number=%s, cpf=%s WHERE id=%s",
                (self.name, self.email, self.phone_number, self.cpf, self.id))

        self.connection.commit()

    def load_addresses(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM addresses WHERE user_id=%s", (self.id))
        rows = cursor.fetchall()
        self.addresses = rows

    def load_orders(self):
        if self.id == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE user_id=%s", (self.id))
        rows = cursor.fetchall()
        self.orders = rows
