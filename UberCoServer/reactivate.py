import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

response = raw_input("Scan card to reactivate: (-1 to exit) ")

while response != "-1":
    cursor.execute("UPDATE card \
                    SET valid=1 \
                    WHERE id=" + response + ";")
    response = raw_input("Scan card to reactivate: (-1 to exit) ")
    db.commit()
