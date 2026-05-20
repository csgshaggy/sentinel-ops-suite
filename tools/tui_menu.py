#!/usr/bin/env python3
from super_doctor import dashboard, print_report, run_checks


def menu():
    while True:
        print("\n=== SuperDoctor Menu ===")
        print("1. Run full check")
        print("2. Show report")
        print("3. Show dashboard")
        print("4. Exit")

        choice = input("> ")

        if choice == "1":
            results = run_checks()
            print_report(results)
        elif choice == "2":
            results = run_checks()
            print_report(results)
        elif choice == "3":
            results = run_checks()
            dashboard(results)
        elif choice == "4":
            return
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()
