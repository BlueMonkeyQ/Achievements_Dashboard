import pandas as pd
import requests
import json
import os
from pathlib import Path


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


def get_api_key():
    """Gets the API key required by the steam API"""
    try:
        filepath = Path(".credentials.txt")
        if os.path.exists(filepath):
            file = open(filepath, "r")
            lines = file.readlines()
            key = lines[0].strip()
            return key
    except:
        print("ERROR: Unable to access .credentials.txt")
        raise
    finally:
        file.close()


def GetPlayerSummaries(api_key, steamid, userid):
    """
    Calls GetPlayerSummaries and Returns basic profile information as a tuple.
    *   Public Data: steamid, personaname, profileurl, avatar, avatarmedium, avatarfull, personastate, communityvisibilitystate, profilestate, lastlogoff, commentpermission
    *   Private Data: realname, primaryclanid, timecreated, gameid, gameserverip, gameextrainfo, cityid, loccountrycode, locstatecode, loccityid
    """
    try:
        jsondata = connection(
            f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid}"
        )
        jsondata = jsondata["response"]["players"][0]

    except:
        return False

    # Checking if account exist by checking if data returned is a empty list
    if jsondata == []:
        return False

    expected_dict = {
        "userid": userid,
        "steamid": None,
        "personaname": None,
        "profileurl": None,
        "avatar": None,
        "avatarmedium": None,
        "avatarfull": None,
        "personastate": None,
        "communityvisibilitystate": None,
        "profilestate": None,
        "lastlogoff": None,
        "commentpermission": None,
        "realname": None,
        "primaryclanid": None,
        "timecreated": None,
        "gameid": None,
        "gameserverip": None,
        "gameextrainfo": None,
        "cityid": None,
        "loccountrycode": None,
        "locstatecode": None,
        "loccityid": None,
    }
    for key in expected_dict:
        try:
            value = jsondata[key]
            expected_dict[key] = value
        except:
            continue

    return (
        expected_dict["userid"],
        expected_dict["steamid"],
        expected_dict["personaname"],
        expected_dict["profileurl"],
        expected_dict["avatar"],
        expected_dict["avatarmedium"],
        expected_dict["avatarfull"],
        expected_dict["personastate"],
        expected_dict["communityvisibilitystate"],
        expected_dict["profilestate"],
        expected_dict["lastlogoff"],
        expected_dict["commentpermission"],
        expected_dict["realname"],
        expected_dict["primaryclanid"],
        expected_dict["timecreated"],
        expected_dict["gameserverip"],
        expected_dict["gameextrainfo"],
        expected_dict["cityid"],
        expected_dict["loccountrycode"],
        expected_dict["locstatecode"],
        expected_dict["loccityid"],
        expected_dict["steamid"],
    )


def GetOwnedGames(api_key, steamid):
    """Calls GetOwnedGames for the provided steamid. Returns List of JSONs of all games"""

    try:
        jsondata = connection(
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steamid}&format=json&include_appinfo=true"
        )
        jsondata = jsondata["response"]["games"]
    except:
        return False

    games = []
    for game in jsondata:
        expected_dict = {
            "steamid": steamid,
            "appid": None,
            "img_icon_url": None,
            "has_community_visible_stats": None,
            "playtime_forever": None,
            "achivements": None,
        }

        for key in expected_dict:
            try:
                value = game[key]
                expected_dict[key] = value
            except:
                continue
        games.append(expected_dict)

    return games


def GetPlayerAchievements(api_key, steamid, appid):
    """Calls GetPlayerAchievements for the provided steamid and appid. Returns JSON String of all achivements"""

    try:
        jsondata = connection(
            f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={api_key}&steamid={steamid}"
        )
        jsondata = jsondata["playerstats"]["achievements"]
    except:
        return False

    achivement_dict = {}
    for achivement in jsondata:
        achivement_dict[achivement["apiname"]] = {
            "achieved": achivement["achieved"],
            "unlocktime": achivement["unlocktime"],
        }

    return json.dumps(achivement_dict)


def GetGlobalAchievementPercentagesForApp(gameid):
    """Calls GetGlobalAchievementPercentagesForApp for the provided gameid. Returns LIST of JSONs of all achivements and Global completion percentage"""

    try:
        jsondata = connection(
            f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={gameid}&format=json"
        )
        jsondata = jsondata["achievementpercentages"]["achievements"]
    except:
        return False

    return jsondata


def GetAppList():
    """Calls GetAppList and returns all games in steam"""

    try:
        jsondata = connection(f"https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        jsondata = jsondata["applist"]["apps"]
    except:
        return False

    return jsondata
