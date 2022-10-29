import streamlit as st


class Transaction:
    def send(self):
        st.write('In Transaction Send Page...')

    def request(self):
        st.write("In Transaction Request Page...")

    def history(self):
        st.write("In Transaction History Page...")
