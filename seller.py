import streamlit as st
import pandas as pd
from product import product
from database import create_seller, login_seller, view_seller, add_seller, maxSeller


def seller():
    st.title("Welcome Sellers!!")

    st.subheader("Top Seller Id:")
    if st.button("Show"):
        st.subheader(maxSeller()[0][0])

    menu = ["Choose", "LOGIN", "REGISTER"]
    choice = st.sidebar.selectbox("New seller, Register else Login:", menu)

    if choice == 'LOGIN':
        st.subheader("Login")

        username = st.text_input("Name:")
        password = st.text_input("Password:", type='password')

        if st.checkbox('login'):
            result = login_seller(username, password)
            if result:
                st.success("Logged in as {}".format(username))
                profile = view_seller(username, password)
                df = pd.DataFrame(profile, columns=[
                                  'ID', 'Name', 'Password', 'Phone No', 'Address'])
                with st.expander("View Profile"):
                    st.dataframe(df)
                sel_id = df.iloc[:, 0]
                product(int(sel_id))

            else:
                st.warning("Incorrect password/username")

    elif choice == 'REGISTER':
        st.subheader("Register")

        new_user = st.text_input("Name:")
        new_password = st.text_input("Password:", type='password')
        new_phone = st.text_input("Phone No:")
        new_address = st.text_input("Address:")

        if st.button('signup'):
            create_seller()
            add_seller(new_user, new_password, new_phone, new_address)
            st.success(
                "You have successfully created an account, Go back login page to login")
