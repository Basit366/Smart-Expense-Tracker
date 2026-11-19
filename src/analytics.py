
import pandas as pd

from src.expense_manager import get_all_expenses


def get_expense_dataframe():
    """Convert database expenses into a Pandas DataFrame."""

    expenses = get_all_expenses()

    columns = [
    "id",
    "title",
    "amount",
    "category",
    "expense_date",
    "description",
    "payment_method"
]
    df = pd.DataFrame(expenses, columns=columns)

    if not df.empty:
        df["expense_date"] = pd.to_datetime(
            df["expense_date"]
        )

        df["amount"] = pd.to_numeric(df["amount"])

    return df


def get_total_expenses(df):
    """Calculate total expenses."""

    if df.empty:
        return 0.0

    return float(df["amount"].sum())


def get_category_summary(df):
    """Calculate expenses by category."""

    if df.empty:
        return pd.DataFrame(
            columns=["category", "amount"]
        )

    return (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )


def get_monthly_summary(df):
    """Calculate monthly expenses."""

    if df.empty:
        return pd.DataFrame(
            columns=["month", "amount"]
        )

    summary = df.copy()

    summary["month"] = (
        summary["expense_date"].dt.to_period("M").astype(str)
    )

    return (
        summary.groupby("month")["amount"]
        .sum()
        .reset_index()
        .sort_values("month")
    )
def get_payment_method_summary(df):
    """Calculate total expenses for each payment method."""

    if df.empty:
        return pd.DataFrame(
            columns=["payment_method", "amount"]
        )

    return (
        df.groupby("payment_method")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )