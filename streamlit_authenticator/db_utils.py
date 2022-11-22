import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text
import streamlit as st


# TODO: Change to use model and Session in Future
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
        stmt = text("SELECT id FROM users WHERE username = :userid AND password = :pwd")
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

def get_user_credential_by_email(email_address):
    """
        Retrieve User Credential by Email

        Parameters
        ----------
            email_address: str
        Returns
        -------
        None or Record
            (id, username, password)
    """

    result = None
    engine = get_db_engine()
    
    connection = engine.connect()
    try:
        stmt = text("SELECT id, username, password FROM users INNER JOIN  user_profiles up ON users.id = up.user_id WHERE email_address = :email")
        result = connection.execute(stmt, email = email_address).one_or_none()
    finally:
        connection.close()
    return result


def get_user_credential_by_phone(phone_number):
    """
        Retrieve User Credential by phone number

        Parameters
        ----------
            phone_number: str
        Returns
        -------
        None or Record
            (id, username, password)
    """

    result = None
    engine = get_db_engine()
    
    connection = engine.connect()
    try:
        stmt = text("SELECT id, username, password FROM users INNER JOIN  user_profiles up ON users.id = up.user_id WHERE mobile_number = :phone")
        result = connection.execute(stmt, phone = phone_number).one_or_none()
    finally:
        connection.close()
    return result


def get_user_profile_by_id(userid):
    """
        Retrieves the user profile data.

        Parameters
        ----------
            userid: bigint
        Returns
        -------
        None or a User Profile Record
            user profile detail: (first name, last name, mobile number, email)
    """

    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT up.first_name, up.last_name, mobile_number, email_address FROM users INNER JOIN user_profiles up ON users.id = up.user_id WHERE users.id = :id")
        result = connection.execute(stmt, id = userid).one_or_none()
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
        stmt = text("SELECT up.first_name, up.last_name, mobile_number, email_address FROM users INNER JOIN user_profiles up ON users.id = up.user_id WHERE users.username = :userid")
        result = connection.execute(stmt, userid = username).one_or_none()
    finally:
        connection.close()
    return result

def get_user_profile_by_phone(phone):
    """
        Retrieves the user profile data by phone.

        Parameters
        ----------
            phone: str
        Returns
        -------
        None or a User Profile Record
            user profile detail: (first name, last name, mobile number, email)
    """

    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT first_name, last_name, mobile_number, email_address FROM user_profiles WHERE mobile_number = :cp")
        result = connection.execute(stmt, cp = phone).one_or_none()
    finally:
        connection.close()
    return result


def get_user_profile_by_email(email):
    """
        Retrieves the user profile data by email address.

        Parameters
        ----------
            phone: str
        Returns
        -------
        None or a User Profile Record
            user profile detail: (first name, last name, mobile number, email)
    """

    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT first_name, last_name, mobile_number, email_address FROM user_profiles WHERE email_address = :email_address")
        result = connection.execute(stmt, email_address = email).one_or_none()
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

def get_default_active_user_wallet_by_user_id(id):
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
        stmt = text("SELECT id, wallet_nickname, wallet_link FROM wallet_accounts WHERE user_id = :userid AND is_default is true AND is_active is true")

        result = connection.execute(stmt, userid = id).one_or_none()
    finally:
        connection.close()
    return result

def get_default_active_user_wallet_by_phone(phone):
    """
        Retrieves the user's active, default wallet given phone.

        Parameters
        ----------
            phone: str
            
        Returns
        -------
        None or A Wallet Account Record
            detail: (wallet id, wallet nickname, wallet link)
    """
    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT wallet.id, wallet_nickname, wallet_link FROM user INNER JOIN wallet_accounts wallet ON users.id = wallet.user_id INNER JOIN user_profiles up ON users.id = up.user_id WHERE mobile_number = :cp and is_default is true and is_active is true")

        result = connection.execute(stmt, cp = phone).one_or_none()
    finally:
        connection.close()
    return result


def get_default_active_user_wallet_by_email(email):
    """
        Retrieves the user's active, default wallet given email address.

        Parameters
        ----------
            phone: str
            
        Returns
        -------
        None or A Wallet Account Record
            detail: (wallet id, wallet nickname, wallet link)
    """
    result = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("SELECT wallet.id, wallet_nickname, wallet_link FROM user INNER JOIN wallet_accounts wallet ON users.id = wallet.user_id INNER JOIN user_profiles up ON users.id = up.user_id WHERE email_address = :email_address AND is_default is true AND is_active is true")

        result = connection.execute(stmt, email_address = email).one_or_none()
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


def create_user(username, password):
    """
        creates user, user profile

        Parameters
        ----------
        username: str
        password: str
            
        Returns
        -------
        None or the record id
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO users (id, username, password) VALUES (nextval('user_id_seq'), :userid, :pwd)")
        result = connection.execute(stmt, userid = username, pwd = password)
        stmt = text("SELECT id FROM users WHERE username = :userid AND password = pwd")
        result = connection.execute(stmt, userid = username, pwd = password).one_or_none()
        if result is not None:
            output = result.id
    finally:
        connection.close()
    return output


def update_password(username, new_password):
    """
        updates the user's login password

        Parameters
        ----------
        username: str
        new_password: str
            
        Returns
        -------
        None or record id
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("UPDATE users SET password = :pwd WHERE username = :userid)")
        result = connection.execute(stmt, pwd = new_password, userid = username)
        stmt = text("SELECT id FROM users WHERE username = :userid AND password = :password")
        result = connection.execute(stmt, userid = username, password = new_password).one_or_none()
        if result is not None:
            output = result.id
        
    finally:
        connection.close()
    return output



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
        None or Record id
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO user_profiles (id, first_name, last_name, user_id, mobile_number, email_address) VALUES (nextval('user_profile_id_seq'), :fn, :ln, :uid, :cp, :email)")
        result = connection.execute(stmt, fn = first_name, ln = last_name, uid = user_id, cp = mobile_number, email = email_address)

        stmt = text("SELECT id FROM user_profiles WHERE user_id = :uid")
        result = connection.execute(stmt, uid = user_id).one_or_none()
        if result is not None:
            output = result.id
        
    finally:
        connection.close()
    return output


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
        None or Record id
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("UPDATE user_profiles SET first_name = :fn, last_name = :ln, mobile_number = :cp, email_address = :email WHERE id = :upid")
        result = connection.execute(stmt, fn = first_name, ln = last_name, cp = mobile_number, email = email_address, upid = id)

        stmt = text("SELECT id FROM user_profiles WHERE first_name = :fn AND last_name = :ln AND mobile_number = :cp AND email_address = :email AND id = :upid")
        result = connection.execute(stmt, fn = first_name, ln = last_name, cp = mobile_number, email = email_address, upid = id)
        if result is not None:
            output = result.id
        
    finally:
        connection.close()
    return output


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
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO wallet_accounts (id, wallet_nickname, wallet_link, user_id, active_indicator, default_indicator) VALUES (nextval('wallet_account_id_seq'), :nickname, :link, :uid, :is_active, :is_default)")
        result = connection.execute(stmt, nickname = wallet_nickname, link = wallet_link, uid = user_id, is_active = active_indicator, is_default = default_indicator)

        stmt = text("SELECT id FROM wallet_accounts WHERE wallet_nickname = :nickname AND wallet_link = :link AND user_id = :uid AND active_indicator = :is_active AND default_indicator = :is_default)")
        result = connection.execute(stmt, nickname = wallet_nickname, link = wallet_link, uid = user_id, is_active = active_indicator, is_default = default_indicator)
        if result is not None:
            output = result.id
    finally:
        connection.close()
    return output


def update_wallet(wallet_id, wallet_nickname, active_indicator, default_indicator):
    """
        updates wallet account (only nickname, active ind, default ind)

        Parameters
        ----------
        wallet_id: bigint
            key of the wallet account object
        wallet_nickname: str
        active indicator: bool
        default_indicator: bool
            
        Returns
        -------
        Success or Fail
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("UPDATE wallet_accounts SET wallet_nickname = :nickname, active_indicator = :is_active, default_indicator = :is_default WHERE id = :wid")
        result = connection.execute(stmt, nickname = wallet_nickname, is_active = active_indicator, is_default = default_indicator, wid = wallet_id)
        stmt = text("SELECT id FROM wallet_accounts WHERE wallet_nickname = :nickname AND active_indicator = :is_active AND default_indicator = :is_default AND id = :wid")
        result = connection.execute(stmt, nickname = wallet_nickname, is_active = active_indicator, is_default = default_indicator, wid = wallet_id)
        if result is not None:
            output = result.id        
    finally:
        connection.close()
    return output


def create_contract(collateral, contract_link):
    """
        creates contract

        Parameters
        ----------
        collateral: str
        contract_link: str
            
        Returns
        -------
        Success or Fail
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO contracts (id, collateral, contract_link) VALUES (nextval('contract_id_seq'), :col, :link)")
        result = connection.execute(stmt, col = collateral, link = contract_link)
        stmt = text("SELECT id from contracts where collateral = :col AND contract_link = :link")
        result = connection.execute(stmt, col = collateral, link = contract_link)
        if result is not None:
            output = result.id   
    finally:
        connection.close()
    return output



def create_party(contract_id, legal_party_type, legal_party_id):
    """
        creates contract legal party

        Parameters
        ----------
        contract_id: bigint
        legal_party_type: str
        legal_party_id: bigint
            
        Returns
        -------
        Success or Fail
    """
    output = None
    engine = get_db_engine()
    connection = engine.connect()
    try:
        stmt = text("INSERT INTO contract_parties (id, contract_id, legal_party_type, legal_party_id) VALUES (nextval('contract_party_id_seq'), :cid, :party_type, :party_id)")
        result = connection.execute(stmt, cid = contract_id, party_type = legal_party_type, party_id = legal_party_id)
        stmt = text("SELECT id FROM contract_parties WHERE contract_id = :cid AND legal_party_type = :party_type AND legal_party_id = :party_id")
        result = connection.execute(stmt, cid = contract_id, party_type = legal_party_type, party_id = legal_party_id)
        if result is not None:
            output = result.id
    finally:
        connection.close()
    return output
