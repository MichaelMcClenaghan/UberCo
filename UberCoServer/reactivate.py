"""Reactivates cards from the command line. Cards can either be scanned
(easiest) or have their IDs entered manually."""
import sqlite3

db = sqlite3.connect('database.db')
cur = db.cursor()

while True:
    response = raw_input('Scan card to reactivate: 1')
    if response == '':
        break

    cur.execute('UPDATE cards SET valid = 1 WHERE id = ?', (response,))
    if cur.rowcount != 1:
        print 'Card with ID %s not found' % response
    db.commit()
