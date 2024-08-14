import tkinter as tk
from tkinter import ttk
from managejobs import ManageJobs
from database import Database

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Notebook to manage jobs")
        self.geometry("400x300")
        self.resizable(True, True)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.database = Database()

        self.manage_jobs_frame = ManageJobs(self)
        self.notebook.add(self.manage_jobs_frame, text="manage urls")

if __name__ == "__main__":
    app = App()
    app.mainloop()