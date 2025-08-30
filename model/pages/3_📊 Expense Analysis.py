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

st.header("📉 Expense Analysis")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    this_month = df[df["Month"] == df["Date"].dt.to_period("M").max()]

    # KPIs
    total_expense = this_month["Amount(₹)"].sum()
    top_categories = this_month.groupby("Category")["Amount(₹)"].sum().nlargest(3)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expense (This Month)", f"₹{total_expense:,.0f}")
    col2.metric("Top Category", top_categories.index[0])
    col3.metric("Categories Tracked", df["Category"].nunique())

    # Budget status
    if budget > 0:
        if total_expense > budget:
            st.error(f"⚠️ You have exceeded your budget of ₹{budget:.0f}!")
        else:
            st.success(f"✅ You are within your budget of ₹{budget:.0f}!")
    else:
        st.info("No budget set yet. Go to settings to set a monthly budget.")

    col4, col5 = st.columns(2)
    with col4:
        fig1 = px.pie(
            df, values="Amount(₹)", names="Category",
            title="Expenses by Category", hole=0.4,
            color_discrete_sequence=px.colors.sequential.Teal
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col5:
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        fig3 = px.bar(
            df, x="Month", y="Amount(₹)",
            title="Monthly Expense Comparison", color="Month", hover_data=["Amount(₹)"]
        )
        st.plotly_chart(fig3, use_container_width=True)

    col6, col7 = st.columns(2)
    with col6:
        df["Month"] = df["Date"].dt.to_period("M")
        monthly = df.groupby("Month", as_index=False)["Amount(₹)"].sum()

        monthly["Budget"] = budget
        monthly["Month"] = monthly["Month"].dt.to_timestamp()

        fig2 = px.line(
            monthly, x="Month", y=["Amount(₹)", "Budget"],
            markers=True, title="Monthly Expenses vs Budget",
            color_discrete_map={"Budget": "red"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col7:
        fig4 = px.treemap(
            df, path=["Category"], values="Amount(₹)",
            title="Expense Distribution by Category",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("No expenses yet.")
