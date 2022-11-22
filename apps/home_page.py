import streamlit as st

class Home:
    def page(self):
        st.title(f'Welcome *{st.session_state["first name"]}*')
        st.write(f'User Name: {st.session_state["username"]}')
        st.write(
            f'Name: {st.session_state["first name"]} {st.session_state["last name"]}')
        st.write(f'Email: {st.session_state["email"]}')
        st.write(f'Phone Number: {st.session_state["phone number"]}')
        count = 0
        wallet_address = ''
        addresses = w3.eth.accounts

        for address in addresses:
            if count == 0:
                st.session_state["wallet address"] = address
            wallet_address = address
            # Get Balance of address in Wei
            wei_balance = w3.eth.get_balance(wallet_address)
            # Convert Wei value to ether
            ether_amount = w3.fromWei(wei_balance, "ether")
            st.write(f'Wallet Address: {wallet_address}')
            st.write(f'Wallet Balance: {ether_amount} ETH')
            count = count + 1
