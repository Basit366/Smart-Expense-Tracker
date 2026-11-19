
import streamlit as st
from src.supabase_client import get_supabase_client
from src.expense_manager import get_current_user_id


def set_budget(month, amount):
    """Add or update the logged-in user's monthly budget."""

    if amount <= 0:
        raise ValueError("Budget amount must be greater than zero.")

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("budgets")
        .upsert(
            {
                "user_id": user_id,
                "category": "Overall",
                "month": str(month),
                "amount": amount
            },
            on_conflict="user_id,category,month"
        )
        .execute()
    )

    return True


def get_budget(month):
    """Get the logged-in user's budget for a specific month."""

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("budgets")
        .select("amount")
        .eq("user_id", user_id)
        .eq("category", "Overall")
        .eq("month", str(month))
        .execute()
    )

    return float(response.data[0]["amount"]) if response.data else 0.0


def get_all_budgets():
    """Get all monthly budgets belonging to the logged-in user."""

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("budgets")
        .select("*")
        .eq("user_id", user_id)
        .eq("category", "Overall")
        .order("month", desc=True)
        .execute()
    )

    return response.data


def delete_budget(month):
    """Delete the logged-in user's monthly budget."""

    user_id = get_current_user_id()
    supabase = get_supabase_client()

    response = (
        supabase.table("budgets")
        .delete()
        .eq("user_id", user_id)
        .eq("category", "Overall")
        .eq("month", str(month))
        .select("id")
        .execute()
    )

    return len(response.data) > 0
