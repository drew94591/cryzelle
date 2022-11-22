import streamlit as st

class Home:
    def page(self):
        st.title(f'Welcome *{st.session_state["first name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(
            f'Name: {st.session_state["first name"]} {st.session_state["last name"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone number"]}')
        wallet_address = st.session_state["wallet address"]
        st.write(f'Wallet Address: {wallet_address}')
        # TODO: get the wallet balance