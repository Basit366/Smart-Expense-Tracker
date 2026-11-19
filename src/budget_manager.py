
from src.database import get_connection


def set_budget(month, amount):
    """Add or update a monthly budget."""

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO budgets (month, amount)
            VALUES (?, ?)
            ON CONFLICT(month)
            DO UPDATE SET amount = excluded.amount
            """,
            (month, amount)
        )

        connection.commit()

    return True


def get_budget(month):
    """Get budget for a specific month."""

    with get_connection() as connection:

        cursor = connection.execute(
            "SELECT amount FROM budgets WHERE month = ?",
            (month,)
        )

        result = cursor.fetchone()

        return float(result["amount"]) if result else 0.0


def get_all_budgets():
    """Get all monthly budgets."""

    with get_connection() as connection:

        cursor = connection.execute(
            "SELECT * FROM budgets ORDER BY month DESC"
        )

        return [dict(row) for row in cursor.fetchall()]


def delete_budget(month):
    """Delete a monthly budget."""

    with get_connection() as connection:

        cursor = connection.execute(
            "DELETE FROM budgets WHERE month = ?",
            (month,)
        )

        connection.commit()

        return cursor.rowcount > 0