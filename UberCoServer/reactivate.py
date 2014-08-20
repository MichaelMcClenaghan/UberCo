import MySQLdb

db = MySQLdb.connect(host="localhost", port=3306, user="uberco", passwd="gideon", db="UberCo")
cursor = db.cursor()

response = raw_input("Scan card to reactivate: (-1 to exit) ")

while response != "-1":
    cursor.execute("UPDATE card \
                    SET valid=1 \
                    WHERE id=" + response + ";")
    response = raw_input("Scan card to reactivate: (-1 to exit) ")
    db.commit()
