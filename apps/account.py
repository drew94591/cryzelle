import streamlit as st
from .wallet import Wallet
from PIL import Image


class Account:
    """
    This class will update, search and show details of the account widgets.
    """
    wallet = Wallet()
    type = ''

    def details(self):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        st.title(f'Welcome *{st.session_state["first name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(
            f'Name: {st.session_state["first name"]} {st.session_state["last name"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone number"]}')
        st.write(f'Wallet Address: {st.session_state["wallet address"]}')

    def update(self):
        st.write('In Account Update Page...')
