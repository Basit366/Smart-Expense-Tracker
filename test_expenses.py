
from unittest.mock import MagicMock

import src.expense_manager as expense_manager


def test_expense_crud(monkeypatch):
    """Test expense CRUD operations using mocked Supabase."""

    client = MagicMock()
    query = MagicMock()

    client.table.return_value = query

    query.insert.return_value = query
    query.select.return_value = query
    query.update.return_value = query
    query.delete.return_value = query
    query.eq.return_value = query
    query.order.return_value = query

    query.execute.return_value.data = [{"id": 1}]

    monkeypatch.setattr(
        expense_manager,
        "get_current_user_id",
        lambda: "test-user-id"
    )

    monkeypatch.setattr(
        expense_manager,
        "get_supabase_client",
        lambda: client
    )

    # CREATE
    expense_id = expense_manager.add_expense(
        "Test Expense",
        500,
        "Food",
        "2026-11-19",
        "Testing database"
    )

    assert expense_id == 1
    print("CREATE: Passed")

    # READ
    query.execute.return_value.data = [
        {"id": 1, "title": "Test Expense"}
    ]

    expenses = expense_manager.get_all_expenses()

    assert len(expenses) == 1
    assert expenses[0]["title"] == "Test Expense"
    print("READ: Passed")

    # UPDATE
    query.execute.return_value.data = [{"id": 1}]

    updated = expense_manager.update_expense(
        1,
        "Updated Expense",
        750,
        "Shopping",
        "2026-11-19",
        "Updated test"
    )

    assert updated is True
    print("UPDATE: Passed")

    # DELETE
    query.execute.return_value.data = [{"id": 1}]

    deleted = expense_manager.delete_expense(1)

    assert deleted is True
    print("DELETE: Passed")


if __name__ == "__main__":
    from pytest import MonkeyPatch

    with MonkeyPatch.context() as monkeypatch:
        test_expense_crud(monkeypatch)

    print("\nAll CRUD tests passed successfully!")
