import json
import os


def load_json_data(file_path='data/data.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файлът {file_path} не съществува.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Невалиден JSON: {e}")

        songs = data.get('songs', [])
        genres = data.get('genres', [])
        artists = data.get('artists', [])

        return songs, genres, artists

# def save_json(file_path, data):
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
