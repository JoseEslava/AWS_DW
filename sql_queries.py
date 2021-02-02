import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events(
artist varchar,
auth varchar,
firstName varchar,
gender char,
itemInSession int,
lastName varchar,
length float,
level varchar,
location varchar,
method varchar,
page varchar,
registration float,
sessionId int,
song varchar,
status int,
ts bigint,
userAgent varchar,
userId int
)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
num_songs int,
artist_id varchar,
artist_latitude float,
artist_longitude float,
artist_location varchar,
artist_name varchar,
song_id varchar,
title varchar,
duration float,
year int
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay (
songplay_id bigint IDENTITY(1,1) PRIMARY KEY,
start_time timestamp NOT NULL,
user_id int NOT NULL,
level varchar,
song_id varchar,
artist_id varchar,
session_id varchar,
location varchar,
user_agent varchar)
DISTSTYLE KEY
DISTKEY(start_time)
SORTKEY(start_time)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id int PRIMARY KEY,
first_name varchar NOT NULL,
last_name varchar NOT NULL,
gender char NOT NULL,
level varchar NOT NULL)
SORTKEY(user_id)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id varchar PRIMARY KEY,
title varchar NOT NULL,
duration float NOT NULL,
year int NOT NULL)
SORTKEY(song_id)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id varchar NOT NULL,
artist_latitude float,
artist_longitude float,
artist_location varchar NOT NULL,
artist_name varchar NOT NULL)
SORTKEY(artist_id)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time timestamp PRIMARY KEY,
hour int NOT NULL,
day int NOT NULL,
week int NOT NULL,
month int NOT NULL,
year int NOT NULL,
weekday varchar NOT NULL)
DISTSTYLE KEY
DISTKEY(start_time)
SORTKEY(start_time)
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {}
iam_role {}
FORMAT AS json {}
REGION AS 'us-west-2'
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs
FROM {}
iam_role {}
FORMAT AS json 'auto'
REGION AS 'us-west-2'
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS start_time, userid, level, song_id, artist_id, sessionid, location, useragent
FROM staging_events AS se
INNER JOIN staging_songs AS ss
ON ss.artist_name = se.artist AND ss.title = se.song AND se.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users
SELECT userId, firstName, lastName, gender, level
FROM staging_events
WHERE userId IS NOT NULL AND page = 'NextSong'
""")

song_table_insert = ("""
INSERT INTO songs
SELECT song_id, title, artist_id, year, duration
FROM staging_songs
WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists
SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time
SELECT
TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' as start_time,
EXTRACT(HOUR FROM start_time)  AS hour,
EXTRACT(DAY FROM start_time)   AS day,
EXTRACT(WEEKS FROM start_time) AS week,
EXTRACT(MONTH FROM start_time) AS month,
EXTRACT(YEAR FROM start_time)  AS year,
to_char(start_time, 'Day') AS weekday
FROM staging_events
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
