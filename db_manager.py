import sqlite3

DB_NAME = "music_app.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist_id INTEGER,
            genre_id INTEGER,
            youtube_url TEXT,
            FOREIGN KEY (artist_id) REFERENCES artists(id),
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_all_artists():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM artists')
    artists = [row[0] for row in cursor.fetchall()]
    conn.close()
    return artists


def get_all_genres():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM genres')
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()
    return genres


def get_all_songs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT songs.title, artists.name, genres.name, songs.youtube_url
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        JOIN genres ON songs.genre_id = genres.id
    ''')
    results = cursor.fetchall()
    conn.close()
    return results


def insert_song(title, url, artist_name, genre_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM artists WHERE name = ?', (artist_name,))
    artist_id = cursor.fetchone()
    if artist_id:
        artist_id = artist_id[0]
    else:
        cursor.execute('INSERT INTO artists (name) VALUES (?)', (artist_name,))
        artist_id = cursor.lastrowid

    cursor.execute('SELECT id FROM genres WHERE name = ?', (genre_name,))
    genre_id = cursor.fetchone()
    if genre_id:
        genre_id = genre_id[0]
    else:
        cursor.execute('INSERT INTO genres (name) VALUES (?)', (genre_name,))
        genre_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO songs (title, youtube_url, artist_id, genre_id)
        VALUES (?, ?, ?, ?)
    ''', (title, url, artist_id, genre_id))

    conn.commit()
    conn.close()
