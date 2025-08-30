import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import base64

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

if "expenses" not in st.session_state:
    try:
        st.session_state.expenses = pd.read_csv("expenses.csv")
    except:
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount(₹)"])

df=pd.read_csv("expenses.csv")
file="expenses.csv"

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
    st.header("📄 Expense Summary")
    if not df.empty:
        df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%b-%Y")
        df.index=df.index+1
        st.subheader("📃 All Expenses")
        st.dataframe(df)

        #monthly total
        monthly_total=df.groupby("Month")["Amount(₹)"].sum().reset_index()
        monthly_total.index=monthly_total.index+1
        st.subheader("📆 Monthly Total Expenses")
        st.dataframe(monthly_total.style.format({"Amount(₹)":"₹{:,.2f}"}))

        #download csv
        csv=df.to_csv(index=False).encode("utf-8")
        st.download_button(label="⬇️ Download Expenses as CSV", data=csv, file_name="expenses.csv", mime="text/csv")
        
    else:
        st.info("No expenses added yet.")