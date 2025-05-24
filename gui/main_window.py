import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from db_manager import export_data_to_json

from gui.add_song_page import AddSongPage
from gui.home_page import HomePage
from gui.import_json_page import ImportJsonPage

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotiwhy")
        self.geometry("1300x430")        


        style = ttk.Style()
        style.theme_use("clam")

        nav_frame = tk.Frame(self, width=200, bg="#6bd85e")
   

        style.configure(".", background="#f0f0f0",
                        foreground="#000000", font=("Arial", 10))       

        style.configure("TFrame", background="#7df26f")
        style.configure("TLabel", background="#7df26f", foreground="#333333")

        style.configure("TEntry", fieldbackground="#ffffff")
        style.configure("TCombobox", fieldbackground="#ffffff",
                        background="#ffffff")

        style.configure("TButton",
                        background="#1b5429",
                        foreground="#ffffff",     
                        font=("Arial", 10, "bold"))
        style.map("TButton",
                  background=[("active", "#000000")], 
                  foreground=[("active", "#ffffff")])

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#000000",
                        fieldbackground="#ffffff")
        style.map("Treeview", background=[("selected", "#1b5429")])

        style.configure("Treeview.Heading",
                        background="#1b5429",
                        foreground="#ffffff",
                        font=("Arial", 10, "bold"))
        style.map("Treeview.Heading",
                  background=[("active", "#000000")],
                  foreground=[("active", "#ffffff")])


        nav_frame = tk.Frame(self, width=250, bg="#24823c")
        nav_frame.pack(side="left", fill="y")

        button_container = tk.Frame(nav_frame, bg="#24823c")
        button_container.place(relx=0.5, rely=0.5, anchor="center")

        btn_home = ttk.Button(button_container, text="Начало",
                              command=lambda: self.show_frame("HomePage"))
        btn_home.pack(pady=10)

        btn_add_song = ttk.Button(
            button_container, text="Добави песен", command=lambda: self.show_frame("AddSongPage"))
        btn_add_song.pack(pady=10)

        btn_import_json = ttk.Button(
            button_container, text="Добави съществуващ плейлист", command=lambda: self.show_frame("ImportJsonPage"))
        btn_import_json.pack(pady=10)

        btn_export_json = ttk.Button(
            button_container, text="Запази плейлиста", command=self.export_json)
        btn_export_json.pack(pady=10)

        self.container = tk.Frame(self, bg="#7df26f")
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

    def export_json(self):
        file_path = filedialog.asksaveasfilename(
        defaultextension=".json", filetypes=[("JSON файлове", "*.json")], title="Запази плейлиста като JSON")

        if file_path:
            try:
                export_data_to_json(file_path)
            except Exception as e:
                tk.messagebox.showerror("Грешка", f"Неуспешно запазване: {e}")
            else:
                tk.messagebox.showinfo("Успех", "Плейлистът беше запазен успешно.")



def run():
    app = MainWindow()
    app.mainloop()
