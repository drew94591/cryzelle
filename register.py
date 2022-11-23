import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

# Loading config file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully!')
        st.markdown('<a href="https://chorizoburrito.streamlit.app" target="_self">Login</a>',
                    unsafe_allow_html=True)
except Exception as e:
    st.error(e)
