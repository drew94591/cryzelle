import streamlit as st
from .wallet import Wallet


class Account:
    """
    This class will update, search and show details of the account widgets.
    """
    wallet = Wallet()
    type = ''

    def details(self):
        st.title(f'Welcome *{st.session_state["first_name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(
            f'Name: {st.session_state["first_name"]} {st.session_state["last_name"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone_number"]}')
        st.write(f'Wallet Address: {st.session_state["wallet_address"]}')

    def update(self):
        st.write('In Account Update Page...')
