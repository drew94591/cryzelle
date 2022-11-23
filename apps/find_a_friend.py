import streamlit as st
from streamlit_authenticator.db_utils import get_user_profile_by_phone, get_user_profile_by_email
from PIL import Image


class Friend:
    def search(self):
        # Image Logo
        image = Image.open('images/cryzelle1.jpeg')
        st.image(image)
        st.markdown("# Find a Friend")
        st.text(" \n")
        st.text(" \n")

        st.write("Please enter your friends phone number or email.")
        friend = st.text_input("Phone or Email")
        at_sym = "@"
        phone = ""
        friend_information = []
        friend_information = None

        if st.button("Find"):
            # Check to see if email or phone number
            numbers = sum(c.isdigit() for c in friend)
            letters = sum(c.isalpha() for c in friend)

            if numbers > 8 and letters < 1:
                # Phone number check first

                for i in friend:
                    if i.isnumeric():
                        phone = phone + i

                if len(phone) > 10:
                    if phone[0] == "1":
                        phone = phone[1:]
                    else:
                        st.write(
                            "The phone number is too long, please try again.")

                if len(phone) == 10:
                    friend_information = get_user_profile_by_phone(phone)

            elif at_sym in friend:
                # Email check
                friend_information = get_user_profile_by_email(friend)

            else:
                # Neither

                st.write("Not a valid entry, please try again.")

            if friend_information != None:
                st.write("We found this person in our system.")

                # (first name, last name, mobile number, email)

                st.write("First Name: ", friend_information[0])
                st.write("Last Name: ", friend_information[1])
                st.write("Mobile Number: ", friend_information[2])
                st.write("Email: ", friend_information[3])
                st.text(" \n")

            elif friend_information == None:
                st.write(f"We could not find {friend} in our database.")
