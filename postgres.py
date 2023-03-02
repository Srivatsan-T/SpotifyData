import psycopg2
from psycopg2.extras import execute_values

def postgres_init(db = 'postgres',user = 'postgres',pw = 'admin',host = 'localhost',port = '5432'):

    conn = psycopg2.connect(database=db, user = user, password = pw, host = host, port = port)
    return conn

def create_liked_songs_table():
    conn = postgres_init()
    cursor = conn.cursor()
    cursor.execute(open('sql/create_liked_songs.sql').read())
    conn.commit()
    cursor.close()
    conn.close()

def create_recent_songs_table():
    conn = postgres_init()
    cursor = conn.cursor()
    cursor.execute(open('sql/create_recent_songs.sql').read())
    conn.commit()
    cursor.close()
    conn.close()

def create_songs_table():
    conn = postgres_init()
    cursor = conn.cursor()
    cursor.execute(open('sql/create_songs.sql').read())
    conn.commit()
    cursor.close()
    conn.close()

def check_liked_songs():
    conn = postgres_init()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(added_at) from liked_songs')
    conn.commit()
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    if res[0] is not None:
        return res[0],True
    return None,False

def add_liked_songs_dict(songs):
    conn = postgres_init()
    cursor = conn.cursor()

    if songs:
        for i in range(len(songs)):
            song_name = songs[i]['song_name']
            song_name = song_name.replace("'","''")

        columns = songs[0].keys()
        query = "INSERT INTO liked_songs ({}) VALUES %s".format(','.join(columns))
        values = [[value for value in song.values()] for song in songs]

        execute_values(cursor, query, values)
        conn.commit()

    cursor.close()
    conn.close()

