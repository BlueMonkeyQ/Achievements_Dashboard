
def get_playstation_trophy_level_image(trophy_level:int) -> str:
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