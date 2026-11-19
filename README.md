#  Smart Expense Tracker

A Python-based personal finance management application built with **Streamlit, SQLite, Pandas, and Plotly**. It helps users record, manage, analyze, and monitor their daily expenses through an interactive dashboard.

##  Features

- **Dashboard:** View total expenses, transaction count, and average expense.
- **Expense Management:** Add, edit, delete, and manage expense records.
- **Search & Filters:** Search expenses and filter by category, date, amount, and payment method.
- **Sorting:** Sort transactions by date or amount.
- **Budget Management:** Set monthly budgets and monitor spending.
- **Data Visualization:** Analyze category-wise and monthly expenses using interactive charts.
- **Payment Analytics:** Review expenses by payment method.
- **Export Reports:** Export expense records to CSV and Excel.
- **Data Validation:** Validate expense inputs to help maintain accurate records.
- **Automated Tests:** Test core expense-management and analytics functionality.

##  Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| SQLite | Database management |
| Pandas | Data processing and analysis |
| Plotly | Interactive charts and visualizations |
| Pytest | Automated testing |

##  Project Structure

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

##  Installation & Setup

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

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

##  Run Tests

Run the automated test suite using:

```bash
pytest -v
```

##  Database

The application uses SQLite to store expense and budget records. The database is initialized by the application's database module.

##  Future Improvements

- Cloud database integration
- User authentication
- Advanced financial analytics
- Improved reporting and visualization
- Online deployment

## 👨‍💻 Author

**Basit**

GitHub: [@Basit366](https://github.com/Basit366)

---

 If you find this project useful, consider giving it a star!