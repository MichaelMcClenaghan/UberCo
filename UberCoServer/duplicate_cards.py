import sqlite3

db = sqlite3.connect('database.db')
cur = db.cursor()

cards = []
cur.execute('SELECT id, type FROM cards')
for result in cur:
    card_id, card_type = result
    cur.execute('INSERT INTO cards VALUES (?, ?, 0)',
                (card_id + 1000, card_type))
    db.commit()
