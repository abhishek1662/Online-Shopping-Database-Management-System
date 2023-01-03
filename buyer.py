import streamlit as st
import pandas as pd
from cus_pro import cus_pro
from database import create_cus, login_cus, view_cus, add_cus


def buyer():
    st.title("Welcome Guyzzz...!!")

    menu = ["Choose", "LOGIN", "REGISTER"]
    choice = st.sidebar.selectbox("Choose to Signup or Login:", menu)

    if choice == 'LOGIN':
        st.subheader("Login")

        username = st.text_input("Name:")
        password = st.text_input("Password:", type='password')

        if st.checkbox('login'):
            result = login_cus(username, password)
            if result:
                st.success("Logged in as {}".format(username))
                profile = view_cus(username, password)
                df = pd.DataFrame(profile, columns=[
                                  'ID', 'Name', 'Password', 'Phone No', 'Address', 'DOB', 'Age'])
                with st.expander("View Profile"):
                    st.dataframe(df)
                cus_id = df.iloc[:, 0]
                cus_pro(int(cus_id))
            else:
                st.warning("Incorrect password/username")

    elif choice == 'REGISTER':
        st.subheader("Register")

        new_user = st.text_input("Name:")
        new_password = st.text_input("Password:", type='password')
        new_phone = st.text_input("Phone No:")
        new_address = st.text_input("Address:")
        new_DOB = st.date_input("DOB:")

        if st.button('signup'):
            create_cus()
            add_cus(new_user, new_password, new_phone, new_address, new_DOB)

            st.success(
                "You have successfully created an account, Go back login page to login")
