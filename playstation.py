import streamlit as st
import sqlite
import pandas as pd
import functions as f
import time
import re
import json
from datetime import datetime, timedelta
from psnawp_api import PSNAWP


def playstation_dashboard(playstation_tab, user: tuple, psnawp: PSNAWP):
    """
    Handles the Playstation Tab
    Displays Basic User Demographics
    Displays Trophy level and progress bar until next tier
    Displays Amount earned for each trophy
    Displays Table of the users Playstation library
    Displays Table of Selected Game
    """

    # Update Button
    with playstation_tab:
        col1, col2 = st.columns(2)
        last_update_time = sqlite.get_table_Users_playstation_update_datetime(user[1])
        last_update_time = datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S.%f")

        with col1:
            # @TODO: Implement Updating Users Game Library
            update = st.button(label='Update Library', key='playstation_update', disabled=False,
                               use_container_width=True)
            if update:
                userid = str(user[1])
                last_update_time = datetime.now()

                values = tuple([
                    datetime.now(),
                    userid
                ])
                sqlite.update_table_Users_playstation_update_datetime(values)

                with st.spinner('Updating Playstation Library...'):
                    time.sleep(1)
                    get_PlaystationUserLibrary(user[4], psnawp)

        # Last updated Datetime
        with col2:
            st.text(
                f"Last Updated: {last_update_time.hour}:{last_update_time.minute} {last_update_time.day}-{last_update_time.month}-{last_update_time.year}")

    with playstation_tab:
        # Basic User Demographics
        user_info = sqlite.get_table_PlaystationUser(onlineid=user[4])

        col1, col2 = st.columns(2)

        # Avatar
        with col1:
            col1.image(user_info[11])

        # Demographics
        with col2:
            col2.header(user_info[1])
            col2.text(f"{user_info[12]} {user_info[13]}")
            col2.text(user_info[14])

        # Trophy's
        col1, col2, col3, col4, col5 = st.columns(5)

    with playstation_tab:
        with col1:
            trophy_level = user_info[3]
            image_file = f.get_playstation_trophy_level_image(trophy_level)
            col1.image(image=image_file)
            col1.subheader(user_info[3])

        # Platinum
        with col2:
            col2.image(image='data\\images\\platinum.png')
            col2.subheader(user_info[9])

        # Gold
        with col3:
            col3.image(image='data\\images\\gold.png')
            col3.subheader(user_info[8])

        # Silver
        with col4:
            col4.image(image='data\\images\\silver.png')
            col4.subheader(user_info[7])

        # Bronze
        with col5:
            col5.image(image='data\\images\\bronze.png')
            col5.subheader(user_info[6])

        # Trophy Tier Progress Bar
        st.progress(value=user_info[4], text=f'Tier: {user_info[5]}')

    # Playstation Library
    account_id = sqlite.get_table_PlaystationUser_accountid(user[4])
    game_library = sqlite.get_table_PlaystationUserLibrary(account_id)

    df = pd.DataFrame(columns=['Logo', 'Title', 'Progress', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Playtime'])
    for game in game_library:
        info = sqlite.get_table_PlaystationLibrary(titleid=game[2])
        dict = {
            'Logo': info[3],
            'Title': info[2],
            'Progress': game[4],
            'Platinum': game[8],
            'Gold': game[7],
            'Silver': game[6],
            'Bronze': game[5],
            'Playtime': game[9]
        }
        new_df = pd.DataFrame([dict])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)

    # Sort by Platinum then Hours
    df = df.sort_values(by=['Platinum', 'Playtime'], ascending=[False, False])
    with playstation_tab:
        # Display the Table
        playstation_tab.data_editor(
            df,
            use_container_width=True,
            column_config={
                "Logo": st.column_config.ImageColumn(),
                "Progress": st.column_config.ProgressColumn(
                    format="%i",
                    min_value=0,
                    max_value=100
                ),
            },
            hide_index=True
        )

    game_titles = df["Title"].tolist()

    title_name = playstation_tab.selectbox(label="Game Title", options=game_titles)
    # Specific Achievements
    if title_name is not None:
        title_id = sqlite.get_table_PlaystationLibrary_titleid_from_titlename(title_name)
        player_achievements = sqlite.get_table_PlaystationUserLibrary_achievements(account_id, title_id)

        player_achievements = player_achievements.replace("True", "true")
        player_achievements = player_achievements.replace("False", "false")
        player_achievements = player_achievements.replace("None", "\"None\"")

        pattern = r"'(.*?)'(?=:|\})"
        matches = re.findall(pattern, player_achievements)

        for match in matches:
            player_achievements = player_achievements.replace(f"'{match}'", f'"{match}"')

        player_achievements = player_achievements
        player_achievements = json.loads(player_achievements)
        game_achievements = sqlite.get_table_PlaystationAchievements(titleid=title_id)
        df = f.playstation_achievements_to_df(game_achievements, player_achievements)
        playstation_tab.data_editor(
            df,
            use_container_width=True,
            column_config={
                "Logo": st.column_config.ImageColumn(),
                "Type": st.column_config.ImageColumn(),
            },
            hide_index=True,
            disabled=["Earned"]
        )

def get_master_url(images):
    """
    
    """

    for image in images:

        if image['type'] == 'MASTER':
            return image['url']

    return None


def get_PlaystationUserLibrary(playstationid, psnawp: PSNAWP):
    """
    Get the Users entire Playstation Library.

    If the Title exist in the [PlaystationLibrary] table. If not, then create new record and
    also get the Achievements and create new records in the [PlaystationAchievements] table
    
    If Title exist in the  [PlaystationUserLibrary] table, then update existing record
    Else, create new record
    """

    # Get all titles in the users library
    print("Getting Playstation Library...")
    p_user = psnawp.user(online_id=playstationid)
    for i in p_user.title_stats():

        # Check if title exist in PlaystationLibrary, if not then add record
        if sqlite.get_table_PlaystationLibrary_titleid(i.title_id) is False:

            try:
                game = psnawp.game_title(title_id=i.title_id, account_id=p_user.account_id)
                game_data = game.get_details()[0]
                game_trophy = game.trophy_groups_summary(i.category.name)
                values = ([
                    i.title_id,
                    game_data['name'],
                    get_master_url(game_data['media']['images']),
                    game_trophy.defined_trophies.bronze,
                    game_trophy.defined_trophies.silver,
                    game_trophy.defined_trophies.gold,
                    game_trophy.defined_trophies.platinum,
                ])
                sqlite.insert_table_PlaystationLibrary(values)
            except:
                values = ([
                    i.title_id,
                    i.name,
                    i.image_url,
                    None,
                    None,
                    None,
                    None,
                ])
                sqlite.insert_table_PlaystationLibrary(values)

            try:
                gametitle = psnawp.game_title(title_id=i.title_id)
                platform = i.category.name
                for trophy in gametitle.trophies(platform):
                    values = tuple([
                        i.title_id,
                        trophy.trophy_name,
                        trophy.trophy_type.value,
                        trophy.trophy_detail,
                        trophy.trophy_icon_url
                    ])
                    sqlite.insert_table_PlaystationAchivements(values)
            except:
                values = tuple([
                    i.title_id,
                    None,
                    None,
                    None,
                    None
                ])
                sqlite.insert_table_PlaystationAchivements(values)

        try:
            trophy_titles = p_user.trophy_titles_for_title(title_ids=[i.title_id])

            if sum(1 for _ in trophy_titles) == 0:
                raise

            for j in p_user.trophy_titles_for_title(title_ids=[i.title_id]):

                # Achievements
                dict = {}
                trophy_data = p_user.trophies(np_communication_id=j.np_communication_id, platform=i.category.name,
                                              include_metadata=True)
                for x in trophy_data:
                    if x.earned is True:
                        dict[x.trophy_name] = {'earned': x.earned, 'date': x.earned_date_time.strftime("%Y/%d/%m")}
                    else:
                        dict[x.trophy_name] = {'earned': x.earned, 'date': None}

                title_data = {
                    'accountid': sqlite.get_table_PlaystationUser_accountid(playstationid),
                    'title_id': i.title_id,
                    'np_communication_id': j.np_communication_id,
                    'progress': j.progress,
                    'bronze': j.earned_trophies['bronze'],
                    'silver': j.earned_trophies['silver'],
                    'gold': j.earned_trophies['gold'],
                    'platinum': j.earned_trophies['platinum'],
                    'play_duration': i.play_duration.seconds,
                    'play_count': i.play_count,
                    'first_played_date_time': i.first_played_date_time.date().strftime("%Y/%m/%d"),
                    'last_played_date_time': i.last_played_date_time.date().strftime("%Y/%m/%d"),
                    'category': i.category.name,
                    'achievements': str(dict)
                }
        except:
            title_data = {
                'accountid': sqlite.get_table_PlaystationUser_accountid(playstationid),
                'title_id': i.title_id,
                'np_communication_id': None,
                'progress': 0,
                'bronze': None,
                'silver': None,
                'gold': None,
                'platinum': None,
                'play_duration': i.play_duration.seconds,
                'play_count': i.play_count,
                'first_played_date_time': i.first_played_date_time.date().strftime("%Y/%m/%d"),
                'last_played_date_time': i.last_played_date_time.date().strftime("%Y/%m/%d"),
                'category': i.category.name,
                'achievements': None
            }

        if sqlite.get_table_PlaystationUsersLibrary_titleid(i.title_id) is False:
            values = tuple[(
                title_data['accountid'],
                title_data['title_id'],
                title_data['np_communication_id'],
                title_data['progress'],
                title_data['bronze'],
                title_data['silver'],
                title_data['gold'],
                title_data['platinum'],
                title_data['play_duration'],
                title_data['play_count'],
                title_data['first_played_date_time'],
                title_data['last_played_date_time'],
                title_data['category'],
                title_data['achievements'],
            )]
            sqlite.insert_table_PlaystationUserLibrary(values)
        else:
            values = tuple([title_data['progress'],
                            title_data['bronze'],
                            title_data['silver'],
                            title_data['gold'],
                            title_data['platinum'],
                            title_data['play_duration'],
                            title_data['play_count'],
                            title_data['last_played_date_time'],
                            title_data['achievements'],
                            title_data['accountid'],
                            title_data['title_id']
                            ])
            sqlite.update_table_PlaystationUserLibary(values)
