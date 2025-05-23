import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_manager import get_all_songs, delete_song_by_title_and_artist, insert_song


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Списък с песни",
                  font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=(
            "title", "artist", "genre", "url"), show="headings")
        for col in ("title", "artist", "genre", "url"):
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label="Редактирай", command=self.edit_song)
        self.context_menu.add_command(label="Изтрий", command=self.delete_song)

        self.load_songs()

    def load_songs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for song in get_all_songs():
            self.tree.insert("", "end", values=song)

    def show_context_menu(self, event):
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_song(self):
        item = self.tree.selection()
        if not item:
            return
        values = self.tree.item(item)["values"]
        title, artist = values[0], values[1]

        if messagebox.askyesno("Потвърждение", f"Наистина ли искате да изтриете '{title}'?"):
            delete_song_by_title_and_artist(title, artist)
            self.load_songs()

    def edit_song(self):
        item = self.tree.selection()
        if not item:
            return
        values = self.tree.item(item)["values"]
        old_title, old_artist, old_genre, old_url = values

        win = tk.Toplevel(self)
        win.title("Редактиране на песен")
        win.geometry("300x250")

        def create_labeled_entry(label, default_val):
            tk.Label(win, text=label).pack()
            e = tk.Entry(win)
            e.insert(0, default_val)
            e.pack(pady=2)
            return e

        title_entry = create_labeled_entry("Заглавие", old_title)
        artist_entry = create_labeled_entry("Изпълнител", old_artist)
        genre_entry = create_labeled_entry("Жанр", old_genre)
        url_entry = create_labeled_entry("YouTube URL", old_url)

        def save_changes():
            delete_song_by_title_and_artist(old_title, old_artist)
            insert_song(
                title=title_entry.get(),
                url=url_entry.get(),
                artist_name=artist_entry.get(),
                genre_name=genre_entry.get()
            )
            self.load_songs()
            win.destroy()

        tk.Button(win, text="Запази", command=save_changes,
                  bg="#4CAF50", fg="white").pack(pady=10)
