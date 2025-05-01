import streamlit as st
from utils.expense_tracker import Account
import time

account = Account(db_name="User.db")

st.markdown("# ➕ Add Your Transactions")
st.markdown("Quickly record your income and expenses to stay on top of your finances.")
st.divider()

# Show current balance
st.session_state.balance = account.getBalance()
formatted_balance = f"₹ {st.session_state.balance:,.2f}"
st.success(f"💰 **Current Balance:** {formatted_balance}")

st.markdown("---")

# Define categories with emojis
income_categories = (
    "-", 
    "💼 Salary", 
    "📈 Investment", 
    "👨‍👩‍👧 Family", 
    "📦 Other"
)

expense_categories = (
    "-", 
    "🍔 Food", 
    "🧍 Personal", 
    "💊 Medical", 
    "🚗 Transport", 
    "📉 Investment", 
    "📦 Other"
)

# Create two side-by-side columns for Income and Expense forms
col1, col2 = st.columns(2)

# 💸 INCOME FORM
with col1:
    st.markdown("### Add Income")
    with st.expander("Add"):
        with st.form("income_form"):
            inName = st.text_input(" Income Title", placeholder="e.g. Salary from Company X")
            inDate = st.date_input(" Date of Income")
            inAmount = st.number_input(" Amount Earned", min_value=0.0, format="%.2f")
            inCateory = st.selectbox(" Category", income_categories)
            inDes = st.text_input(" Description", placeholder="Optional note...")
        
            submit_income = st.form_submit_button("✅ Add Income")

            if submit_income:
                account.addIncome(inDate, inName, inAmount, inCateory, inDes)
                st.session_state.balance += inAmount
                st.toast("Income Added Successfully!")
                time.sleep(1.5)
                st.rerun()

# 💳 EXPENSE FORM
with col2:
    st.markdown("###  Add Expense")
    with st.expander("Add"):
        with st.form("expense_form"):
            exName = st.text_input(" Expense Title", placeholder="e.g. Grocery shopping")
            exDate = st.date_input(" Date of Expense")
            exAmount = st.number_input(" Amount Spent", min_value=0.0, format="%.2f")
            exCateory = st.selectbox(" Category", expense_categories)
            exDes = st.text_input(" Description", placeholder="Optional note...")
        
            submit_expense = st.form_submit_button("✅ Add Expense")

            if submit_expense:
                account.addExpense(exDate, exName, exAmount, exCateory, exDes)
                st.session_state.balance -= exAmount
                st.toast("Expense Added Successfully!")
                time.sleep(1.5)
                st.rerun()
