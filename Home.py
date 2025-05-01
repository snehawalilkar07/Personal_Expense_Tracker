# import pandas as pd
# import matplotlib.pyplot as plt
# import streamlit as st
# import seaborn as sns

# # if 'expenses' not in st.session_state:
# #     st.session_state.expenses = pd.DataFrame(columns=['Date','Category','Amount','Description'])

# st.title("CashCompass")
# st.write("This is your own personal expense tracker")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.expense_tracker import Account
import seaborn as sns

# Set wide layout and page title
st.set_page_config(page_title="CashCompass", layout="wide")

# Optional: add a nice title and subtitle
st.markdown(
    """
    <div style="text-align:center;">
        <h1 style='color:#4CAF50;'>💰 CashCompass</h1>
        <h4 style='color:gray;'>Your smart, simple, and sleek personal expense tracker</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Divider
st.markdown("---")

# Welcome content
st.markdown("""
    <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: #2a2e35; box-shadow: 0 0 10px rgba(0,0,0,0.2); color: #cbd5e1;    '>
        <h2>Welcome!</h2>
        <p>Use the navigation sidebar to:</p>
        <p>📝 Add your daily expenses</p>
        <p>📊 View your past transactions</p>
        <p>📈 Analyze your spending trends</p>
        <br>
        <p>Let's help you take control of your money!</p>
    </div>
""", unsafe_allow_html=True)


