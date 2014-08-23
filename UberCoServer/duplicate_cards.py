import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

cards = []
cursor.execute('SELECT id, type FROM card')
for result in cursor:
    card_id, card_type = result
    cursor.execute('INSERT INTO card VALUES (?, ?, 1)', (card_id + 1000, card_type))
    db.commit()
