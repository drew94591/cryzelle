import os
from twilio.rest import Client
import streamlit as st


class SMS:
    def invite(self, control_name: str, location: str = 'main'):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        if location == 'main':
            input_phone_number = st.text_input("Enter Phone Number")
            first_name = st.text_input("Friend's First Name")
            if st.button(control_name):
                st.write(
                    f"Phone Number: {input_phone_number} for {first_name}")
                body_msg = (f"Hello {first_name}, {st.session_state['first name']} {st.session_state['last name']} thought you might be interested in joining our network of friends!"
                            f" Just click this link https://drew94591-cryzelle-register-ytjnoc.streamlitapp.com/ to register and receive 100 free Ethereum tokens instantly just for signing up!")
                to_phone_number = f"+1{input_phone_number}"
                message = client.messages \
                    .create(
                        body=body_msg,
                        from_='+18316035984',
                        to=to_phone_number
                    )
                st.write(message.sid)
            elif location == 'sidebar':
                input_phone_number = st.sidebar.text_input(
                    "Enter Phone Number")
                first_name = st.text_input("Friend's First Name")
                if st.sidebar.checkbox(control_name):
                    st.write(
                        f"Phone Number: {input_phone_number} for {first_name}")
                    body_msg = (f"Hello {first_name}, {st.session_state['first name']} {st.session_state['last name']} thought you might be interested in joining our network of friends!"
                                f" Just click this link https://drew94591-cryzelle-register-ytjnoc.streamlitapp.com/ to register and receive 100 free Ethereum tokens instantly just for signing up!")
                    to_phone_number = f"+1{input_phone_number}"
                    message = client.messages \
                        .create(
                            body=body_msg,
                            from_='+18316035984',
                            to=to_phone_number
                        )
                    st.write(message.sid)
