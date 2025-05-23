import os
import sqlite3
from db_manager import init_db, connect_db, DB_NAME
from json_loader import load_json
from gui.main_window import run

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ARTISTS_FILE = os.path.join(DATA_DIR, 'artists.json')
GENRES_FILE = os.path.join(DATA_DIR, 'genres.json')
SONGS_FILE = os.path.join(DATA_DIR, 'songs.json')


def populate_table_from_json(conn, table, json_data, unique_field, fields):
    """
    Добавя записи в таблицата, ако не съществуват по указаното уникално поле.
    """
    cursor = conn.cursor()
    for item in json_data:
        cursor.execute(
            f"SELECT id FROM {table} WHERE {unique_field} = ?", (
                item[unique_field],)
        )
        if cursor.fetchone():
            continue
        placeholders = ','.join('?' for _ in fields)
        columns = ','.join(fields)
        values = [item.get(f) for f in fields]
        cursor.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values
        )
    conn.commit()


def populate_songs(conn, songs):
    """
    Добавя песни, ако нямат точно същата комбинация от title, artist_id и genre_id.
    """
    cursor = conn.cursor()
    for song in songs:
        cursor.execute(
            "SELECT id FROM artists WHERE name = ?", (song['artist'],)
        )
        artist = cursor.fetchone()
        cursor.execute(
            "SELECT id FROM genres WHERE name = ?", (song['genre'],)
        )
        genre = cursor.fetchone()
        if not artist or not genre:
            continue
        artist_id = artist[0]
        genre_id = genre[0]

        cursor.execute(
            "SELECT id FROM songs WHERE title = ? AND artist_id = ? AND genre_id = ?",
            (song['title'], artist_id, genre_id)
        )
        if cursor.fetchone():
            continue
        cursor.execute(
            "INSERT INTO songs (title, artist_id, genre_id, youtube_url) VALUES (?, ?, ?, ?)",
            (song['title'], artist_id, genre_id, song.get('youtube_url'))
        )
    conn.commit()


def main():
    init_db()
    conn = connect_db()

    artists = load_json(ARTISTS_FILE)
    genres = load_json(GENRES_FILE)
    songs = load_json(SONGS_FILE)

    populate_table_from_json(conn, 'artists', artists, 'name', ['name'])
    populate_table_from_json(conn, 'genres', genres, 'name', ['name'])
    populate_songs(conn, songs)

    conn.close()

    print("Инициализацията на базата е завършена. Добави GUI стартер тук.")

    run()


if __name__ == '__main__':
    main()
