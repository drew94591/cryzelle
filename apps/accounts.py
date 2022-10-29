import streamlit as st


class Account:
    """
    This class will update, search and show details of the account widgets.
    """

    def details(self):
        st.title(f'Welcome *{st.session_state["name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone_number"]}')
        st.write(f'Wallet Address: {st.session_state["wallet_address"]}')

    def update(self):
        st.write('In Account Update Page...')

    def search(self, control_name: str, location: str = 'main'):
        if location == 'main':
            input_val = st.text_input("Enter a phone number or email address")

            if st.button(control_name):
                st.write(f"Value of input string: {input_val}")

        elif location == 'sidebar':
            input_val = st.sidebar.text_input(
                "Enter a phone number or email address")
            if st.sidebar.checkbox(control_name):
                st.write(f"Value of input string: {input_val}")
