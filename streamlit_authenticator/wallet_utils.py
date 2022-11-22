from streamlit_authenticator.db_utils import is_wallet_available
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://52.87.239.109:8545'))

def get_free_wallet_link():
    addresses = w3.eth.accounts

    for address in addresses:
        if is_wallet_available(address):
            return address
    return None