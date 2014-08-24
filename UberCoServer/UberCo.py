import json
import os
import random
import sqlite3

import flask
from flask import Flask
from flask import g
from flask import request
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
cors = CORS(app, headers=['Content-Type', 'X-Requested-With', 'Accept'])


def jsonify(data, status_code=200):
    """A wrapper for flask.jsonify that allows you to set the response code."""
    response = flask.make_response(json.dumps(data))
    response.status_code = status_code
    response.mimetype = 'application/json'
    return response


@app.before_request
def check_database():
    if request.method == 'OPTIONS':
        return

    if not os.path.exists('database.db'):
        return jsonify({'error': 'Database not ready'}, 500)

    g.db = sqlite3.connect('database.db')
    g.cur = g.db.cursor()


@app.after_request
def request_cleanup(response):
    """Commit any changes and close the database after every request."""
    if hasattr(g, 'db'):
        g.db.commit()
        g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description}, 404)


@app.route('/<team_id>/cards/redeem/<card_id>')
def redeem_card(team_id, card_id):
    """Adds a card to a team's inventory and marks the card as used.
    Occurs when a team member scans a card."""
    g.cur.execute('SELECT id, redeemed, type FROM cards WHERE id = ?',
                  (card_id,))
    row = g.cur.fetchone()
    if row is None:
        return jsonify({'error': 'Card not found'}, 400)

    card_id, card_redeemed, card_type = row
    print 'Scanned card:', card_id

    if card_redeemed:
        return jsonify({'error': 'Card has already been redeemed'}, 400)

    g.cur.execute('UPDATE cards SET redeemed = 1 WHERE id = ?', (card_id,))
    g.cur.execute('INSERT INTO team_items VALUES (?, ?)', (team_id, card_type))

    g.cur.execute('SELECT id, name, description, is_chest, rarity, image '
                  'FROM items WHERE id = ?', (card_type,))
    row = g.cur.fetchone()
    if row is None:
        return jsonify({'error': 'Failed to find the item that belongs to '
                                 'this card.'}, 400)

    item_id, item_name, item_description, item_is_chest, item_rarity, \
        item_image = row
    return jsonify({'id': item_id, 'name': item_name,
                    'description': item_description,
                    'is_chest': bool(item_is_chest),
                    'rarity': item_rarity, 'image': item_image})


@app.route('/<team_id>/chests/redeem/<chest_id>')
def redeem_chest(team_id, chest_id):
    """Verifies that a team has all the keys for a particular chest and selects
    a random reward for the team. This process removes the keys and chest from
    the team's inventory."""
    g.cur.execute('SELECT team_items.ROWID, item_id, rarity, is_chest '
                  'FROM team_items '
                  'JOIN items ON items.id = team_items.item_id '
                  'WHERE team_id = ? AND item_id = ?', (team_id, chest_id))
    row = g.cur.fetchone()
    if row is None:
        return jsonify({'error': 'Your team does not own this chest!'}, 400)

    internal_id, item_id, item_rarity, is_chest = row
    if not is_chest:
        return jsonify({'error': 'Attempting to redeem key, not chest'}, 400)

    print 'Unlocking chest %s (rarity %d)' % (item_id, item_rarity)

    # Find which keys are required to open this chest
    g.cur.execute('SELECT key_id FROM chest_keys WHERE chest_id = ?',
                  (chest_id,))
    keys_required = [row[0] for row in g.cur]

    # Create a list of the internal IDs for each item type that the team owns.
    # This way we can selectively specific items from the inventory later.
    g.cur.execute('SELECT ROWID, item_id FROM team_items WHERE team_id = ?',
                  (team_id,))
    team_items = {}
    for item in g.cur:
        if item[1] not in team_items:
            team_items[item[1]] = []
        team_items[item[1]].append(item[0])

    # Attempt to "take" each required key from the team inventory. If we
    # encounter an error, that means that team doesn't have enough keys.
    items_consumed = [internal_id]
    for key in keys_required:
        try:
            items_consumed.append(team_items[key].pop())
        except (KeyError, IndexError):
            return jsonify({'error': 'Your team does not have the '
                                     'required keys!'}, 400)

    # Grab a list of available rewards
    g.cur.execute('SELECT id, name, description, rarity, numberRemaining '
                  'FROM rewards '
                  'WHERE numberRemaining != 0 AND rarity <= ?', (item_rarity,))
    rewards = []
    for result in g.cur:
        reward_id, reward_name, reward_description, reward_rarity, \
            rewards_remaining = result
        rewards.append({'id': reward_id, 'name': reward_name,
                        'description': reward_description,
                        'rarity': reward_rarity,
                        'remaining': rewards_remaining, 'image': 'reward.png'})

    # Select a reward to give
    if len(rewards) == 0:
        return jsonify({'error': 'There are no rewards left! (Your items have '
                                 'not been used.)'}, 400)
    reward = random.choice(rewards)
    print "Reward %s given (rarity %d)" % (reward['id'], reward['rarity'])

    # Reduce the number of that reward remaining (if not unlimited)
    if reward['remaining'] > 0:
        g.cur.execute('UPDATE rewards SET numberRemaining = '
                      'numberRemaining - 1 '
                      'WHERE id = ?', (reward['id'],))
    g.cur.execute('INSERT INTO team_rewards VALUES (?, ?)', (team_id,
                                                             reward['id']))

    # Remove required keys and the chest from the team inventory
    for item in items_consumed:
        g.cur.execute('DELETE FROM team_items WHERE ROWID = ?', (item,))
    print '%d items consumed' % len(items_consumed)

    return jsonify(reward)


@app.route('/<team_id>/rewards/redeem/<reward_id>')
def redeem_reward(team_id, reward_id):
    g.cur.execute('DELETE FROM team_rewards WHERE ROWID = ('
                  'SELECT ROWID FROM team_rewards WHERE team_id = ? '
                  'AND reward_id = ? LIMIT 1)', (team_id, reward_id))


@app.route('/<team_id>/items')
def get_team_items(team_id):
    items = []
    g.cur.execute('SELECT item_id, name, description, is_chest, rarity, image '
                  'FROM team_items '
                  'JOIN items ON items.id = team_items.item_id '
                  'WHERE team_id = ?', (team_id,))
    results = g.cur.fetchall()
    for result in results:
        item_id, item_name, item_description, item_is_chest, item_rarity, \
            item_image = result
        items.append({'id': item_id, 'name': item_name,
                      'description': item_description,
                      'is_chest': item_is_chest, 'rarity': item_rarity,
                      'image': item_image})
    return jsonify(items)


@app.route('/<team_id>/rewards')
def get_team_rewards(team_id):
    rewards = []
    g.cur.execute('SELECT reward_id, name, description, rarity '
                  'FROM team_rewards '
                  'JOIN rewards ON rewards.id = team_rewards.reward_id '
                  'WHERE team_id = ?', (team_id,))
    results = g.cur.fetchall()

    for result in results:
        reward_id, reward_name, reward_description, reward_rarity = result
        rewards.append({'id': reward_id, 'name': reward_name,
                        'description': reward_description,
                        'rarity': reward_rarity, 'image': 'reward.png'})
    return jsonify(rewards)


@app.route('/chests')
def get_all_chest_keys():
    g.cur.execute('SELECT chest_id, key_id FROM chest_keys')
    relationships = {}
    for result in g.cur:
        chest_id, key_id = result
        if chest_id not in relationships:
            relationships[chest_id] = []
        relationships[chest_id].append(key_id)

    # We need the output to be in a specific format for the frontend.
    output = [{'chest': c, 'keys': k} for c, k in relationships.iteritems()]
    return jsonify(output)


@app.route('/cards/list')
def get_cards():
    cards = []
    g.cur.execute('SELECT id, redeemed, type FROM cards')
    for result in g.cur:
        card_id, card_redeemed, card_type = result
        cards.append({'id': card_id, 'redeemed': bool(card_redeemed),
                      'type': card_type})
    return jsonify(cards)


@app.route('/items/list')
def get_items():
    items = []
    g.cur.execute('SELECT id, name, description, is_chest, rarity, image '
                  'FROM items')
    for result in g.cur:
        item_id, item_name, item_description, item_is_chest, item_rarity, \
            item_image = result
        items.append({'id': item_id, 'name': item_name,
                      'description': item_description,
                      'is_chest': item_is_chest, 'rarity': item_rarity,
                      'image': item_image})
    return jsonify(items)


@app.route('/teams/list')
def get_teams():
    teams = []
    g.cur.execute('SELECT id, name, colour FROM teams')
    for result in g.cur:
        team_id, team_name, team_colour = result
        teams.append({'id': team_id, 'name': team_name, 'colour': team_colour})
    return jsonify(teams)


@app.route('/cards/reactivate/<card_id>')
def reactivate_card(card_id):
    g.cur.execute('UPDATE cards SET redeemed = 0 WHERE id = ?', (card_id,))
    if g.cur.rowcount != 1:
        return jsonify({'error': 'Card with ID %s not found' % card_id}, 400)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(port=5051, host='0.0.0.0')
