import streamlit as st


class Home:
    def page(self):
        st.title(f'Welcome *{st.session_state["name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone_number"]}')
        st.write(f'Wallet Address: {st.session_state["wallet_address"]}')
        st.write(f'Wallet Balance: 100 ETH')
