def main():
    while True:
        print("Welcome to the CLI interface!")
        print("1. Register User")
        print("2. Register Product")
        print("3. Place Order")
        print("4. Exit")

        choice = input("Please enter your choice: ")

        if choice == "1":
            print("Registering User...")
        elif choice == "2":
            print("Registering Product...")
        elif choice == "3":
            print("Placing Order...")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
