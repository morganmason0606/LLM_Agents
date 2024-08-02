from tkinter import * 
from tkinter import ttk

import requests # 3rd party lib

import datetime
import hashlib

import periodic # personal lib for scheduling periodic tasks using python threading lib


def alert_popup(alert = "Changes Detected", title = None):
    """create a separate Tkinter window to alert user of change

    Args:
        alert (str, optional): the alert to be displayed. Defaults to "Changes Detected".
        title (_type_, optional): the title of the window. Defaults to alert value.
    """
    if not title:
        title = alert

    top= Toplevel(root)
    top.title(title)
    Label(top, text= alert, justify='center').pack()
    top.focus_force()
    #top.lift()
    top.attributes('-topmost',True)


#useful global vars

# object for storing checking loop
schedule = None

# can add values to this dictionary, make sure they are in form: string description : float representing seconds of time
# will automatically update
values ={
    "10 seconds" : 10, 
    "30 seconds": 30, 
    "1 minute": 60, 
    "2 minutes": 120, 
    "5 minutes": 300
}
# automatic row number selector
rown = 0


# tk frame
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

#button functions
def check_url(old_hash, hash_fun): 
    """compares the result of using hash_fun on a new request to the url with an old/ original hash

    Args:
        old_hash (_type_): hash of old request made by running hash_fun on the first, baseline request
        hash_fun (bool): 'hashing' function for requests of type requests.Response -> type(old_hash)
    """
    url = url_entry.get()
    # cleaning url, requests lib likes it to be a full url
    if url[:3] not in ("www", "htt"):
        url = "http://www." + url 
    elif url[:3] == "www": 
        url = "http://" + url
    #checking for valid frequency
    try: 
        resp = requests.get(url)
    except:
        alert_popup("Error with url")
        exit("1") # panic exit
    
    new_hash = hash_fun(resp)
    if new_hash != old_hash: 
        alert_popup()

def check_header(old_time): 
    """uses If-Modified-Since header to check if website has been updated

    Args:
        old_time (str): RCF 1123 date time representation of when script started
    """
    try: 
        resp = requests.head(
            url=url_entry.get(), 
            headers = {
                "If-Modified-Since": old_time
            },
            allow_redirects=True
        )
    except:
        alert_popup("Error with url")
        exit("1")

    # if response indicates that change has been made, exit
    if resp.status_code == 200: 
        alert_popup()

def run():
    """runs the website-checking scrip
    sets all inputs to be disabled
    checks if the url is valid (and fixes small issues with it)
    sets up schedule
    """
    #setting global variables
    global stopped, schedule
    stopped = False

    
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
    frequency_s = values[freq]

    # freezing fields
    run_button.config(state=DISABLED)
    url_entry.config(state=DISABLED)
    freq_select.config(state=DISABLED)
 

    # we can check if a page has changed using the If-Modified-Since header
    # but if the header isn't supported by the server, we will instead compare other ways

    #builidng http data
    now = datetime.datetime.now(datetime.UTC)
    http_date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # sending request with haeder
    resp = requests.head(
        url=url, 
        headers = {
            "If-Modified-Since": http_date
        },
        allow_redirects=True
    )

    # if head request reflects it understand the request, we will use it to check
    if resp.status_code == 304:
        schedule = periodic.Periodic(frequency_s, lambda: check_header(http_date))
    # if head request was not understood, we will check for other ways
    else: 
        # we can either use the Last-Modified header if it is available, or hash the response if it is not
        # hashing the response is likely to create false positives 
        if "Last-Modified" not in resp.headers:
            # our hashing function will be to compare the hashes of the response object
            hashf = lambda response: hashlib.sha256(response.text.encode('utf-8')).hexdigest() 
        else: 
            # our hashing function will be to compare the Last modified header value
            hashf = lambda response: response.headers['Last-Modified']
        
        old_val = hashf(resp)
        schedule = periodic.Periodic(frequency_s, lambda: check_url(old_val, hashf))

def stop(): 
    """stops schedule from running and reactivates input forms
    """
    global stopped, schedule
    schedule.stop(); del schedule; schedlue = None
    stopped = True
    run_button.config(state=NORMAL)
    url_entry.config(state=NORMAL)
    freq_select.config(state=READABLE)

#button declaration
(run_button := ttk.Button(frm, text="Run", command=run)).grid(column = 0, row=rown);  ttk.Button(frm, text="Stop", command=stop).grid(column = 1, row=rown); rown += 1 

# quit button
ttk.Button(frm, text="Quit", command=root.destroy).grid(columnspan=2, column=0, row = rown); rown += 1



root.mainloop()
