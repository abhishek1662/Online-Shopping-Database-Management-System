import streamlit as st
import pandas as pd
from database import view_cart, view_par_cart, update_cart, delete_pro


def View_Up_Del(cus_id):
    # choice = st.selectbox("Do you wanna view cart or update the cart??", [
    #                       "Choose", "View", "Update/Delete"])
    # if choice == 'View':
    #     cus_id = st.text_input("Enter your Id:")
    #     result1 = view_cart(cus_id)
    #     df = pd.DataFrame(
    #         result1, columns=['PId', 'Name', 'Quantity', 'Amount', 'Total Cost'])
    #     st.dataframe(df)

    # elif choice == 'Update/Delete':
    # st.write("Hello")
    st.text_input("Customer ID:", cus_id)
    result1 = view_cart(cus_id)
    df = pd.DataFrame(result1, columns=[
        'Cart Id', 'PId', 'Name', 'Quantity', 'Amount', 'Total Cost'])
    # with st.expander("Cart"):
    st.dataframe(df)
    st.subheader("Enter the cart Id and product Id to update your cart:")
    cart_id = st.text_input("Enter yout Cart Id:")
    pro_id = st.text_input("Product Id:")
    row = view_par_cart(pro_id)

    if pro_id:
        # st.write(row)
        new_quantity = st.number_input("Quantity:", min_value=0, step=True)
        price = row[0][3]
        quantity = row[0][2]
        new_tc = new_quantity*price
        st.text_input("Name:", row[0][1])
        st.text_input("Price:", price)
        st.text_input("Total Cost", new_tc)
        if st.button("Update"):
            if new_quantity > 0:
                update_cart(new_quantity, new_tc, cart_id)
                st.success("Cart updated successfully")

            elif new_quantity == 0:
                delete_pro(pro_id)
                st.success(
                    "Product successfully removed from the cart")

        result2 = view_cart(cus_id)
        # st.write(result2)
        df2 = pd.DataFrame(result2, columns=[
            'Cart Id', 'PId', 'Name', 'Quantity', 'Amount', 'Total Cost'])
        with st.expander("Updated data"):
            st.dataframe(df2)
