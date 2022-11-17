import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text
import streamlit as st


def get_db_engine():
    """
        Initializes DB engine

        Returns
        -------
            db engine
    """
    # Load .env envrionment variables
    load_dotenv()
    
    # Read in database settings
    database_connection_string = os.getenv("DATABASE_URL")

    engine = create_engine(database_connection_string)
    return engine


def verify(username, password) -> bool:
    """
        Checks the validity of the entered credentials.

        Parameters
        ----------
            username: username
            password: hashed password.
        Returns
        -------
        bool
            Validity of entered credentials.
    """

    result = None
    engine = get_db_engine()
    
    connection = engine.connect()
    try:
        stmt = text("SELECT id FROM users WHERE username = :userid and password = :pwd")
        result = connection.execute(stmt, userid = username, pwd = password).one_or_none()
    finally:
        connection.close()
    return result is not None


def get_user_credentials(username):
    """
        Checks the validity of the entered credentials.

        Parameters
        ----------
            username: username
        Returns
        -------
        None or Record
            (id, user name, password) .
    """

    result = None
    engine = get_db_engine()
    
    connection = engine.connect()
    try:
        stmt = text("SELECT id, username, password FROM users WHERE username = :userid")
        result = connection.execute(stmt, userid = username).one_or_none()
    finally:
        connection.close()
    return result


def get_user_profile_by_username(username):
    """
        Retrieves the user profile data.

        Parameters
        ----------
            username: username
        Returns
        -------
        None or a User Profile Record
            user profile detail: (first name, last name, mobile number, email)
    """

    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT up.first_name, up.last_name, mobile_number, email_address FROM users INNER JOIN user_profiles up ON users.id = up.user_id WHERE username = :userid")
        result = connection.execute(stmt, userid = username).one_or_none()
    finally:
        connection.close()
    return result


def get_user_profile_by_user_id(user_id):
    """
        Retrieves the user profile data.

        Parameters
        ----------
            user_id: userid
        Returns
        -------
        None or a User Profile Record
            user profile detail: (first name, last name, mobile number, email)
    """

    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT first_name, last_name, mobile_number, email_address FROM user_profiles WHERE user_id= :id")
        result = connection.execute(stmt, id = user_id).one_or_none()
    finally:
        connection.close()
    return result


def get_default_active_user_wallet(username):
    """
        Retrieves the user's active, default wallet.

        Parameters
        ----------
            username: username
        Returns
        -------
        None or A Wallet Account Record
            detail: (wallet id, wallet nickname, wallet link)
    """
    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT wallet.id, wallet_nickname, wallet_link FROM users INNER JOIN wallet_accounts wallet ON users.id = wallet.user_id WHERE username = :userid and is_default is true and is_active is true")

        result = connection.execute(stmt, userid = username).one_or_none()
    finally:
        connection.close()
    return result


def get_default_active_user_wallet_by_user_id(user_id):
    """
        Retrieves the user's active, default wallet.

        Parameters
        ----------
            user_id: user id
        Returns
        -------
        None or A Wallet Account Record
            detail: (wallet id, wallet nickname, wallet link)
    """
    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT wallet.id, wallet_nickname, wallet_link FROM wallet_accounts WHERE user_id = :id and is_default is true and is_active is true")

        result = connection.execute(stmt, id = user_id).one_or_none()
    finally:
        connection.close()
    return result



def get_all_user_wallets(username):
    """
        Retrieves all of user's wallets.

        Parameters
        ----------
            username: username
        Returns
        -------
        [] or Wallet Account Records
            detail: (wallet id, user id, wallet nickname, wallet link, active indicator, default indicator)
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT wallet.* FROM users INNER JOIN wallet_accounts wallet ON users.id = wallet.user_id WHERE username = :userid")

        result = connection.execute(stmt, userid = username).fetchall()
    finally:
        connection.close()
    return result



def get_all_user_wallets_by_user_id(user_id):
    """
        Retrieves all of user's wallets.

        Parameters
        ----------
            user_id: user id
        Returns
        -------
        [] or Wallet Account Records
            detail: [(wallet id, user id, wallet nickname, wallet link, active indicator, default indicator)]
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT wallet.* FROM users INNER JOIN wallet_accounts wallet WHERE user_id = :id")

        result = connection.execute(stmt, id = user_id).fetchall()
    finally:
        connection.close()
    return result


def create_user(username, password):
    """
        creates user, user profile

        Parameters
        ----------
        user_credential_dict: dict
            dictionary for user credential to create user and user profile
            
        Returns
        -------
        Success or Fail
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO users (id, username, password) VALUES (nextval('user_id_seq'), :userid, :pwd)")

        result = connection.execute(stmt, userid = username, pwd = password)
        
    finally:
        connection.close()
    return result


def update_password(user_id, new_password):
    """
        updates the user's login password

        Parameters
        ----------
        new_password: str
            new password
            
        Returns
        -------
        Success or Fail
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("UPDATE users SET password = :pwd WHERE id = :id)")

        result = connection.execute(stmt, pwd = new_password, id = user_id)
        
    finally:
        connection.close()
    return result



def create_user_profile(user_id, first_name, last_name, mobile_number, email_address):
    """
        creates user profile

        Parameters
        ----------
        user_id: bigint
            key of the user object
        first_name: str
        last_name: str
        mobile_number: str
        email_address: str
            
        Returns
        -------
        Success or Fail
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO user_profiles (id, first_name, last_name, user_id, mobile_number, email_address) VALUES (nextval('user_profile_id_seq'), :fn, :ln, :uid, :cp, :email)")

        result = connection.execute(stmt, fn = first_name, ln = last_name, uid = user_id, cp = mobile_number, email = email_address)
        
    finally:
        connection.close()
    return result


def update_user_profile(id, first_name, last_name, mobile_number, email_address):
    """
        updates user profile

        Parameters
        ----------
        id: bigint
            key of the user profile object
        first_name: str
        last_name: str
        mobile_number: str
        email_address: str
            
        Returns
        -------
        Success or Fail
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("UPDATE user_profiles SET first_name = :fn, last_name = :ln, mobile_number = :cp, email_address = :email WHERE id = :upid")

        result = connection.execute(stmt, fn = first_name, ln = last_name, cp = mobile_number, email = email_address, upid = id)
        
    finally:
        connection.close()
    return result



def create_wallet(user_id, wallet_nickname, wallet_link, active_indicator=True, default_indicator=False):
    """
        creates wallet account

        Parameters
        ----------
        user_id: bigint
            key of the user object
        wallet_nickname: str
        wallet_link: str
        active indicator: bool
        default_indicator: bool
            
        Returns
        -------
        Success or Fail
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO wallet_accounts (id, wallet_nickname, wallet_link, active_indicator, default_indicator) VALUES (nextval('wallet_account_id_seq'), :nickname, :link, :uid, :is_active, :is_default)")

        result = connection.execute(stmt, nickname = wallet_nickname, link = wallet_link, uid = user_id, is_active = active_indicator, is_default = default_indicator)
        
    finally:
        connection.close()
    return result


def update_wallet(wallet_id, wallet_nickname, active_indicator, default_indicator):
    """
        updates wallet account (only nickname, active ind, default ind)

        Parameters
        ----------
        wallet_id: bigint
            key of the wallet account object
        first_name: str
        last_name: str
        mobile_number: str
        email_address: str
            
        Returns
        -------
        Success or Fail
    """
    result = []
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("UPDATE wallet_accounts SET wallet_nickname = :nickname, active_indicator = :is_active, default_indicator = :is_default WHERE id = :wid")

        result = connection.execute(stmt, nickname = wallet_nickname, is_active = active_indicator, is_default = default_indicator, wid = wallet_id)
        
    finally:
        connection.close()
    return result

