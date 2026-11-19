
import sqlite3
from pathlib import Path

# Define database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "expenses.db"


def get_connection():
    """Create and return a database connection."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create tables and update existing database schema."""

    with get_connection() as connection:

        # Expenses Table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                description TEXT,
                payment_method TEXT NOT NULL DEFAULT 'Cash',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add payment_method to existing databases if missing
        columns = [
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(expenses)"
            ).fetchall()
        ]

        if "payment_method" not in columns:
            connection.execute("""
                ALTER TABLE expenses
                ADD COLUMN payment_method TEXT NOT NULL DEFAULT 'Cash'
            """)

        # Monthly Budget Table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL CHECK(amount > 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
