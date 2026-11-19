
import pytest

from src.expense_manager import (
    add_expense,
    update_expense,
    delete_expense,
    get_all_expenses
)


def test_add_expense():
    expense_id = add_expense(
        title="Internet Bill",
        amount=2000,
        category="Bills",
        expense_date="2026-11-19",
        description="Monthly internet bill"
    )

    assert expense_id is not None
    assert expense_id > 0


def test_add_expense_empty_title():
    with pytest.raises(ValueError):
        add_expense(
            title="",
            amount=1000,
            category="Food",
            expense_date="2026-11-19"
        )


def test_add_expense_negative_amount():
    with pytest.raises(ValueError):
        add_expense(
            title="Food",
            amount=-100,
            category="Food",
            expense_date="2026-11-19"
        )


def test_add_expense_empty_category():
    with pytest.raises(ValueError):
        add_expense(
            title="Food",
            amount=1000,
            category="",
            expense_date="2026-11-19"
        )


def test_add_expense_missing_date():
    with pytest.raises(ValueError):
        add_expense(
            title="Food",
            amount=1000,
            category="Food",
            expense_date=""
        )
def test_update_expense():
    expense_id = add_expense(
        title="Old Internet Bill",
        amount=1500,
        category="Bills",
        expense_date="2026-11-19"
    )

    result = update_expense(
        expense_id=expense_id,
        title="Updated Internet Bill",
        amount=2000,
        category="Utilities",
        expense_date="2026-11-19",
        description="Updated monthly bill"
    )

    assert result is True



def test_delete_expense():
    expense_id = add_expense(
        title="Temporary Expense",
        amount=500,
        category="Other",
        expense_date="2026-11-19"
    )

    result = delete_expense(expense_id)

    assert result is True


def test_get_all_expenses():
    add_expense(
        title="Electricity Bill",
        amount=3000,
        category="Bills",
        expense_date="2026-11-19"
    )

    expenses = get_all_expenses()

    assert len(expenses) > 0
    assert isinstance(expenses, list)
