import sqlite3
from json_loader import load_json_data

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


def insert_artist(name):
    """
    Добавя изпълнител, ако не съществува вече.
    """
    if not name:
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM artists WHERE name = ?', (name,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO artists (name) VALUES (?)', (name,))

    conn.commit()
    conn.close()


def insert_genre(name):
    """
    Добавя жанр, ако не съществува вече.
    """
    if not name:
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM genres WHERE name = ?', (name,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO genres (name) VALUES (?)', (name,))

    conn.commit()
    conn.close()


def insert_song(title, url, artist_name, genre_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM artists WHERE name = ?', (artist_name,))
    artist = cursor.fetchone()
    if artist:
        artist_id = artist[0]
    else:
        cursor.execute('INSERT INTO artists (name) VALUES (?)', (artist_name,))
        artist_id = cursor.lastrowid

    cursor.execute('SELECT id FROM genres WHERE name = ?', (genre_name,))
    genre = cursor.fetchone()
    if genre:
        genre_id = genre[0]
    else:
        cursor.execute('INSERT INTO genres (name) VALUES (?)', (genre_name,))
        genre_id = cursor.lastrowid

    cursor.execute('''
        SELECT id FROM songs
        WHERE title = ? AND artist_id = ? AND genre_id = ?
    ''', (title, artist_id, genre_id))
    song = cursor.fetchone()
    if not song:
        cursor.execute('''
            INSERT INTO songs (title, youtube_url, artist_id, genre_id)
            VALUES (?, ?, ?, ?)
        ''', (title, url, artist_id, genre_id))

    conn.commit()
    conn.close()


def insert_initial_data():
    try:
        songs, genres, artists = load_json_data('data/data.json')
    except Exception as e:
        print(f"Грешка при зареждане на JSON: {e}")
        return

    for artist in artists:
        insert_artist(artist.get('name', ''))

    for genre in genres:
        insert_genre(genre.get('name', ''))

    for song in songs:
        insert_song(
            title=song.get('title', ''),
            url=song.get('youtube_url', ''),
            artist_name=song.get('artist', ''),
            genre_name=song.get('genre', '')
        )


def delete_song_by_title_and_artist(title, artist_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT songs.id FROM songs
        JOIN artists ON songs.artist_id = artists.id
        WHERE songs.title = ? AND artists.name = ?
    ''', (title, artist_name))
    song = cursor.fetchone()
    if song:
        cursor.execute('DELETE FROM songs WHERE id = ?', (song[0],))
        conn.commit()
    conn.close()
