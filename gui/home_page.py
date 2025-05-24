import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import get_all_songs, delete_song_by_title_and_artist, insert_song, get_all_genres, get_all_artists

import threading
import os
import subprocess
import glob
import pygame


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent,  bg="#7df26f")
        pygame.mixer.init()
        self.controller = controller
        self.current_audio_file = None

        ttk.Label(self, text="Списък с песни",
                  font=("Arial", 16)).pack(pady=10)

        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=(0, 10))

        ttk.Label(filter_frame, text="Заглавие:").pack(side="left")
        self.title_filter = ttk.Entry(filter_frame)
        self.title_filter.pack(side="left", padx=5)
        self.title_filter.bind("<KeyRelease>", lambda e: self.load_songs())

        ttk.Label(filter_frame, text="Жанр:").pack(side="left", padx=(10, 0))
        self.genre_filter = ttk.Combobox(filter_frame, state="readonly")
        self.genre_filter.pack(side="left", padx=5)
        self.genre_filter.bind("<<ComboboxSelected>>", lambda e: self.load_songs())

        ttk.Label(filter_frame, text="Изпълнител:").pack(side="left", padx=(10, 0))
        self.artist_filter = ttk.Combobox(filter_frame, state="readonly")
        self.artist_filter.pack(side="left", padx=5)
        self.artist_filter.bind("<<ComboboxSelected>>", lambda e: self.load_songs())

        ttk.Label(filter_frame, text="Рейтинг от:").pack(
            side="left", padx=(10, 0))
        self.rating_min = ttk.Entry(filter_frame, width=5)
        self.rating_min.pack(side="left", padx=(0, 5))
        self.rating_min.bind("<KeyRelease>", lambda e: self.load_songs())

        ttk.Label(filter_frame, text="до:").pack(side="left")
        self.rating_max = ttk.Entry(filter_frame, width=5)
        self.rating_max.pack(side="left", padx=(0, 10))
        self.rating_max.bind("<KeyRelease>", lambda e: self.load_songs())


        self.clear_filters_btn = ttk.Button(
            filter_frame, text="Изчисти филтрите", command=self.clear_filters)
        self.clear_filters_btn.pack(side="left", padx=(10, 0))


        self.tree = ttk.Treeview(self, columns=(
            "title", "artist", "genre", "rating", "url"), show="headings")
        for col, text in [("title", "Заглавие"), ("artist", "Изпълнител"),
                          ("genre", "Жанр"), ("rating", "Рейтинг"), ("url", "YouTube URL")]:
            self.tree.heading(col, text=text)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label="Пусни",     command=self.play_song)
        self.context_menu.add_command(
            label="Редактирай", command=self.edit_song)
        self.context_menu.add_command(
            label="Изтрий",     command=self.delete_song)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.stop_button = ttk.Button(
            self, text="Спри песента", command=self.stop_song)
        self.stop_button.pack(pady=5)
        self.stop_button.pack_forget()

        self.load_songs()

    def load_songs(self):
        self.populate_filters()

        title_query = self.title_filter.get().strip().lower()
        selected_genre = self.genre_filter.get()
        selected_artist = self.artist_filter.get()
        min_rating = self.rating_min.get().strip().lower()
        max_rating = self.rating_max.get().strip().lower()

        try:
            min_rating = float(self.rating_min.get()
                               ) if self.rating_min.get() else None
        except ValueError:
            min_rating = None

        try:
            max_rating = float(self.rating_max.get()
                               ) if self.rating_max.get() else None
        except ValueError:
            max_rating = None


        for row in self.tree.get_children():
            self.tree.delete(row)

        for song in get_all_songs():
            title, artist, genre, rating, url = song

            if min_rating is not None and rating < min_rating:
                continue
            if max_rating is not None and rating > max_rating:
                continue
            if title_query and title_query not in title.lower():
                continue
            if selected_genre != "Всички жанрове" and selected_genre != genre:
                continue
            if selected_artist != "Всички изпълнители" and selected_artist != artist:
                continue

            self.tree.insert("", "end", values=song)

    def populate_filters(self):
        genres = ["Всички жанрове"] + get_all_genres()
        artists = ["Всички изпълнители"] + get_all_artists()

        current_genre = self.genre_filter.get()
        current_artist = self.artist_filter.get()

        self.genre_filter["values"] = genres
        self.artist_filter["values"] = artists

        self.genre_filter.set(current_genre if current_genre else "Всички жанрове")
        self.artist_filter.set(
            current_artist if current_artist else "Всички изпълнители")

    def clear_filters(self):
        self.rating_min.delete(0, tk.END)
        self.rating_max.delete(0, tk.END)
        self.title_filter.delete(0, tk.END)
        self.genre_filter.set("Всички жанрове")
        self.artist_filter.set("Всички изпълнители")
        self.load_songs()


    def show_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_song(self):
        item = self.tree.selection()
        if not item:
            return
        title, artist = self.tree.item(item)["values"][:2]
        if messagebox.askyesno("Потвърждение", f"Изтриване на '{title}'?"):
            delete_song_by_title_and_artist(title, artist)
            self.load_songs()

    def edit_song(self):
        item = self.tree.selection()
        if not item:
            return
        old_title, old_artist, old_genre, old_rating, old_url = self.tree.item(item)[
            "values"]

        win = tk.Toplevel(self)
        win.title("Редактиране на песен")
        win.geometry("250x300")

        def labeled_entry(label, val):
            ttk.Label(win, text=label).pack(anchor="w", padx=10, pady=(5, 0))
            e = ttk.Entry(win)
            e.insert(0, val)
            e.pack(fill="x", padx=10)
            return e

        title_e = labeled_entry("Заглавие",    old_title)
        artist_e = labeled_entry("Изпълнител",  old_artist)
        genre_e = labeled_entry("Жанр",        old_genre)
        url_e = labeled_entry("YouTube URL", old_url)
        rating_e = labeled_entry("рейтинг", old_rating)

        def save():
            delete_song_by_title_and_artist(old_title, old_artist)

            try:
                rating = float(rating_e.get().strip())
                if not (0.0 <= rating <= 10.0):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Грешка", "Рейтингът трябва да е число между 0.0 и 10.0.")
                return

            insert_song(
                title=title_e.get().strip(),
                url=url_e.get().strip(),
                artist_name=artist_e.get().strip(),
                genre_name=genre_e.get().strip(),
                rating=rating
            )
            self.load_songs()
            win.destroy()

        ttk.Button(win, text="Запази", command=save).pack(pady=15)

    def play_song(self):

        item = self.tree.selection()

        if not item:
            return
        youtube_url = self.tree.item(item)["values"][4]

        def download_and_play():
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.unload()
                    except:
                        pass
                    self._cleanup_file()

                subprocess.run([
                    "yt-dlp",
                    "-x",
                    "--audio-format", "mp3",
                    "--force-overwrites",
                    "-o", "temp_audio.%(ext)s",
                    youtube_url
                ], check=True)

                files = glob.glob("temp_audio.*")
                if not files:
                    raise FileNotFoundError("Не е намерен аудио файл.")
                self.current_audio_file = files[0]

                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                self.stop_button.pack(pady=5)

                while pygame.mixer.music.get_busy():
                    pygame.time.wait(500)

                self._cleanup_file()

            except Exception as e:
                messagebox.showerror("Грешка при пускане", str(e))

        threading.Thread(target=download_and_play, daemon=True).start()

    def stop_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            try:
                pygame.mixer.music.unload()
            except:
                pass
        self._cleanup_file()

    def _cleanup_file(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            pass

        self.stop_button.pack_forget()

        for f in glob.glob("temp_audio.*"):
            try:
                os.remove(f)
            except Exception as e:
                print(f"Грешка при триене на файл: {e}")
