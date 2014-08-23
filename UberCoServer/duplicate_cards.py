import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

cards = []
cursor.execute("SELECT id,valid,type \
                FROM card")
results = cursor.fetchall()
for result in results:
    card_id, card_valid, card_type = result
    cursor.execute("INSERT INTO card VALUES (" + str(card_id + 1000) + "," + str(card_type) + "," + "1" + ")")
    db.commit()
