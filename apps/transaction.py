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
        wallet_address = st.session_state['wallet address']
        wei_balance = w3.eth.get_balance(wallet_address)
        # Convert Wei value to ether
        ether_amount = w3.fromWei(wei_balance, "ether")
        st.write(f'Wallet Address: {wallet_address}')
        st.write(f'Wallet Balance: {ether_amount} ETH')

