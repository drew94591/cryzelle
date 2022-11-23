import streamlit as st
from PIL import Image
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://52.87.239.109:8545'))


class Home:
    def page(self):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)

        st.title(f'Welcome *{st.session_state["first name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(
            f'Name: {st.session_state["first name"]} {st.session_state["last name"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone number"]}')
        wallet_address = st.session_state["wallet address"]
        st.write(f'Wallet Address: {wallet_address}')
        wei_balance = w3.eth.get_balance(wallet_address)
        # Convert Wei value to ether
        ether_amount = w3.fromWei(wei_balance, "ether")
        st.write(f'Wallet Balance: {ether_amount} ETH')
