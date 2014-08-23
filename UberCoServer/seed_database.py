import sqlite3
import unicodecsv as csv
from sqlite3 import DatabaseError

db = sqlite3.connect('database.db')
cursor = db.cursor()

print 'Loading cards...'
with open('data/cards.csv') as cards:
    reader = csv.reader(cards)
    for card in reader:
        try:
            cursor.execute('INSERT INTO card VALUES (?, ?, 1)', card)
        except DatabaseError, e:
            print 'Error adding card %s (%s)' % (card[0], e)

print 'Loading items...'
with open('data/items.csv') as items:
    reader = csv.reader(items, delimiter='|')
    for item in reader:
        try:
            cursor.execute('INSERT INTO item VALUES (?, ?, ?, ?, ?, ?)', item)
        except DatabaseError, e:
            print 'Error adding item %s (%s)' % (item[1], e)

print 'Loading teams...'
with open('data/teams.csv') as teams:
    reader = csv.reader(teams)
    for team in reader:
        try:
            cursor.execute('INSERT INTO team VALUES (?, ?, ?)', team)
        except DatabaseError, e:
            print 'Error adding team %s (%s)' % (team[1], e)

print 'Loading chest/key relationships...'
with open('data/chest_keys.csv') as relationships:
    reader = csv.reader(relationships)
    for relationship in reader:
        try:
            cursor.execute('INSERT INTO chest_keys VALUES(?, ?)', relationship)
        except DatabaseError, e:
            print 'Error adding relationship %s/%s (%s): ' % (relationship[0], relationship[1], e)

print 'Loading rewards...'
with open('data/rewards.csv') as rewards:
    reader = csv.reader(rewards, delimiter='|')
    for reward in reader:
        try:
            cursor.execute('INSERT INTO reward VALUES (?, ?, ?, ?, ?)', reward)
        except DatabaseError, e:
            print 'Error adding reward %s (%s)' % (reward[1], e)

db.commit()