import psycopg2


def postgres_init(db = 'postgres',user = 'postgres',pw = 'admin',host = 'localhost',port = '5432'):

    conn = psycopg2.connect(database=db, user = user, password = pw, host = host, port = port)
    return conn

def create_liked_songs_table():
    pass