import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import get_all_songs, delete_song_by_title_and_artist, insert_song

import threading
import os
import subprocess
import glob
import pygame


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        pygame.mixer.init()
        self.controller = controller
        self.current_audio_file = None

        ttk.Label(self, text="Списък с песни",
                  font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=(
            "title", "artist", "genre", "url"), show="headings")
        for col, text in [("title", "Заглавие"), ("artist", "Изпълнител"),
                          ("genre", "Жанр"), ("url", "YouTube URL")]:
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
        for row in self.tree.get_children():
            self.tree.delete(row)
        for song in get_all_songs():
            self.tree.insert("", "end", values=song)

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
        old_title, old_artist, old_genre, old_url = self.tree.item(item)[
            "values"]

        win = tk.Toplevel(self)
        win.title("Редактиране на песен")
        win.geometry("300x250")

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

        def save():
            delete_song_by_title_and_artist(old_title, old_artist)
            insert_song(
                title=title_e.get().strip(),
                url=url_e.get().strip(),
                artist_name=artist_e.get().strip(),
                genre_name=genre_e.get().strip()
            )
            self.load_songs()
            win.destroy()

        ttk.Button(win, text="Запази", command=save).pack(pady=15)

    def play_song(self):

        item = self.tree.selection()

        if not item:
            return
        youtube_url = self.tree.item(item)["values"][3]

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
