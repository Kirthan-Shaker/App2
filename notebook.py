import streamlit as st
import pandas as pd
import altair as alt

# Title of the app
st.title("Personal Finance Management App")

# Sidebar for user inputs
st.sidebar.header("Add a new investment")

# Input fields for new investments
investment_name = st.sidebar.text_input("Investment Name")
investment_type = st.sidebar.selectbox("Investment Type", ["Stock", "Bond", "Mutual Fund", "Real Estate", "Cryptocurrency"])
amount_invested = st.sidebar.number_input("Amount Invested", min_value=0.0, step=100.0)
investment_date = st.sidebar.date_input("Investment Date")
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
        "Investment Date": investment_date
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
        color='Investment Type'
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart)
else:
    st.write("No investments added yet.")

# Display total amount invested
if st.session_state['investments']:
    total_invested = sum([investment["Amount Invested"] for investment in st.session_state['investments']])
    st.subheader(f"Total Amount Invested: ${total_invested:.2f}")
