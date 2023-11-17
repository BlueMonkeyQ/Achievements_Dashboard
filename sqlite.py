import sqlite3


def connect_to_database():
    """Establishes a connection to local sqlite3 database"""
    database_name = "data/Achievements.db"
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error: {e}")
        raise


def disconnect_from_database(conn):
    """Disconnects from sqlite3 database if connected"""
    if conn:
        conn.close()


# ---------------------------------------- Stored Procedure ----------------------------------------
def steamgame_analytics(gamename):
    """SELECT all unique games that belong to a steamid"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT
        sa.apiname
        ,sa.percent
        ,sul.img_icon_url
        ,sul.playtime_forever
        ,sul.achivements
        FROM SteamGames as sg
        JOIN SteamAchivements as sa
        ON sa.appid = sg.appid
        JOIN SteamUserLibrary as sul
        ON sul.appid = sg.appid
        WHERE sg.gamename = ?
        """
        cursor.execute(query, (gamename,))
        records = cursor.fetchall()
        return records
    except:
        print(f"ERROR: Unable to SELECT gamename: {gamename}")
        return False
    finally:
        disconnect_from_database(conn)


# ---------------------------------------- Users Table ----------------------------------------
def users_select_account_exist(userid):
    """SELECT userid from Users Table to see if record exist"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT COUNT(*) FROM Users WHERE userid = ?
        """
        cursor.execute(query, (userid,))
        records = cursor.fetchone()[0]
        return records > 0
    except:
        print(f"ERROR: Unable to SELECT userid: {userid}")
        return False
    finally:
        disconnect_from_database(conn)


# ---------------------------------------- SteamUsers Table ----------------------------------------
def steamusers_select_account_exist(userid):
    """SELECT userid from SteamUsers Table to see if record exist"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT COUNT(*) FROM SteamUsers WHERE userid = ?
        """
        cursor.execute(query, (userid,))
        records = cursor.fetchone()[0]
        return records > 0
    except:
        print(f"ERROR: Unable to SELECT userid: {userid}")
        return False
    finally:
        disconnect_from_database(conn)


def steamusers_select_account(userid):
    """SELECT steamid in the SteamUsers Table. Returns a Tuples of users data"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT * FROM SteamUsers WHERE userid = ?
        """
        cursor.execute(query, (userid,))
        records = cursor.fetchone()
        return records
    except:
        print(f"ERROR: Unable to SELECT userid: {userid}")
        return False
    finally:
        disconnect_from_database(conn)


def steamusers_select_account_steamid(userid):
    """SELECT steamid in the SteamUsers Table. Returns the userid's steamid"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT steamid FROM SteamUsers WHERE userid = ?
        """
        cursor.execute(query, (userid,))
        records = cursor.fetchone()[0]
        return records
    except:
        print(f"ERROR: Unable to SELECT userid: {userid}")
        return False
    finally:
        disconnect_from_database(conn)


def steamusers_insert_account(values):
    """INSERT a new record into the SteamUsers Table"""
    try:
        conn, cursor = connect_to_database()
        query = """
        INSERT INTO SteamUsers (userid, steamid, personaname, profileurl, avatar, avatarmedium, avatarfull, personastate, communityvisibilitystate, profilestate, lastlogoff, commentpermission, realname, primaryclanid, timecreated, gameid, gameserverip, gameextrainfo, cityid, loccountrycode, locstatecode, loccityid)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(query, values)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("WARNING: Record already Exists")
        return True
    except sqlite3.OperationalError as e:
        print(f"ERROR: Unable to INSERT SteamUsers: {e}")
        return False
    finally:
        disconnect_from_database(conn)


# ---------------------------------------- SteamUserLibrary Table ----------------------------------------
def steamuserlibrary_insert_game(values):
    """INSERT a new record into the SteamUserLibrary Table"""
    try:
        conn, cursor = connect_to_database()
        query = """
        INSERT INTO SteamUserLibrary (steamid, appid, img_icon_url, has_community_visible_stats, playtime_forever, achivements)
        VALUES (?,?,?,?,?,?)
        """
        cursor.execute(query, values)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("WARNING: Record already Exists")
        return True
    except sqlite3.OperationalError as e:
        print(f"ERROR: Unable to INSERT SteamUserLibrary: {e}")
        return False
    finally:
        disconnect_from_database(conn)


def steamuserlibrary_select_all(steamid):
    """SELECT all unique games FROM STEAMUSERLIBRARY that belong to a steamid"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT * FROM SteamUserLibrary WHERE steamid = ?
        """
        cursor.execute(query, (steamid,))
        records = cursor.fetchall()
        return records
    except:
        print(f"ERROR: Unable to SELECT userid: {steamid}")
        return False
    finally:
        disconnect_from_database(conn)


def steamuserlibrary_select_all_unique(steamid):
    """SELECT all unique games that belong to a steamid adn returns list of them"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT gamename 
        FROM SteamUserLibrary as sl 
        JOIN SteamGames as sg
        ON sg.appid = sl.appid
        WHERE sl.steamid = ?
        """
        cursor.execute(query, (steamid,))
        records = cursor.fetchall()
        records = [_[0] for _ in records]
        return records
    except:
        print(f"ERROR: Unable to SELECT userid: {steamid}")
        return False
    finally:
        disconnect_from_database(conn)


# ---------------------------------------- SteamAchivements Table ----------------------------------------
def steamachivements_insert_game(values):
    """INSERT a new record into the SteamAchivements Table"""
    try:
        conn, cursor = connect_to_database()
        query = """
        INSERT INTO SteamAchivements (appid, apiname, percent)
        VALUES (?,?,?)
        """
        cursor.execute(query, values)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("WARNING: Record already Exists")
        return True
    except sqlite3.OperationalError as e:
        print(f"ERROR: Unable to INSERT SteamAchivements: {e}")
        return False
    finally:
        disconnect_from_database(conn)


# ---------------------------------------- SteamGames Table ----------------------------------------
def steamgames_select_game_name(appid):
    """SELECT gamename in the SteamGames Table. Returns the appid's gamename"""
    try:
        conn, cursor = connect_to_database()
        query = """
        SELECT gamename FROM SteamGames WHERE appid = ?
        """
        cursor.execute(query, (appid,))
        records = cursor.fetchone()[0]
        return records
    except:
        print(f"ERROR: Unable to SELECT appid: {appid}")
        return False
    finally:
        disconnect_from_database(conn)
