import streamlit as st
import datetime as dt
from .account import Account
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

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
        st.write(w3.eth.getTransaction(st.session_state['wallet address']))