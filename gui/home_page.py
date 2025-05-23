import tkinter as tk
from tkinter import ttk
from db_manager import get_all_songs


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Списък с песни",
                  font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=(
            "title", "artist", "genre", "url"), show="headings")
        self.tree.heading("title", text="Заглавие")
        self.tree.heading("artist", text="Изпълнител")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("url", text="YouTube URL")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_songs()

    def load_songs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        songs = get_all_songs()
        for song in songs:
            self.tree.insert("", "end", values=song)
