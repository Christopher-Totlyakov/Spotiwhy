import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import insert_song, get_all_artists, get_all_genres


def create_add_song_tab(notebook):
    
    frame = ttk.Frame(notebook)
    notebook.add(frame, text='Добави песен')

    ttk.Label(frame, text="Заглавие:").grid(row=0, column=0, sticky='e')
    title_entry = ttk.Entry(frame)
    title_entry.grid(row=0, column=1)

    ttk.Label(frame, text="YouTube URL:").grid(row=1, column=0, sticky='e')
    url_entry = ttk.Entry(frame)
    url_entry.grid(row=1, column=1)

    ttk.Label(frame, text="Изпълнител:").grid(row=2, column=0, sticky='e')
    artist_cb = ttk.Combobox(frame, state="readonly", values=get_all_artists())
    artist_cb.grid(row=2, column=1)

    ttk.Label(frame, text="Жанр:").grid(row=3, column=0, sticky='e')
    genre_cb = ttk.Combobox(frame, state="readonly", values=get_all_genres())
    genre_cb.grid(row=3, column=1)

    def add_song():
        title = title_entry.get()
        url = url_entry.get()
        artist = artist_cb.get()
        genre = genre_cb.get()

        if not all([title, url, artist, genre]):
            messagebox.showwarning("Грешка", "Моля, попълни всички полета.")
            return

        insert_song(title, url, artist, genre)
        messagebox.showinfo("Успех", "Песента беше добавена.")
        title_entry.delete(0, tk.END)
        url_entry.delete(0, tk.END)

    ttk.Button(frame, text="Добави песен", command=add_song).grid(
        row=4, columnspan=2, pady=10)

    return frame
