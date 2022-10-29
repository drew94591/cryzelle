import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader
from apps import home_page, accounts, loans, sms_util, transactions

st.set_page_config(
    page_title="Login",
    page_icon=""
)


# Loading config file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


def set_left_nav():
    authenticator.logout("Logout", "sidebar")
    account = accounts.Account()
    #account.search("Search", "sidebar")
    trx = transactions.Transaction()

    choice = st.sidebar.selectbox(
        "Navigation", ["Home", "Search", "My Account", "Transaction History", "Send Cryptocurrency", "Request Cryptocurrency", "Loan Information", "Refer A Friend!"])
    if choice == "Home":
        home = home_page.Home()
        home.page()
    elif choice == "Search":
        account.search("Find", "main")
    elif choice == "My Account":
        account.details()
        # Creating an update account details widget
        try:
            if authenticator.update_account_details(st.session_state['username'], 'Account Details'):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)

        if st.button('Reset Password'):
            try:
                if authenticator.reset_password(st.session_state['username'], 'Reset password'):
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)
    elif choice == "Transaction History":
        trx.history()
    elif choice == "Send Cryptocurrency":
        trx.send()
    elif choice == "Request Cryptocurrency":
        trx.request()
    elif choice == "Loan Information":
        loan = loans.Loan()
        loan.details()
    elif choice == "Refer A Friend!":
        sms = sms_util.SMS()
        sms.invite()


def main():
    if not st.session_state["authentication_status"]:
        #hashed_passwords = stauth.Hasher(['SecretPassword55']).generate()
        #st.write(f'hashed_passwords: {hashed_passwords}')

        # creating a login widget
        name, authentication_status, username = authenticator.login(
            'Login', 'main')

        #st.write(f'authentication_status = {authentication_status}')

        if authentication_status:
            set_left_nav()
        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button('Forgot Password'):
                # Creating a forgot password widget
                try:
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password(
                        'Forgot password')
                    if username_forgot_pw:
                        st.write(f'random_password: {random_password}')
                        new_hashed_password = authenticator.Hasher(
                            [random_password]).generate()
                        st.write(f'new_hashed_password: {new_hashed_password}')

                        st.success('New password sent securely')
                        # Random password to be transferred to user securely
                    elif username_forgot_pw == False:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)
        with col2:
            if st.button('Forgot UserName'):
                # Creating a forgot username widget
                try:
                    username_forgot_username, email_forgot_username = authenticator.forgot_username(
                        'Forgot username')
                    if username_forgot_username:
                        st.success('Username sent securely')
                        # Username to be transferred to user securely
                    elif username_forgot_username == False:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)
        with col3:
            st.markdown(
                '<a href="https://drew94591-cryzelle-register-ytjnoc.streamlitapp.com" target="_self">Not Registered?</a>', unsafe_allow_html=True)
    else:
        set_left_nav()


if __name__ == "__main__":
    main()
