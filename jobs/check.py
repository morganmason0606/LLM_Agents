import requests

import concurrent.futures
from typing import Type
from tkinter import messagebox

from utils.database import Database
from utils.helperfunctions import get_http_date, get_hash


class Checker():
    def __init__(self): 
        self.database: Type[Database] = Database()
    
    def check_web_change(self, id, url, lastmodified, hash):
        print(f"checking {url}")
        if lastmodified:
            now = get_http_date()
            resp = requests.head(
                url=url, 
                headers = {
                    "If-Modified-Since": now
                },
                allow_redirects=True
            )
            if resp.status_code == 200: 
                return (id, url, lastmodified, hash)
        else:
            print("checking hash")
            resp = requests.get(url=url)
            nhash = get_hash(resp)
            if nhash != hash:
                return (id, url, lastmodified, hash)
        return None
    
    def get_jobs(self): 
        res = self.database.get_jobs()
        return res.fetchall()
    
def main(): 
    checker = Checker()
    jobs = checker.get_jobs()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor: 
        futures = {executor.submit(checker.check_web_change, id, url, lastmodified, hash): url for id, url, lastmodified, hash in jobs}
        changed = []
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
            else:
                if result:
                    id, url, hash, lastmodified = result
                    changed.append(url)
                    if lastmodified: 
                        checker.database.update_job(id, hash=None, lastmodified=lastmodified)
                    else: 
                        checker.database.update_job(id, hash=hash, lastmodified=None)


    if changed: 
        with open("../changes.txt", "w+") as f:
            for url in changed: 
                f.write(url)
        messagebox.showinfo("Change detected", f"Changes have been detected. Changes have been written to changes.txt.\nA change has been detected in the following urls:\n{'\n'.join(changed)} ")


if __name__ == "__main__":
    main()