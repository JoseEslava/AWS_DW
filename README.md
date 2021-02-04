# Project Summary
A startup called Sparkify wants to analyze the data they've been collecting on songs [SONG DATA] and user activity [LOG DATA] on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, Sparkify has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

# Files on this repository
Making a Cloud DataWarehouse using Amazon Redshift Cluster requires load data from S3 to staging tables and insert records from staging tables to star schema tables

- 'create_tables.py' calls drop_tables & create_tables functions for making data structure
- 'etl.py' calls load_staging_tables & insert_tables functions for loading data and insert rows on star schema. Data from S3 is json format, the file 'log_json_path.json' is a format template for LOG data.
- 'sql_queries.py' is used to define tables structure
- 'wordcloud.ipynb' is a notebook that makes a wordcloud with songs titles, is necessary to install wordcloud library
![image](wordcloudTitles.png)

# Star schema
Perform ETL to create `songs`, `artists`, `users` and `time` dimensional tables; `songplay` fact table INTO AWS redshift cluster

- Use the `load_staging_tables` function to load JSON files from LOG_DATA and SONG_DATA (raw data)
- Use the `insert_tables` function to read records from staging tables (temp storage without filters) and write them on dimensional and fact tables (permanent storage); the main filter applied is page = 'NextSong'. This function execute some queries:
    - `songplay_table_insert` is for fact table and filters records that match song title, artist name and song duration
    - `user_table_insert` is for dim table without additional record filter
    - `song_table_insert` is for dim table with song_id IS NOT NULL record filter
    - `artist_table_insert` is for dim table with song_id IS NOT NULL record filter
    - `time_table_insert` is for dim table without additional record filter

# Services in different AWS regions
Be careful if redshift cluster is in a different region from S3 bucket, in that case you have to specify the REGION on COPY statement. This operation between regions is time consuming

- COPY staging_events FROM {} iam_role {} FORMAT AS json {} REGION AS 'us-west-2'

 # How to run the python scripts
 From terminal windows you should use python command followed by the file name:
 - python create_tables.py
 - python etl.py