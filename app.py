import streamlit as st
import base64
from seller import seller
from buyer import buyer


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/gif;base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('bg.gif')


def main():
    # st.title("ONLINE STORE")
    title = '<p style="font-family:Brush Script MT,cursive; color:cyan; font-size:100px;margin-left:170px;margin-top:-50px;margin-bottom:-24px">My Store</p>'
    st.markdown(title, unsafe_allow_html=True)

    # st.caption("#place where small shops get large customers")
    # tagline = '<p style="font-family:Courier; color:cyan; font-size: 20px;margin-top:-20px;margin-left:65px">#place where small stores get large customers</p>'
    # st.markdown(tagline, unsafe_allow_html=True)
    st.markdown('***')

    # st.info("Are you Seller or Buyer??")
    menu = ["Home", "Seller", "Buyer"]
    choice = st.sidebar.selectbox("Are you Seller or Buyer??", menu)

    if choice == 'home':
        st.sidebar.subheader("Home")

    elif choice == 'Seller':
        # st.sidebar.subheader("Welcome!!")
        seller()

    elif choice == 'Buyer':
        # st.sidebar.subheader("Welcome!!")
        buyer()


if __name__ == '__main__':
    main()
