from dotenv import load_dotenv
import cohere
import os
import streamlit as st
import pandas as pd
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

try:
    st.session_state.expenses = pd.read_csv("expenses.csv")
except:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount(₹)"])

load_dotenv()
# api_key = os.getenv('COHERE_API_KEY')
api_key= "Fc544AAFm9YvcqSRxZ1WjmTC6TUkHMwUxm11vgDb"
co = cohere.Client(api_key)

def get_budget_insights(user_query, transaction_text):
    prompt = f"""
You are Finbot, a friendly financial assistant built by Arpita for the Expense Tracker app.
- All amounts are stored in Indian Rupees (₹). Always answer in Rupees.
- Only answer financial queries (budgeting, expenses, savings).
- Use transaction history if needed, but give general advice even if data is limited.
- If user asks to add/delete expenses, say: "I can assist with the process but cannot directly make changes."
- If user asks about yourself, say: "I am Finbot, a financial assistant built by Ritika to help with budgeting and expense management."

User query: {user_query}
Transactions (if any):
{transaction_text}
"""
    response = co.chat(
        model="command-r-plus",
        message=prompt
    )
    return response.text.strip()

col1,col2,col3=st.columns([1,6,1])

with col2:
    with st.expander("💬 Chat with Finbot", expanded = True):
        st.markdown("<h3>Hi 👋 How can I help you today?</h3>", unsafe_allow_html=True)
        # ---------- Quick Preset Questions ----------
        st.markdown("💡 Quick Questions:")
        cols = st.columns(3)
        preset_questions = [
            "💰What is the Total Expense of this month?",
            "How much I spended on food🍔?",
            "How can I Improve my Savings💵?"
        ]
        triggered = False
        for i, q in enumerate(preset_questions):
            if cols[i].button(q):
                if "expenses" in st.session_state and not st.session_state.expenses.empty:
                    transactions_text = "\n".join(st.session_state.expenses.apply(
                        lambda row: f"{row['Date']} | {row['Category']} | {row['Description']} | {row['Amount(₹)']}", axis=1
                        ))
                    with st.spinner("🤖Finbot is thinking..."):
                        budget_tip = get_budget_insights(q , transactions_text)
                        st.text_area("💬 Finbot says:", value=budget_tip, height=200)
                        triggered = True
                else:
                    st.warning("⚠No transaction data available yet!")
                    transactions_text = ""

        if not triggered:
            st.info("Select a question above or ask your own below ✍.")


        user_query = st.text_input("Enter your question: ")

        if st.button("Send▶"):
            if user_query.strip():
                # if "expenses" in st.session_state and not st.session_state.expenses.empty:
                #     transactions_text = "\n".join(st.session_state.expenses.apply(
                #         lambda row: f"{row['Date']} | {row['Category']} | {row['Description']} | {row['Amount(₹)']}", axis=1
                #         ))
                #     with st.spinner("🤖Finbot is thinking..."):
                #         budget_tip = get_budget_insights(user_query , transactions_text)
                #         st.text_area("💬 Finbot says:", value=budget_tip, height=200)
                # else:
                #     st.warning("⚠No transaction data available yet!")
                #     transactions_text = ""
                if not st.session_state.expenses.empty:
                    transactions_text = "\n".join(st.session_state.expenses.apply(
                    lambda row: f"{row['Date']} | {row['Category']} | {row['Description']} | {row['Amount(₹)']}", axis=1
                        ))
                    budget_tip = get_budget_insights(user_query, transactions_text)
                    st.text_area("💬 Finbot says:", value=budget_tip, height=200)
                else:
                    st.warning("⚠ No transaction data available yet!")

            else:
                st.warning("Please Enter valid question.")