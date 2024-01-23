import streamlit as st
import sqlite
import pandas as pd
from main import psnawp
from pathlib import Path


def playstation_dashboard(playstation_tab, user):
    """
    
    """

    # Basic User Information
    # Avatar
    # Username
    # Firstname, Lastname, About me
    user_info = sqlite.get_table_PlaystationUser(onlineid=user.online_id)
    
    col1,col2 = playstation_tab.columns(2)

    with col1:
        col1.image(user_info[11])

    with col2:
        col2.header(user_info[1])
        col2.text(f"{user_info[12]} {user_info[13]}")
        col2.text(user_info[14])
        
    # Tropheys
    # Trophey Level, Platinum, Gold, Silver, Bronze
    col1,col2,col3,col4,col5 = playstation_tab.columns(5)
    
    with col1:
        trophy_level = user_info[3]
        if trophy_level == 999:
            col1.image(image='data\\images\\trophey_level_10.png')

        elif trophy_level >= 800:
            col1.image(image='data\\images\\trophey_level_9.png')

        elif trophy_level >= 700:
            col1.image(image='data\\images\\trophey_level_8.png')
        
        elif trophy_level >= 600:
            col1.image(image='data\\images\\trophey_level_7.png')
            
        elif trophy_level >= 500:
            col1.image(image='data\\images\\trophey_level._6png')
            
        elif trophy_level >= 400:
            col1.image(image='data\\images\\trophey_level_5.png')
            
        elif trophy_level >= 300:
            col1.image(image='data\\images\\trophey_level_4.png')
            
        elif trophy_level >= 200:
            col1.image(image='data\\images\\trophey_level_3.png')
            
        elif trophy_level >= 100:
            col1.image(image='data\\images\\trophey_level_2.png')
            
        else:
            col1.image(image='data\\images\\trophey_level_1.png')
            
        col1.subheader(user_info[3])

    with col2:
        col2.image(image='data\\images\\platinum.png')
        col2.subheader(user_info[9])

    with col3:
        col3.image(image='data\\images\\gold.png')
        col3.subheader(user_info[8])

    with col4:
        col4.image(image='data\\images\\silver.png')
        col4.subheader(user_info[7])
                    
    with col5:
        col5.image(image='data\\images\\bronze.png')
        col5.subheader(user_info[6])

    playstation_tab.progress(value=user_info[4],text=f'Tier: {user_info[5]}')

    # Trophys
    game_library = sqlite.get_table_PlaystationUserLibary('6742668592208867459')
    df = pd.DataFrame(columns=['image_url','title_name','progress','bronze','silver','gold','platinum','hours'])
    for game in game_library:
        info = sqlite.get_table_PlaystationLibary(titleid=game[2])
        dict = {
            'image_url':info[3],
            'title_name':info[2],
            'progress':game[4],
            'bronze':game[5],
            'silver':game[6],
            'gold':game[7],
            'platinum':game[8],
            'hours':game[9]
        }
        new_df = pd.DataFrame([dict])
        df = pd.concat([df,new_df],axis=0,ignore_index=True)
    
    playstation_tab.data_editor(
        df,
        use_container_width=True,
        column_config={
            "image_url": st.column_config.ImageColumn(
                width=100
            ),
            "progress": st.column_config.ProgressColumn(
                format="%i",
                min_value=0,
                max_value=100
            ),
        },
        hide_index=True
    )

def steam_dashboard(steam_tab, user):
    pass

def get_master_url(images):
    for image in images:
        if image['type'] == 'MASTER':
            return image['url']
    return None

def update_PlaystationUserLibrary(online_id, p_user):
    for i in p_user.title_stats():
        if sqlite.get_table_PlaystationLibrary_titleid(i.title_id) == False:
            try:
                game = psnawp.game_title(title_id=i.title_id,account_id='6515971742264256071')
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
                    game_data['name'],
                    get_master_url(game_data['media']['images']),
                    game_trophy.defined_trophies.bronze,
                    game_trophy.defined_trophies.silver,
                    game_trophy.defined_trophies.gold,
                    game_trophy.defined_trophies.platinum,
                ])
                sqlite.insert_table_PlaystationLibrary(values)
                continue

            try:
                gametitle = psnawp.game_title(title_id=i.title_id)
                platform = sqlite.get_table_PlaystationUserLibary_platform(i.title_id)
                if platform == False: raise
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
                continue

        for j in p_user.trophy_titles_for_title(title_ids=[i.title_id]):

            # Achivements
            dict = {}
            trophy_data = p_user.trophies(np_communication_id=j.np_communication_id, platform=i.category.name, include_metadata=True)
            for x in trophy_data:
                if x.earned == True:
                    dict[x.trophy_name] = {'earned':x.earned, 'date':x.earned_date_time.strftime("%Y/%d/%m")}
                else:
                    dict[x.trophy_name] = {'earned':x.earned, 'date':None}

            values = tuple([
                sqlite.get_table_PlaystationUser_accountid('BluemonkeyQ'),
                i.title_id,
                j.np_communication_id,
                j.progress,
                j.earned_trophies['bronze'],
                j.earned_trophies['silver'],
                j.earned_trophies['gold'],
                j.earned_trophies['platinum'],
                i.play_duration.seconds,
                i.play_count,
                i.first_played_date_time.date().strftime("%Y/%m/%d"),
                i.last_played_date_time.date().strftime("%Y/%m/%d"),
                i.category.name,
                str(dict)
            ])
        
        sqlite.insert_table_PlaystationUserLibary(values)
        sqlite.insert_table_PlaystationUserLibary(values)


def account_dashboard(account_tab, user, p_user):

    col1,col2 = account_tab.columns(2)

    with col1:
        col1.image(image='data\\images\\steam_logo.jpeg')

    with col2:
        on = st.toggle("Update", key="steam")
        if on:
            pass

    col1,col2 = account_tab.columns(2)

    with col1:
        col1.image(image='data\\images\\steam_logo.jpeg')

    with col2:
        if col2.button(label="Update",key='playstation'):
            update_PlaystationUserLibrary(user[4],p_user)