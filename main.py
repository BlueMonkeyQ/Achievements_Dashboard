import streamlit as st
import dashboard
import sqlite
from playstation import playstation_dashboard
from psnawp_api import PSNAWP

# api_key = "14EB214CEC3F1701FD192885D330990F"
# psnawp: PSNAWP = None

def main():
    st.set_page_config()
    st.title("Achievements Dashboard")
    psnawp = playstation_api()
    user = sqlite.get_table_Users('bluemonkeyq')
    steam_tab, playstation_tab, account_tab = st.tabs(["Steam", "Playstation", "Account"])

    playstation_dashboard(playstation_tab, user, psnawp)


@st.cache_data
def playstation_api():
    """
    Gets the Playstation Network API Wrapper.
    Caches this return to reduce api calls
    """
    npsso = 'S5TjhWutt5jULkEZPCl7Q95599Hshst58vwxy4UEw97XHhGEeYdd8MkwbIBmDPhe'
    psnawp = PSNAWP(npsso_cookie=npsso)
    return psnawp


if __name__ == "__main__":
    main()
