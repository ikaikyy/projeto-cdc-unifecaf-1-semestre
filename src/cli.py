from mysql_connection import new_mysql_connection

from entities.user import User
from entities.product import Product


def register_user():
    try:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone_number = input("Enter your phone number: ")
        cpf = input("Enter your CPF: ")
    except TypeError:
        print("There's an error on the values you've provided, please insert valid values")

    connection = new_mysql_connection()
    user = User(0, name, email, phone_number, cpf, connection)
    user.save()

    print(f"User {name} registered successfully!")


def register_product():
    try:
        name = input("Enter the product's name: ")
        description = input("Enter the product's description: ")
        price = float(input("Enter the product's price: "))
        available_on_stock = int(input(
            "Enter the product's qauntity available on stock: "))
    except TypeError:
        print("There's an error on the values you've provided, please insert valid values")

    connection = new_mysql_connection()
    product = Product(0, name, description, price,
                      available_on_stock, connection)
    product.save()


def main():
    while True:
        print("Welcome to the CLI interface!")
        print("1. Register User")
        print("2. Register Product")
        print("3. Place Order")
        print("4. Exit")

        choice = input("Please enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            register_product()
        elif choice == "3":
            print("Placing Order...")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
