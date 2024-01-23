import sqlite
import api

api_key = "14EB214CEC3F1701FD192885D330990F"
steamid = "76561198050437739"

# -------------------- SteamUsers --------------------

def test_reset_table_SteamUsers():
    # Passing
    assert sqlite.reset_table_SteamUsers() == True


def test_insert_table_SteamUsers():
    global api_key
    global steamid

    # Passing
    assert sqlite.reset_table_SteamUsers() == True
    values = api.get_SteamUsers(api_key, steamid)
    assert type(values) == tuple
    assert sqlite.insert_table_SteamUsers(values) == True
    assert sqlite.insert_table_SteamUsers(values) == True

    # Failing
    values = tuple([])
    assert sqlite.insert_table_SteamUsers(values) == False


def test_update_table_SteamUsers():
    global api_key
    global steamid

    # Passing
    values = api.get_SteamUsers(api_key, steamid)
    assert sqlite.update_table_SteamUsers(values) == True

    # Failing
    values = tuple([])
    assert sqlite.insert_table_SteamUsers(values) == False


def test_get_table_SteamUsers():
    global api_key
    global steamid

    # Passing
    values = sqlite.get_table_SteamUsers(steamid)
    assert len(values) == 22

    # Failing
    values = sqlite.get_table_SteamUsers('DNE')
    assert values == False

# -------------------- SteamUserFriends --------------------
def test_reset_table_SteamUserFriends():
    # Passing
    assert sqlite.reset_table_SteamUserFriends() == True

def test_insert_table_SteamUserFriends():
    global api_key
    global steamid

    # Passing
    assert sqlite.reset_table_SteamUserFriends() == True
    values = api.get_SteamUserFriends(api_key,steamid)
    for friend in values:
        assert sqlite.insert_table_SteamUserFriends(friend) == True
        assert sqlite.insert_table_SteamUserFriends(friend) == True
    
    # Failing
    values = tuple([])
    assert sqlite.insert_table_SteamUserFriends(values) == False

# -------------------- SteamUserLibrary --------------------
def test_reset_table_SteamUserLibrary():
    # Passing
    assert sqlite.reset_table_SteamUserLibrary() == True


def test_insert_table_SteamUserLibrary():
    global api_key
    global steamid

    # Passing
    assert sqlite.reset_table_SteamUserLibrary() == True
    values = api.get_SteamUserLibrary(api_key,steamid)
    for game in values:
        assert sqlite.insert_table_SteamUserLibrary(game) == True
        assert sqlite.insert_table_SteamUserLibrary(game) == True

    # Failing
    values = tuple([])
    assert sqlite.insert_table_SteamUserLibrary(values) == False


def test_update_table_SteamUserLibrary_Achivements():
    global api_key
    global steamid

    # Passing
    values = api.get_Users_SteamAchivements(api_key,steamid,240)
    assert type(values) == tuple
    assert sqlite.update_table_SteamUserLibrary_Achivements(values) == True

    # Failing
    values = api.get_Users_SteamAchivements(api_key,steamid,10011010100101)
    assert sqlite.update_table_SteamUserLibrary_Achivements(values) == False