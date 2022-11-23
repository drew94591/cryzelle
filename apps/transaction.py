import streamlit as st
import datetime as dt
from .account import Account
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://52.87.239.109:8545'))

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
        st.write(f"You have {w3.eth.getTransactionCount(st.session_state['wallet address'])} total transactions")
        st.write(f"Your current balance is: {w3.eth.get_balance(st.session_state['wallet address'])}")
