# id INT AUTO_INCREMENT PRIMARY KEY,
# state VARCHAR(30) NOT NULL,
# city VARCHAR(64) NOT NULL,
# cep VARCHAR(8) NOT NULL,
# 1st_line VARCHAR(100) NOT NULL,
# 2nd_line VARCHAR(100),
# 3rd_line VARCHAR(100),
# user_id INT,
# FOREIGN KEY (user_id) REFERENCES users(id),

import mysql.connector


class Address:
    def __init__(self, id, state, city, cep, first_line, second_line, third_line, user_id, connection: mysql.connector.connection.MySQLConnection):
        self.id = id
        self.state = state
        self.city = city
        self.cep = cep
        self.first_line = first_line
        self.second_line = second_line
        self.third_line = third_line
        self.user_id = user_id
        self.connection = connection

    def __str__(self):
        return f"Address(id={self.id}, state='{self.state}', city='{self.city}', cep='{self.cep}', first_line='{self.first_line}', second_line='{self.second_line}', third_line='{self.third_line}', user_id={self.user_id})"

    def as_dict(self, translate=False):
        if translate:
            return {
                "ID": self.id,
                "Estado": self.state,
                "Cidade": self.city,
                "CEP": self.cep,
                "Logradouro": self.first_line,
                "Complemento": self.second_line,
                "Bairro": self.third_line,
                "ID do usuário": self.user_id
            }

        return {
            "id": self.id,
            "state": self.state,
            "city": self.city,
            "cep": self.cep,
            "first_line": self.first_line,
            "second_line": self.second_line,
            "third_line": self.third_line,
            "user_id": self.user_id
        }

    @staticmethod
    def list_all(connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM addresses")
        rows = cursor.fetchall()
        addresses = []
        for row in rows:
            address = Address(row[0], row[1], row[2], row[3],
                              row[4], row[5], row[6], row[7], connection)
            addresses.append(address)

        return addresses

    @staticmethod
    def get_by_id(address_id, connection: mysql.connector.connection.MySQLConnection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM addresses WHERE id=%s", (address_id,))
        row = cursor.fetchone()
        if row:
            return Address(row[0], row[1], row[2], row[3],
                           row[4], row[5], row[6], row[7], connection)
        return None

    def save(self):
        cursor = self.connection.cursor()

        if self.id == 0:
            cursor.execute(
                "INSERT INTO addresses (state, city, cep, 1st_line, 2nd_line, 3rd_line, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (self.state, self.city, self.cep, self.first_line, self.second_line, self.third_line, self.user_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE addresses SET state=%s, city=%s, cep=%s, 1st_line=%s, 2nd_line=%s, 3rd_line=%s WHERE id=%s",
                (self.state, self.city, self.cep,
                 self.first_line,
                 self.second_line,
                 self.third_line,
                 self.id))

        self.connection.commit()

    def load_user(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id=%s", (self.user_id))
        row = cursor.fetchone()
        self.user = row
