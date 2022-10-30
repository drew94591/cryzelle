import streamlit as st
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://52.87.239.109:8545'))


class Home:
    def page(self):
        st.title(f'Welcome *{st.session_state["name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone_number"]}')
        wallet_address = ''
        wallet_addresses = w3.eth.accounts

        for i in wallet_addresses:
            st.session_state["wallet_address"] = i
            wallet_address = i
            # Get Balance of address in Wei
            wei_balance = w3.eth.get_balance(wallet_address)
            # Convert Wei value to ether
            ether_amount = w3.fromWei(wei_balance, "ether")
            st.write(f'Wallet Address: {wallet_address}')
            st.write(f'Wallet Balance: {ether_amount} ETH')
