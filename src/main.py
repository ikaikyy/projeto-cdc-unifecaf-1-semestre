import argparse

from mysql_connection import new_mysql_connection

parser = argparse.ArgumentParser(
    description="A program to register users and products and place orders.")

parser.add_argument("--drop", action="store_true",
                    help="Drop all tables in the database.")
parser.add_argument("--setup", action="store_true",
                    help="Setup the database with the initial schema.")
parser.add_argument("--seed", action="store_true",
                    help="Seed the database with initial data.")
parser.add_argument("--interface", type=str,
                    default="cli", choices=["cli", "gui"],)

args = parser.parse_args()

if args.setup or args.seed or args.drop:
    connection = new_mysql_connection(True)

    if args.drop:
        from setup import drop_database
        drop_database(connection)

    if args.setup:
        from setup import setup_database
        setup_database(connection)

    if args.seed:
        from seed import seed_database
        seed_database(connection)

    connection.close()
    exit(0)

if args.interface == "cli":
    from cli import main as cli_main
    cli_main()
elif args.interface == "gui":
    from gui import main as gui_main
    gui_main()
