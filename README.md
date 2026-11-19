# Smart Expense Tracker

A personal finance management application built with **Python, Streamlit, Supabase, Pandas, and Plotly**. It allows users to securely manage, track, and analyze their daily expenses through an interactive dashboard.

## Features

- **User Authentication:** Secure user registration, login, and logout.
- **Multi-User Support:** Each user manages their own expenses and budgets.
- **Dashboard:** View total expenses, transaction count, and average expense.
- **Expense Management:** Add, edit, delete, and manage expense records.
- **Search & Filters:** Search expenses and filter by category, date, amount, and payment method.
- **Sorting:** Sort transactions by date or amount.
- **Budget Management:** Set and manage monthly budgets.
- **Data Visualization:** Analyze category-wise and monthly expenses using interactive charts.
- **Payment Analytics:** Review expenses by payment method.
- **Export Reports:** Export expense records to CSV and Excel.
- **Data Validation:** Validate expense and budget inputs.
- **Data Security:** Supabase Row Level Security (RLS) protects user-specific records.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Supabase | Cloud database and authentication |
| PostgreSQL | Database engine |
| Pandas | Data processing and analysis |
| Plotly | Interactive charts |
| Pytest | Automated testing |

## Project Structure

```text
Smart-Expense-Tracker/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── supabase_client.py
│   ├── auth_manager.py
│   ├── auth_ui.py
│   ├── expense_manager.py
│   ├── analytics.py
│   └── budget_manager.py
│
├── tests/
│   ├── test_analytics.py
│   └── test_expense_manager.py
│
├── test_expenses.py
│
└── .streamlit/
    └── config.toml
```

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Basit366/Smart-Expense-Tracker.git
```

### 2. Navigate to the project directory

```bash
cd Smart-Expense-Tracker
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Supabase

Create a Supabase project and configure the required database tables, authentication, and Row Level Security policies.

Create a `.streamlit/secrets.toml` file in the project directory:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-publishable-key"
```

**Important:** Never upload your `secrets.toml` file or private credentials to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Database

The application uses **Supabase PostgreSQL** to store user-specific expense and budget records.

- `expenses`: Stores expense transactions.
- `budgets`: Stores monthly budgets.
- `profiles`: Stores user profile information.

Row Level Security (RLS) policies ensure that authenticated users can access only their own records.

## Run Tests

Run the automated test suite using:

```bash
pytest -v
```

## Future Improvements

- Advanced financial analytics and insights.
- Improved reporting and visualization.
- Additional financial management features.

## Author

**Basit**

GitHub: [@Basit366](https://github.com/Basit366)

---

If you find this project useful, consider giving it a star on GitHub.
