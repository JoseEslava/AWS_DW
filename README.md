# Project Summary
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, Sparkify has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

# Star schema
Perform ETL to create `songs`, `artists`, `users` and `time` dimensional tables; `songplay` fact table INTO AWS redshift cluster

- Use the `load_staging_tables` function to load JSON files from LOG_DATA and SONG_DATA
- Use the `insert_tables` function to read records from staging tables (temp storage) and write them on dimensional and fact tables (permanent storage)

# Different regions
Be careful if redshift cluster is in a different region from S3 bucket, in that case you have to specify the REGION on COPY statement. This operation between regions is time consuming

- COPY staging_events FROM {} iam_role {} FORMAT AS json {} REGION AS 'us-west-2'