from tkinter import * 
from tkinter import ttk

import hashlib

import requests

import periodic

def alert_popup(alert = "Changes Detected", title = None):
    if not title:
        title = alert

    top= Toplevel(root)
    top.title(title)
    Label(top, text= alert, justify='center').pack()
    top.focus_force()
    #top.lift()
    top.attributes('-topmost',True)

schedule = None

values ={
    "10 seconds" : 10, 
    "30 seconds": 30, 
    "1 minute": 60, 
    "2 minutes": 120, 
    "5 minutes": 300
}
rown = 0


root = Tk()

frm = ttk.Frame(root, padding=10)
frm.grid()

#title
ttk.Label(frm, text="This app will check a url for changes while running").grid(columnspan=2, row = rown); rown += 1

#url selector
ttk.Label(frm, text="URL:").grid(column=0, row=rown) 
(url_entry := ttk.Entry(frm)).grid(column = 1, row =  rown); rown += 1

#time selector
ttk.Label(frm, text="Frequency of check:").grid(column=0, row=rown); 
(freq_select := ttk.Combobox(frm, state="readonly", values=list(values.keys()))).grid(column=1,row = rown); rown += 1

#buttons
def check_url(old_hash, hash_fun): 
    url = url_entry.get()
    # cleaning url, requests lib likes it to be a full url
    if url[:3] not in ("www", "htt"):
        url = "http://www." + url 
    elif url[:3] == "www": 
        url = "http://" + url
    #checking for valid frequency
    try: 
        resp = requests.get(url)
    except Exception as inst:
        alert_popup("Error with url")
        exit("1")
    
    new_hash = hash_fun(resp)
    if new_hash != old_hash: 
        alert_popup()


def run():
    #setting global variables
    global stopped, schedule
    stopped = False

    run_button.config(state=DISABLED)
    url_entry.config(state=DISABLED)
    freq_select.config(state=DISABLED)
    
    url = url_entry.get()
    # cleaning url, requests lib likes it to be a full url
    if url[:3] not in ("www", "htt"):
        url = "http://www." + url 
    elif url[:3] == "www": 
        url = "http://" + url
    
    #checking for valid frequency
    try: 
        resp = requests.get(url)
    except Exception as inst:
        alert_popup("Error with Url.\nEnter full url, starting with \"http://\"", "Error with URL")
        return
    freq = freq_select.get()
    if not freq or freq not in values: 
        alert_popup("select valid frequency")
        return


    #our hashing function can either be hashing the response or looking at the last-modified header
    if "Last-Modified" not in resp.headers:
        hashf = lambda response: hashlib.sha256(response.text.encode('utf-8')).hexdigest() 
    else: 
        hashf = lambda response: response.headers['Last-Modified']
    
    old_val = hashf(resp)

    frequency_s = values[freq]
    schedule = periodic.Periodic(frequency_s, lambda: check_url(old_val, hashf))




def stop(): 
    global stopped, schedule
    schedule.stop(); del schedule; schedlue = None
    stopped = True
    run_button.config(state=NORMAL)
    url_entry.config(state=NORMAL)
    freq_select.config(state=NORMAL)
(run_button := ttk.Button(frm, text="Run", command=run)).grid(column = 0, row=rown);  ttk.Button(frm, text="Stop", command=stop).grid(column = 1, row=rown); rown += 1 

ttk.Button(frm, text="Quit", command=root.destroy).grid(columnspan=2, column=0, row = rown); rown += 1



root.mainloop()
