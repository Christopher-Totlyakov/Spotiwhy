import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import insert_song, get_all_artists, get_all_genres


class AddSongPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Добави нова песен",
                  font=("Arial", 16)).pack(pady=10)

        self.title_var = tk.StringVar()
        self.url_var = tk.StringVar()
        self.artist_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.rating_var = tk.StringVar()

        form = ttk.Frame(self)
        form.pack(pady=20)

        ttk.Label(form, text="Заглавие:").grid(row=0, column=0, sticky="e")
        ttk.Entry(form, textvariable=self.title_var).grid(row=0, column=1)

        ttk.Label(form, text="YouTube URL:").grid(row=1, column=0, sticky="e")
        ttk.Entry(form, textvariable=self.url_var).grid(row=1, column=1)

        ttk.Label(form, text="Изпълнител:").grid(row=2, column=0, sticky="e")
        self.artist_cb = ttk.Combobox(
            form, textvariable=self.artist_var, values=get_all_artists())
        self.artist_cb.grid(row=2, column=1)

        ttk.Label(form, text="Жанр:").grid(row=3, column=0, sticky="e")
        self.genre_cb = ttk.Combobox(
            form, textvariable=self.genre_var, values=get_all_genres())
        self.genre_cb.grid(row=3, column=1)

        ttk.Label(form, text="Рейтинг (0.0 - 10.0):").grid(row=4, column=0, sticky="e")
        ttk.Entry(form, textvariable=self.rating_var).grid(row=4, column=1)

        ttk.Button(self, text="Добави", command=self.add_song).pack(pady=10)

    def add_song(self):
        title = self.title_var.get()
        url = self.url_var.get()
        artist = self.artist_var.get()
        genre = self.genre_var.get()
        rating = self.rating_var.get()

        if not all([title, url, artist, genre, rating]):
            messagebox.showwarning("Грешка", "Всички полета са задължителни.")
            return

        insert_song(title, url, artist, genre, rating)
        messagebox.showinfo("Успех", "Песента е добавена успешно.")
        self.title_var.set("")
        self.url_var.set("")
        self.artist_var.set("")
        self.genre_var.set("")
        self.rating_var.set("")
