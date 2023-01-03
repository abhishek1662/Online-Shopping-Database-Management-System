import streamlit as st
import pandas as pd
from database import create_pay, add_pay, join, display, delete_cart, view_pay, check_cart, update_after_buy, cart_pro, payId, backup_cart


def pay(cus_id):
    st.subheader("Payment:")
    create_pay()
    st.text_input("Customer id:", cus_id)
    date = st.date_input("Date:")
    bank = st.text_input("Bank:")
    # total = 0
    if st.button("View total amount"):
        amount = display(cus_id)
        st.success('The amount to be paid is "{}"'.format(amount[0][0]))

    cart = check_cart()
    if cart:
        if st.button("Pay"):
            amount = display(cus_id)

            res = cart_pro()
            new_avail = []
            pro_id = []

            for i in range(len(res)):
                availability = res[i][2]
                quantity = res[i][3]
                avail = availability-quantity
                new_avail.append(avail)
                pro_id.append(res[i][0])

            flag = True
            for i in range(len(new_avail)):
                if new_avail[i] < 0:
                    flag = False
                    break

            if flag == True:
                add_pay(date, bank, amount[0][0], cus_id)
                id = payId(cus_id)
                pay_id = id[len(id)-1][0]
                st.success("Payment Done!!")

                joinRes = join(cus_id, pay_id)
                df = pd.DataFrame(joinRes, columns=[
                    'Cart Id', 'Name', 'Quantity', 'Amount', 'Total Cost', 'Pay Id', 'Date'])
                with st.expander("Payment Details"):
                    st.dataframe(df)

                for i in range(len(new_avail)):
                    update_after_buy(new_avail[i], pro_id[i])

                # back_up = backup_cart(cus_id)
                # df = pd.DataFrame(back_up, columns=[
                #                   'Cart Id', 'PId', 'Name', 'Quantity', 'Amount', 'Total Cost'])
                # if st.checkbox("BackUp cart"):
                #     st.dataframe(df)
                delete_cart(cus_id)

            else:
                st.warning(
                    "No of selected items are greater than availability")
