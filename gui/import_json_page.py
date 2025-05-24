import tkinter as tk
from tkinter import filedialog, messagebox
from json_loader import load_json_data
from db_manager import insert_song, insert_genre, insert_artist


class ImportJsonPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent,  bg="#7df26f")
        self.controller = controller

        tk.Label(self, text="Импортиране на JSON файл",
                 font=("Arial", 16), bg="#7df26f").pack(pady=80)

        tk.Button(self, text="Избери JSON файл", command=self.import_json,
                  bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(self, text="Назад", command=lambda: controller.show_frame("HomePage"),
                  bg="#f44336", fg="white").pack(pady=5)

    def import_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON файлове", "*.json")])
        if not file_path:
            return

        try:
            songs, genres, artists = load_json_data(file_path)

            for artist in artists:
                insert_artist(artist.get('name', ''))

            for genre in genres:
                insert_genre(genre.get('name', ''))

            for song in songs:
                insert_song(
                    title=song.get('title', ''),
                    url=song.get('youtube_url', ''),
                    artist_name=song.get('artist', ''),
                    genre_name=song.get('genre', ''),
                    rating=song.get('rating', '')
                )
            messagebox.showinfo(
                "Успех", f"Успешно импортирани {len(songs)} песни, {len(artists)} изпълнители, {len(genres)} жанрове.")
        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка при импортиране: {e}")
