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

        # Calculate and display
