"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko

This function concentrates all database related functions - table creation
"""

import pymysql
import pandas as pd
from game_parser import game_parser
from feed_parser import feed_parser
from sqlalchemy import create_engine
from config import SET_RELEASE_DICT
from datetime import date



def insert_matches(match_url, winner, loser, database_parameters):
    """
    This function writes results of matches into matches table
    """
    with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                         db=database_parameters['Database_Name']) as con:
        con.execute('SELECT MAX(Deck_ID) FROM Decks')  # find max deck_id (latest input)
        deck_id = con.fetchall()[0][0]
        winner_rank = winner[1]
        looser_rank = loser[1]
        insert_command = '''INSERT INTO Matches (
        Match_URL, Winner_Deck_ID, Looser_Deck_ID, Winner_Player_Rank, Looser_Player_Rank) VALUES (%s, %s, %s, %s, %s)'''
        insert_values = [match_url, deck_id, deck_id - 1, winner_rank, looser_rank]
        con.execute(insert_command, insert_values)


def insert_card(name, card_dict, database_parameters):
    """This function gets the card's name and details and inserts it into the cards database,
    unless it's there already"""
    db_connection_str = 'mysql+pymysql://root:%s@%s/%s' % (database_parameters['Password'],
                                                           database_parameters['Host_Name'],
                                                           database_parameters['Database_Name'])
    engine = create_engine(db_connection_str)
    df = pd.read_sql_query(r'SELECT 1 FROM Cards WHERE Card_Name = "%s"' % name, engine)
    if df.shape[0] == 0:  # This means the card was not found in the database and should be inserted
        with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                             db=database_parameters['Database_Name']) as con:
            insert_command = '''INSERT INTO Cards (Card_name, Class, Type, Rarity, Card_set, Release_year, Cost, 
                                Artist, Mana_Cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            try:
                card_dict['Release Year'] = SET_RELEASE_DICT[card_dict['Set']]
            except KeyError:
                # if a new set was released and isn't found in the dictionary the current year will be taken
                card_dict['Release Year'] = date.today().year
            insert_values = [name, card_dict['Class'], card_dict['Type'], card_dict['Rarity'], card_dict['Set'],
                             card_dict['Release Year'], card_dict['Cost'], card_dict['Artist'], card_dict['Mana Cost'],
                             card_dict['Attack'], card_dict['Health']]
            con.execute(insert_command, insert_values)
            print("%s was put into the database" % name)


def insert_mechanics(card_info, database_parameters):
    with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                         db=database_parameters['Database_Name']) as con:
        mechanics_list = ' '.join(card_info['Mechanics'])
        # mechanics_list = ' '.join(card_api(card_name)['Mechanics'])
        insert_command = '''INSERT INTO Mechanics (
                   Mechanic_Name) VALUES (%s)'''
        con.execute(insert_command, mechanics_list)


def insert_card_mechanics(card_name, card_info, database_parameters):
    with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                         db=database_parameters['Database_Name']) as con:
        # gather
        con.execute('SELECT Сard_ID, Card_Name FROM Cards WHERE Card_Name = VALUES (%s)', card_name)
        card_id = con.fetchall()[0][0]
        mechanics_list = ' '.join(card_info['Mechanics'])
        con.execute('SELECT Mechanics_ID FROM Mechanics WHERE Mechanic_Name = VALUES (%s)', mechanics_list)  # ugly?
        mechanics_id = con.fetchall()[0][0]
        # insert
        insert_command = '''INSERT INTO Card_Mechanics (
           Card_ID, Mechanic_ID) VALUES (%s, %s)'''
        insert_values = [card_id, mechanics_id]
        con.execute(insert_command, insert_values)


def insert_decks(winner_deck, loser_deck, database_parameters):
    """Given a winning and losing deck from a match - insert into Decks table in the database"""
    decks = [loser_deck, winner_deck]
    insert_command = '''INSERT INTO Decks (Deck_Name, Winner, Deck_Prefix, Class, Deck_Cost, 
            Average_Card_Cost, Most_Common_Set, Most_Common_Type, Number_of_Unique_Cards) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                         db=database_parameters['Database_Name']) as con:
        for win, deck in enumerate(decks):
            # Insert winner and loser deck into the database / for loser win = 0 and for winner win = 1
            name = ' '.join([deck['Deck'], deck['Class']])
            insert_values = [name, bool(win), deck['Deck'], deck['Class'], deck['Deck Cost'], deck['Average Card Cost'],
                             deck['Most_Common_Set'], deck['Most_Common_Type'], len(deck['Cards'])]
            con.execute(insert_command, insert_values)


def card_in_deck_update(winner_cards, loser_cards, database_parameters):
    """Given cards from winning and losing deck in a match - insert into card_in_deck table in the database"""
    decks = [winner_cards, loser_cards]
    insert_command = 'INSERT INTO Card_In_Deck (Deck_ID, Card_ID, Number_of_Copies) VALUES (%s, %s, %s)'
    with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                         db=database_parameters['Database_Name']) as con:
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


def create_database(database_parameters):
    with pymysql.connect(host=database_parameters['Host_Name'], user='root',
                         passwd=database_parameters['Password']) as con:
        con.execute("CREATE DATABASE %s" % database_parameters['Database_Name'])


def create_tables(database_parameters):
    """Create tables in HS_stats Database"""
    create_table_decks = '''CREATE TABLE Decks (
        Deck_ID INT AUTO_INCREMENT,
        Deck_Name VARCHAR(100),
        Winner BOOL,
        Deck_Prefix VARCHAR(100),
        Class VARCHAR(100),
        Deck_Cost INT,
        Average_Card_Cost FLOAT,
        Most_Common_Set VARCHAR(100),
        Most_Common_Type VARCHAR(100),
        Number_of_Unique_Cards INT,
        PRIMARY KEY (Deck_ID))'''
    create_table_matches = '''CREATE TABLE Matches (
        Match_ID INT AUTO_INCREMENT,
        Match_URL VARCHAR(100),
        Winner_Deck_ID INT,
        Looser_Deck_ID INT,
        Winner_Player_Rank VARCHAR(100),
        Looser_Player_Rank VARCHAR(100),
        FOREIGN KEY(Winner_Deck_ID) REFERENCES Decks(Deck_ID),
        FOREIGN KEY(Looser_Deck_ID) REFERENCES Decks(Deck_ID),
        PRIMARY KEY (Match_ID))'''
    create_table_cards = '''CREATE TABLE Cards (
        Card_ID INT AUTO_INCREMENT,
        Card_name VARCHAR(100),
        Class VARCHAR(100),
        Type VARCHAR(100),
        Rarity VARCHAR(100),
        Card_set VARCHAR(100),
        Release_year YEAR,
        Cost INT,
        Artist VARCHAR(100),
        Mana_Cost INT,
        Attack INT,
        Health INT,
        PRIMARY KEY (Card_ID))'''
    create_table_card_in_deck = '''CREATE TABLE Card_In_Deck (
        ID INT AUTO_INCREMENT,
        Number_of_Copies INT,
        Deck_ID INT,
        Card_ID INT,
        FOREIGN KEY(Deck_ID) REFERENCES Decks(Deck_ID),
        FOREIGN KEY(Card_ID) REFERENCES Cards(Card_ID),
        PRIMARY KEY (ID))'''
    create_table_mechanics = '''CREATE TABLE Mechanics (
        Mechanics_ID INT AUTO_INCREMENT,
        Mechanic_Name VARCHAR(100),
        PRIMARY KEY (Mechanics_ID))'''
    create_table_card_mechanics = '''CREATE TABLE Card_Mechanics (
        Card_Mechanics_ID INT AUTO_INCREMENT,
        Card_ID INT,
        Mechanic_ID INT,
        FOREIGN KEY(Card_ID) REFERENCES Cards(Card_ID),
        FOREIGN KEY(Mechanic_ID) REFERENCES Mechanics(Mechanics_ID),
        PRIMARY KEY (Card_Mechanics_ID))'''
    table_commands = [create_table_decks, create_table_matches, create_table_cards, create_table_card_in_deck,
                      create_table_mechanics, create_table_card_mechanics]
    with pymysql.connect(host=database_parameters['Host_Name'], user='root', passwd=database_parameters['Password'],
                         db=database_parameters['Database_Name']) as con:
        for command in table_commands:
            con.execute(command)


def main():
    """Function used to test the decks_table creation and handling functions"""
    database_parameters = {'Host_Name': 'localhost', 'Password': 'YourPasswrd', 'Database_Name': 'HS_Stats'}
    # Use to reset database as needed
    # try:
    #     with pymysql.connect(host='localhost', user='root', passwd=PASSWORD) as con:
    #         con.execute("DROP DATABASE %s" % DB_FILENAME)
    #         print("database found and deleted")
    # create_database(database_parameters)  # will throw an error if already exists
    # create_tables(database_parameters)  # will throw an error if already exists
    feed_results = feed_parser()
    for iterations, match in enumerate(feed_results):
        match_url, winner, loser = match[0], match[1], match[2]
        winner_rank = winner[1]
        looser_rank = loser[1]
        print('{} - winner deck {}, winner rank {}, looser deck {}, looser rank {}'.format(match_url, winner[0],
                                                                                           winner_rank, loser[0],
                                                                                           looser_rank))
        winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, False)
        insert_decks(winner_deck, loser_deck, database_parameters)
        insert_matches(match_url, winner, loser, database_parameters)
        for card_name, card_info in mined_cards.items():
            insert_card(card_name, card_info, database_parameters)
            insert_mechanics(card_info, database_parameters)
            insert_card_mechanics(card_name, card_info, database_parameters)
        card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'], database_parameters)
        if iterations == 1:
            break


if __name__ == '__main__':
    main()