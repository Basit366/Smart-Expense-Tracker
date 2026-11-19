
import pandas as pd

from src import analytics


def test_get_expense_dataframe(monkeypatch):
    sample_expenses = [
        {
            "id": 1,
            "title": "Internet Bill",
            "amount": 2000,
            "category": "Bills",
            "expense_date": "2026-11-19",
            "description": "Monthly bill"
        }
    ]

    monkeypatch.setattr(
        analytics,
        "get_all_expenses",
        lambda: sample_expenses
    )

    df = analytics.get_expense_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["title"] == "Internet Bill"


def test_get_total_expenses():
    df = pd.DataFrame({
        "amount": [1000, 2000, 3000]
    })

    result = analytics.get_total_expenses(df)

    assert result == 6000.0


def test_get_total_expenses_empty():
    df = pd.DataFrame(columns=["amount"])

    result = analytics.get_total_expenses(df)

    assert result == 0.0


def test_get_category_summary():
    df = pd.DataFrame({
        "category": ["Food", "Bills", "Food"],
        "amount": [1000, 2000, 500]
    })

    result = analytics.get_category_summary(df)

    assert len(result) == 2

    assert result.iloc[0]["category"] == "Bills"
    assert result.iloc[0]["amount"] == 2000

    assert result.iloc[1]["category"] == "Food"
    assert result.iloc[1]["amount"] == 1500


def test_get_monthly_summary():
    df = pd.DataFrame({
        "expense_date": pd.to_datetime([
            "2026-11-05",
            "2026-11-15",
            "2026-12-05"
        ]),
        "amount": [1000, 2000, 3000]
    })

    result = analytics.get_monthly_summary(df)

    assert len(result) == 2
    assert result.iloc[0]["month"] == "2026-11"
    assert result.iloc[0]["amount"] == 3000


def test_get_category_summary_empty():
    df = pd.DataFrame(columns=["category", "amount"])

    result = analytics.get_category_summary(df)

    assert result.empty


def test_get_monthly_summary_empty():
    df = pd.DataFrame(columns=["expense_date", "amount"])

    result = analytics.get_monthly_summary(df)

    assert result.empty
