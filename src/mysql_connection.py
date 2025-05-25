import mysql.connector


def new_mysql_connection(no_init_command=False):
    if no_init_command:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
        )

    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        init_command="USE ecommerce",
    )
