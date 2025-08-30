import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import base64

file="expenses.csv"
budget_file="budget.txt"

st.set_page_config(layout="wide")

image_path="model\\images\\bg1.jpg"

with open(image_path,"rb") as f:
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
        /* filter: contrast(1.5);*/
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# initializing expenses csv
if not os.path.exists(file):
    df=pd.DataFrame(columns=["Date", "Category","Description", "Amount(₹)"])
    df.to_csv(file, index=False)

if "expenses" not in st.session_state:
    try:
        st.session_state.expenses = pd.read_csv("expenses.csv")
    except:
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount(₹)"])

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

col1,col2,col3=st.columns([1,11,1])

with col2:
    col4,col5=st.columns([1,3])
    with col4:
        st.image("model\\images\\logo.png", width=210)
    #Load data
        df=pd.read_csv(file)

    #loading budget
    if os.path.exists(budget_file):
        with open(budget_file, "r") as f:
            budget=float(f.read())
    else:
        budget=0.0
    
    with col5:
        st.sidebar.title("💰 Expense Tracker")
        st.write("")
        st.header("Welcome to Your Expense Tracker!💰")
        st.subheader(""" Track your daily expenses, analyze spending patterns, and stay within budget. """)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    df_month = df[df["Month"] == df["Date"].dt.to_period("M").max()]
    total_expense=df_month["Amount(₹)"].sum()

    num_transac=len(df_month)

    days_in_month=datetime.now().day
    avg_daily_spending=round(total_expense/days_in_month,2) if days_in_month>0 else 0

    remaining_budget=budget-total_expense

    #kpis
    this_month = df[df["Month"] == df["Date"].dt.to_period("M").max()]
    st.write("")
    col6,col7=st.columns(2)
    with col6:
        st.metric("**💰 Total expenses(This Month)**",f"₹{total_expense}")
    with col7:
        st.metric("**💵 Remaining Budget**", f"₹{remaining_budget}")
    st.write("")

    col8,col9=st.columns(2)
    with col8:
        st.metric("**📉 Average Daily Spending**",f"₹{avg_daily_spending}")
    with col9:
        st.metric("**📜 Transactions (This Month)**", num_transac)

