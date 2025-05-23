import tkinter as tk
from tkinter import ttk
from db_manager import connect_db


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music App")
        self.geometry("800x600")
        self._create_widgets()
        self._populate_data()

    def _create_widgets(self): 

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.songs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.songs_frame, text='Песни')
        self.songs_tree = ttk.Treeview(self.songs_frame, columns=(
            'Title', 'Artist', 'Genre'), show='headings')
        for col in ('Title', 'Artist', 'Genre'):
            self.songs_tree.heading(col, text=col)
            self.songs_tree.column(col, width=200)
        self.songs_tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text='Добави песен')
        ttk.Label(self.add_frame, text='Заглавие:').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.title_entry = ttk.Entry(self.add_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

    def _populate_data(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT songs.title, artists.name, genres.name
            FROM songs
            JOIN artists ON songs.artist_id = artists.id
            JOIN genres ON songs.genre_id = genres.id
            '''
        )
        for row in cursor.fetchall():
            self.songs_tree.insert('', 'end', values=row)
        conn.close()


def run():
    app = MainWindow()
    app.mainloop()
