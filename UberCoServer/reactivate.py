"""Reactivates cards from the command line. Cards can either be scanned
(easiest) or have their IDs entered manually."""
import sqlite3

db = sqlite3.connect('database.db')
cur = db.cursor()

while True:
    response = raw_input('Scan card to reactivate: ')
    if response == '':
        break

    cur.execute('UPDATE cards SET redeemed = 0 WHERE id = ?', (response,))
    if cur.rowcount != 1:
        print 'Card with ID %s not found' % response
    db.commit()
