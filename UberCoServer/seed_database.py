import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

# Add data from card.csv
card_data = open("data/cards.csv", "r")
data = card_data.read()

for card in data.split("\n"):
    card_id, card_type = card.split(',')
    try:
        cursor.execute("INSERT INTO card VALUES (" + card_id + "," + card_type + ",1);")
        db.commit()
    except:
        print "Error adding card: ", card_id
        db.rollback()

item_data = open("data/items.csv", "r")
data = item_data.read()

for item in data.split("\n"):
    try:
        item_id, item_name, item_description, item_is_chest, item_rarity, item_image_name = item.split('|')
    except:
        print "Invalid line in file: " + item

    try:
        cursor.execute("INSERT INTO item VALUES (" + item_id + ",'" + item_name + "','" + \
            item_description + "'," + item_is_chest + "," + item_rarity + ",'" + item_image_name + "');")
        db.commit()
    except:
        print "Error adding item: ", item_name
        db.rollback()


team_data = open("data/teams.csv", "r")
data = team_data.read()

for item in data.split("\n"):
    try:
        team_id, team_name, team_colour = item.split(',')
    except:
        print "Invalid line in file: " + item

    try:
        cursor.execute("INSERT INTO team VALUES (" + team_id + ",'" + team_name + "','" + \
            team_colour + "');")
        db.commit()
    except:
        print "Error adding team: ", team_name
        db.rollback()

relationships = open("data/chest_keys.csv", "r")
data = relationships.read()

for item in data.split("\n"):
    try:
        chest_id, key_id = item.split(',')
    except:
        print "Invalid line in file: " + item

    try:
        cursor.execute("INSERT INTO chest_keys \
                        VALUES (" + chest_id + "," + key_id  +");")
        db.commit()
    except:
        print "Error adding relationship: ", chest_id
        db.rollback()

rewards = open("data/rewards.csv", "r")
data = rewards.read()

for item in data.split("\n"):
    try:
        reward_id, reward_name, reward_description, reward_rarity, rewards_remaining = item.split('|')
    except:
        print "Invalid line in file: " + item

    try:
        cursor.execute("INSERT INTO reward \
                        VALUES (" + reward_id + ",'" + reward_name + "','" + \
                        reward_description + "'," + reward_rarity + "," + rewards_remaining + ");")
        db.commit()
    except:
        print "Error adding reward: ", reward_name
        db.rollback()
