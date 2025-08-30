import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import base64

st.sidebar.title("💰 Expense Tracker")
img_path="model\\images\\bg2.jpeg"

with open(img_path,"rb") as f:
    encoded_img=base64.b64encode(f.read()).decode()

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
if "expenses" not in st.session_state:
    try:
        st.session_state.expenses = pd.read_csv("expenses.csv")
    except:
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount(₹)"])

df=pd.read_csv("expenses.csv")
file="expenses.csv"

col1,col2,col3=st.columns([1,6,1])

with col2:
    st.header("➕ Add Daily Expense")
    date=st.date_input("Select Date", datetime.today())
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    category=st.selectbox("Select Category",["Other", "Food", "Travel", "Shopping", "Bills"])
    desc=st.text_input("Expense Discription")
    amount=st.number_input("Amount(₹)", min_value=0.0, step=1.0)

    if st.button("Add Expense"):
        new_data=pd.DataFrame([[date, category, desc, amount]], columns=["Date", "Category","Description","Amount(₹)"])
        df=pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file, index=False)
        st.success("✅Expense Added Successfully!")