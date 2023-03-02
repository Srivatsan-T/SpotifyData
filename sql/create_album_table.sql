CREATE TABLE IF NOT EXISTS album
(album_id character varying,album_name character varying,popularity integer,artists character varying, genres character varying, PRIMARY KEY(album_id,artists,genres));


