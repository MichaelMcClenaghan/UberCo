"""Creates the SQLite database and populates it with data. If the database
already exists, it will be deleted first."""
import os
import sqlite3
import unicodecsv as csv
from sqlite3 import DatabaseError

# Delete the database if it currently exists
if os.path.exists('database.db'):
    print 'Deleting existing database...'
    os.remove('database.db')

db = sqlite3.connect('database.db')
cur = db.cursor()

print 'Creating database tables...'
sql = open('data/schema.sql', 'r').read()
db.executescript(sql)

print 'Loading cards...'
with open('data/cards.csv') as cards:
    reader = csv.reader(cards)
    for card in reader:
        try:
            cur.execute('INSERT INTO cards VALUES (?, ?, 0)', card)
        except DatabaseError, e:
            print 'Error adding card %s (%s)' % (card[0], e)

print 'Loading items...'
with open('data/items.csv') as items:
    reader = csv.reader(items, delimiter='|')
    for item in reader:
        try:
            cur.execute('INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)', item)
        except DatabaseError, e:
            print 'Error adding item %s (%s)' % (item[1], e)

print 'Loading teams...'
with open('data/teams.csv') as teams:
    reader = csv.reader(teams)
    for team in reader:
        try:
            cur.execute('INSERT INTO teams VALUES (?, ?, ?)', team)
        except DatabaseError, e:
            print 'Error adding team %s (%s)' % (team[1], e)

print 'Loading chest/key relationships...'
with open('data/chest_keys.csv') as relationships:
    reader = csv.reader(relationships)
    for relationship in reader:
        try:
            cur.execute('INSERT INTO chest_keys VALUES(?, ?)', relationship)
        except DatabaseError, e:
            print 'Error adding relationship %s/%s (%s): ' % (relationship[0],
                                                              relationship[1],
                                                              e)

print 'Loading rewards...'
with open('data/rewards.csv') as rewards:
    reader = csv.reader(rewards, delimiter='|')
    for reward in reader:
        try:
            cur.execute('INSERT INTO rewards VALUES (?, ?, ?, ?, ?)', reward)
        except DatabaseError, e:
            print 'Error adding reward %s (%s)' % (reward[1], e)

db.commit()
