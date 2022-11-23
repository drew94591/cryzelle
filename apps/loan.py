import streamlit as st
from .account import Account
from PIL import Image


class Loan:
    lender_account = Account()
    borrower_account = Account()
    term = ''
    interest_rate = 1.0

    def details(self):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        st.write("Details on how to package a loan here...")
        if st.button("Package A Loan"):
            self.package_loan()

        st.write("Details on how to take out a loan here...")

        if st.button("Takeout A Loan"):
            self.takeout_loan()

    def package_loan(self):
        st.write("Package A loan Initiated!")

    def takeout_loan(self):
        st.write("Takeout A loan Initiated!")
