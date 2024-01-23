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

def query_database(query,values=None):
    try:
        conn, cursor = connect_to_database()
        if values:
            cursor.execute(query,values)
            conn.commit()
            print("SUCCESS: Query ran")
        else:
            cursor.execute(query)

        return cursor.fetchall()

    except sqlite3.IntegrityError:
        print("WARNING: Record already Exists")
        return True
    
    except sqlite3.OperationalError as e:
        print(f"ERROR: Unable to INSERT query: {e}")
        return False
    
    finally:
        disconnect_from_database(conn)

def disconnect_from_database(conn):
    """Disconnects from sqlite3 database if connected"""
    if conn:
        conn.close()

def insert_table_Users(values):
    try:
        query = """
        INSERT INTO "Users" (
            userid,
            password,
            steamid,
            playstationid
            )
        VALUES (?,?,?,?)
        """
        query_database(query,values)
    except:
        return False

def get_table_Users(userid):
    try:
        query = """
        SELECT
        *
        FROM Users
        WHERE userid = ?
        """
        return query_database(query,(userid,))[0]
    except:
        return False

# -------------------- STEAM --------------------

# SteamUsers
def reset_table_SteamUsers() -> bool:
    # Drops the Table and re-creates it
    try:
        query = """
        DROP TABLE SteamUsers;
        """
        query_database(query)

        query = """
        CREATE TABLE IF NOT EXISTS "SteamUsers" (
        id INTEGER PRIMARY KEY,
        steamid INTEGER NOT NULL,
        communityvisibilitystate INTEGER DEFAULT NULL,
        profilestate INTEGER DEFAULT NULL,
        personaname TEXT DEFAULT NULL,
        profileurl TEXT DEFAULT NULL,
        avatar TEXT DEFAULT NULL,
        avatarmedium TEXT DEFAULT NULL,
        avatarfull TEXT DEFAULT NULL,
        avatarhash TEXT DEFAULT NULL,
        lastlogoff INTEGER DEFAULT NULL,
        personastate INTEGER DEFAULT NULL,
        realname TEXT DEFAULT NULL,
        primaryclanid TEXT DEFAULT NULL,
        timecreated INTEGER DEFAULT NULL,
        personastateflags INTEGER DEFAULT NULL,
        commentpermission TEXT DEFAULT NULL,
        loccountrycode TEXT DEFAULT NULL,
        locstatecode TEXT DEFAULT NULL,
        loccityid TEXT DEFAULT NULL,
        userid INTEGER NOT NULL,
        lastupdate TEXT DEFAULT NULL,
        UNIQUE(userid,steamid)
        );
        """
        query_database(query)
        return True
    except:
        return False

def insert_table_SteamUsers(values) -> bool:
    try:
        query = """
        INSERT INTO SteamUsers (
            steamid, communityvisibilitystate, profilestate, 
            personaname, profileurl, avatar, 
            avatarmedium, avatarfull, avatarhash, 
            lastlogoff, personastate, realname, 
            primaryclanid, timecreated, personastateflags,
            commentpermission,
            loccountrycode, locstatecode, loccityid,
            userid, lastupdate)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        """
        query_database(query,values)
        return True
    except:
        return False

def get_table_SteamUsers(steamid) -> tuple:
    try:
        query = """
        SELECT
        *
        FROM SteamUsers
        WHERE steamid = ?
        """
        return query_database(query,(steamid,))[0]
    except:
        return False

def update_table_SteamUsers(values) -> bool:
    try:
        query = """
        UPDATE SteamUserLibrary 
        SET communityvisibilitystate  = ?,
            profilestate  = ?,
            personaname  = ?,
            profileurl  = ?,
            avatar  = ?,
            avatarmedium  = ?,
            avatarfull  = ?,
            avatarhash  = ?,
            lastlogoff  = ?,
            personastate  = ?,
            realname  = ?,
            primaryclanid  = ?,
            timecreated  = ?,
            personastateflags  = ?,
            commentpermission  = ?,
            loccountrycode  = ?,
            locstatecode  = ?,
            loccityid  = ?,
            userid  = ?,
            lastupdate  = ? 
        WHERE steamid = ?
        """
        query_database(query,values)
        return True
    except:
        return False
    
# SteamUserFriends
def reset_table_SteamUserFriends() -> bool:
    # Drops the Table and re-creates it
    try:
        query = """
        DROP TABLE SteamUserFriends;
        """
        query_database(query)

        query = """
        CREATE TABLE IF NOT EXISTS "SteamUserFriends" (
        id INTEGER PRIMARY KEY,
        steamid INTEGER NOT NULL,
        friendid INTEGER NOT NULL,
        friend_since INTEGER DEFAULT NULL,
        UNIQUE(steamid,friendid)
        );
        """
        query_database(query)
        return True
    except:
        return False
    
def insert_table_SteamUserFriends(values) -> bool:
    try:
        query = """
        INSERT INTO SteamUserFriends (
            steamid, friendid, friend_since
            )
        VALUES (?,?,?);
        """
        query_database(query,values)
        return True
    except:
        return False
    
# SteamUserLibrary
def reset_table_SteamUserLibrary() -> bool:
    # Drops the Table and re-creates it
    try:
        query = """
        DROP TABLE SteamUserLibrary;
        """
        query_database(query)

        query = """
        CREATE TABLE IF NOT EXISTS "SteamUserLibrary" (
        id INTEGER PRIMARY KEY,
        steamid INTEGER NOT NULL,
        appid INTEGER NOT NULL,
        img_icon_url TEXT DEFAULT NULL,
        has_community_visible_stats INTEGER DEFAULT NULL,
        playtime_forever INTEGER DEFAULT NULL,
        achivements TEXT DEFAULT NULL,
        UNIQUE(steamid,appid)
        );
        """
        query_database(query)
        return True
    except:
        return False

def insert_table_SteamUserLibrary(values) -> bool:
    try:
        query = """
        INSERT INTO SteamUserLibrary (
            steamid, appid, img_icon_url,
            has_community_visible_stats, playtime_forever, achivements
            )
        VALUES (?,?,?,?,?,?);
        """
        query_database(query,values)
        return True
    except:
        return False


def update_table_SteamUserLibrary_Achivements(values) -> bool:
    try:
        query = """
        UPDATE SteamUserLibrary 
        SET achivements = ? 
        WHERE steamid = ?
        AND appid = ?
        """
        query_database(query,values)
        return True
    except:
        return False

# -------------------- PLAYSTATION --------------------
# PlaystationUser
def get_table_PlaystationUser(onlineid):
    """
    
    """
    try:
        query = """
        SELECT
        *
        FROM PlaystationUser
        WHERE onlineid = ?
        """
        return query_database(query,(onlineid,))[0]
    except:
        return False
    
def get_table_PlaystationUser_accountid(onlineid:str):
    try:
        query = """
        SELECT
        accountid
        FROM PlaystationUser
        WHERE onlineid = ?
        """
        return query_database(query,(onlineid,))[0][0]
    except:
        return False
    
def insert_table_PlaystationUser(values) -> bool:
    try:
        query = """
        INSERT INTO "PlaystationUser" (
            onlineid,
            accountid,
            trophy_level,
            progress,
            tier,
            bronze,
            silver,
            gold,
            platinum,
            profile_url,
            avatar_url,
            firstname,
            lastname,
            about_me
            )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        """
        query_database(query,values)
        return True
    except:
        return False

# PlaystationAchivements
def insert_table_PlaystationAchivements(values) -> bool:
    try:
        query = """
        INSERT INTO "PlaystationAchivements" (
            titleid,
            trophy_name,
            trophy_type,
            trophy_detail,
            trophy_icon_url
            )
        VALUES (?,?,?,?,?);
        """
        query_database(query,values)
        return True
    except:
        return False

def get_table_PlaystationAchivements_trophy_count(titleid,trophy_type):
    try:
        query = """
        SELECT
        COUNT (*)
        FROM PlaystationAchivements
        WHERE titleid = ?
        AND trophy_type = ?
        """
        return query_database(query,(titleid,trophy_type,))[0][0]
    except:
        return False
    
# PlaystationLibrary
def insert_table_PlaystationLibrary(values):
    try:
        query = """
        INSERT INTO "PlaystationLibrary" (
            titleid,
            title_name,
            title_icon_url,
            bronze,
            silver,
            gold,
            platinum
            )
        VALUES (?,?,?,?,?,?,?);
        """
        query_database(query,values)
    except:
        return False

def update_table_PlaystationLibrary_trophys(values) -> bool:
    try:
        query = """
        UPDATE PlaystationUserLibrary 
        SET 
        bronze = ?,
        silver = ?,
        gold = ?,
        platinum = ?
        WHERE titleid = ?
        """
        query_database(query,values)
    except:
        return False

def get_table_PlaystationLibrary_titleid(title_name):
    try:
        query = f" SELECT titleid FROM PlaystationLibrary WHERE title_name LIKE '%{title_name}%' "
        return query_database(query)[0][0]
    except:
        return False
    
def get_table_PlaystationLibary(titleid):
    try:
        query = """
        SELECT
        *
        FROM PlaystationLibrary
        WHERE titleid = ?
        """
        return query_database(query,(titleid,))[0]
    except:
        return False
    
# PlaystationUserLibrary
    
def insert_table_PlaystationUserLibary(values) -> bool:
    try:
        query = """
        INSERT INTO "PlaystationUserLibrary" (
            accountid,
            titleid,
            np_communication_id,
            progress,
            bronze,
            silver,
            gold,
            platinum,
            playtime,
            play_count,
            first_date_time,
            last_updated_date_time,
            title_platform,
            achivements
            )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        """
        query_database(query,values)
    except:
        return False

def update_table_PlaystationUserLibary_trophys(values) -> bool:
    try:
        query = """
        UPDATE PlaystationUserLibrary 
        SET 
        progress = ?,
        bronze = ?,
        silver = ?,
        gold = ?,
        platinum = ?,
        achivements = ?
        WHERE accountid = ?
        AND titleid = ?
        """
        query_database(query,values)
    except:
        return False

def get_table_PlaystationUserLibary_platform(titleid):
    try:
        query = """
        SELECT
        title_platform
        FROM PlaystationUserLibrary
        WHERE titleid = ?
        """
        return query_database(query,(titleid,))[0][0]
    except:
        return False

def get_table_PlaystationUserLibary(accountid):
    try:
        query = """
        SELECT
        *
        FROM PlaystationUserLibrary
        WHERE accountid = ?
        """
        return query_database(query,(accountid,))
    except:
        return False