import pandas as pd
import json
import streamlit as st


def get_playstation_trophy_level_image(trophy_level: int) -> str:
    """
    Gets the correct Trophy level tier image to display on the users
    playstation tab
    """

    if trophy_level == 999:
        return 'data\\images\\trophey_level_10.png'

    elif trophy_level >= 800:
        return 'data\\images\\trophey_level_9.png'

    elif trophy_level >= 700:
        return 'data\\images\\trophey_level_8.png'

    elif trophy_level >= 600:
        return 'data\\images\\trophey_level_7.png'

    elif trophy_level >= 500:
        return 'data\\images\\trophey_level._6png'

    elif trophy_level >= 400:
        return 'data\\images\\trophey_level_5.png'

    elif trophy_level >= 300:
        return 'data\\images\\trophey_level_4.png'

    elif trophy_level >= 200:
        return 'data\\images\\trophey_level_3.png'

    elif trophy_level >= 100:
        return 'data\\images\\trophey_level_2.png'

    else:
        return 'data\\images\\trophey_level_1.png'


def get_playstation_trophy_type_url(trophy_type):
    """

    """
    if trophy_type == "bronze":
        return "https://wrapup.playstation.com/_ipx/w_3840,q_100//assets/trophies/antman-trophy-bronze.png?url=/assets/trophies/antman-trophy-bronze.png&w=3840&q=100"

    elif trophy_type == "silver":
        return "https://wrapup.playstation.com/_ipx/w_3840,q_100//assets/trophies/antman-trophy-silver.png?url=/assets/trophies/antman-trophy-silver.png&w=3840&q=100"

    elif trophy_type == "gold":
        return "https://wrapup.playstation.com/_ipx/w_3840,q_100//assets/trophies/antman-trophy-gold.png?url=/assets/trophies/antman-trophy-gold.png&w=3840&q=100"

    elif trophy_type == "platinum":
        return "https://wrapup.playstation.com/_ipx/w_3840,q_100//assets/trophies/antman-trophy-platinum.png?url=/assets/trophies/antman-trophy-platinum.png&w=3840&q=100"


def playstation_achievements_to_df(game_achievements, player_achievements):
    """

    """

    columns = ["Logo", "Trophy Name", "Description", "Type"]
    df = pd.DataFrame(columns=columns)
    for achievement in game_achievements:
        dict = {
            "Logo": achievement[5],
            "Trophy Name": achievement[2],
            "Description": achievement[4],
            "Type": get_playstation_trophy_type_url(achievement[3]),
            "Earned": player_achievements[achievement[2]]["earned"]
        }
        new_df = pd.DataFrame([dict])
        df = pd.concat([df, new_df], ignore_index=True)

    return df
