import streamlit as st
import pandas as pd
import sqlite as sql
import dashboard
import api

api_key = api.get_api_key()

st.title("Achievements Dashboard")

userid = st.text_input("Enter Account ID")
userid = str(userid).upper()

if sql.users_select_account_exist(userid):
    steam_tab, playstation_tab = st.tabs(["Steam", "Playstation"])

    dashboard.steam_dashboard(api_key, steam_tab, userid)
