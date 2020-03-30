"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko

This function concentrates all database related functions - table creation
"""

import pymysql
import os
import pandas as pd
from game_parser import game_parser
from feed_parser import feed_parser

# TODO: Move these constants to the config file (UPDATE: check if any of these consts. are redundant)
# TODO: converting the DB creation to MySQL complete. Now the insertion must be converted to MySQL.
DB_FILENAME = 'HS_Stats.db'
DB = os.path.join(os.path.dirname(os.path.realpath(__file__)), DB_FILENAME)
SET_RELEASE_DIC = {'Basic': 2014, 'Classic': 2014, 'Ashes of Outland': 2020, 'Descent of Dragons': 2019,
                   'Saviors of Uldum': 2019, 'Rise of Shadows': 2019, 'The Witchwood': 2018, 'Hall of Fame': 2014,
                   "Galakrond's Awakening": 2020, 'The Boomsday Project': 2018, "Rastakhan's Rumble": 2018}


def remove_rank_from_rank(rank_str):
    if 'Rank' in rank_str.split():
        return rank_str.split()[1]
    else:
        return rank_str


def insert_matches(match_url, winner, loser):
    """
    This function writes results of matches into matches table
    """
    with pymysql.connect(DB_FILENAME) as con:
        con.execute('SELECT MAX(Deck_ID) FROM Decks')  # find max deck_id (latest input)
        deck_id = con.fetchall()[0][0]
        winner_rank = remove_rank_from_rank(winner[1])
        looser_rank = remove_rank_from_rank(loser[1])
        insert_command = '''INSERT INTO matches (
        Match_URL, Winner_Deck_ID, Looser_Deck_ID, Winner_Player_Rank, Looser_Player_Rank) VALUES (?, ?, ?, ?, ?)'''
        insert_values = [match_url, deck_id, deck_id - 1, winner_rank, looser_rank]
        con.execute(insert_command, insert_values)
        con.commit()


def insert_card(name, card_dict):
    """This function gets the card's name and details and inserts it into the cards database,
    unless it's there already"""
    with pymysql.connect(DB_FILENAME) as con:
        df = pd.read_sql(r'SELECT 1 FROM Cards WHERE Card_Name = "%s"' % name, con)
        if df.shape[0] == 0:  # This means the card was not found in the database and should be inserted
            insert_command = '''INSERT INTO Cards (Card_name, Class, Type, Rarity, 'Set', Release_year, Cost, 
                                Artist, Mana_Cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            card_dict['Release Year'] = SET_RELEASE_DIC[card_dict['Set']]
            insert_values = [name, card_dict['Class'], card_dict['Type'], card_dict['Rarity'], card_dict['Set'],
                             card_dict['Release Year'], card_dict['Cost'], card_dict['Artist'], card_dict['Mana Cost']]
            con.execute(insert_command, insert_values)
        con.commit()


def insert_decks(winner_deck, loser_deck):
    """Given a winning and losing deck from a match - insert into Decks table in the database"""
    decks = [loser_deck, winner_deck]
    insert_command = '''INSERT INTO Decks (Deck_Name, Winner, Deck_Prefix, Class, Deck_Cost, 
            Average_Card_Cost, Most_Common_Set, Most_Common_Type, Number_of_Unique_Cards) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    with pymysql.connect(DB_FILENAME) as con:
        for win, deck in enumerate(decks):
            # Insert winner and loser deck into the database / for loser win = 0 and for winner win = 1
            name = ' '.join([deck['Deck'], deck['Class']])
            insert_values = [name, bool(win), deck['Deck'], deck['Class'], deck['Deck Cost'], deck['Average Card Cost'],
                             deck['Most_Common_Set'], deck['Most_Common_Type'], len(deck['Cards'])]
            con.execute(insert_command, insert_values)
        con.commit()


def card_in_deck_update(winner_cards, loser_cards):  # , winner_deck_id, loser_deck_id):
    """Given cards from winning and losing deck in a match - insert into card_in_deck table in the database"""
    decks = [winner_cards, loser_cards]
    # deck_id = [loser_deck_id, winner_deck_id]
    insert_command = 'INSERT INTO Card_In_Deck (Deck_ID, Card_ID, Number_of_Copies) VALUES (?, ?, ?)'
    with pymysql.connect(DB_FILENAME) as con:
        con.execute('SELECT MAX(Deck_ID) FROM Decks')  # find max deck_id (latest input)
        result = con.fetchall()[0][0]
        for index, deck in enumerate(decks):
            # for win/lose pair loser is inserted into decks first to decks so here winner cards gets deck_id for
            # latest insert in decks and loser cards get deck_id for deck above that which is the loser of the pair
            deck_id = result - index
            for card, duplicates in deck.items():
                con.execute('SELECT Card_ID FROM Cards WHERE Card_Name = "%s"' % card)
                card_id = con.fetchall()[0][0]
                insert_values = [deck_id, card_id, duplicates]
                con.execute(insert_command, insert_values)


def create_database():
    with pymysql.connect(host='localhost', user='root', passwd='mazaz123') as con:
        # cur = con.cursor()
        con.execute("CREATE DATABASE hs_stats")


def create_tables():
    """Create tables in HS_stats Database"""
    create_table_decks = '''CREATE TABLE Decks (
        Deck_ID INT AUTO_INCREMENT PRIMARY KEY,
        Deck_Name VARCHAR(50),
        Winner BOOL,
        Deck_Prefix VARCHAR(50),
        Class VARCHAR(50),
        Deck_Cost INT,
        Average_Card_Cost FLOAT,
        Most_Common_Set VARCHAR(50),
        Most_Common_Type VARCHAR(50),
        Number_of_Unique_Cards INT)'''
    create_table_matches = '''CREATE TABLE Matches (
        Match_ID INT AUTO_INCREMENT PRIMARY KEY,
        Match_URL VARCHAR(100),
        Winner_Deck_ID INT,
        Looser_Deck_ID INT,
        Winner_Player_Rank VARCHAR(10),
        Looser_Player_Rank VARCHAR(10),
        FOREIGN KEY(Winner_Deck_ID) REFERENCES Decks(Deck_ID),
        FOREIGN KEY(Looser_Deck_ID) REFERENCES Decks(Deck_ID))'''
    create_table_cards = '''CREATE TABLE Cards (
        Card_ID INT AUTO_INCREMENT PRIMARY KEY,
        Card_name VARCHAR(50),
        Class VARCHAR(50),
        Type VARCHAR(50),
        Rarity VARCHAR(50),
        Card_set VARCHAR(50),
        Release_year YEAR,
        Cost INT,
        Artist VARCHAR(50),
        Mana_Cost INT)'''
    create_table_card_in_deck = '''CREATE TABLE Card_In_Deck (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Number_of_Copies INT,
        Deck_ID INT,
        Card_ID INT,
        FOREIGN KEY(Deck_ID) REFERENCES Decks(Deck_ID),
        FOREIGN KEY(Card_ID) REFERENCES Cards(Card_ID))'''
    table_commands = [create_table_decks, create_table_matches, create_table_cards, create_table_card_in_deck]
    # type your own password !
    with pymysql.connect(host='localhost', user='root', passwd='password?', db='HS_Stats') as con:
        for command in table_commands:
            con.execute(command)


def main():
    """Function used to test the decks_table creation and handling functions"""
    # Use to reset database as needed
    if os.path.exists(DB):
        os.remove(DB)
    create_database()  # will throw an error if already exists
    create_tables()  # will throw an error if already exists
    feed_results = feed_parser()
    for iterations, match in enumerate(feed_results):
        match_url, winner, loser = match[0], match[1], match[2]
        winner_rank = remove_rank_from_rank(winner[1])
        looser_rank = remove_rank_from_rank(loser[1])
        print('{} - winner deck {}, winner rank {}, looser deck {}, looser rank {}'.format(match_url, winner[0],
                                                                                           winner_rank, loser[0],
                                                                                           looser_rank))
        winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, False)
        insert_decks(winner_deck, loser_deck)
        insert_matches(match_url, winner, loser)
        for card_name, card_info in mined_cards.items():
            insert_card(card_name, card_info)
        card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'])


if __name__ == '__main__':
    main()

# def create_matches_table():
#     """
#         This function creates the matches table within the Hs_stats database.
#     """
#     with sqlite3.connect(DB_FILENAME) as con:
#         cur = con.cursor()
#         cur.execute('''CREATE TABLE matches (
#                             Match_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                             Match_URL VARCHAR,
#                             FOREIGN KEY (Winner_Deck_ID) REFERENCES decks(Deck_ID))
#                             FOREIGN KEY (Looser_Deck_ID) REFERENCES decks(Deck_ID))
#                             Winner_Player_Rank VARCHAR,
#                             Looser_Player_Rank VARCHAR)''')
#         con.commit()
#         cur.close()


# What we need:
#    Winner_Deck_ID = decks.Deck_ID WHERE decks.Deck_Name = winner_deck_name AND decks.Winner = True
#    Looser_Deck_ID = decks.Deck_ID WHERE decks.Deck_Name = winner_deck_name AND decks.Winner = False
#
#
# def main():
#     create_matches_table()
#     update_matches_table()
#
#
# if __name__ == '__main__':
#     main()
#
# checking
