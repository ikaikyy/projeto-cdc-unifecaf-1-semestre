from entities.address import Address
from entities.category import Category
from entities.product import Product
from entities.user import User
from mysql_connection import new_mysql_connection


def list_users():
    connection = new_mysql_connection()
    users = User.list_all(connection)
    for user in users:
        print(user)


def register_user():
    try:
        name = input("Enter the user's name: ")
        email = input("Enter the user's email: ")
        phone_number = input("Enter the user's phone number: ")
        cpf = input("Enter the user's CPF: ")
    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    user = User(0, name, email, phone_number, cpf, connection)
    user.save()

    print(f"User {name} registered successfully!")


def update_user():
    try:
        user_id = int(input("Enter the user's ID: "))
    except ValueError:
        print("Invalid user ID. Please enter a valid integer.")
        return

    connection = new_mysql_connection()
    user = User.get_by_id(user_id, connection)

    try:
        name = input(f"Enter the new name ({user.name}): ")
        email = input(f"Enter the new email ({user.email}): ")
        phone_number = input(f"Enter the new phone number ({user.phone_number}): ")
        cpf = input(f"Enter the new CPF ({user.cpf}): ")
    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    if name:
        user.name = name
    if email:
        user.email = email
    if phone_number:
        user.phone_number = phone_number
    if cpf:
        user.cpf = cpf
    user.save()

    print(f"User {name} updated successfully!")


def list_categories():
    connection = new_mysql_connection()
    categories = Category.list_all(connection)
    for category in categories:
        print(category)


def register_category():
    try:
        name = input("Enter the category's name: ")
    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    category = Category(0, name, connection)
    category.save()

    print(f"Category {name} registered successfully!")


def update_category():
    try:
        category_id = int(input("Enter the category's ID: "))
    except ValueError:
        print("Invalid category ID. Please enter a valid integer.")
        return

    connection = new_mysql_connection()
    category = Category.get_by_id(category_id, connection)

    try:
        name = input(f"Enter the new name ({category.name}): ")
    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    if name:
        category.name = name
    category.save()

    print(f"Category {name} updated successfully!")


def list_products():
    connection = new_mysql_connection()
    products = Product.list_all(connection)
    for product in products:
        print(product)


def register_product():
    try:
        name = input("Enter the product's name: ")
        description = input("Enter the product's description: ")
        categories = input("Enter the product's categories (ex: 1,2,3,4): ").split(",")
        price = float(input("Enter the product's price: "))
        available_on_stock = int(
            input("Enter the product's quantity available on stock: ")
        )
    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    product = Product(0, name, description, price, available_on_stock, connection)
    product.save()

    if len(categories) > 0:
        for category_id in categories:
            category = Category.get_by_id(int(category_id), connection)
            if category:
                product.add_category(category.id)
            else:
                print(f"Category with ID {category_id} not found.")
                return

    product.save()


def update_product():
    try:
        product_id = int(input("Enter the product's ID: "))
    except ValueError:
        print("Invalid product ID. Please enter a valid integer.")
        return

    connection = new_mysql_connection()
    product = Product.get_by_id(product_id, connection)
    product.load_categories()

    try:
        name = input(f"Enter the new name ({product.name}): ")
        description = input(f"Enter the new description ({product.description}): ")
        categories = input(
            f"Enter the new categories ({', '.join([str(c) for c in product.categories])}): "
        ).split(",")
        price = input(f"Enter the new price ({str(product.price)}): ")
        if price != "":
            price = float(price)
        available_on_stock = input(
                f"Enter the new quantity available on stock ({product.available_on_stock}): "
            )
        if available_on_stock != "":
            available_on_stock = int(available_on_stock)
    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    if name:
        product.name = name
    if description:
        product.description = description
    if len(categories) > 0:
        product.clear_categories()
        for category in categories:
            if category != "":
                product.add_category(category)
    if price:
        product.price = price
    if available_on_stock:
        product.available_on_stock = available_on_stock
    product.save()

    print(f"Product {name} updated successfully!")


def list_addresses(user_id):
    connection = new_mysql_connection()
    user = User.get_by_id(user_id, connection)
    user.load_addresses()
    addresses = user.addresses
    for address in addresses:
        print(address)


def register_address(user_id):
    try:
        state = input("Enter the address's state: ")
        city = input("Enter the address's city: ")
        cep = input("Enter the address's cep: ")
        first_line = input("Enter the address's first line: ")
        second_line = input("Enter the address's second line: ")
        third_line = input("Enter the address's third line: ")

    except TypeError:
        print(
            "There's an error on the values you've provided, please insert valid values"
        )

    connection = new_mysql_connection()
    user = User.get_by_id(user_id, connection)
    if not user:
        print(f"User with ID {user_id} not found.")
        return
    address = Address(
        0, state, city, cep, first_line, second_line, third_line, user_id, connection
    )
    address.save()

    print("Address registered successfully!")


def main():
    while True:
        print("Welcome to the CLI!")
        print("1. Users")
        print("2. Products")
        print("3. Categories")
        print("4. Addresses")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("1. List Users")
            print("2. Register User")
            print("3. Update User")
            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                list_users()
            elif user_choice == "2":
                register_user()
            elif user_choice == "3":
                update_user()
            else:
                print("Invalid choice, please try again.")

        elif choice == "2":
            print("1. List Products")
            print("2. Register Product")
            print("3. Update Product")
            product_choice = input("Enter your choice: ")

            if product_choice == "1":
                list_products()
            elif product_choice == "2":
                register_product()
            elif product_choice == "3":
                update_product()
            else:
                print("Invalid choice, please try again.")

        elif choice == "3":
            print("1. List Categories")
            print("2. Register Category")
            print("3. Update Category")
            category_choice = input("Enter your choice: ")

            if category_choice == "1":
                list_categories()
            elif category_choice == "2":
                register_category()
            elif category_choice == "3":
                update_category()
            else:
                print("Invalid choice, please try again.")

        elif choice == "4":
            user_id = int(input("Enter the user ID to manage addresses: "))
            print("1. List Addresses")
            print("2. Register Address")
            address_choice = input("Enter your choice: ")

            if address_choice == "1":
                list_addresses(user_id)
            elif address_choice == "2":
                register_address(user_id)
            else:
                print("Invalid choice, please try again.")

        elif choice == "5":
            print("Exiting the CLI. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")
