from mysql_connection import new_mysql_connection

from entities.user import User


def register_user():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone_number = input("Enter your phone number: ")
    cpf = input("Enter your CPF: ")

    connection = new_mysql_connection()
    user = User(0, name, email, phone_number, cpf, connection)
    user.save()

    print(f"User {name} registered successfully!")


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
            print("Registering Product...")
        elif choice == "3":
            print("Placing Order...")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
