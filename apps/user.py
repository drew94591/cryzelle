import streamlit as st
from .account import Account


class User:
    user_id = ''
    name = ''
    password = ''
    phone_number = ''
    email_address = ''
    account = Account()

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def get_email_address(self):
        return self.email_address

    def set_email_address(self, email_address):
        self.email_address = email_address

    def get_account(self):
        return self.account

    def set_account(self, new_account):
        self.account = new_account

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
