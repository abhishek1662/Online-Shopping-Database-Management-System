import streamlit as st
import pandas as pd
from database import view_pro, show_pro, create_cart, add_cart, view_cart
from cart import View_Up_Del
from payment import pay


def cus_pro(cus_id):
    st.subheader("Available Products:")
    result = view_pro()
    df = pd.DataFrame(
        result, columns=['PId', 'Name', 'Price', 'Type', 'Details', "Availability"])
    with st.expander("View products"):
        st.dataframe(df)

    # buy = st.radio("Do you want to buy something??",
    #                ["Choose", "Yes", "No"])
    # if buy == 'Yes':

    st.subheader("Cart:")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Your Id:", cus_id)
        # if st.button("View cart"):
    # with col2:

    result1 = view_cart(cus_id)
    df = pd.DataFrame(
        result1, columns=['Cart Id', 'PId', 'Name', 'Quantity', 'Amount', 'Total Cost'])
    if st.button("View cart"):
        st.dataframe(df)

    # st.subheader("Select from the below option:")
    header = '<p style="font-size:20px;margin-bottom:-30px;margin-top:5px">Select from the below option:</p>'
    st.markdown(header, unsafe_allow_html=True)

    choose = st.radio(
        "Choose:", ["Select", "Add product to cart", "Update Cart", "Checkout"], label_visibility="hidden")
    if choose == "Add product to cart":
        st.subheader("Enter the product ID to add it to your cart:")
        create_cart()
        st.text_input("Customer Id:", cus_id)
        pro_id = st.text_input("Product Id:")
        quantity = st.number_input("Quantity:", min_value=1, step=True)
        price = show_pro(pro_id)
        if pro_id:
            tc = quantity*price[0][2]
            st.text_input("Name:", price[0][1])
            st.text_input("Price:", price[0][2])
            st.text_input("Total Cost:", tc)

            if st.button("add to cart"):
                add_cart(pro_id, price[0][1], quantity,
                         price[0][2], tc, cus_id)
                st.success("Your cart has been updated successfully")

    # elif buy == 'No':
    elif choose == "Update Cart":
        View_Up_Del(int(cus_id))

    elif choose == "Checkout":
        pay(int(cus_id))
