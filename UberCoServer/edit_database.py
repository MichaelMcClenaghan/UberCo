"""A command line interface for adding new cards, items, rewards and teams to
the database."""
import os
import sqlite3
from sqlite3 import DatabaseError

db = sqlite3.connect('database.db')
cur = db.cursor()


def add_cards():
    while True:
        card_id = raw_input('Please enter card id: ')
        if card_id == '':
            return

        item_type = raw_input('Please enter item type id: ')
        try:
            cur.execute('INSERT INTO cards VALUES (?, ?, 0)', (card_id,
                                                               item_type))
            db.commit()
        except DatabaseError as e:
            print 'Error adding card:', e


def add_items():
    while True:
        item_id = raw_input('Please enter item type id: ')
        if item_id == '':
            return

        item_name = raw_input('Item name? ')
        item_description = raw_input('Item description? ')
        item_is_key = raw_input('Is the item a key? (y/N) ')
        item_is_key = 1 if item_is_key in ['Y', 'y'] else 0
        item_rarity = raw_input('Enter item rarity: (0-9) ')
        item_image = raw_input('Enter image filename: ')

        try:
            cur.execute('INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)',
                        (item_id, item_name, item_description, item_is_key,
                         item_rarity, item_image))
            db.commit()
        except DatabaseError as e:
            print 'Error adding item:', e


def add_rewards():
    while True:
        reward_name = raw_input('Reward name? ')
        if reward_name == '':
            return

        reward_description = raw_input('Reward description? ')
        reward_rarity = raw_input('Reward rarity? ')

        cur.execute('INSERT INTO rewards (name, description, rarity) '
                    'VALUES (?, ?, ?)',
                    (reward_name, reward_description, reward_rarity))
        db.commit()


def add_teams():
    while True:
        team_name = raw_input('Team name? ')
        if team_name == '':
            return
        team_colour = raw_input('Hex colour for team? (in format 123456) ')

        cur.execute('INSERT INTO teams (name, colour) VALUES (?, ?)',
                    (team_name, team_colour))
        db.commit()


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print '1. Add cards to database'
        print '2. Add items to database'
        print '3. Add rewards to database'
        print '4. Add teams to database'
        print '5. Exit'
        option = raw_input('What would you like to do? ')

        if option == '1':
            add_cards()
        elif option == '2':
            add_items()
        elif option == '3':
            add_rewards()
        elif option == '4':
            add_teams()
        elif option == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        else:
            print 'I''m sorry, that option is not valid'

if __name__ == '__main__':
    main()
