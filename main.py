import streamlit as st
import dashboard
import sqlite
from psnawp_api import PSNAWP

npsso = 'qw01QRUnPCxrpTLPjLavxPEe7lqZzIAo46zCot06mxyqyHefbIVJ5aUbzgsrv2Vc'
psnawp = PSNAWP(npsso_cookie=npsso)

api_key = "14EB214CEC3F1701FD192885D330990F"
user = sqlite.get_table_Users('bluemonkeyq')

def main():
    st.set_page_config()
    st.title("Achievements Dashboard")
    p_user = psnawp.user(online_id="BluemonkeyQ")

    steam_tab, playstation_tab, account_tab = st.tabs(["Steam","Playstation","Account"])

    dashboard.steam_dashboard(steam_tab, user)
    dashboard.playstation_dashboard(playstation_tab, p_user)
    dashboard.account_dashboard(account_tab, user, p_user)

if __name__ == "__main__":
    main()