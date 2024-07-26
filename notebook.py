import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# Title and description of the app
st.image("https://miro.medium.com/v2/resize:fit:1400/0*bHrRhzNjMW5dEHJM.png", use_column_width=True, width=1000)
st.title("Welcome to Your Investment and Budget Tracker")
st.write("""
## Personal Finance Management App
This app allows you to track your investments across different asset classes and manage your monthly budgets. You can add new investments, view your portfolio, analyze your investment data with risk metrics, and keep track of your spending.
Features include:
- Adding investments with details like investment name, type, amount, date, currency, and stock name.
- Viewing and analyzing your investment portfolio.
- Visualizing your investments with charts.
- Tracking total amount invested.
- Calculating and visualizing risk metrics.
- Managing monthly budgets and tracking spending.
- Placeholder for fetching and storing stock fundamentals.

Developed by Kirthan Shaker Iyangar.
""")

# Creating tabs for Investment Tracker, Stock Fundamentals, and Budget Tracker
tab1, tab2, tab3 = st.tabs(["Investment Tracker", "Stock Fundamentals", "Budget Tracker"])

with tab1:
    # Sidebar for user inputs
    st.sidebar.header("How to Use This App")
    st.sidebar.write("""
    1. Enter the details of your investment in the fields below.
    2. Click "Add Investment" to save the investment.
    3. View your investments in the main table.
    4. Analyze your investment data with the provided charts and risk metrics.
    """)

    st.sidebar.header("Add a New Investment")

    # Input fields for new investments
    investment_name = st.sidebar.text_input("Investment Name")
    investment_type = st.sidebar.selectbox("Investment Type", ["Stock", "Bond", "Mutual Fund", "Real Estate", "Cryptocurrency"])
    amount_invested = st.sidebar.number_input("Amount Invested", min_value=0.0, step=100.0)
    investment_date = st.sidebar.date_input("Investment Date")
    currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "INR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
    stock_name = st.sidebar.text_input("Stock Name (if applicable)")
    expected_return = st.sidebar.number_input("Expected Annual Return (%)", min_value=-100.0, max_value=100.0, step=1.0)
    add_investment = st.sidebar.button("Add Investment")

    # Data storage for investments
    if 'investments' not in st.session_state:
        st.session_state['investments'] = []

    # Adding new investment to the list
    if add_investment:
        st.session_state['investments'].append({
            "Investment Name": investment_name,
            "Investment Type": investment_type,
            "Amount Invested": amount_invested,
            "Investment Date": investment_date,
            "Currency": currency,
            "Stock Name": stock_name,
            "Expected Return (%)": expected_return
        })
        st.sidebar.success("Investment added successfully!")

    # Display investments
    st.header("Your Investments")

    if st.session_state['investments']:
        df = pd.DataFrame(st.session_state['investments'])
        st.dataframe(df)

        # Bar chart of investments
        st.subheader("Investment Summary")
        chart = alt.Chart(df).mark_bar().encode(
            x='Investment Type',
            y='Amount Invested',
            color='Investment Type',
            tooltip=['Investment Name', 'Amount Invested', 'Currency', 'Stock Name', 'Investment Date', 'Expected Return (%)']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart)

        # Display total amount invested
        total_invested = sum([investment["Amount Invested"] for investment in st.session_state['investments']])
        st.subheader(f"Total Amount Invested: ${total_invested:.2f}")

        # Calculate and display risk metrics
        st.subheader("Risk Analysis")
        
        def calculate_risk_metrics(df):
            df['Volatility'] = np.random.uniform(10, 30, len(df))  # Placeholder for volatility
            df['Sharpe Ratio'] = df['Expected Return (%)'] / df['Volatility']  # Simplified Sharpe Ratio
            return df

        df = calculate_risk_metrics(df)
        st.dataframe(df[['Investment Name', 'Investment Type', 'Amount Invested', 'Expected Return (%)', 'Volatility', 'Sharpe Ratio']])

        # Risk metrics chart
        risk_chart = alt.Chart(df).mark_circle(size=60).encode(
            x='Volatility',
            y='Expected Return (%)',
            color='Investment Type',
            tooltip=['Investment Name', 'Volatility', 'Expected Return (%)', 'Sharpe Ratio']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(risk_chart)
    else:
        st.write("No investments added yet.")

with tab2:
    st.header("Stock Fundamentals")

    stock_ticker = st.text_input("Enter Stock Ticker")
    fetch_fundamentals = st.button("Fetch Fundamentals")

    if fetch_fundamentals:
        # Placeholder for fetching fundamentals
        st.write("This feature is currently unavailable. Please install yfinance to enable this feature.")

    # Display stored fundamentals
    if 'fundamentals' in st.session_state and st.session_state['fundamentals']:
        selected_ticker = st.selectbox("Select Stock Ticker to View Fundamentals", list(st.session_state['fundamentals'].keys()))

        if selected_ticker:
            fundamentals = st.session_state['fundamentals'][selected_ticker]
            st.write(f"### Fundamentals for {selected_ticker}")
            st.json(fundamentals)

with tab3:
    st.header("Budget Tracker")

    # Sidebar for budget tracker
    st.sidebar.header("Add a Budget")

    # Input fields for budget
    budget_category = st.sidebar.text_input("Category (e.g., Food, Rent, Entertainment)")
    budget_amount = st.sidebar.number_input("Budget Amount", min_value=0.0, step=100.0)
    budget_currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "INR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
    budget_date = st.sidebar.date_input("Date")
    add_budget = st.sidebar.button("Add Budget")

    # Data storage for budgets
    if 'budgets' not in st.session_state:
        st.session_state['budgets'] = []

    # Adding new budget to the list
    if add_budget:
        st.session_state['budgets'].append({
            "Category": budget_category,
            "Budget Amount": budget_amount,
            "Currency": budget_currency,
            "Date": budget_date,
            "Spent": 0.0
        })
        st.sidebar.success("Budget added successfully!")

    # Display budgets
    st.header("Your Budgets")

    if st.session_state['budgets']:
        df_budgets = pd.DataFrame(st.session_state['budgets'])
        st.dataframe(df_budgets)

        # Function to update spending
        def update_spending(category, date, amount, currency):
            for budget in st.session_state['budgets']:
                if budget["Category"] == category and budget["Date"] == date and budget["Currency"] == currency:
                    budget["Spent"] += amount
                    st.success("Spending updated successfully!")
                    break

        # Input fields to update spending
        st.subheader("Update Spending")
        spend_category = st.selectbox("Category to Update", list(set([budget["Category"] for budget in st.session_state['budgets']])))
        spend_date = st.date_input("Date to Update")
        spend_currency = st.selectbox("Currency", ["USD", "EUR", "INR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
        amount_spent = st.number_input("Amount Spent", min_value=0.0, step=10.0)
        update_spend = st.button("Update Spending")

        if update_spend:
            update_spending(spend_category, spend_date, amount_spent, spend_currency)

        # Display updated budgets
        df_budgets = pd.DataFrame(st.session_state['budgets'])
        st.dataframe(df_budgets)

        # Bar chart of budget vs spending
        st.subheader("Budget vs Spending")
        budget_chart = alt.Chart(df_budgets).mark_bar().encode(
            x='Category',
            y='Budget Amount',
            color='Category',
            tooltip=['Category', 'Budget Amount', 'Currency', 'Spent', 'Date']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(budget_chart)

        # Spending chart
        st.subheader("Spending Analysis")
        spend_chart = alt.Chart(df_budgets).mark_bar().encode(
            x='Category',
            y='Spent',
            color='Category',
            tooltip=['Category', 'Spent', 'Budget Amount', 'Currency', 'Date']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(spend_chart)
    else:
        st.write("No budgets added yet")
