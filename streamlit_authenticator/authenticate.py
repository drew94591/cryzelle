import jwt
import bcrypt
import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx
import streamlit_authenticator.db_utils as db
from streamlit_authenticator.wallet_utils import get_free_wallet_link

from .hasher import Hasher
from .utils import generate_random_pw

from .exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError


class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot username, and modify user details widgets.
    """

    def __init__(self, cookie_name: str, key: str, cookie_expiry_days: int = 30,
                 preauthorized: list = None):
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------
        credentials: dict
            The dictionary of usernames, names, passwords, and emails.
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: int
            The number of days before the cookie expires on the client's browser.
        preauthorized: list
            The list of emails of unregistered users authorized to register.
        """
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        self.preauthorized = preauthorized
        self.cookie_manager = stx.CookieManager()

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'first name' not in st.session_state:
            st.session_state['first name'] = None
        if 'last name' not in st.session_state:
            st.session_state['last name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'email' not in st.session_state:
            st.session_state['email'] = None
        if 'phone number' not in st.session_state:
            st.session_state['phone number'] = None
        if 'wallet address' not in st.session_state:
            st.session_state['wallet address'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
        if 'search' not in st.session_state:
            st.session_state['search'] = None

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({'name': st.session_state['name'],
                           'username': st.session_state['username'],
                           'exp_date': self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_pw(self, saved_password) -> bool:
        """
        Checks the validity of the entered password.

        Parameters
        ----------
        saved_password: str
        
        Returns
        -------
        bool
            The validity of the entered password by comparing it to the hashed password on db.
        """
        return bcrypt.checkpw(self.password.encode(),
                              saved_password.encode())

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'username' in self.token:
                            st.session_state['name'] = self.token['name']
                            st.session_state['username'] = self.token['username']
                            st.session_state['authentication_status'] = True

    def _check_credentials(self, inplace: bool = True) -> bool:
        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        inplace: bool
            Inplace setting, True: authentication status will be stored in session state, 
            False: authentication status will be returned as bool.
        Returns
        -------
        bool
            Validity of entered credentials.
        """
        
        user_credential = db.get_user_credentials(self.username)
        
        if user_credential is not None and user_credential.username == self.username:
            
            try:
                if self._check_pw(user_credential.password):
                    if inplace:
                        user_profile = db.get_user_profile_by_id(user_credential.id)
                        wallet = db.get_default_active_user_wallet_by_user_id(user_credential.id)
                        st.session_state['user_id'] = user_credential.id
                        st.session_state['profile_id'] = user_profile.id
                        st.session_state['first name'] = user_profile.first_name
                        st.session_state['last name'] = user_profile.last_name
                        st.session_state['email'] = user_profile.email_address
                        st.session_state['phone number'] = user_profile.mobile_number
                        st.session_state['wallet_id'] = wallet.id
                        st.session_state['wallet address'] = wallet.wallet_link
                        self.exp_date = self._set_exp_date()
                        self.token = self._token_encode()
                        self.cookie_manager.set(self.cookie_name, self.token,
                                                expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                        st.session_state['authentication_status'] = True
                    else:
                        return True
                else:
                    if inplace:
                        st.session_state['authentication_status'] = False
                    else:
                        return False
            except Exception as e:
                print(e)
        else:
            if inplace:
                st.session_state['authentication_status'] = False
            else:
                return False

    def login(self, form_name: str, location: str = 'main') -> tuple:
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            Username of the authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(form_name)
                self.username = login_form.text_input('Username').lower()
                st.session_state['username'] = self.username
                self.password = login_form.text_input(
                    'Password', type='password')

                if login_form.form_submit_button('Login'):
                    self._check_credentials()

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['username']

    def reset_session_state(self):
        st.session_state['logout'] = True
        st.session_state['name'] = None
        st.session_state['first name'] = None
        st.session_state['last name'] = None
        st.session_state['username'] = None
        st.session_state['user_id'] = None
        st.session_state['wallet_id'] = None
        st.session_state['profile_id'] = None
        st.session_state['wallet address'] = None
        st.session_state['authentication_status'] = None     

    def logout(self, button_name: str, location: str = 'main'):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name):
                self.cookie_manager.delete(self.cookie_name)
                self.reset_session_state()
        elif location == 'sidebar':
            if st.sidebar.button(button_name):
                self.cookie_manager.delete(self.cookie_name)
                self.reset_session_state()

    def _update_password(self, username: str, password: str):
        """
        Updates credentials data in DB with user's reset hashed password.

        Parameters
        ----------
        username: str
            The username of the user to update the password for.
        password: str
            The updated plain text password.
        """
        hashed_password = Hasher([password]).generate()[0]
        output = db.update_password(username, hashed_password)
        if output is None:
            raise ResetError("Unable to update password")

    def reset_password(self, username: str, form_name: str, location: str = 'main') -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        username: str
            The username of the user to reset the password for.
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        Returns
        -------
        str
            The status of resetting the password.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            reset_password_form = st.form('Reset password')
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Reset password')

        reset_password_form.subheader(form_name)
        self.username = username.lower()
        self.password = reset_password_form.text_input(
            'Current password', type='password')
        new_password = reset_password_form.text_input(
            'New password', type='password')
        new_password_repeat = reset_password_form.text_input(
            'Repeat password', type='password')

        if reset_password_form.form_submit_button('Reset'):
            if self._check_credentials(inplace=False):
                if len(new_password) > 0:
                    if new_password == new_password_repeat:
                        if self.password != new_password:
                            self._update_password(self.username, new_password)
                            return True
                        else:
                            raise ResetError(
                                'New and current passwords are the same')
                    else:
                        raise ResetError('Passwords do not match')
                else:
                    raise ResetError('No new password provided')
            else:
                raise CredentialsError

    def _register_credentials(self, username: str, first_name: str, last_name: str, password: str, email: str, phone_number: str, preauthorization: bool):
        """
        Adds to credentials dictionary the new user's information.

        Parameters
        ----------
        username: str
            The username of the new user.
        first_name: str
            The first name of the new user.
        last_name: str
            The last name of the new user.
        password: str
            The password of the new user.
        email: str
            The email of the new user.
        phone_number: str
            The phone number of the new user.            
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        """
        
        wallet_link = get_free_wallet_link()
        if wallet_link is None:
                raise RegisterError('No more free wallet available.')

        hashed_password = Hasher([password]).generate()[0]
        user = db.create_user(username, hashed_password)        
        profile = db.create_user_profile(user, first_name, last_name, phone_number, email)
        wallet = db.create_wallet(user, "DEFAULT", wallet_link)

        st.session_state['user_id'] = user
        st.session_state['profile_id'] = profile
        st.session_state['first name'] = first_name
        st.session_state['last name'] = last_name
        st.session_state['email'] = email
        st.session_state['phone number'] = phone_number
        st.session_state['wallet_id'] = wallet
        st.session_state['wallet address'] = wallet_link

        if preauthorization:
            self.preauthorized['emails'].remove(email)

    def register_user(self, form_name: str, location: str = 'main', preauthorization=True) -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """
        if not self.preauthorized:
            raise ValueError("preauthorization argument must not be None")
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form('Register user')
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        register_user_form.subheader(form_name)
        new_email = register_user_form.text_input('Email')
        new_phone_number = register_user_form.text_input('Phone Number')
        new_username = register_user_form.text_input('Username').lower()
        new_first_name = register_user_form.text_input('First Name')
        new_last_name = register_user_form.text_input('Last Name')
        new_password = register_user_form.text_input(
            'Password', type='password')
        new_password_repeat = register_user_form.text_input(
            'Repeat password', type='password')

        if register_user_form.form_submit_button('Register'):
            if len(new_email) and len(new_phone_number) and len(new_username) and len(new_first_name) and len(new_last_name) and len(new_password) > 0:
                if db.get_user_credentials(new_username) is None:
                    if new_password == new_password_repeat:
                        if preauthorization:
                            if new_email in self.preauthorized['emails']:
                                self._register_credentials(
                                    new_username, new_first_name, new_last_name, new_password, new_email, new_phone_number, preauthorization)
                                return True
                            else:
                                raise RegisterError(
                                    'User not preauthorized to register')
                        else:
                            self._register_credentials(
                                new_username, new_first_name, new_last_name, new_password, new_email, new_phone_number, preauthorization)
                            return True
                    else:
                        raise RegisterError('Passwords do not match')
                else:
                    raise RegisterError('Username already taken')
            else:
                raise RegisterError(
                    'Please enter an email, phone number, username, first name, last name, and password')

    def forgot_password(self, form_name: str, location: str = 'main') -> tuple:
        """
        Creates a forgot password widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot password form.
        location: str
            The location of the forgot password form i.e. main or sidebar.
        Returns
        -------
        str
            Username associated with forgotten password.
        str
            Email associated with forgotten password.
        str
            New plain text password that should be transferred to user securely.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_password_form = st.form('Forgot password')
        elif location == 'sidebar':
            forgot_password_form = st.sidebar.form('Forgot password')

        forgot_password_form.subheader(form_name)
        username = forgot_password_form.text_input('Username').lower()

        if forgot_password_form.form_submit_button('Submit'):
            if len(username) > 0:
                credential = db.get_user_credentials(username)
                if credential is not None:
                    return username, credential.email, self._set_random_password(username)
                else:
                    return False, None, None
            else:
                raise ForgotError('Username not provided')
        return None, None, None

    def _get_username(self, key: str, value: str) -> str:
        """
        Retrieves username based on a provided entry.

        Parameters
        ----------
        key: str
            Name of the credential to query i.e. "email".
        value: str
            Value of the queried credential i.e. "jsmith@gmail.com".
        Returns
        -------
        str
            Username associated with given key, value pair i.e. "jsmith".
        """
        if key == "email":
            user = db.get_user_credential_by_email(value)
        if key == "phone number":
            user = db.get_user_credential_by_phone(value)

        if user is None:
            return False
        else:
            return user.username


    def forgot_username(self, form_name: str, location: str = 'main') -> tuple:
        """
        Creates a forgot username widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot username form.
        location: str
            The location of the forgot username form i.e. main or sidebar.
        Returns
        -------
        str
            Forgotten username that should be transferred to user securely.
        str
            Email associated with forgotten username.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_username_form = st.form('Forgot username')
        elif location == 'sidebar':
            forgot_username_form = st.sidebar.form('Forgot username')

        forgot_username_form.subheader(form_name)
        email = forgot_username_form.text_input('Email')

        if forgot_username_form.form_submit_button('Submit'):
            if len(email) > 0:
                return self._get_username('email', email), email
            else:
                raise ForgotError('Email not provided')
        return None, email

    def update_account_details(self, username: str, form_name: str, location: str = 'main') -> bool:
        """
        Creates a update account details widget.

        Parameters
        ----------
        username: str
            The username of the user to update user details for.
        form_name: str
            The rendered name of the update user details form.
        location: str
            The location of the update user details form i.e. main or sidebar.
        Returns
        -------
        str
            The status of updating user details.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            update_account_details_form = st.form('Update account details')
        elif location == 'sidebar':
            update_account_details_form = st.sidebar.form(
                'Update account details')

        update_account_details_form.subheader(form_name)
        self.username = username.lower()
        field = update_account_details_form.selectbox(
            'Field', ['First Name', 'Last Name', 'Email', 'Phone Number']).lower()
        new_value = update_account_details_form.text_input('New value')

        if update_account_details_form.form_submit_button('Update'):
            if len(new_value) > 0:
                key = field.lower()
                if new_value != st.session_state[key]:
                    st.session_state[key] = new_value

                    db.update_user_profile(st.session_state['user_id'], st.session_state['first name'], st.session_state['last name'], st.session_state['phone number'], st.session_state['email'])

                    self.exp_date = self._set_exp_date()
                    self.token = self._token_encode()
                    self.cookie_manager.set(self.cookie_name, self.token,
                                            expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                    return True
                else:
                    raise UpdateError('New and current values are the same')
            if len(new_value) == 0:
                raise UpdateError('New value not provided')

