import io
import pandas as pd
import streamlit as st
import plotly.express as px

from src.auth_ui import show_auth_page, show_logout_button
from src.analytics import (
    get_expense_dataframe,
    get_total_expenses,
    get_category_summary,
    get_monthly_summary,
    get_payment_method_summary
)
from src.expense_manager import (
    add_expense,
    update_expense,
    delete_expense
)
from src.database import initialize_database

initialize_database()

# Page Configuration
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)
# Authentication Protection
if "user" not in st.session_state:
    show_auth_page()
    st.stop()

show_logout_button()


# Sidebar Navigation
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0 18px 0;">
        <h1 style="font-size: 42px; margin: 0;">💰</h1>
        <h2 style="font-size: 21px; margin: 8px 0 4px 0;">
            Smart Expense Tracker
        </h2>
        <p style="font-size: 12px; color: gray; margin: 0;">
            Personal Finance Management
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.markdown("### 🧭 Main Menu")

page = st.sidebar.radio(
    "Navigate to",
    [
        "Dashboard",
        "Add Expense",
        "Manage Expenses",
        "Budget Management",
        "Export Reports"
    ],
    label_visibility="collapsed"
)
st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 12px 0;">
        <p style="font-size: 12px; color: gray; margin: 0;">
            Built with Python & Streamlit
        </p>
        <p style="font-size: 11px; color: gray; margin: 5px 0 0 0;">
            Smart Finance Management
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Load Data
df = get_expense_dataframe()






# ==========================================
# DASHBOARD PAGE
# ==========================================





# Dashboard Date Filter
if page == "Dashboard":
    from datetime import date, timedelta

    st.sidebar.divider()
    st.sidebar.subheader("📅 Dashboard Filters")

    today = date.today()

    date_preset = st.sidebar.selectbox(
        "Quick Date Filter",
        [
            "All Time",
            "Today",
            "Last 7 Days",
            "Last 30 Days",
            "This Month",
            "Custom Range"
        ]
    )

    if date_preset == "All Time" and not df.empty:
        default_start = df["expense_date"].min().date()
        default_end = df["expense_date"].max().date()

    elif date_preset == "Today":
        default_start = today
        default_end = today

    elif date_preset == "Last 7 Days":
        default_start = today - timedelta(days=6)
        default_end = today

    elif date_preset == "This Month":
        default_start = today.replace(day=1)
        default_end = today

    else:
        default_start = today - timedelta(days=29)
        default_end = today

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(default_start, default_end)
    )

    if not df.empty and len(selected_dates) == 2:
        start_date, end_date = selected_dates

        df = df[
            (df["expense_date"].dt.date >= start_date) &
            (df["expense_date"].dt.date <= end_date)
        ]

    # Professional Dashboard Header
    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #1E3A8A, #2563EB);
            padding: 28px;
            border-radius: 15px;
            margin-bottom: 20px;
        ">
            <h1 style="color: white; margin: 0;">
                💰 Smart Expense Tracker
            </h1>
            <p style="
                color: #DBEAFE;
                font-size: 16px;
                margin: 8px 0 0 0;
            ">
                Take control of your finances. Track, analyze and manage your expenses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Dashboard Calculations
    total = get_total_expenses(df)
    total_transactions = len(df)
    average = total / total_transactions if total_transactions else 0

    # Dashboard Metric Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style="
                background-color: #DBEAFE;
                padding: 22px;
                border-radius: 12px;
                border-left: 5px solid #2563EB;
            ">
                <p style="color: #1E40AF; font-size: 15px; margin: 0;">
                    💰 Total Expenses
                </p>
                <h2 style="color: #1E3A8A; margin: 8px 0;">
                    Rs. {total:,.2f}
                </h2>
                <p style="color: #475569; font-size: 12px; margin: 0;">
                    Total recorded spending
                </p>
            </div>
            """.format(total=total),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="
                background-color: #DCFCE7;
                padding: 22px;
                border-radius: 12px;
                border-left: 5px solid #16A34A;
            ">
                <p style="color: #166534; font-size: 15px; margin: 0;">
                    🧾 Total Transactions
                </p>
                <h2 style="color: #14532D; margin: 8px 0;">
                    {transactions}
                </h2>
                <p style="color: #475569; font-size: 12px; margin: 0;">
                    Total recorded entries
                </p>
            </div>
            """.format(transactions=total_transactions),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style="
                background-color: #F3E8FF;
                padding: 22px;
                border-radius: 12px;
                border-left: 5px solid #9333EA;
            ">
                <p style="color: #6B21A8; font-size: 15px; margin: 0;">
                    📊 Average Expense
                </p>
                <h2 style="color: #581C87; margin: 8px 0;">
                    Rs. {average:,.2f}
                </h2>
                <p style="color: #475569; font-size: 12px; margin: 0;">
                    Average per transaction
                </p>
            </div>
            """.format(average=average),
            unsafe_allow_html=True
        )

    st.divider()
    st.subheader("📊 Expense Analytics")

    if not df.empty:

        # Category-wise Pie Chart
        col1, col2 = st.columns(2)

        with col1:
            category_data = get_category_summary(df)

            fig = px.pie(
                category_data,
                names="category",
                values="amount",
                title="Expense Distribution by Category",
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Amount: Rs. %{value:,.2f}<br>Share: %{percent}<extra></extra>"
            )

            fig.update_layout(
                title_x=0.5,
                legend_title_text="Expense Categories",
                margin=dict(t=60, b=20, l=20, r=20)
            )

            st.plotly_chart(fig, use_container_width=True)

        # Monthly Bar Chart
        with col2:
            monthly_data = get_monthly_summary(df)

            fig = px.bar(
                monthly_data,
                x="month",
                y="amount",
                title="Monthly Expense Trends",
                labels={
                    "month": "Month",
                    "amount": "Amount (Rs.)"
                },
                color="amount",
                color_continuous_scale="Blues",
                template="plotly_white"
            )

            fig.update_traces(
                hovertemplate="<b>Month:</b> %{x}<br><b>Total:</b> Rs. %{y:,.2f}<extra></extra>",
                marker_line_width=0
            )

            fig.update_layout(
                title_x=0.5,
                xaxis_title="Month",
                yaxis_title="Expense Amount (Rs.)",
                coloraxis_showscale=False,
                margin=dict(t=60, b=20, l=20, r=20)
            )

            st.plotly_chart(fig, use_container_width=True)
                    # Payment Method Analytics
        st.divider()
        st.subheader("💳 Spending by Payment Method")

        payment_data = get_payment_method_summary(df)

        if not payment_data.empty:

            fig = px.pie(
                payment_data,
                names="payment_method",
                values="amount",
                title="Expenses by Payment Method",
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Amount: Rs. %{value:,.2f}"
                    "<extra></extra>"
                )
            )

            fig.update_layout(
                title_x=0.5,
                legend_title="Payment Methods"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No payment method data available.")
                # Spending Insights
        st.divider()
        st.subheader("💡 Spending Insights")

        highest_category = (
            df.groupby("category")["amount"]
            .sum()
            .idxmax()
        )

        highest_expense = df.loc[df["amount"].idxmax()]

        total_days = (
            df["expense_date"].max() - df["expense_date"].min()
        ).days + 1

        daily_average = total / total_days if total_days > 0 else 0

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"🏆 Highest Spending Category: **{highest_category}**"
            )

            st.info(
                f"💸 Highest Single Expense: **Rs. {highest_expense['amount']:,.2f}**"
                f" ({highest_expense['title']})"
            )

        with col2:
            st.info(
                f"📅 Average Daily Spending: **Rs. {daily_average:,.2f}**"
            )

            st.info(
                f"🧾 Total Transactions: **{total_transactions}**"
            )
        # Recent Transactions
        st.divider()
        st.subheader("🕒 Recent Transactions")

        recent_expenses = df.sort_values(
            by=["expense_date", "id"],
            ascending=False
        ).head(5)

        st.dataframe(
            recent_expenses[
                ["title", "amount", "category", "expense_date"]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "title": "Expense Title",
                "amount": st.column_config.NumberColumn(
                    "Amount (Rs.)",
                    format="Rs. %.2f"
                ),
                "category": "Category",
                "expense_date": st.column_config.DateColumn(
                    "Date",
                    format="DD MMM YYYY"
                )
            }
        )

    else:
        st.info("No expenses available. Add your first expense.")




# ==========================================
# ADD EXPENSE PAGE
# ==========================================

elif page == "Add Expense":

    st.title("➕ Add New Expense")
    st.caption("Track your spending with a clean and organized expense form.")
    st.divider()

    categories = {
        "🍔 Food": "Food",
        "🚗 Transport": "Transport",
        "🛍️ Shopping": "Shopping",
        "💡 Bills": "Bills",
        "📚 Education": "Education",
        "🏥 Healthcare": "Healthcare",
        "🎮 Entertainment": "Entertainment",
        "📦 Other": "Other"
    }

    st.subheader("📝 Expense Information")

    with st.form("expense_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input(
                "Expense Title *",
                placeholder="e.g. Grocery Shopping"
            )

            amount = st.number_input(
                "Amount (Rs.) *",
                min_value=0.01,
                value=100.0,
                step=100.0,
                format="%.2f"
            )

            selected_category = st.selectbox(
                "Expense Category",
                list(categories.keys())
            )

        with col2:
            expense_date = st.date_input("Expense Date")

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "Debit Card",
                    "Credit Card",
                    "Bank Transfer",
                    "Mobile Wallet"
                ]
            )

            description = st.text_area(
                "Description (Optional)",
                placeholder="Add details about this expense...",
                height=110
            )

        st.divider()
        st.caption("* Required fields")

        submitted = st.form_submit_button(
            "💾 Save Expense",
            use_container_width=True,
            type="primary"
        )

    if submitted:

        if not title.strip():
            st.error("Please enter an expense title.")

        elif amount <= 0:
            st.error("Please enter a valid amount.")

        else:
            add_expense(
                title.strip(),
                amount,
                categories[selected_category],
                expense_date.isoformat(),
                description.strip(),
                payment_method
            )

            st.success("✅ Expense added successfully!")
            st.balloons()
            st.rerun()


# ==========================================
# MANAGE EXPENSES PAGE
# ==========================================

elif page == "Manage Expenses":

    st.title("📋 Manage Expenses")
    st.caption("Search, filter, edit and delete expenses")
    st.divider()

    if not df.empty:

        st.subheader("🔎 Search & Filter")

        search_query = st.text_input(
            "Search by Expense Title"
        )

        categories = ["All"] + sorted(
            df["category"].unique().tolist()
        )

        selected_category = st.selectbox(
            "Filter by Category",
            categories
        )

        # Payment Method Filter
        payment_methods = ["All"] + sorted(
            df["payment_method"].dropna().unique().tolist()
        )

        selected_payment_method = st.selectbox(
            "Filter by Payment Method",
            payment_methods
        )

        col1, col2 = st.columns(2)

        min_amount = float(df["amount"].min())
        max_amount = float(df["amount"].max())

        with col1:
            amount_min = st.number_input(
                "Minimum Amount (Rs.)",
                min_value=0.0,
                value=min_amount
            )

        with col2:
            amount_max = st.number_input(
                "Maximum Amount (Rs.)",
                min_value=0.0,
                value=max_amount
            )

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Start Date",
                value=df["expense_date"].min().date()
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=df["expense_date"].max().date()
            )

        # Sorting Dropdown
        sort_option = st.selectbox(
            "Sort Expenses By",
            [
                "Newest First",
                "Oldest First",
                "Highest Amount",
                "Lowest Amount"
            ]
        )

        filtered_df = df.copy()

        if amount_min > amount_max:
            st.error("Minimum amount cannot exceed maximum amount.")

        elif start_date > end_date:
            st.error("Start Date cannot be after End Date.")

        else:

            # Amount Filter
            filtered_df = filtered_df[
                (filtered_df["amount"] >= amount_min) &
                (filtered_df["amount"] <= amount_max)
            ]

            # Date Filter
            filtered_df = filtered_df[
                (filtered_df["expense_date"].dt.date >= start_date) &
                (filtered_df["expense_date"].dt.date <= end_date)
            ]

            # Search Filter
            if search_query:
                filtered_df = filtered_df[
                    filtered_df["title"].str.contains(
                        search_query,
                        case=False,
                        na=False
                    )
                ]

            # Category Filter
            if selected_category != "All":
                filtered_df = filtered_df[
                    filtered_df["category"] == selected_category
                ]

            # Payment Method Filter
            if selected_payment_method != "All":
                filtered_df = filtered_df[
                    filtered_df["payment_method"] == selected_payment_method
                ]

            # Apply Sorting
            if sort_option == "Newest First":
                filtered_df = filtered_df.sort_values(
                    by=["expense_date", "id"],
                    ascending=False
                )

            elif sort_option == "Oldest First":
                filtered_df = filtered_df.sort_values(
                    by=["expense_date", "id"],
                    ascending=True
                )

            elif sort_option == "Highest Amount":
                filtered_df = filtered_df.sort_values(
                    by="amount",
                    ascending=False
                )

            elif sort_option == "Lowest Amount":
                filtered_df = filtered_df.sort_values(
                    by="amount",
                    ascending=True
                )

            st.write(f"Matching Expenses: {len(filtered_df)}")

            # Display Filtered Expenses
            st.dataframe(
                filtered_df[
                    [
                        "id",
                        "title",
                        "amount",
                        "category",
                        "expense_date",
                        "payment_method",
                        "description"
                    ]
                ],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.NumberColumn(
                        "ID",
                        format="%d"
                    ),
                    "title": st.column_config.TextColumn(
                        "Expense Title"
                    ),
                    "amount": st.column_config.NumberColumn(
                        "Amount (Rs.)",
                        format="Rs. %.2f"
                    ),
                    "category": st.column_config.TextColumn(
                        "Category"
                    ),
                    "expense_date": st.column_config.DateColumn(
                        "Expense Date",
                        format="DD MMM YYYY"
                    ),
                    "payment_method": st.column_config.TextColumn(
                        "Payment Method"
                    ),
                    "description": st.column_config.TextColumn(
                        "Description"
                    )
                }
            )

        # ==========================================
        # EXPENSE RECORDS
        # ==========================================

        st.divider()
        st.subheader("📋 Expense Records")

        for _, expense in df.iterrows():

            expense_id = int(expense["id"])

            with st.expander(
                f"{expense['title']} | Rs. {expense['amount']:,.2f}"
            ):

                st.write(f"Category: {expense['category']}")
                st.write(f"Date: {expense['expense_date'].date()}")

                st.write(
                    f"Payment Method: {expense['payment_method']}"
                )

                st.write(
                    f"Description: {expense['description'] or 'No description'}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{expense_id}"
                    ):
                        delete_expense(expense_id)
                        st.success("Expense deleted!")
                        st.rerun()

                with col2:
                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{expense_id}"
                    ):
                        st.session_state["editing_expense"] = expense_id
                        st.rerun()

        # ==========================================
        # EDIT EXPENSE FORM
        # ==========================================

        if "editing_expense" in st.session_state:

            expense_id = st.session_state["editing_expense"]

            selected = df[df["id"] == expense_id]

            if not selected.empty:

                expense = selected.iloc[0]

                st.divider()
                st.subheader("✏️ Edit Expense")

                with st.form("edit_expense_form"):

                    new_title = st.text_input(
                        "Expense Title",
                        value=expense["title"]
                    )

                    new_amount = st.number_input(
                        "Amount (Rs.)",
                        min_value=0.01,
                        value=float(expense["amount"])
                    )

                    edit_categories = [
                        "Food",
                        "Transport",
                        "Shopping",
                        "Bills",
                        "Education",
                        "Healthcare",
                        "Entertainment",
                        "Other"
                    ]

                    current_category = expense["category"]

                    if current_category not in edit_categories:
                        edit_categories.append(current_category)

                    new_category = st.selectbox(
                        "Category",
                        edit_categories,
                        index=edit_categories.index(current_category)
                    )

                    new_date = st.date_input(
                        "Expense Date",
                        value=expense["expense_date"].date()
                    )

                    payment_methods = [
                        "Cash",
                        "Debit Card",
                        "Credit Card",
                        "Bank Transfer",
                        "Mobile Wallet"
                    ]

                    current_payment_method = expense.get(
                        "payment_method", "Cash"
                    )

                    if current_payment_method not in payment_methods:
                        payment_methods.append(current_payment_method)

                    new_payment_method = st.selectbox(
                        "Payment Method",
                        payment_methods,
                        index=payment_methods.index(
                            current_payment_method
                        )
                    )

                    new_description = st.text_area(
                        "Description",
                        value=expense["description"] or ""
                    )

                    save_changes = st.form_submit_button(
                        "💾 Update Expense",
                        use_container_width=True
                    )

                    if save_changes:

                        if not new_title.strip():
                            st.error("Expense title is required.")

                        elif new_amount <= 0:
                            st.error("Please enter a valid amount.")

                        else:
                            update_expense(
                                expense_id,
                                new_title.strip(),
                                new_amount,
                                new_category,
                                new_date.isoformat(),
                                new_description.strip(),
                                new_payment_method
                            )

                            del st.session_state["editing_expense"]

                            st.success(
                                "Expense updated successfully!"
                            )

                            st.rerun()

                if st.button("Cancel Editing"):
                    del st.session_state["editing_expense"]
                    st.rerun()

    else:
        st.info(
            "No expense records available. Add your first expense."
        )

        # Edit Expense Form
        if "editing_expense" in st.session_state:

            expense_id = st.session_state["editing_expense"]

            selected = df[df["id"] == expense_id]

            if not selected.empty:

                expense = selected.iloc[0]

                st.divider()
                st.subheader("✏️ Edit Expense")

                with st.form("edit_expense_form"):

                    new_title = st.text_input(
                        "Expense Title",
                        value=expense["title"]
                    )

                    new_amount = st.number_input(
                        "Amount (Rs.)",
                        min_value=0.01,
                        value=float(expense["amount"])
                    )

                    edit_categories = [
                        "Food",
                        "Transport",
                        "Shopping",
                        "Bills",
                        "Education",
                        "Healthcare",
                        "Entertainment",
                        "Other"
                    ]

                    current_category = expense["category"]

                    if current_category not in edit_categories:
                        edit_categories.append(current_category)

                    new_category = st.selectbox(
                        "Category",
                        edit_categories,
                        index=edit_categories.index(current_category)
                    )

                    new_date = st.date_input(
                        "Expense Date",
                        value=expense["expense_date"].date()
                    )

                    payment_methods = [
                        "Cash",
                        "Debit Card",
                        "Credit Card",
                        "Bank Transfer",
                        "Mobile Wallet"
                    ]

                    current_payment_method = expense.get(
                        "payment_method", "Cash"
                    )

                    if current_payment_method not in payment_methods:
                        payment_methods.append(current_payment_method)

                    new_payment_method = st.selectbox(
                        "Payment Method",
                        payment_methods,
                        index=payment_methods.index(
                            current_payment_method
                        )
                    )

                    new_description = st.text_area(
                        "Description",
                        value=expense["description"] or ""
                    )

                    save_changes = st.form_submit_button(
                        "💾 Update Expense",
                        use_container_width=True
                    )

                    if save_changes:

                        if not new_title.strip():
                            st.error("Expense title is required.")

                        elif new_amount <= 0:
                            st.error("Please enter a valid amount.")

                        else:
                            update_expense(
                                expense_id,
                                new_title.strip(),
                                new_amount,
                                new_category,
                                new_date.isoformat(),
                                new_description.strip(),
                                new_payment_method
                            )

                            del st.session_state["editing_expense"]

                            st.success(
                                "Expense updated successfully!"
                            )

                            st.rerun()

                if st.button("Cancel Editing"):
                    del st.session_state["editing_expense"]
                    st.rerun()

        else:
         st.info(
            "No expense records available. Add your first expense."
        )



        # ==========================================
        # EXPENSE RECORDS
        # ==========================================

        st.divider()
        st.subheader("📋 Expense Records")

        for _, expense in df.iterrows():

            expense_id = int(expense["id"])

            with st.expander(
                f"{expense['title']} | Rs. {expense['amount']:,.2f}"
            ):

                st.write(
                    f"Category: {expense['category']}"
                )

                st.write(
                    f"Date: {expense['expense_date'].date()}"
                )

                st.write(
                    f"Description: {expense['description'] or 'No description'}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{expense_id}"
                    ):
                        delete_expense(expense_id)

                        st.success("Expense deleted!")
                        st.rerun()

                with col2:
                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{expense_id}"
                    ):
                        st.session_state["editing_expense"] = expense_id
                        st.rerun()

        # ==========================================
        # EDIT EXPENSE FORM
        # ==========================================

        if "editing_expense" in st.session_state:

            expense_id = st.session_state["editing_expense"]

            selected = df[df["id"] == expense_id]

            if not selected.empty:

                expense = selected.iloc[0]

                st.divider()
                st.subheader("✏️ Edit Expense")

                with st.form("edit_expense_form"):

                    new_title = st.text_input(
                        "Expense Title",
                        value=expense["title"]
                    )

                    new_amount = st.number_input(
                        "Amount (Rs.)",
                        min_value=0.01,
                        value=float(expense["amount"])
                    )

                    edit_categories = [
                        "Food",
                        "Transport",
                        "Shopping",
                        "Bills",
                        "Education",
                        "Healthcare",
                        "Entertainment",
                        "Other"
                    ]

                    current_category = expense["category"]

                    if current_category not in edit_categories:
                        edit_categories.append(current_category)

                    new_category = st.selectbox(
                        "Category",
                        edit_categories,
                        index=edit_categories.index(current_category)
                    )

                    new_date = st.date_input(
                        "Expense Date",
                        value=expense["expense_date"].date()
                    )

                    new_description = st.text_area(
                        "Description",
                        value=expense["description"] or ""
                    )

                    save_changes = st.form_submit_button(
                        "💾 Update Expense",
                        use_container_width=True
                    )

                    if save_changes:

                        if not new_title.strip():
                            st.error("Expense title is required.")

                        else:
                            update_expense(
                                expense_id,
                                new_title.strip(),
                                new_amount,
                                new_category,
                                new_date.isoformat(),
                                new_description.strip()
                            )

                            del st.session_state["editing_expense"]

                            st.success(
                                "Expense updated successfully!"
                            )

                            st.rerun()

                if st.button("Cancel Editing"):
                    del st.session_state["editing_expense"]
                    st.rerun()

        else:
         st.info(
            "No expense records available. Add your first expense."
        )


# ==========================================
# EXPORT REPORTS PAGE
# ==========================================


# ==========================================
# EXPORT REPORTS PAGE
# ==========================================


# ==========================================
# BUDGET MANAGEMENT PAGE
# ==========================================

elif page == "Budget Management":

    from datetime import date
    from src.budget_manager import (
    set_budget,
    get_budget,
    get_all_budgets,
    delete_budget
)
    st.title("💰 Budget Management")
    st.caption("Set and monitor your monthly spending limits.")
    st.divider()

    current_month = date.today().strftime("%Y-%m")

    st.subheader("📝 Set Monthly Budget")

    with st.form("budget_form"):

        selected_month = st.date_input(
            "Select Month",
            value=date.today().replace(day=1)
        )

        budget_amount = st.number_input(
            "Monthly Budget (Rs.)",
            min_value=0.01,
            value=10000.0,
            step=1000.0
        )

        save_budget = st.form_submit_button(
            "💾 Save Monthly Budget",
            use_container_width=True,
            type="primary"
        )

        if save_budget:

            month_key = selected_month.strftime("%Y-%m-01")

            set_budget(month_key, budget_amount)

            st.success("Monthly budget saved successfully!")
            st.rerun()

    st.divider()

    # Current Month Budget
    st.subheader("📊 Current Month Budget")

    monthly_budget = get_budget(f"{current_month}-01")

    current_month_expenses = df[
        df["expense_date"].dt.strftime("%Y-%m") == current_month
    ]

    monthly_spending = get_total_expenses(current_month_expenses)

    remaining_budget = monthly_budget - monthly_spending

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Monthly Budget",
            f"Rs. {monthly_budget:,.2f}"
        )

    with col2:
        st.metric(
            "Monthly Spending",
            f"Rs. {monthly_spending:,.2f}"
        )

    with col3:
        st.metric(
            "Remaining Budget",
            f"Rs. {remaining_budget:,.2f}"
        )

    if monthly_budget > 0:

        budget_usage = monthly_spending / monthly_budget

        st.subheader("Budget Usage")

        st.progress(
            min(budget_usage, 1.0)
        )

        st.write(
            f"Budget Used: {budget_usage * 100:.1f}%"
        )

        if budget_usage >= 1:
            st.error("You have exceeded your monthly budget!")

        elif budget_usage >= 0.8:
            st.warning("You have used 80% or more of your budget.")

        else:
            st.success("Your spending is within the budget.")

    else:
        st.info("Please set a monthly budget to monitor your spending.")

    st.divider()

    # ==========================================
    # MONTHLY SPENDING CHART
    # ==========================================

    st.divider()
    st.subheader("📈 Monthly Spending Trends")

    if not df.empty:

        monthly_chart_data = df.copy()

        monthly_chart_data["month"] = (
            monthly_chart_data["expense_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_chart_data = (
            monthly_chart_data
            .groupby("month")["amount"]
            .sum()
            .reset_index()
            .sort_values("month")
        )

        fig = px.bar(
            monthly_chart_data,
            x="month",
            y="amount",
            title="Monthly Expense Overview",
            labels={
                "month": "Month",
                "amount": "Total Spending (Rs.)"
            },
            color="amount",
            color_continuous_scale="Blues",
            template="plotly_white"
        )

        fig.update_layout(
            title_x=0.5,
            xaxis_title="Month",
            yaxis_title="Total Spending (Rs.)",
            coloraxis_showscale=False
        )

        fig.update_traces(
            hovertemplate=(
                "<b>Month:</b> %{x}<br>"
                "<b>Spending:</b> Rs. %{y:,.2f}"
                "<extra></extra>"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No expense data available for the monthly chart.")


    # ==========================================
    # BUDGET VS ACTUAL COMPARISON
    # ==========================================

    st.divider()
    st.subheader("📊 Budget vs Actual Comparison")

    all_budgets = get_all_budgets()

    if all_budgets:

        comparison_data = pd.DataFrame(all_budgets)

        comparison_data["actual_spending"] = (
            comparison_data["month"].map(
                df.assign(
                    month=df["expense_date"].dt.strftime("%Y-%m")
                ).groupby("month")["amount"].sum()
            ).fillna(0)
        )

        fig = px.bar(
            comparison_data,
            x="month",
            y=["amount", "actual_spending"],
            barmode="group",
            title="Monthly Budget vs Actual Spending",
            labels={
                "month": "Month",
                "value": "Amount (Rs.)",
                "variable": "Type"
            },
            color_discrete_sequence=["#2563EB", "#16A34A"],
            template="plotly_white"
        )

        fig.update_layout(
            title_x=0.5,
            xaxis_title="Month",
            yaxis_title="Amount (Rs.)",
            legend_title="Comparison",
            margin=dict(t=60, b=20)
        )

        fig.update_traces(
            hovertemplate=(
                "<b>Month:</b> %{x}<br>"
                "<b>Amount:</b> Rs. %{y:,.2f}"
                "<extra></extra>"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Set a monthly budget to view the comparison chart.")

    # ==========================================
    # CATEGORY-WISE BUDGET INSIGHTS
    # ==========================================

    st.divider()
    st.subheader("🥧 Category-wise Spending Insights")

    if not df.empty:

        category_data = (
            df.groupby("category")["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
        )

        fig = px.pie(
            category_data,
            names="category",
            values="amount",
            title="Expense Distribution by Category",
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Amount: Rs. %{value:,.2f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            title_x=0.5,
            legend_title="Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        highest_category = category_data.iloc[0]

        st.info(
            f"Highest spending category: {highest_category['category']} "
            f"(Rs. {highest_category['amount']:,.2f})"
        )

    else:
        st.info("Add expenses to view category-wise insights.")

    # All Saved Budgets
    st.divider()
    st.subheader("📋 All Monthly Budgets")

    all_budgets = get_all_budgets()

    if all_budgets:

        budget_df = pd.DataFrame(all_budgets)

        st.dataframe(
            budget_df[["month", "amount"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "month": "Month",
                "amount": st.column_config.NumberColumn(
                    "Budget Amount (Rs.)",
                    format="Rs. %.2f"
                )
            }
        )

        st.divider()
        st.subheader("✏️ Edit or Delete Budget")

        budget_months = [budget["month"] for budget in all_budgets]

        selected_budget_month = st.selectbox(
            "Select a month",
            budget_months
        )

        selected_budget_amount = get_budget(selected_budget_month)

        with st.form("edit_budget_form"):

            updated_amount = st.number_input(
                "Updated Monthly Budget (Rs.)",
                min_value=0.01,
                value=float(selected_budget_amount),
                step=1000.0
            )

            update_budget = st.form_submit_button(
                "💾 Update Budget",
                use_container_width=True,
                type="primary"
            )

            if update_budget:
                set_budget(selected_budget_month, updated_amount)
                st.success("Budget updated successfully!")
                st.rerun()

        if st.button(
            "🗑️ Delete Selected Budget",
            use_container_width=True
        ):
            delete_budget(selected_budget_month)
            st.success("Budget deleted successfully!")
            st.rerun()

    else:
        st.info("No monthly budgets have been saved yet.")

elif page == "Export Reports":

    st.title("📥 Export Expense Reports")
    st.caption("Generate and download your financial reports.")
    st.divider()

    if not df.empty:

        # ==========================================
        # REPORT SUMMARY
        # ==========================================

        st.subheader("📊 Report Summary")

        total_expenses = get_total_expenses(df)
        total_transactions = len(df)
        average_expense = (
            total_expenses / total_transactions
            if total_transactions > 0 else 0
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Expenses",
                f"Rs. {total_expenses:,.2f}"
            )

        with col2:
            st.metric(
                "Total Transactions",
                total_transactions
            )

        with col3:
            st.metric(
                "Average Expense",
                f"Rs. {average_expense:,.2f}"
            )

        st.divider()

        # ==========================================
        # CATEGORY-WISE REPORT
        # ==========================================

        st.subheader("📁 Category-wise Expense Report")

        category_report = get_category_summary(df)

        category_report = category_report.rename(
            columns={
                "category": "Category",
                "amount": "Total Amount (Rs.)"
            }
        )

        st.dataframe(
            category_report,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Category": st.column_config.TextColumn(
                    "Expense Category"
                ),
                "Total Amount (Rs.)": st.column_config.NumberColumn(
                    "Total Amount (Rs.)",
                    format="Rs. %.2f"
                )
            }
        )

        st.divider()

        # ==========================================
        # DOWNLOAD REPORTS
        # ==========================================

        st.subheader("📥 Download Your Reports")

        st.write(
            "Choose your preferred file format to download your expense records."
        )

        col1, col2 = st.columns(2)

        with col1:

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📄 Download CSV Report",
                data=csv_data,
                file_name="smart_expense_report.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )

        with col2:

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:

                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Expenses"
                )

                category_report.to_excel(
                    writer,
                    index=False,
                    sheet_name="Category Summary"
                )

            st.download_button(
                label="📊 Download Excel Report",
                data=excel_buffer.getvalue(),
                file_name="smart_expense_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

        st.success(
            "Your expense report is ready to download!"
        )

    else:
        st.info(
            "No expense records available. Add expenses before exporting reports."
        )
def get_payment_method_summary(df):
    """Calculate total expenses for each payment method."""

    if df.empty:
        return pd.DataFrame(
            columns=["payment_method", "amount"]
        )

    summary = (
        df.groupby("payment_method")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    return summary