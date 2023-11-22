import sqlite
import api
import functions
import streamlit as st
from stqdm import stqdm
from pathlib import Path
from PIL import Image
from datetime import datetime, timedelta


def account_dashboard(api_key, account_tab, userid):
    """
    Handles building the Account Tab
    Shows each platform the account is able to connect to and allows the user to update those accounts
    """

    col1, col2 = account_tab.columns(2)

    image = Image.open(Path("data/images/steam_logo.jpeg"))
    col1.image(image)

    summary = sqlite.steamusers_select_account(userid)
    with col2:
        st.image(f"{summary[6]}")  # Profile Picture
        st.write(f"[Profile]({summary[4]})")  # Steam URL
        st.text(f"{summary[3]}")  # Profile Name
        st.text(f"SteamID: {summary[2]}")

        on = st.toggle("Update", key="steamid")
        if on:
            new_steamid = st.text_input("Enter New SteamID", label_visibility="visible")

            if new_steamid:
                steam_set_steamid(api_key, userid, new_steamid, account_tab)


def steam_set_steamid(api_key, userid, steamid, account_tab):
    """"""
    # Calls GetPlayerSummaries using the provided SteamID and Userid
    # If the response is False: then warning and prompt the user to try again
    # If the response if True: INSERT/UPDATE record into SteamUser

    # Get SteamID account summary
    summary_response = api.GetPlayerSummaries(api_key, steamid, userid)

    if summary_response == False:
        account_tab.warning(f"SteamID Not found: {steamid}")
        return 0
    else:
        # If record with userid does not exist, create
        if sqlite.steamusers_select_account_exist(userid) == False:
            sqlite.steamusers_insert_account(summary_response)
        # If record with userid and steamid exist, pass
        elif (
            sqlite.steamusers_select_account_and_steamid_exist(userid, steamid) == True
        ):
            pass
        # If record with userid exist, update
        else:
            sqlite.steamusers_update_account(
                userid=summary_response[0],
                steamid=summary_response[1],
                personaname=summary_response[2],
                profileurl=summary_response[3],
                avatar=summary_response[4],
                avatarmedium=summary_response[5],
                avatarfull=summary_response[6],
                personastate=summary_response[7],
                communityvisibilitystate=summary_response[8],
                profilestate=summary_response[9],
                lastlogoff=summary_response[10],
                commentpermission=summary_response[11],
                realname=summary_response[12],
                primaryclanid=summary_response[13],
                timecreated=summary_response[14],
                gameid=summary_response[15],
                gameserverip=summary_response[16],
                gameextrainfo=summary_response[17],
                cityid=summary_response[18],
                loccountrycode=summary_response[19],
                locstatecode=summary_response[20],
                loccityid=summary_response[21],
                lastupdate=summary_response[22],
            )
            return True


def steam_dashboard(api_key, steam_tab, userid):
    """Handles building the Steam Tab"""

    # Check if any records under the userid exist in SteamUsers Table
    # If Account does not exist: then Prompt user for SteamID and create new record
    # Else: Load account from SQL
    if sqlite.steamusers_select_account_exist(userid) == False:
        steam_tab.write("Add Steam account under Account Tab")
    else:
        # Update
        # Get current time and see if it is eligable for updating
        current_time = datetime.now()
        current_time = current_time.time()

        lastupdate = sqlite.steamusers_select_account_lastupdated(userid)
        t_format = "%H:%M:%S.%f" if "." in lastupdate else "%H:%M:%S"
        lastupdate = datetime.strptime(lastupdate, t_format).time()

        # Disables the Update button if the lastupdate time has not been passed
        disabled = False
        if current_time < lastupdate:
            disabled = True
        steam_tab.button(
            "Update",
            on_click=steam_update,
            args=(api_key, userid, steam_tab),
            disabled=disabled,
        )

        # Demographics
        steam_user_demographics(api_key, steam_tab, userid)

        # Game Analytics
        steam_game_analytics(api_key, steam_tab, userid)


def steam_user_demographics(api_key, steam_tab, userid):
    """
    Displays basic demographics of a users steam profile
    @Metrics:
    *   Total Games
    *   Total Achievements,
    *   Achievements % Completed

    @Library: Table of Users Steam Library with timeplayed and achievement progress
    """

    # Query SteamUsers Table for userid
    summary = sqlite.steamusers_select_account(userid)

    col1, col2 = steam_tab.columns(2)
    col1.image(summary[7])  # Profile Picture
    col2.subheader(summary[3])  # Username

    # Metrics
    num_games, num_achieved, percentage_achieved, df = functions.steam_account_metrics(
        summary[2]
    )
    col1, col2, col3 = steam_tab.columns(3)
    col1.metric("Total Games", num_games)  # Total games a user ownes
    col2.metric(
        "Total Achievements", num_achieved
    )  # Total number of achieved achievments
    col3.metric("Completion", percentage_achieved)  # Percentage of achieved / total

    # Table of steam library, sorted by playtime
    steam_tab.data_editor(
        df,
        use_container_width=True,
        column_config={
            "Icon": st.column_config.ImageColumn(
                "Preview Image", help="Streamlit app preview screenshots", width=50
            ),
            "Achievements": st.column_config.ProgressColumn(
                format="%d",
                min_value=0,
                max_value=100,
            ),
        },
        hide_index=True,
    )


def steam_update(api_key, userid):
    """
    Manual way to allow user to update thier profile.
    Gets the most updated information for each game and updates the entry
    Sets a 1 min timer from last click to prevent spamming
    """

    # Get the users SteamID and Steam Library
    steamid = sqlite.steamusers_select_account_steamid(userid)
    owned_games_response = api.GetOwnedGames(api_key, steamid)

    # If user has no libray, then exit
    if owned_games_response == False:
        return 0

    # Call GetPlayerAchievements and update each record in Steam Library
    for game in stqdm(owned_games_response, desc="Updating Steam Data"):

        try:
            achievements_json = api.GetPlayerAchievements(
                api_key, steamid, game["appid"]
            )

            if achievements_json != False:
                game["achivements"] = achievements_json
            sqlite.steamuserlibrary_update_game(
                game["steamid"],
                game["appid"],
                game["img_icon_url"],
                game["has_community_visible_stats"],
                game["playtime_forever"],
                game["achivements"],
            )
        except:
            continue

    # UPDATE lastupdate in SteamUser Table
    lastupdate = datetime.now()
    lastupdate = lastupdate + timedelta(seconds=10)
    lastupdate = str(lastupdate.time())
    sqlite.steamusers_update_account_lastupdated(userid, lastupdate)


def steam_game_analytics(api_key, steam_tab, userid):
    """Displays Global and user analytics of selected game"""

    # Get list of owned games from userid
    steamid = sqlite.steamusers_select_account_steamid(userid)
    unique_games = sqlite.steamuserlibrary_select_all_unique(steamid)

    # Search Specific Game
    option = steam_tab.selectbox(
        "",
        unique_games,
        index=None,
        placeholder="Select Game in Library...",
    )

    # Game Analytics
    if option != None:
        steam_tab.write("WIP")
