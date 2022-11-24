from PIL import Image
import os
from dotenv import load_dotenv
import streamlit as st
import datetime as dt
from twilio.rest import Client
from .account import Account
from streamlit_authenticator.db_utils import get_default_active_user_wallet_by_phone
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://52.87.239.109:8545'))


class Transaction:
    from_account = Account()
    to_account = Account()
    tx_amount = 0
    tx_date = dt.datetime

    def send(self, location: str = 'main'):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        # Load .env envrionment variables
        load_dotenv()

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        messaging_service_id = os.environ['TWILIO_MESSAGING_SERVICE_ID']
        client = Client(account_sid, auth_token)
        placeholder = st.empty()
        placeholder.empty()
        friend_information = None

        if location == 'main':

            st.markdown("# Send Crypto from a Friend")
            st.text(" \n")
            st.text(" \n")
            st.write(
                "Please enter the phone number for a friend that is in our network.")
            st.write("Followed by the amount you would like to send in Eth.")
            st.text(" \n")
            input_phone_number = st.text_input(
                "Friend's Phone Number", max_chars=10)
            amount = st.text_input("Amount you wish to send.")
            phone_number = ""
            source_account = st.session_state['wallet address']

            if st.button("SEND"):

                for i in input_phone_number:
                    if i.isnumeric():
                        phone_number = phone_number + i

                if len(phone_number) > 10:
                    if phone_number[0] == "1":
                        phone_number = phone_number[1:]
                    else:
                        st.write(
                            "The phone number is too long, please try again.")

                if len(phone_number) == 10:
                    friend_information = get_default_active_user_wallet_by_phone(
                        phone_number)
                    if friend_information is None:
                        st.write(
                            f"We could not find {phone_number} in our database.")

                    else:
                        destination_account = friend_information.wallet_link
                        try:
                            # Set gas price strategy
                            w3.eth.setGasPriceStrategy(
                                medium_gas_price_strategy)

                            # Convert eth amount to Wei
                            value = w3.toWei(amount, "ether")

                            # Calculate gas estimate
                            gasEstimate = w3.eth.estimateGas(
                                {"to": destination_account, "from": source_account, "value": value})

                            # Construct a raw transaction
                            raw_tx = {
                                "to": destination_account,
                                "from": source_account,
                                "value": value,
                                "gas": gasEstimate,
                                "gasPrice": 0
                            }

                            # Sign the raw transaction with ethereum account
                            sent_txn = w3.eth.send_transaction(raw_tx)
                            st.write(sent_txn)

                            body_msg = (f"Hello {friend_information[3]}, {st.session_state['first name']} {st.session_state['last name']} sent you {amount} Eth."
                                        f" Please sign in to your account to check your current balance.")
                            to_phone_number = f"+1{phone_number}"
                            message = client.messages \
                                .create(
                                    messaging_service_sid=messaging_service_id,
                                    body=body_msg,
                                    to=to_phone_number
                                )
                            with placeholder.container():
                                st.info(
                                    f"Your friend received a Message for transaction: {sent_txn}.")
                        except:
                            with placeholder.container():
                                st.error("Unable to send transaction!")

    def request(self):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        st.write("In Transaction Request Page...")

    def history(self):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        st.text(" \n")
        st.text(" \n")
        wallet_address = st.session_state['wallet address']

        wei_balance = w3.eth.get_balance(wallet_address)
        # Convert Wei value to ether
        ether_amount = w3.fromWei(wei_balance, "ether")

        transaction_count = w3.eth.get_transaction_count(wallet_address)

        st.write(f'Wallet Address: {wallet_address}')
        st.write(f'Wallet Balance: {ether_amount} ETH')
        st.write(f'Total number of Transactions: {transaction_count}')
