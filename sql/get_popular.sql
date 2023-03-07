with liked as

(select song_id,song_name,album.album_name ,array_to_string(array_agg(distinct artist_name),',') as artists ,ls.popularity,preview_url,ls.added_at  from liked_songs ls ,artist a,album 
where ls.artists = a.artist_id and ls.album = album.album_id  group by song_id,song_name,album_name,ls.popularity,preview_url,ls.added_at  order by added_at desc),

yearwise as
(select * from liked where date_part('YEAR',added_at)  = {} and date_part('MONTH',added_at)  = {})

select song_name,album_name,popularity,date_part('YEAR',added_at) as added_year,date_part('MONTH',added_at) as added_month from yearwise order by popularity {} limit 1
 
