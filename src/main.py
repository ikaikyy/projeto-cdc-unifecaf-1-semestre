import argparse

parser = argparse.ArgumentParser(
    description="A program to register users and products and place orders.")

parser.add_argument("--interface", type=str,
                    default="cli", choices=["cli", "gui"],)

args = parser.parse_args()

if args.interface == "cli":
    from cli import main as cli_main
    cli_main()
elif args.interface == "gui":
    print("GUI interface is not implemented yet.")
