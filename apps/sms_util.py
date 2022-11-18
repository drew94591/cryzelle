import os
from twilio.rest import Client
import streamlit as st


class SMS:
    def invite(self, control_name: str, location: str = 'main'):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
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
                            body=body_msg,
                            from_=twilio_phone_number,
                            to=to_phone_number
                        )
                except:
                    with placeholder.container():
                        st.error("You've entered an invalid phone number!")
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
                                body=body_msg,
                                from_=twilio_phone_number,
                                to=to_phone_number
                            )
                    except:
                        with placeholder.container():
                            st.error("You've entered an invalid phone number!")
                    else:
                        with placeholder.container():
                            st.info("Message sent successfully!")
