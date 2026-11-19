
from src.database import get_connection


def add_expense(
    title, amount, category, expense_date,
    description="", payment_method="Cash"
):
    """Add a new expense to the database."""

    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty.")

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if not category or not category.strip():
        raise ValueError("Expense category cannot be empty.")

    if not expense_date:
        raise ValueError("Expense date is required.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO expenses
            (title, amount, category, expense_date,
             description, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title.strip(),
                amount,
                category.strip(),
                expense_date,
                description.strip(),
                payment_method.strip()
            )
        )

        return cursor.lastrowid


def get_all_expenses():
    """Retrieve all expenses from the database."""

    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
        )

        return [dict(row) for row in cursor.fetchall()]


def update_expense(
    expense_id, title, amount, category,
    expense_date, description="", payment_method="Cash"
):
    """Update an existing expense."""

    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty.")

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if not category or not category.strip():
        raise ValueError("Expense category cannot be empty.")

    if not expense_date:
        raise ValueError("Expense date is required.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE expenses
            SET title = ?, amount = ?, category = ?,
                expense_date = ?, description = ?,
                payment_method = ?
            WHERE id = ?
            """,
            (
                title.strip(),
                amount,
                category.strip(),
                expense_date,
                description.strip(),
                payment_method.strip(),
                expense_id
            )
        )

        return cursor.rowcount > 0


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        return cursor.rowcount > 0
