import os
import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()


def add_cards():
    while True:
        card_id = raw_input("Please enter card id: (-1 for exit) ")
        if card_id == "-1":
            return 0
        card_type = raw_input("What type is this card? ")
        try:
            cursor.execute("INSERT INTO card VALUES (" + card_id + "," + card_type + ",1);")
            db.commit()
        except:
            print "Error adding card: ", card_id
            db.rollback()


def add_items():
    while True:
        item_id = raw_input("Please enter item type id: (-1 for exit) ")

        if item_id == "-1":
            return 0

        item_name = raw_input("Item name? ")
        item_description = raw_input("Item description? ")
        item_is_key = raw_input("Is the item a key or chest? (Y/N) ")
        if item_is_key == "Y" or item_is_key == "y":
            item_is_key = "1"
        else:
            item_is_key = "0"
        item_rarity = raw_input("Enter item rarity: (0-9) ")

        try:
            cursor.execute("INSERT INTO item VALUES (" + item_id + ",'" + item_name + "','" + \
                item_description + "'," + item_is_key + "," + item_rarity + ");")
            db.commit()
        except:
            print "Error adding item: ", item_name
            db.rollback()

def add_rewards():
    while True:
        reward_name = raw_input("Reward name? (-1 for exit) ")
        if reward_name == "-1":
            return 0
        reward_description = raw_input("Reward description? ")
        reward_rarity = raw_input("Reward rarity? ")

        try:
            cursor.execute("INSERT INTO reward (name,description,rarity) VALUES ('" + reward_name + "','" + reward_description + "'," + reward_rarity + ");")
            db.commit()
        except:
            print "Error adding reward: ", reward_name
            db.rollback()

def add_teams():
    while True:
        team_name = raw_input("Team name? (-1 for exit) ")
        if team_name == "-1":
            return 0
        team_colour = raw_input("Hex colour for team? (in format 123456) ")

        try:
            cursor.execute("INSERT INTO team (name,colour) VALUES ('" + team_name + "','" + team_colour + "');")
            db.commit()
        except:
            print "Error adding team: ", team_name
            db.rollback()

def main():
    should_continue = True

    while should_continue:
        os.system('cls' if os.name == 'nt' else 'clear')
        print "1. Add cards to database"
        print "2. Add items to database"
        print "3. Add rewards to database"
        print "4. Add teams to database"
        print "5. Exit"
        option = raw_input("What would you like to do? ")

        if option == "1":
            add_cards()
        elif option == "2":
            add_items()
        elif option == "3":
            add_rewards()
        elif option == "4":
            add_teams()
        elif option == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            return 0
        else:
            print "I'm sorry, that option is not valid"

if __name__ == "__main__":
    main()