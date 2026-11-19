
from src.supabase_client import get_supabase_client
import streamlit as st


def get_current_user_id():
    """Get the authenticated user's ID."""

    user = st.session_state.get("user")

    if user is None:
        raise PermissionError("Please log in first.")

    return user.id


def add_expense(
    title, amount, category, expense_date,
    description="", payment_method="Cash"
):
    """Add an expense for the logged-in user."""

    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty.")

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if not category or not category.strip():
        raise ValueError("Expense category cannot be empty.")

    if not expense_date:
        raise ValueError("Expense date is required.")

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = supabase.table("expenses").insert({
        "user_id": user_id,
        "title": title.strip(),
        "amount": amount,
        "category": category.strip(),
        "expense_date": str(expense_date),
        "description": description.strip(),
        "payment_method": payment_method.strip()
    }).execute()

    return response.data[0]["id"]


def get_all_expenses():
    """Retrieve only the logged-in user's expenses."""

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("expenses")
        .select("*")
        .eq("user_id", user_id)
        .order("expense_date", desc=True)
        .order("id", desc=True)
        .execute()
    )

    return response.data


def update_expense(
    expense_id, title, amount, category,
    expense_date, description="", payment_method="Cash"
):
    """Update an expense belonging to the logged-in user."""

    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty.")

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if not category or not category.strip():
        raise ValueError("Expense category cannot be empty.")

    if not expense_date:
        raise ValueError("Expense date is required.")

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("expenses")
        .update({
            "title": title.strip(),
            "amount": amount,
            "category": category.strip(),
            "expense_date": str(expense_date),
            "description": description.strip(),
            "payment_method": payment_method.strip()
        })
        .eq("id", expense_id)
        .eq("user_id", user_id)
        .select("id")
        .execute()
    )

    return len(response.data) > 0


def delete_expense(expense_id):
    """Delete an expense belonging to the logged-in user."""

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("expenses")
        .delete()
        .eq("id", expense_id)
        .eq("user_id", user_id)
        .select("id")
        .execute()
    )

    return len(response.data) > 0
