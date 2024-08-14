import sqlite3
import os

class Database(): 
    ENCODING = [
    ("websites","""
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        url TEXT UNIQUE NOT NULL, 
        hash TEXT,
        lastmodified TEXT
    """),
    ("times", """
       id INTEGER PRIMARY KEY AUTOINCREMENT, 
       time TEXT UNIQUE
    """)
    ]

    DATABASE_PATH=os.path.join(os.path.dirname(__file__), "jobs.db")

    def __init__(self): 
        self.conn: sqlite3.Connection = None
        try:
            self.connect()
            with self.conn: 
                for name, encoding in Database.ENCODING:
                    self.conn.execute(f"CREATE TABLE IF NOT EXISTS {name} ({encoding})")
        except Exception as e: 
            print(f"Initialization Error: {e}")
    def connect(self):
        print(self.DATABASE_PATH)
        self.conn = sqlite3.connect(self.DATABASE_PATH)

    def close(self): 
        if self.conn:
            self.conn.close()
            self.conn = None
    def __del__(self): 
        self.close

    def get_jobs(self):
        return self.conn.execute("SELECT * FROM websites")
    def delete_job(self, id): 
        with self.conn: 
            return self.conn.execute("DELETE FROM websites WHERE id=?", (id, ))
    def add_job(self,url, hash=None, lastmodified=None): 
        if hash: 
            with self.conn: 
                return self.conn.execute("INSERT OR REPLACE INTO websites (url, hash) VALUES (?, ?)", (url, hash))
        elif lastmodified:
            with self.conn:
                return self.conn.execute("INSERT OR REPLACE INTO websites (url, lastmodified) VALUES (?, ?)", (url, lastmodified))
        else: 
            return None
    def update_job(self, id, hash=None, lastmodified=None):
        if hash: 
            with self.conn: 
                return self.conn.execute("UPDATE websites SET hash=? WHERE id=?", (hash, id))
        elif lastmodified:
            with self.conn:
                return self.conn.execute("UPDATE websites SET lastmodified=? WHERE id=?", (lastmodified, id))
        else: 
            return None

    def get_times(self): 
        return self.conn.execute("SELECT * FROM times")
    def delete_times(self, id):
        with self.conn: 
            return self.conn.delete("DELETE FROM times WHERE id=?", (id, ))