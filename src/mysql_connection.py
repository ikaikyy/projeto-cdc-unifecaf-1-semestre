import mysql.connector


def new_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        init_command="USE ecommerce",
    )
