import datetime

def clean_url(url: str):
    url = url.strip()
    if url[:4] != "http":
        url = "http://" + url  
    return url

def get_http_date() -> str: 
        #builidng http data
        now = datetime.datetime.now(datetime.UTC)
        return now.strftime("%a, %d %b %Y %H:%M:%S GMT")