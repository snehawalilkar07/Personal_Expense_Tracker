import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.expense_tracker import Account

# Setup
st.set_page_config(layout="wide")
sns.set_style("darkgrid")
account = Account(db_name="User.db")

st.title("📈 Let's Analyze Result")
st.caption("Analyze your income and spending patterns with beautiful visual insights.")
st.divider()

# Load Data
income_df = account.income_List()
expenses_df = account.expense_List()

# Normalize columns
def normalize_columns(df):
    df.columns = [col.strip().capitalize().replace("_", " ") for col in df.columns]
    return df

income_df = normalize_columns(income_df)
expenses_df = normalize_columns(expenses_df)

# Rename for consistency
income_df.rename(columns={"Income category": "Category", "Amount": "Amount"}, inplace=True)
expenses_df.rename(columns={"Expense category": "Category", "Amount": "Amount"}, inplace=True)


# Pie Charts: Equal Size
vis1, vis2 , vis3 = st.columns([1, 1, 1])

with vis1:
    st.subheader("🔴 Expenses by Category")
    if not expenses_df.empty and "Category" in expenses_df.columns:
        category_sum = expenses_df.groupby("Category")["Amount"].sum().sort_values()
        fig1, ax1 = plt.subplots(figsize=(5.5, 5.5), facecolor='none')
        ax1.axis("equal")
        colors_expense = sns.color_palette("Reds", len(category_sum))
        wedges, texts, autotexts = ax1.pie(
            category_sum.values,
            labels=None,
            colors=colors_expense,
            startangle=140,
            autopct='%1.1f%%',
            textprops={'color': 'white', 'fontsize': 10}
        )
        for i, text in enumerate(texts):
            text.set_text(f"{category_sum.index[i]}: ₹{category_sum.values[i]:,.0f}")
            text.set_color("white")
        ax1.set_title("Expenses by Category", color='white')
        fig1.patch.set_alpha(0.0)
        st.pyplot(fig1)
    else:
        st.info("No expenses data available.")

st.divider()
with vis2:
    st.subheader("🟢 Income by Category")
    if not income_df.empty and "Category" in income_df.columns:
        category_sum_income = income_df.groupby("Category")["Amount"].sum().sort_values()
        fig2, ax2 = plt.subplots(figsize=(5.5, 5.5), facecolor='none')
        ax2.axis("equal")
        colors_income = sns.color_palette("Greens", len(category_sum_income))
        wedges, texts, autotexts = ax2.pie(
            category_sum_income.values,
            labels=None,
            colors=colors_income,
            startangle=140,
            autopct='%1.1f%%',
            textprops={'color': 'white', 'fontsize': 10}
        )
        for i, text in enumerate(texts):
            text.set_text(f"{category_sum_income.index[i]}: ₹{category_sum_income.values[i]:,.0f}")
            text.set_color("white")
        ax2.set_title("Income by Category", color='white')
        fig2.patch.set_alpha(0.0)
        st.pyplot(fig2)
    else:
        st.info("No income data available.")

st.divider()

# Bar Chart: Compact and Blue Toned
with vis3:
    st.subheader("🔵 Income vs Expenses")
    if not income_df.empty and not expenses_df.empty:
        total_income = income_df["Amount"].sum()
        total_expense = expenses_df["Amount"].sum()
        balance = total_income - total_expense

        summary_df = pd.DataFrame({
            "Type": ["Income", "Expenses"],
            "Amount": [total_income, total_expense]
        })

        fig3, ax3 = plt.subplots(figsize=(5.5, 5.5), facecolor='none')
        ax3.axis("equal")
        colors = ["#4A90E2", "#50E3C2"]

        wedges, texts, autotexts = ax3.pie(
            summary_df["Amount"],
            labels=None,
            colors=colors,
            startangle=140,
            autopct='%1.1f%%',
            textprops={'color': 'white', 'fontsize': 10}
        )

        # Custom label with values
        for i, text in enumerate(texts):
            text.set_text(f"{summary_df['Type'][i]}: ₹{summary_df['Amount'][i]:,.0f}")
            text.set_color("white")

        ax3.set_title("Income vs Expenses", color='white')
        fig3.patch.set_alpha(0.0)
        st.pyplot(fig3)

    else:
        st.info("Insufficient data to compare income and expenses.")

st.success(f"💼 **Net Balance:** ₹ {balance:,.2f}")
