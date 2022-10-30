import streamlit as st


class Wallet:
    address = ''
    balance = 0
    currency_type = 'ETH'

    def withdraw(self, amount):
        self.balance = self.balance - amount

    def deposit(self, amount):
        self.balance = self.balance + amount

    def get_currency_type(self):
        return self.currency_type

    def set_currency_type(self, type):
        self.currency_type = type
