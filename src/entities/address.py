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
