import sqlite
import json
import pandas as pd


def steam_account_metrics(steamid):
    """
    Query the SteamUserLibrary for the provided steamid
    @returns:
    *   num_games - number of unique games
    *   num_achieved - number of achievements achieved
    *   percentage_achieved - percentage of achieved / total
    *   df - Dataframe for the table demographics\
    """

    # Query STEAMUSERLIBRARY for all records for steamid
    response = sqlite.steamuserlibrary_select_all(steamid)

    # If Steamid has no associated records, return None
    if response == False:
        return None, None, None, None

    num_games = len(response)
    num_achieved = 0
    num_achievements = 0
    columns = ["Icon", "Game", "Playtime", "Achievements"]
    df = pd.DataFrame(columns=columns)

    for game in response:
        icon = f"https://media.steampowered.com/steamcommunity/public/images/apps/{game[2]}/{game[3]}.jpg"
        gamename = sqlite.steamgames_select_game_name(game[2])
        hours, minutes = divmod(game[5], 60)

        # playtime is set to the number of hours. If sub hour, then use minutes
        if hours == 0:
            playtime = minutes / 100
        else:
            playtime = hours

        achievements = 0

        # If game has data
        if game[6] != None:
            json_object = json.loads(game[6])
            total_achievements = len(json_object.keys())
            num_achievements += total_achievements

            for key in json_object.keys():
                if json_object[key]["achieved"] == 1:
                    num_achieved += 1
                    achievements += 1
            achievements = int((achievements / total_achievements) * 100)

        # Create Dataframe record for each game
        dict = {
            "Icon": icon,
            "Game": gamename,
            "Playtime": playtime,
            "Achievements": achievements,
        }
        new_df = pd.DataFrame([dict])
        df = pd.concat([df, new_df], ignore_index=True)

    # Sort dataframe by Playtime Descending
    df = df.sort_values(by=["Playtime"], ascending=False)

    # Percentage of achieved / total
    percentage_achieved = round((num_achieved / num_achievements) * 100, 2)

    return num_games, num_achieved, percentage_achieved, df
