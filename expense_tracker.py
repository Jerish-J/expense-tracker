import json
import os
from datetime import datetime
from typing import List, Dict, Any

DATA_FILE = "expenses.json"


def load_expenses() -> List[Dict[str, Any]]:
    """Load expenses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Data file is corrupted. Starting with an empty list.")
        return []


def save_expenses(expenses: List[Dict[str, Any]]) -> None:
    """Save expenses to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses: List[Dict[str, Any]]) -> None:
    """Add a new expense."""
    try:
        amount_str = input("Enter amount: ").strip()
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Enter category (e.g., food, travel, rent): ").strip()
    description = input("Enter description (optional): ").strip()
    date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()

    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date_str,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.\n")


def list_expenses(expenses: List[Dict[str, Any]]) -> None:
    """List all expenses."""
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    print("\nAll Expenses:")
    print("-" * 50)
    for idx, exp in enumerate(expenses, start=1):
        print(
            f"{idx}. {exp['date']} | ₹{exp['amount']:.2f} | "
            f"{exp['category']} | {exp['description']}"
        )
    print("-" * 50)
    print()


def summary_by_category(expenses: List[Dict[str, Any]]) -> None:
    """Show total amount spent per category."""
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    summary = {}
    for exp in expenses:
        cat = exp["category"] or "uncategorized"
        summary[cat] = summary.get(cat, 0) + exp["amount"]

    print("\nSpending Summary by Category:")
    print("-" * 50)
    for cat, total in summary.items():
        print(f"{cat}: ₹{total:.2f}")
    print("-" * 50)
    print()


def summary_by_month(expenses: List[Dict[str, Any]]) -> None:
    """Show total amount spent per month (YYYY-MM)."""
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    summary = {}
    for exp in expenses:
        # date is in format YYYY-MM-DD
        month = exp["date"][:7]  # YYYY-MM
        summary[month] = summary.get(month, 0) + exp["amount"]

    print("\nSpending Summary by Month:")
    print("-" * 50)
    for month, total in sorted(summary.items()):
        print(f"{month}: ₹{total:.2f}")
    print("-" * 50)
    print()


def delete_expense(expenses: List[Dict[str, Any]]) -> None:
    """Delete an expense by its index."""
    if not expenses:
        print("No expenses to delete.\n")
        return

    list_expenses(expenses)
    choice = input("Enter the number of the expense to delete: ").strip()
    try:
        idx = int(choice)
        if 1 <= idx <= len(expenses):
            removed = expenses.pop(idx - 1)
            save_expenses(expenses)
            print(
                f"Deleted: {removed['date']} | ₹{removed['amount']:.2f} | "
                f"{removed['category']} | {removed['description']}\n"
            )
        else:
            print("Invalid index.\n")
    except ValueError:
        print("Please enter a valid number.\n")


def print_menu() -> None:
    """Print the main menu."""
    print("==== Personal Expense Tracker ====")
    print("1. Add expense")
    print("2. List all expenses")
    print("3. Summary by category")
    print("4. Summary by month")
    print("5. Delete an expense")
    print("0. Exit")


def main() -> None:
    expenses = load_expenses()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        print()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            summary_by_category(expenses)
        elif choice == "4":
            summary_by_month(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()