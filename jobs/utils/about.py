import tkinter as tk
from tkinter import ttk
import os

class About(tk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.about_label = tk.Text(self, wrap="word")
        self.about_label.insert(tk.END, f"""
This is the interface for managing the website checking app.
- To set up the app, make sure you have python installed. 
- Check this by opening command and running "python --version"

Additionally, make sure you have the requests library installed.
- run : "pip install requests" 

Then to schedule the app, open the windows Task Scheduler.
- Select 'Create Task' on the right. Name it and write a basic description.
- Then select triggers, 'new', and select when you want this script to run.
- Finally, go to actions, create new action. 
- Under program, type in 'python'
    - and under args add the following: 
{os.path.join(os.path.dirname(os.path.dirname(__file__)), "check.py")}

During the selected time, if a change is detected, a window will pop up \
to alert you. 

If you with to disable this script, you need to go back into task scheduler\
and disable it.""")
        self.about_label.pack()