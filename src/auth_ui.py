
import streamlit as st
from src.auth_manager import (
    signup_user,
    login_user,
    logout_user,
    resend_confirmation_email
)


def show_auth_page():
    """Display signup and login pages."""

    st.title("💰 Smart Expense Tracker")
    st.subheader("Welcome! Please login or create an account.")

    signup_tab, login_tab = st.tabs(["Sign Up", "Login"])

    with signup_tab:
        with st.form("signup_form"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )

            signup_button = st.form_submit_button("Create Account")

            if signup_button:
                if not full_name.strip() or not email.strip() or not password:
                    st.error("Please fill in all fields.")

                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")

                else:
                    try:
                        response = signup_user(
                            full_name.strip(),
                            email.strip(),
                            password
                        )

                        if response.session is not None:
                            st.session_state["user"] = response.user
                            st.success("Account created successfully!")
                            st.rerun()
                        else:
                            st.success(
                                "Account created! Please check your email "
                                "to confirm your account, then log in."
                            )

                            
                    except Exception:
                     st.error(
        "Account creation failed. Please check your details "
        "or try again later."
    )


    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Login Email")

            password = st.text_input(
                "Login Password",
                type="password"
            )

            login_button = st.form_submit_button("Login")

            resend_button = st.form_submit_button(
                "Resend Confirmation Email"
            )

            if login_button:
                try:
                    login_user(email.strip(), password)
                    st.success("Login successful!")
                    st.rerun()

                except Exception:
                    st.error(
                        "Login failed. Check your email and password. "
                        "Also confirm your email if required."
                    )

            elif resend_button:
                if not email.strip():
                    st.error("Please enter your email address.")

                else:
                    try:
                        resend_confirmation_email(email)
                        st.success(
                            "Confirmation email sent! "
                            "Please check your inbox."
                        )

                    except Exception:
                       st.error(
        "Unable to resend confirmation email. "
        "Please try again later."
    )


def show_logout_button():
    """Display logged-in user information and logout button."""

    user = st.session_state.get("user")

    if user:
        st.sidebar.success(f"Logged in: {user.email}")

        if st.sidebar.button("Logout"):
            try:
                logout_user()
                st.rerun()

            except Exception:
                st.error(
        "Unable to resend confirmation email. "
        "Please try again later."
    )
