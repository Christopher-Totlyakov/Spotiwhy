import tkinter as tk
from tkinter import ttk
from gui.add_song_page import AddSongPage
from gui.home_page import HomePage
from gui.import_json_page import ImportJsonPage

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotiwhy")
        self.geometry("800x600")

        nav_frame = tk.Frame(self, width=200, bg="#cccccc")
        nav_frame.pack(side="left", fill="y")

        btn_home = ttk.Button(nav_frame, text="Начало",
                              command=lambda: self.show_frame("HomePage"))
        btn_home.pack(pady=10)

        btn_add_song = ttk.Button(
            nav_frame, text="Добави песен", command=lambda: self.show_frame("AddSongPage"))
        btn_add_song.pack(pady=10)

        btn_import_json = ttk.Button(
            nav_frame, text="Добави съществуващ плейлист", command=lambda: self.show_frame("ImportJsonPage"))
        btn_import_json.pack(pady=10)

        self.container = tk.Frame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.frames = {}

        for PageClass in (HomePage, AddSongPage, ImportJsonPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "load_songs"):
            frame.load_songs()
        frame.tkraise()



def run():
    app = MainWindow()
    app.mainloop()
