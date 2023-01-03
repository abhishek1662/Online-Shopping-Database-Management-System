import streamlit as st
import pandas as pd
from database import create_pro, add_pro, view_pro1, delete_pro1, view_PId, view_pro2, update_pro, getNumberofProducts


def product(sel_id):
    # st.subheader("Products")

    menu = ["Choose", "Add", "View", "Delete", "Change"]
    choice = st.selectbox(
        "Do you want to add, view, delete or change product:", menu)
    if choice == 'Add':
        st.subheader("Add products")

        st.text_input("Seller Id:", sel_id)
        new_name = st.text_input("Product Name:")
        new_cost = st.text_input("Product Price:")
        new_type = st.text_input("Type of Product:")
        new_detail = st.text_input("Details:")
        availability = st.text_input("No of products available:")

        if st.button('add'):
            st.subheader("Add new products:")
            create_pro()
            add_pro(new_name, new_cost, new_type,
                    new_detail, availability, sel_id)
            st.success("You have successfully added the product")

    elif choice == 'View':
        if st.button("Total no of products"):
            st.subheader(getNumberofProducts(sel_id)[0][0])
        st.subheader("View existing products:")
        st.text_input("Seller Id:", sel_id)
        result = view_pro1(sel_id)
        df = pd.DataFrame(
            result, columns=['SId', 'PId', 'Name', 'Price', 'Type', 'Details', 'Availability'])
        st.dataframe(df)

    elif choice == 'Delete':
        st.subheader("Delete products:")
        sel_id = st.text_input('Seller Id:', sel_id)
        result = view_pro1(sel_id)
        df = pd.DataFrame(
            result, columns=['SId', 'PId', 'Name', 'Price', 'Type', 'Details', 'Availability'])
        with st.expander("Products available:"):
            st.dataframe(df)
        # with st.expander("Current products"):

        pro_id = st.text_input("Enter product ID that has to be deleted:")
        # st.warning("Do you want to delete??")
        if st.button("Delete Product"):
            delete_pro1(pro_id)
            st.success("Product has been deleted successfully")

        new_result = view_pro1(sel_id)
        df2 = pd.DataFrame(new_result, columns=[
                           'SId', 'PId', 'Name', 'Price', 'Type', 'Details', 'Availability'])
        with st.expander("Updated data"):
            st.dataframe(df2)

    elif choice == 'Change':
        st.subheader("Change product specs:")
        st.text_input('Seller Id:', sel_id)
        result = view_pro1(sel_id)
        df = pd.DataFrame(
            result, columns=['SId', 'PId', 'Name', 'Price', 'Type', 'Details', 'Availability'])
        st.dataframe(df)

        list_of_products = [i[0] for i in view_PId()]
        selected_pro = st.selectbox(
            "Select PId for the Product to be Edited", list_of_products)
        selected_res = view_pro2(selected_pro)
        if selected_res:
            name = selected_res[0][0]
            price = selected_res[0][1]
            type = selected_res[0][2]
            details = selected_res[0][3]
            avail = selected_res[0][4]
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Name:", name)
                new_price = st.text_input("Price:", price)
                new_type = st.text_input("Type:", type)
            with col2:
                new_detail = st.text_input("Details:", details)
                new_avail = st.text_input("Availability:", avail)

            if st.button("Update Product"):
                update_pro(new_name, new_price, new_type,
                           new_detail, new_avail, sel_id, selected_pro)
                st.success("Successfully updated product")
            result2 = view_pro1(sel_id)
            df2 = pd.DataFrame(result2, columns=[
                'SId', 'PId', 'Name', 'Price', 'Type', 'Details', 'Availability'])
            with st.expander("Updated data"):
                st.dataframe(df2)
