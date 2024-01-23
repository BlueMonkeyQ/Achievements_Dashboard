import requests
from datetime import datetime, timedelta

def connection(url):
    """Establishes a connection to the provided url"""

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return f"Error: Unexpected response {response}"

        geodata = response.json()
        return geodata

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        raise

def cleanup_api_response(dict,expected_keys):
    """
    Given the api and its response dictionary.
    Check if it has all expected Keys. If not, then add the key with a null value.
    Then order the dictionary to its expected order
    """
    
    ordered_dict = {}
    for key in expected_keys:
        if key not in dict:
            dict[key] = None
        ordered_dict[key] = dict[key]
        
    return ordered_dict

# -------------------- STEAM --------------------

# SteamUsers
def get_SteamUsers(api_key,steamid):
    try:
        geodata = connection(
                f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid}"
        )
        jsondata = geodata['response']['players'][0]
        lastupdate = datetime.now()
        lastupdate = lastupdate + timedelta(seconds=10)
        lastupdate = str(lastupdate.time())
        jsondata['userid'] = 0
        jsondata['lastupdate'] = lastupdate

        expected_keys = ['steamid','communityvisibilitystate',
                                'profilestate','personaname','profileurl',
                                'avatar','avatarmedium','avatarfull','avatarhash',
                                'lastlogoff','personastate','realname',
                                'primaryclanid','timecreated','personastateflags',
                                'commentpermission','loccountrycode','locstatecode',
                                'loccityid','userid','lastupdate']

        jsondata = cleanup_api_response(jsondata,expected_keys)
        return tuple(jsondata.values())
    except:
        return False
    
# SteamUsersFriends
def get_SteamUserFriends(api_key,steamid):
    try:
        geodata = connection(
                f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steamid}&relationship=friend"
        )
        jsondata = geodata['friendslist']['friends']
        expected_keys = ['steamid','relationship','friend_since']

        for i in range(len(jsondata)):
            jsondata[i] = cleanup_api_response(jsondata[i],expected_keys)
            dict = {'steamid':steamid,'friendid':jsondata[i]['steamid'],'friend_since':jsondata[i]['friend_since']}
            jsondata[i] = dict

        return [tuple(dict.values()) for dict in jsondata]
    except:
        return False
    
# SteamUserLibrary
def get_SteamUserLibrary(api_key,steamid):
    try:
        geodata = connection(
                f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steamid}&format=json&include_appinfo=true"
        )
        jsondata = geodata['response']['games']
        expected_keys = ['appid','img_icon_url','has_community_visible_stats','playtime_forever','achivements']

        for i in range(len(jsondata)):
            jsondata[i] = cleanup_api_response(jsondata[i],expected_keys)
            dict = {'steamid':steamid,'appid':jsondata[i]['appid'],
                    'img_icon_url':jsondata[i]['img_icon_url'],
                    'has_community_visible_stats':jsondata[i]['has_community_visible_stats'],
                    'playtime_forever':jsondata[i]['playtime_forever'],
                    'achivements':jsondata[i]['achivements']}
            jsondata[i] = dict

        return [tuple(dict.values()) for dict in jsondata]
    except:
        return False
    
# SteamAchivements
def get_Users_SteamAchivements(api_key,steamid,appid):
    try:
        geodata = connection(
                f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={api_key}&steamid={steamid}"
        )
        jsondata = geodata['playerstats']['achievements']
        expected_keys = ['apiname','achieved','unlocktime']

        dict = {}
        for i in range(len(jsondata)):
            jsondata[i] = cleanup_api_response(jsondata[i],expected_keys)
            dict[jsondata[i]['apiname']] = {'achieved':jsondata[i]['achieved'],'unlocktime':jsondata[i]['unlocktime']}

        return tuple([str(dict), steamid, 240])
    except:
        return False

def get_SteamAchivements(appid):
    try:
        geodata = connection(
                f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json"
        )
        jsondata = geodata['achievementpercentages']['achievements']
        expected_keys = ['name','percent']

        dict = {}
        for i in range(len(jsondata)):
            jsondata[i] = cleanup_api_response(jsondata[i],expected_keys)
            dict = {'appid':appid,'apiname':jsondata[i]['name'], 'percent':jsondata[i]['percent']}
            jsondata[i] = dict
            
        return [tuple(dict.values()) for dict in jsondata][0]
    except:
        return False