
import pytest
from unittest.mock import MagicMock

import src.expense_manager as expense_manager


@pytest.fixture
def mock_supabase(monkeypatch):
    """Create a mock Supabase client for testing."""

    client = MagicMock()
    query = MagicMock()

    client.table.return_value = query

    query.insert.return_value = query
    query.update.return_value = query
    query.delete.return_value = query
    query.select.return_value = query
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

    return client, query


def test_add_expense(mock_supabase):
    expense_id = expense_manager.add_expense(
        title="Internet Bill",
        amount=2000,
        category="Bills",
        expense_date="2026-11-19",
        description="Monthly internet bill"
    )

    assert expense_id == 1


def test_add_expense_empty_title():
    with pytest.raises(ValueError):
        expense_manager.add_expense(
            "", 1000, "Food", "2026-11-19"
        )


def test_add_expense_negative_amount():
    with pytest.raises(ValueError):
        expense_manager.add_expense(
            "Food", -100, "Food", "2026-11-19"
        )


def test_add_expense_empty_category():
    with pytest.raises(ValueError):
        expense_manager.add_expense(
            "Food", 1000, "", "2026-11-19"
        )


def test_add_expense_missing_date():
    with pytest.raises(ValueError):
        expense_manager.add_expense(
            "Food", 1000, "Food", ""
        )


def test_update_expense(mock_supabase):
    result = expense_manager.update_expense(
        expense_id=1,
        title="Updated Internet Bill",
        amount=2000,
        category="Utilities",
        expense_date="2026-11-19",
        description="Updated monthly bill"
    )

    assert result is True


def test_delete_expense(mock_supabase):
    result = expense_manager.delete_expense(1)

    assert result is True


def test_get_all_expenses(mock_supabase):
    _, query = mock_supabase

    query.execute.return_value.data = [
        {"id": 1, "title": "Electricity Bill"},
        {"id": 2, "title": "Internet Bill"}
    ]

    expenses = expense_manager.get_all_expenses()

    assert len(expenses) == 2
    assert isinstance(expenses, list)
