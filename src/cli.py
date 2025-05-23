from mysql_connection import new_mysql_connection

from entities.user import User
from entities.product import Product
from entities.category import Category


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


def list_users():
    connection = new_mysql_connection()
    users = User.list_all(connection)
    for user in users:
        print(user)


def register_category():
    try:
        name = input("Enter the category's name: ")
    except TypeError:
        print("There's an error on the values you've provided, please insert valid values")

    connection = new_mysql_connection()
    category = Category(0, name, connection)
    category.save()

    print(f"Category {name} registered successfully!")


def list_categories():
    connection = new_mysql_connection()
    categories = Category.list_all(connection)
    for category in categories:
        print(category)


def register_product():
    try:
        name = input("Enter the product's name: ")
        description = input("Enter the product's description: ")
        categories = input(
            "Enter the product's categories (ex: 1,2,3,4): ").split(",")
        price = float(input("Enter the product's price: "))
        available_on_stock = int(input(
            "Enter the product's quantity available on stock: "))
    except TypeError:
        print("There's an error on the values you've provided, please insert valid values")

    connection = new_mysql_connection()
    product = Product(0, name, description, price,
                      available_on_stock, connection)
    product.save()


def list_products():
    connection = new_mysql_connection()
    products = Product.list_all(connection)
    for product in products:
        print(product)


def main():
    while True:
        print("Welcome to the CLI!")
        print("1. Users")
        print("2. Products")
        print("3. Orders")
        print("4. Exit")

        choice = input("Please enter your choice: ")

        if choice == "4":
            print("Exiting the CLI. Goodbye!")
            break

        print("1. Register")
        print("2. List")
        print("3. Back")

        action = input("Please enter your action: ")

        if choice == "1":
            if action == "1":
                register_user()
            elif action == "2":
                list_users()
        elif choice == "2":
            if action == "1":
                register_product()
            elif action == "2":
                list_products()
        elif choice == "3":
            print("Orders functionality is not implemented yet.")
        else:
            print("Invalid choice, please try again.")
