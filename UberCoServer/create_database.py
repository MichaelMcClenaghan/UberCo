import os
import sqlite3

# Delete the database if it currently exists
if os.path.exists('database.db'):
    os.remove('database.db')

db = sqlite3.connect('database.db')
sql = open('data/schema.sql', 'r').read()
db.executescript(sql)