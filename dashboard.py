import sqlite
import api
import functions
import streamlit as st


def steam_dashboard(api_key, steam_tab, userid):
    """Handles building the Steam Tab"""

    # Check if any records under the userid exist in SteamUsers Table
    # If Account does not exist: then Prompt user for SteamID and create new record
    # Else: Load account from SQL
    if sqlite.steamusers_select_account_exist(userid) == False:
        # Calls GetPlayerSummaries using the provided SteamID
        # If the response is False, then warning and prompt the user to try again
        # If the response if True:
        # 1) Add a new record SteamUser record
        # 2) GetOwnedGames
        # 3) GetPlayerAchievements

        # 1) Add a new record SteamUser record
        steamid = steam_tab.text_input("Enter SteamID")
        summary_response = api.GetPlayerSummaries(api_key, steamid, userid)

        if summary_response == False:
            steam_tab.warning(f"SteamID Not found; ID: {steamid}")

        else:
            sqlite.steamusers_insert_account(summary_response)

            # # 2) GetOwnedGames and insert new records
            owned_games_response = api.GetOwnedGames(api_key, steamid)
            for game in owned_games_response:
                # 3) GetPlayerAchievements and insert new records
                achievements_json = api.GetPlayerAchievements(
                    api_key, steamid, game["appid"]
                )
                if achievements_json != False:
                    game["achivements"] = achievements_json
                sqlite.steamuserlibrary_insert_game(
                    (
                        game["steamid"],
                        game["appid"],
                        game["img_icon_url"],
                        game["has_community_visible_stats"],
                        game["playtime_forever"],
                        game["achivements"],
                    )
                )

    else:
        # Demographics
        steam_user_demographics(api_key, steam_tab, userid)

        # Game Analytics
        steam_game_analytics(api_key, steam_tab, userid)


def steam_user_demographics(api_key, steam_tab, userid):
    """Displays basic demographics of a users steam profile"""

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

    # Table of steam library, default sorted by playtime
    # Displays app icon, and progress bar of achievments
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


def steam_game_analytics(api_key, steam_tab, userid):
    """Displays Global and user analytics of selected game"""

    # Get list of owned games from userid
    steamid = sqlite.steamusers_select_account_steamid(userid)
    unique_games = sqlite.steamuserlibrary_select_all_unique(steamid)

    # Search Specific Game
    option = st.selectbox(
        "",
        unique_games,
        index=None,
        placeholder="Select Game in Library...",
    )

    # Game Analytics
    if option != None:
        steam_tab.write("WIP")
