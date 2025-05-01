import streamlit as st
from utils.expense_tracker import Account
import time

account = Account(db_name="User.db")

st.title("💼 Keep Track on Your Expenses")
st.divider()

st.markdown("### Current Balance")

balance = account.getBalance()
formatted_balance = f"₹ {balance:,.2f}"
st.success(f"**💰 Available Balance:** {formatted_balance}")

# View Income Section
st.subheader("💸 View Income")
income_df = account.income_List()

if income_df.empty:
    st.caption("No income records yet >_<")
else:
    st.dataframe(income_df, use_container_width=True)

    with st.expander("🗑️ Delete Income Entry"):
        with st.form("delete_income_form"):
            income_id = st.number_input("Enter Income ID to Delete", min_value=0, step=1)
            if st.form_submit_button("Delete Income"):
                account.deleteIncome(income_id)
                st.toast("Income Deleted Successfully!")
                time.sleep(1.5)
                st.rerun()

st.divider()

# 🧾 View Expenses Section
st.subheader("🧾 View Expenses")
expenses_df = account.expense_List()

if expenses_df.empty:
    st.caption("No expenses added yet >_<")
else:
    st.dataframe(expenses_df, use_container_width=True)

    with st.expander("🗑️ Delete Expense Entry"):
        with st.form("delete_expense_form"):
            expense_id = st.number_input("Enter Expense ID to Delete", min_value=0, step=1)
            if st.form_submit_button("Delete Expense"):
                account.deleteExpense(expense_id)
                st.toast("Expense Deleted Successfully!")
                time.sleep(1.5)
                st.rerun()
