CREATE TABLE if not EXISTS liked_songs
(song_id character varying,song_name character varying,added_at timestamp,popularity integer,preview_url character varying,duration_ms integer,
album character varying , artists character varying, PRIMARY KEY(song_id,artists));

