import json
import os
import random
import sqlite3

from flask import Flask
from flask import g
from flask import make_response
from flask import request
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
cors = CORS(app, headers=['Content-Type', 'X-Requested-With'])


@app.before_request
def check_database():
    if request.method == "OPTIONS":
        return

    if not os.path.exists('database.db'):
        return make_response(json.dumps({'error': 'Database not ready'}), 500)

    g.db = sqlite3.connect('database.db')
    g.cursor = g.db.cursor()


@app.after_request
def request_cleanup(response):
    g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps( { 'error': 'Not found, check URL' } ), 404)

@app.route("/<team_id>/cards/redeem/<card_id>/")
def redeem_card(team_id, card_id):
    try:
        g.cursor.execute('SELECT id, valid, type FROM card WHERE id = %d' % card_id)

        card_id, card_valid, card_type = cursor.fetchone()
        print "Scanned card: ", card_id
    except:
        return make_response(json.dumps( { 'error': 'Card not found' } ), 400)
    
    if card_valid == 0:
        return make_response(json.dumps( { 'error': 'Card has already been redeemed' } ), 400)

    try:
        g.cursor.execute("INSERT INTO team_items VALUES(%d, %s)" % team_id, str(card_type))
        g.db.commit()
    except:
        return make_response(json.dumps( { 'error': 'Database failed to update' } ), 400)
        g.db.rollback()

    try:
        g.cursor.execute("SELECT id,name,description,is_chest,rarity,image \
                        FROM item \
                        WHERE id = " + str(card_type) + ";")
        item_id, item_name, item_description, item_is_chest, item_rarity, item_image = cursor.fetchone()

        return make_response(json.dumps({"id": item_id, "name": item_name, "description": item_description, \
            "is_chest": bool(item_is_chest), "rarity": item_rarity, "image": item_image}), 200)
    except:
        return make_response(json.dumps( { 'error': 'Failed to get item from card' } ), 400)

@app.route("/<team_id>/chests/redeem/<chest_id>/")
def redeem_chest(team_id, chest_id):
    rewards = []

    try:
        g.cursor.execute("SELECT item_id,rarity,is_chest \
                        FROM team_items \
                        INNER JOIN item \
                        ON item.id = team_items.item_id \
                        WHERE team_id = " + team_id + \
                        " AND item_id = " + chest_id)
        item_id, item_rarity, is_chest = cursor.fetchone()

        if is_chest == 0:
            return make_response(json.dumps( { 'error': 'Attempting to redeem key, not chest' } ), 400)
    except:
        return make_response(json.dumps( { 'error': 'Your team does not own this chest!' } ), 400) 
    
    try:
        chest_keys = get_chest_keys(chest_id)['keys']
        items = get_team_item_ids(team_id)
    except:
        return make_response(json.dumps( { 'error': 'Failed to get required keys!' } ), 400)     
    
    for item in chest_keys:
        try:
            items.remove(item)
        except:
            return make_response(json.dumps( { 'error': 'Your team does not have the required keys!' } ), 400)

    # Remove required keys from team inventory
    for item in chest_keys:
        try:
            g.cursor.execute("DELETE FROM team_items \
                            WHERE team_id = " + team_id + \
                            " AND item_id = " + str(item) + \
                            " LIMIT 1")
            g.db.commit()
        except:
            return make_response(json.dumps( { 'error': 'Failed to remove items from database' } ), 400)

    # Remove the chest itself from the inventory
    try:
        g.cursor.execute("DELETE FROM team_items \
                        WHERE team_id = " + team_id + \
                        " AND item_id = " + chest_id + \
                        " LIMIT 1")
        g.db.commit()
    except:
        return make_response(json.dumps( { 'error': 'Failed to remove items from database' } ), 400)

    try:
        g.cursor.execute("SELECT id,name,description,rarity,numberRemaining \
                        FROM reward \
                        WHERE numberRemaining != 0")
        results = g.cursor.fetchall()
    except:
        return make_response(json.dumps( { 'error': 'Failed to get rewards from database' } ), 400)

    for result in results:
        reward_id, reward_name, reward_description, reward_rarity, rewards_remaining = result
        rewards.append({"id": reward_id, "name": reward_name, "description": reward_description, \
            "rarity": reward_rarity, "remaining": rewards_remaining, "image": "reward.png"})        

    reward = select_reward(rewards, item_rarity)   

    try:
        g.cursor.execute("UPDATE reward " + \
                       "SET numberRemaining=" + str(rewards_remaining - 1) + \
                       " WHERE id = " + str(reward['id']))
        g.db.commit()
    except:
        return make_response(json.dumps( { 'error': 'Failed to subtract 1 from remaining rewards' } ), 400)

    try:
        g.cursor.execute("INSERT INTO team_rewards \
                        VALUES(" + team_id + "," + str(reward['id']) + ",0" + ");")
        g.db.commit()
    except:
        return make_response(json.dumps( { 'error': 'Failed to add reward to team' } ), 400)

    return json.dumps(reward)

def select_reward(rewards, reward_level):
    num_rewards = len(rewards[reward_level-1])
    if num_rewards == 0:
        return False
    else:
        return rewards[random.randint(0,num_rewards-1)]

@app.route("/<team_id>/rewards/redeem/<reward_id>/")
def redeem_reward(team_id, reward_id):
    try:
        g.cursor.execute("DELETE FROM team_rewards \
                    WHERE team_id = " + team_id + \
                    " AND reward_id = " + str(reward_id) + \
                    " LIMIT 1")
    except:
        return make_response(json.dumps( { 'error': 'Failed to remove reward from team' } ), 400)


@app.route("/<team_id>/items/")
def get_team_items(team_id):
    items = []
    g.cursor.execute("SELECT item_id,name,description,is_chest,rarity,image \
                    FROM team_items \
                    INNER JOIN item \
                    ON item.id = team_items.item_id \
                    WHERE team_id=" + team_id)
    results = g.cursor.fetchall()
    for result in results:
        item_id, item_name, item_description, item_is_chest, item_rarity, item_image = result
        items.append({"id": item_id, "name": item_name, "description": item_description, \
            "is_chest": item_is_chest, "rarity": item_rarity, "image": item_image})
    return json.dumps(items)

@app.route("/<team_id>/rewards/")
def get_team_rewards(team_id):
    rewards = []
    g.cursor.execute("SELECT reward_id,name,description,rarity \
                    FROM team_rewards \
                    INNER JOIN reward \
                    ON reward.id = team_rewards.reward_id \
                    WHERE team_id=" + team_id)
    results = g.cursor.fetchall()

    for result in results:
        reward_id, reward_name, reward_description, reward_rarity = result
        rewards.append({"id": reward_id, "name": reward_name, "description": reward_description, \
            "rarity": reward_rarity, "image": "reward.png"})

    return json.dumps(rewards)

def get_team_item_ids(team_id):
    items = []
    g.cursor.execute("SELECT item_id \
                    FROM team_items \
                    WHERE team_id=" + team_id)
    results = g.cursor.fetchall()
    for result in results:
        item_id = result[0]
        items.append(item_id)
    return items

def get_chest_keys(chest_id):
    relationships = []
    used_chests = []

    g.cursor.execute("SELECT chest_id,key_id \
                    FROM chest_keys \
                    WHERE chest_id = " + chest_id)
    results = g.cursor.fetchall()

    for result in results:
        chest_id, key_id = result
        if used_chests.__contains__(chest_id):
            for relationship in relationships:
                if relationship["chest"] == chest_id:
                    relationship["keys"].append(key_id)
        else:
            relationships.append({"chest": chest_id, "keys": [key_id]})
        used_chests.append(chest_id)
    return relationships[0]


@app.route("/chests/")
def get_all_chest_keys():
    relationships = []
    used_chests = []

    g.cursor.execute("SELECT chest_id,key_id \
        FROM chest_keys")
    results = g.cursor.fetchall()

    for result in results:
        chest_id, key_id = result
        if used_chests.__contains__(chest_id):
            for relationship in relationships:
                if relationship["chest"] == chest_id:
                    relationship["keys"].append(key_id)
        else:
            relationships.append({"chest": chest_id, "keys": [key_id]})
        used_chests.append(chest_id)
    return json.dumps(relationships)

@app.route("/cards/list/")
def get_cards():
    cards = []
    g.cursor.execute("SELECT id,valid,type \
                    FROM card")
    results = g.cursor.fetchall()
    for result in results:
        card_id, card_valid, card_type = result
        cards.append({"id": card_id, "valid": bool(card_valid), "type": card_type})
    return json.dumps(cards)

@app.route("/items/list/")
def get_items():
    items = []
    g.cursor.execute("SELECT id,name,description,is_chest,rarity,image \
                    FROM item")
    results = g.cursor.fetchall()
    for result in results:
        item_id, item_name, item_description, item_is_chest, item_rarity, item_image = result
        items.append({"id": item_id, "name": item_name, "description": item_description, \
            "is_chest": item_is_chest, "rarity": item_rarity, "image": item_image})
    return json.dumps(items)

@app.route("/teams/list/")
def get_teams():
    teams = []
    g.cursor.execute("SELECT id,name,colour \
                    FROM team")
    results = g.cursor.fetchall()
    for result in results:
        team_id, team_name, team_colour = result
        teams.append({"id": team_id, "name": team_name, "colour": team_colour})
    return json.dumps(teams)

if __name__ == "__main__":
    app.run(port=5051, host='0.0.0.0')