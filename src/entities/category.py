# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(30),

import mysql.connector


class Category:
    def __init__(self, id, name, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.name = name
        self.connection = connection

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
