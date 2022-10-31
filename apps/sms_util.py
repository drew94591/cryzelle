import os
from twilio.rest import Client
import streamlit as st


class SMS:
    def invite(self, control_name: str, location: str = 'main'):
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        if location == 'main':
            input_val = st.text_input("Enter Phone Number")
            first_name = st.text_input("Friend's First Name")
            if st.button(control_name):
                st.write(
                    f"Phone Number: {input_val} for {first_name}")
                message = client.messages \
                    .create(
                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        from_='+15017122661',
                        to='+17078530940'
                    )
                st.write(message.sid)
            elif location == 'sidebar':
                input_val = st.sidebar.text_input("Enter Phone Number")
                if st.sidebar.checkbox(control_name):
                    st.write(f"Phone Number: {input_val} for {first_name}")
                    message = client.messages \
                        .create(
                            body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                            from_='+15017122661',
                            to='+17078530940'
                        )
                    st.write(message.sid)
