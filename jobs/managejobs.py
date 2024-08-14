import requests

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import hashlib
from typing import Type, List

from database import Database
from utils import get_http_date, clean_url


class ManageJobs(tk.Frame): 
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        
        self.parent = parent
        self.database: Type[Database] = self.parent.database

        self.label = ttk.Label(self, text="Manage urls", )
        self.label.grid(column=0, row = 0, columnspan=2, pady=10)

        self.url_add = ttk.Button(self, text="Add", command=self.add_job)
        self.url_add.grid(column = 0, row = 1, sticky='w', pady=10)

        self.url_entry = ttk.Entry(self, )
        self.url_entry.grid(column=1, row=1, padx=10, pady=10, sticky='w')


        self.job_groups: List[JobGroup] =[]
        self.create_groups()
    
    
    def create_groups(self): 
        jobs = self.database.get_jobs().fetchall()
        
        for i, (id, url, _, _) in enumerate(jobs, 2): 
            group = JobGroup(self, id, url)
            group.grid(column=0, row=i, sticky='w', columnspan=2, padx=10, pady=1)
            self.job_groups.append(group)

    def refresh_group(self): 
        for g in self.job_groups:
            g.destroy()
        self.job_groups.clear()
        self.create_groups()

    def add_job(self):
        self.url_add.config(state=tk.DISABLED)
        self.url_entry.config(state=tk.DISABLED)

        url = self.url_entry.get()
        url = clean_url(url)
        try:
            resp = requests.get(
                url=url,
                allow_redirects=True
            )
        except Exception as e: 
            messagebox.showerror("Error", f"Failed to reach url:{url}")
            
        else:
            if "Last-Modified" in resp.headers:
                http_date = get_http_date()
                self.database.add_job(url=url, hash=None, lastmodified=http_date)
            else:
                hashv = hashlib.sha256(resp.text.encode("utf-8")).hexdigest()
                self.database.add_job(url, hash=hashv, lastmodified=None)
            self.url_entry.delete(0, tk.END)  
        finally:
            self.refresh_group()
            self.url_add.config(state=tk.NORMAL)
            self.url_entry.config(state=tk.NORMAL)
            
    def delete_job(self, id): 
        self.database.delete_job(id)
        self.refresh_group()
        
class JobGroup(tk.Frame): 
    def __init__(self, parent: Type[ManageJobs], id, url, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        self.id = id
        self.parent = parent

        self.delete_button = ttk.Button(self, text="Delete", command=lambda: self.parent.delete_job(self.id))
        self.delete_button.grid(column=0, row=0)
        
        self.url_entry = ttk.Label(self, text=url)
        self.url_entry.grid(column = 1, row = 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = ManageJobs(root)
    root.mainloop()