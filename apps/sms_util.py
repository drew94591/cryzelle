import os
from dotenv import load_dotenv
from twilio.rest import Client
import streamlit as st
from streamlit_authenticator.db_utils import get_user_profile_by_phone
from PIL import Image


class SMS:
    def invite(self, control_name: str, location: str = 'main'):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        st.text(" \n")
        st.text(" \n")
        # Load .env envrionment variables
        load_dotenv()
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        messaging_service_id = os.environ['TWILIO_MESSAGING_SERVICE_ID']
        client = Client(account_sid, auth_token)
        placeholder = st.empty()
        placeholder.empty()

        if location == 'main':
            input_phone_number = st.text_input("Enter Phone Number")
            first_name = st.text_input("Friend's First Name")
            if st.button(control_name):
                try:
                    body_msg = (f"Hello {first_name}, {st.session_state['first name']} {st.session_state['last name']} thought you might be interested in joining our network of friends!"
                                f" Just click this link https://jollibeechicken.streamlit.app/ to register @cryptoXchange and receive 100 free Ethereum tokens instantly just for signing up!")
                    to_phone_number = f"+1{input_phone_number}"
                    message = client.messages \
                        .create(
                            messaging_service_sid=messaging_service_id,
                            body=body_msg,
                            to=to_phone_number
                        )
                except:
                    with placeholder.container():
                        st.error("Unable to send message!")
                else:
                    with placeholder.container():
                        st.info("Message sent successfully!")

        elif location == 'sidebar':
            input_phone_number = st.sidebar.text_input(
                "Enter Phone Number")
            first_name = st.text_input("Friend's First Name")
            if st.sidebar.checkbox(control_name):
                try:
                    body_msg = (f"Hello {first_name}, {st.session_state['first name']} {st.session_state['last name']} thought you might be interested in joining our network of friends!"
                                f" Just click this link https://jollibeechicken.streamlit.app/ to register @cryptoXchange and receive 100 free Ethereum tokens instantly just for signing up!")
                    to_phone_number = f"+1{input_phone_number}"
                    message = client.messages \
                        .create(
                            messaging_service_sid=messaging_service_id,
                            body=body_msg,
                            to=to_phone_number
                        )
                    with placeholder.container():
                        st.info("Message sent successfully!")
                except:
                    with placeholder.container():
                        st.error("Unable to send message!")

    def request(self, control_name: str, location: str = 'main'):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        messaging_service_id = os.environ['TWILIO_MESSAGING_SERVICE_ID']
        client = Client(account_sid, auth_token)
        placeholder = st.empty()
        placeholder.empty()
        friend_information = []

        if location == 'main':

            st.markdown("# Request Crypto from a Friend")
            st.text(" \n")
            st.text(" \n")
            st.write(
                "Please enter the phone number for a friend that is in our network.")
            st.write("Followed by the amount you would like to request in Eth.")
            st.text(" \n")
            input_phone_number = st.text_input("Friend's Phone Number")
            amount = st.text_input("Amount you wish to request.")
            phone_number = ""

            if st.button(control_name):

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
                    friend_information = get_user_profile_by_phone(
                        phone_number)

                if friend_information == None:
                    st.write(
                        f"We could not find {phone_number} in our database.")

                try:
                    body_msg = (f"Hello {friend_information[0]}, {st.session_state['first name']} {st.session_state['last name']} wished to request {amount} Eth from you."
                                f" Please sign in to your account and go to the Send page to send {st.session_state['first name']} the requested amount.")
                    to_phone_number = f"+1{phone_number}"
                    message = client.messages \
                        .create(
                            messaging_service_sid=messaging_service_id,
                            body=body_msg,
                            to=to_phone_number
                        )
                    with placeholder.container():
                        st.info(
                            f"Message sent successfully! Please wait for {friend_information[0]} to sign-on and check on your request.")
                except:
                    with placeholder.container():
                        st.error("Unable to send message!")
