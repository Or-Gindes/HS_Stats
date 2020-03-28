"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko

This function concentrates all database related functions - table creation
"""

import sqlite3
import os
import pandas as pd
from game_parser import game_parser

# TODO: Move these constants to the config file
DB_FILENAME = 'HS_Stats.db'
DB = os.path.join(os.path.dirname(os.path.realpath(__file__)), DB_FILENAME)
SET_RELEASE_DIC = {'Basic': 2014, 'Classic': 2014, 'Ashes of Outland': 2020, 'Descent of Dragons': 2019,
                   'Saviors of Uldum': 2019, 'Rise of Shadows': 2019, 'The Witchwood': 2018, 'Hall of Fame': 2014,
                   "Galakrond's Awakening": 2020, 'The Boomsday Project': 2018, "Rastakhan's Rumble": 2018}


def insert_card(name, card_dict):
    """This function gets the card's name and details and inserts it into the cards database,
    unless it's there already"""
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        df = pd.read_sql(r'SELECT 1 FROM Cards WHERE Card_Name = "%s"' % name, con)
        if df.shape[0] == 0:    # This means the card was not found in the database and should be inserted
            insert_command = '''INSERT INTO Cards (Card_name, Class, Type, Rarity, 'Set', Release_year, Cost, 
                                Artist, Mana_Cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            card_dict['Release Year'] = SET_RELEASE_DIC[card_dict['Set']]
            insert_values = [name, card_dict['Class'], card_dict['Type'], card_dict['Rarity'], card_dict['Set'],
                             card_dict['Release Year'], card_dict['Cost'], card_dict['Artist'], card_dict['Mana Cost']]
            cur.execute(insert_command, insert_values)
        con.commit()
        cur.close()


def insert_decks(winner_deck, loser_deck):
    """Given a winning and losing deck from a match - insert into Decks table in the database"""
    decks = [loser_deck, winner_deck]
    insert_command = '''INSERT INTO Decks (Deck_Name, Winner, Deck_Prefix, Class, Deck_Cost, 
            Average_Card_Cost, Most_Common_Set, Most_Common_Type, Number_of_Unique_Cards) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        for win, deck in enumerate(decks):
            # Insert winner and loser deck into the database / for loser win = 0 and for winner win = 1
            name = ' '.join([deck['Deck'], deck['Class']])
            insert_values = [name, bool(win), deck['Deck'], deck['Class'], deck['Deck Cost'], deck['Average Card Cost'],
                             deck['Most_Common_Set'], deck['Most_Common_Type'], len(deck['Cards'])]
            cur.execute(insert_command, insert_values)
        con.commit()
        cur.close()


def card_in_deck_update(winner_cards, loser_cards):  # , winner_deck_id, loser_deck_id):
    """Given cards from winning and losing deck in a match - insert into card_in_deck table in the database"""
    decks = [winner_cards, loser_cards]
    # deck_id = [loser_deck_id, winner_deck_id]
    insert_command = 'INSERT INTO Card_In_Deck (Deck_ID, Card_ID, Number_of_Copies) VALUES (?, ?, ?)'
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        cur.execute('SELECT MAX(Deck_ID) FROM Decks')  # find max deck_id (latest input)
        result = cur.fetchall()[0][0]
        for index, deck in enumerate(decks):
            # for win/lose pair loser is inserted into decks first to decks so here winner cards gets deck_id for
            # latest insert in decks and loser cards get deck_id for deck above that which is the loser of the pair
            deck_id = result - index
            for card, duplicates in deck.items():
                cur.execute('SELECT Card_ID FROM Cards WHERE Card_Name = "%s"' % card)
                card_id = cur.fetchall()[0][0]
                insert_values = [deck_id, card_id, duplicates]
                cur.execute(insert_command, insert_values)


def create_tables():
    """Create tables in HS_stats Database"""
    create_table_decks = '''CREATE TABLE Decks (
        Deck_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Deck_Name VARCHAR,
        Winner BOOL,
        Deck_Prefix VARCHAR,
        Class VARCHAR,
        Deck_Cost INT,
        Average_Card_Cost FLOAT,
        Most_Common_Set VARCHAR,
        Most_Common_Type VARCHAR,
        Number_of_Unique_Cards INT)'''
    create_table_cards = '''CREATE TABLE Cards (
        Card_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Card_name VARCHAR,
        Class VARCHAR,
        Type VARCHAR,
        Rarity VARCHAR,
        'Set' VARCHAR,
        Release_year YEAR,
        Cost INT,
        Artist VARCHAR,
        Mana_Cost INT)'''
    create_table_card_in_deck = '''CREATE TABLE Card_In_Deck (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Deck_ID INTEGER REFERENCES Decks (Deck_ID),
        Card_ID INTEGER REFERENCES Cards (Card_ID),
        Number_of_Copies INTEGER)'''
    table_commands = [create_table_decks, create_table_cards, create_table_card_in_deck]
    with sqlite3.connect(DB_FILENAME) as con:
        for command in table_commands:
            cur = con.cursor()
            cur.execute(command)
            con.commit()
        cur.close()


def main():
    """Function used to test the decks_table creation and handling functions"""
    # Use to reset database as needed
    # if os.path.exists(DB):
    #     os.remove(DB)
    # create_tables()
    # game_url = 'https://hsreplay.net/replay/rh4z669MM9bhAnpuE6Ad53'
    # game_url = 'https://hsreplay.net/replay/tHc63LLjsgnHAao2yki6DX'
    game_url = 'https://hsreplay.net/replay/qUZw3utrzMVgLLcVEy3z9e'
    # winner_deck, loser_deck, mined_cards = game_parser(game_url, ('Aggro Overload Shaman', 'Rank 1'),
    #                                                    ('Bomb Warrior', 'Legend 1000'), False)
    # winner_deck, loser_deck, mined_cards = game_parser(game_url, ('Aggro Overload Shaman', 'Rank 1'),
    #                                                    ('Quest Hunter', 'Legend 1000'), False)
    winner_deck, loser_deck, mined_cards = game_parser(game_url, ('Aggro Overload Shaman', 'Rank 1'),
                                                       ('Quest Druid', 'Legend 1000'), False)
    insert_decks(winner_deck, loser_deck)
    for card_name, card_info in mined_cards.items():
        insert_card(card_name, card_info)
    card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'])


if __name__ == '__main__':
    main()
