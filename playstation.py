import streamlit as st
import sqlite
import pandas as pd
import functions as f
from psnawp_api import PSNAWP
from datetime import datetime, timedelta


def playstation_dashboard(playstation_tab, user:tuple, p_user: PSNAWP):
    """
    Handles the Playstation Tab
    Displays Basic User Demographics
    Displays Trophy level and progress bar until next tier
    Displays Amount earned for each trophy
    Displays Table of the users Playstation library
    """

    # Update Button
    # If enough time has passed, update button becomes available
    col1, col2 = st.columns(2)
    last_update_time = sqlite.get_table_Users_playstation_update_datetime(user[1])
    last_update_time = datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S.%f")

    with col1:

        #@TODO: Prevent update spamming by adding a timer 
        # current_datetime = datetime.now()
        # target_datetime = last_update_time + timedelta(minutes=1)

        # if current_datetime < target_datetime:
        #     st.button(label=f"Available in {target_datetime.second} seconds",key='playstation_update',disabled=True, use_container_width=True)
        # else:
            # update = st.button(label='Update Library',key='playstation_update',disabled=False, use_container_width=True)
            # if update:
            #     last_update_time = datetime.now()
            #     values = tuple[(
            #         datetime.now(),
            #         str(user[1])
            #     )]
            #     sqlite.update_table_Users_playstation_update_datetime(values)
        
        # @TODO: Implement Updating Users Game Library
        update = st.button(label='Update Library',key='playstation_update',disabled=False, use_container_width=True)
        if update:
            userid = str(user[1])
            last_update_time = datetime.now()
            values = tuple([
                datetime.now(),
                userid
            ])
            sqlite.update_table_Users_playstation_update_datetime(values)

    # Last updated Datetime
    with col2:
        st.text(f"Last Updated: {last_update_time.hour}:{last_update_time.minute} {last_update_time.day}-{last_update_time.month}-{last_update_time.year}")

    # Basic User Demographics
    user_info = sqlite.get_table_PlaystationUser(onlineid=p_user.online_id)
    
    col1,col2 = playstation_tab.columns(2)

    # Avatar
    with col1:
        col1.image(user_info[11])

    # Demographics
    with col2:
        col2.header(user_info[1])
        col2.text(f"{user_info[12]} {user_info[13]}")
        col2.text(user_info[14])
        
    # Trophys
    col1,col2,col3,col4,col5 = playstation_tab.columns(5)

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
    playstation_tab.progress(value=user_info[4],text=f'Tier: {user_info[5]}')

    # Playstation Library
    game_library = sqlite.get_table_PlaystationUserLibary('6742668592208867459')

    df = pd.DataFrame(columns=['Logo','Title','Progress','Platinum','Gold','Silver','Bronze','Playtime'])
    for game in game_library:
        info = sqlite.get_table_PlaystationLibary(titleid=game[2])
        dict = {
            'Logo':info[3],
            'Title':info[2],
            'Progress':game[4],
            'Platinum':game[8],
            'Gold':game[7],
            'Silver':game[6],
            'Bronze':game[5],
            'Playtime':game[9]
        }
        new_df = pd.DataFrame([dict])
        df = pd.concat([df,new_df],axis=0,ignore_index=True)
    
    # Sort by Platinum then Hours
    df = df.sort_values(by=['Platinum','Playtime'], ascending=[False,False])

    # Display the Table
    playstation_tab.data_editor(
        df,
        use_container_width=True,
        column_config={
            "Logo": st.column_config.ImageColumn(
                width=100
            ),
            "Progress": st.column_config.ProgressColumn(
                format="%i",
                min_value=0,
                max_value=100
            ),
        },
        hide_index=True
    )