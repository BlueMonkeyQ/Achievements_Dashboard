import streamlit as st
import pandas as pd
import sqlite as sql
import dashboard
import api

api_key = api.get_api_key()


def main():
    st.title("Achievements Dashboard")

    userid = None
    if userid == None:
        userid = st.text_input("Enter Account ID")
        userid = str(userid).upper()

    if sql.users_select_account_exist(userid):
        steam_tab, account_tab = st.tabs(["Steam", "Account"])

        dashboard.account_dashboard(api_key, account_tab, userid)
        dashboard.steam_dashboard(api_key, steam_tab, userid)


if __name__ == "__main__":
    main()
