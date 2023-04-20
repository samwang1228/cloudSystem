import sqlite3
import os
filepath = os.path.join('share/uploads/user')
os.makedirs(filepath, exist_ok=True)
SQLITE_DB_PATH = 'backend/SparkVideo.db'
SQLITE_DB_SCHEMA = 'backend/create_db.sql'

with open(SQLITE_DB_SCHEMA) as f: # Read SQL file
    create_db_sql = f.read() 

db = sqlite3.connect(SQLITE_DB_PATH) # Assign DB path and connect DB

with db: # Run SQL to create table
    db.executescript(create_db_sql) 

with db: # init DB data
    db.execute("PRAGMA foreign_keys = ON")
    db.execute(
        'INSERT INTO members (account, password) VALUES ("user", "123456")'
    )
