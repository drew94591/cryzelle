import streamlit as st
import datetime as dt
from .account import Account


class Transaction:
    from_account = Account()
    to_account = Account()
    tx_amount = 0
    tx_date = dt.datetime

    def send(self):
        st.write('In Transaction Send Page...')

    def request(self):
        st.write("In Transaction Request Page...")

    def history(self):
        st.write("In Transaction History Page...")
