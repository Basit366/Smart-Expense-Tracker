
from src.database import initialize_database
from src.expense_manager import (
    add_expense,
    get_all_expenses,
    update_expense,
    delete_expense
)

from datetime import date


def test_expense_crud():

    initialize_database()

    # CREATE
    expense_id = add_expense(
        "Test Expense",
        500,
        "Food",
        date.today().isoformat(),
        "Testing database"
    )

    assert expense_id > 0
    print("CREATE: Passed")

    # READ
    expenses = get_all_expenses()

    expense = next(
        item for item in expenses
        if item["id"] == expense_id
    )

    assert expense["title"] == "Test Expense"
    print("READ: Passed")

    # UPDATE
    updated = update_expense(
        expense_id,
        "Updated Expense",
        750,
        "Shopping",
        date.today().isoformat(),
        "Updated test"
    )

    assert updated is True
    print("UPDATE: Passed")

    # DELETE
    deleted = delete_expense(expense_id)

    assert deleted is True
    print("DELETE: Passed")


if __name__ == "__main__":
    test_expense_crud()
    print("\nAll CRUD tests passed successfully!")
