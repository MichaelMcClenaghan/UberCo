import os
import sqlite3

# Delete the database if it currently exists
if os.path.exists('database.db'):
    os.remove('database.db')

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute("CREATE TABLE card (id int NOT NULL UNIQUE, type int, valid int);")
cursor.execute("CREATE TABLE item (id int NOT NULL UNIQUE, name varchar(255), description varchar(255), is_chest int, rarity int, image varchar(255));")
cursor.execute("CREATE TABLE reward (id int NOT NULL UNIQUE, name varchar(255), description varchar(255), rarity int, numberRemaining int);")
cursor.execute("CREATE TABLE team (id int NOT NULL UNIQUE, name varchar(255), colour char(20));")
cursor.execute("CREATE TABLE team_items (team_id int, item_id int);")
cursor.execute("CREATE TABLE team_rewards (team_id int, reward_id int);")
cursor.execute("CREATE TABLE chest_keys (chest_id int, key_id int);")