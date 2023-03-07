with liked as

(select song_id,song_name,album.album_name ,array_to_string(array_agg(distinct artist_name),',') as artists ,ls.popularity,preview_url,ls.added_at  from liked_songs ls ,artist a,album 
where ls.artists = a.artist_id and ls.album = album.album_id  group by song_id,song_name,album_name,ls.popularity,preview_url,ls.added_at  order by added_at desc),

yearwise as
(select * from liked where extract ('year' from added_at) = {})

select album_name,count(*) from yearwise group by album_name order by count(*)desc ,album_name desc limit 3
 
