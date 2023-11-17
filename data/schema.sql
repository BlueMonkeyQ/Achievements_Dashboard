CREATE TABLE IF NOT EXISTS "Users" (
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    password TEXT DEFAULT NULL,
    UNIQUE(userid)
);

INSERT INTO Users (userid) VALUES ("FFA3837");

CREATE TABLE IF NOT EXISTS "SteamUsers" (
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    steamid INTEGER NOT NULL,
    personaname TEXT DEFAULT NULL,
    profileurl TEXT DEFAULT NULL,
    avatar TEXT DEFAULT NULL,
    avatarmedium TEXT DEFAULT NULL,
    avatarfull TEXT DEFAULT NULL,
    personastate INTEGER DEFAULT NULL,
    communityvisibilitystate INTEGER DEFAULT NULL,
    profilestate INTEGER DEFAULT NULL,
    lastlogoff INTEGER DEFAULT NULL,
    commentpermission TEXT DEFAULT NULL,
    realname TEXT DEFAULT NULL,
    primaryclanid TEXT DEFAULT NULL,
    timecreated INTEGER DEFAULT NULL,
    gameid INTEGER DEFAULT NULL,
    gameserverip TEXT DEFAULT NULL,
    gameextrainfo TEXT DEFAULT NULL,
    cityid INTEGER DEFAULT NULL,
    loccountrycode TEXT DEFAULT NULL,
    locstatecode TEXT DEFAULT NULL,
    loccityid TEXT DEFAULT NULL,
    UNIQUE(userid,steamid)
);

CREATE TABLE IF NOT EXISTS "SteamUserFriends" (
    id INTEGER PRIMARY KEY,
    steamid INTEGER NOT NULL,
    friendid INTEGER NOT NULL,
    friend_since INTEGER DEFAULT NULL,
    UNIQUE(steamid,friendid)
);

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

CREATE TABLE IF NOT EXISTS "SteamGames" (
    id INTEGER PRIMARY KEY,
    appid INTEGER NOT NULL,
    gamename TEXT DEFAULT NULL,
    UNIQUE(appid)
);

CREATE TABLE IF NOT EXISTS "SteamAchivements" (
    id INTEGER PRIMARY KEY,
    appid INTEGER NOT NULL,
    apiname TEXT NOT NULL,
    percent REAL DEFAULT NULL,
    UNIQUE(appid, apiname)
);