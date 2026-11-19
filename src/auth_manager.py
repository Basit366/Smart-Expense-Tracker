import streamlit as st
from src.supabase_client import get_supabase_client


def get_email_redirect_url():
    """Get the configured email confirmation redirect URL."""

    return st.secrets.get(
        "EMAIL_REDIRECT_URL",
        "http://localhost:8501"
    )


def signup_user(full_name, email, password):
    """Register a new user."""

    supabase = get_supabase_client()

    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "full_name": full_name
            },
            "email_redirect_to": get_email_redirect_url()
        }
    })

    return response


def login_user(email, password):
    """Log in an existing user."""

    supabase = get_supabase_client()

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    st.session_state["user"] = response.user

    return response


def logout_user():
    """Log out the current user."""

    supabase = get_supabase_client()
    supabase.auth.sign_out()

    st.session_state.pop("user", None)


def resend_confirmation_email(email):
    """Resend signup confirmation email."""

    supabase = get_supabase_client()

    response = supabase.auth.resend({
        "type": "signup",
        "email": email.strip(),
        "options": {
            "email_redirect_to": get_email_redirect_url()
        }
    })

    return response