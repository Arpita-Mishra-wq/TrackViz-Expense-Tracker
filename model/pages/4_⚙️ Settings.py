import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import base64

if "expenses" not in st.session_state:
    try:
        st.session_state.expenses = pd.read_csv("expenses.csv")
    except:
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount(₹)"])

st.sidebar.title("💰 Expense Tracker")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #383838;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df=pd.read_csv("expenses.csv")
file="expenses.csv"

budget_file="budget.txt"
if os.path.exists(budget_file):
    with open(budget_file, "r") as f:
        budget=float(f.read())
else:
    budget=0.0

img_path="model\\images\\bg2.jpeg"

with open(img_path,"rb") as f:
    encoded_img=base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
    
col1,col2,col3=st.columns([1,6,1])

with col2:
    st.header("⚙️ Settings")

    st.subheader("🎯Set Monthly Budget")
    new_budget=st.number_input("Enter your monthly budget (₹)", min_value=0.0, step=100.0, value=budget)

    if st.button("Save Budget"):
        with open(budget_file, "w") as f:
            f.write(str(new_budget))
        st.success(f"Budget set to ₹{new_budget:,.0f}")
        budget=new_budget

    st.subheader("🔄️ Reset / Clear Expenses")
    col1, col2=st.columns(2)
    with col1:
        if st.button("Clear All Data"):
            df=pd.DataFrame(columns=["Date", "Category", "Amount(₹)"])
            df.to_csv(file, index=False)
            st.success("All expense data cleared!")

    with col2:
        if st.button("Reset Current Month"):
            df["Date"]=pd.to_datetime(df["Date"])
            current_month=df["Date"].dt.to_period("M").max()
            df=df[df["Date"].dt.to_period("M") != current_month]
            df.to_csv(file, index=False)
            st.success("Current month expenses reset!")