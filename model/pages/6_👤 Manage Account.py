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

user_file="users.csv"

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
if not os.path.exists(user_file):
    users=pd.DataFrame(columns=["Name", "Username", "Password"])
    users.to_csv(user_file, index=False)
else:
    users = pd.read_csv(user_file)

#signup function
def sign_up(name, username, password):
    global users
    if username in users["Username"].values:
        st.info("⚠️Username already exists!")
        return
    new_user=pd.DataFrame([[name,username,password]], columns=["Name", "Username", "Password"])
    users=pd.concat([users, new_user], ignore_index=True)
    users.to_csv(user_file, index=False)
    st.success("✅Account Created Successfully!")

#login function
def log_in(username, password):
    if username not in users["Username"].values:
        st.error("❌Username does not exist!")
    elif users.loc[users["Username"] == username, "Password"].values[0] != password:
        st.error("❌Incorrect Password!")
    else:
        st.success(f"✅ Welcome {users[username]['name']}!")
        
col1,col2,col3=st.columns([1,6,1])

with col2:
    st.header("🔐 Login / Signup")
    menu=st.selectbox("Manage Account", ["Sign Up","Login"])
    if menu=="Sign Up":
        st.subheader("Create an Account")
        name=st.text_input("Full Name", placeholder="Enter your Full Name",kwargs={"autocomplete":"off"}, key="signup_name")
        username=st.text_input("Username", placeholder="Create a Username", kwargs={"autocomplete":"off"}, key="signup_username")
        password=st.text_input("Password", type="password", placeholder="Enter Password")
        if st.button("Sign Up"):
            sign_up(name, username, password)

    elif menu=="Login":
        st.subheader("Log In")
        username=st.text_input("Username", placeholder="Enter your Username", kwargs={"autocomplete":"off"}, key="login_username")
        password=st.text_input("Password", placeholder="Enter Password", type="password")
        if st.button("Login"):
            log_in(username, password)