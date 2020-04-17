"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko

This function concentrates all database related functions - table creation
"""

import pymysql
from game_parser import game_parser
from feed_parser import feed_parser
from config import SET_RELEASE_DICT, USER, HOST_NAME, DB_FILENAME
from datetime import date
import numpy as np


def insert_matches(match_url, winner, loser, con):
    """
    This function writes results of matches into matches table
    :param match_url: url of the game
    :param winner: name and rank of winning deck
    :param loser: name and rank of losing deck
    :param con: connection object to mysql database
    """
    con.execute('SELECT MAX(Deck_ID) FROM Decks')  # find max deck_id (latest input)
    deck_id = con.fetchall()[0][0]
    winner_rank = winner[1]
    looser_rank = loser[1]
    insert_command = '''INSERT INTO Matches (Match_URL, Winner_Deck_ID, Looser_Deck_ID, Winner_Player_Rank, 
                Looser_Player_Rank) VALUES (%s, %s, %s, %s, %s)'''
    insert_values = [match_url, deck_id, deck_id - 1, winner_rank, looser_rank]
    con.execute(insert_command, insert_values)


def insert_card(name, card_dict, con):
    """
    This function gets the card's name and details and inserts it into the cards database,
    unless it's there already
    :param name: name of the card
    :param card_dict: card info in dictionary format
    :param con: connection object to mysql database
    """
    con.execute(f'SELECT 1 FROM Cards WHERE Card_Name = "{name}"')
    search_card_name = con.fetchall()
    if np.shape(search_card_name) == (0,):  # This means the card was not found in the database and should be inserted
        try:
            card_dict['Release Year'] = SET_RELEASE_DICT[card_dict['Set']]
        except KeyError:
            # if a new set was released and isn't found in the dictionary the current year will be taken
            card_dict['Release Year'] = date.today().year
        insert_command = '''INSERT INTO Cards (Card_name, Class, Type, Rarity, Card_set, Release_year, Cost,
                            Artist, Mana_Cost, Attack, Health) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        insert_values = [name, card_dict['Class'], card_dict['Type'], card_dict['Rarity'], card_dict['Set'],
                         card_dict['Release Year'], card_dict['Cost'], card_dict['Artist'], card_dict['Mana Cost'],
                         card_dict['Attack'], card_dict['Health']]
        con.execute(insert_command, insert_values)
        print(f"{name} was put into the database")


def insert_mechanics(card_info, con):
    """
    Insert into mechanics table any new mechanics found on cards
    :param card_info: card info in dictionary format
    :param con: connection object to mysql database
    """
    mechanics_list = card_info['Mechanics']
    for mechanic in mechanics_list:
        con.execute(f'select 1 from Mechanics where Mechanic_Name = "{mechanic}"')
        search_mechanic_name = con.fetchall()
        if np.shape(search_mechanic_name) == (0,):
            con.execute(f'INSERT INTO Mechanics (Mechanic_Name) VALUES ("{mechanic}")')


def insert_card_mechanics(card_name, card_info, con):
    """
    insert into the connection table rows which connect between card_id and mechanic_id
    :param card_name: name of the card
    :param card_info: card info in dictionary format
    :param con: connection object to mysql database
    """
    con.execute(f'SELECT Card_ID, Card_Name FROM Cards WHERE Card_Name = "{card_name}"')
    card_id = con.fetchall()[0][0]
    con.execute(f'SELECT 1 FROM Card_Mechanics WHERE Card_ID = "{card_id}"')
    search_card_id = con.fetchall()
    if np.shape(search_card_id) == (0,):
        mechanics_list = card_info['Mechanics']
        for mechanic in mechanics_list:
            con.execute(f'SELECT Mechanic_ID FROM Mechanics WHERE Mechanic_Name = "{mechanic}"')
            mechanics_id = con.fetchall()[0][0]
            con.execute(f'INSERT INTO Card_Mechanics (Card_ID, Mechanic_ID) VALUES ("{card_id}", "{mechanics_id}")')


def insert_decks(winner_deck, loser_deck, con):
    """
    Given a winning and losing deck from a match - insert into Decks table in the database
    :param winner_deck: name of the winning deck in a match
    :param loser_deck: name of the losing deck in a match
    :param con: connection object to mysql database
    """
    decks = [loser_deck, winner_deck]
    insert_command = '''INSERT INTO Decks (Deck_Name, Winner, Deck_Prefix, Class, Deck_Cost, 
            Average_Card_Cost, Most_Common_Set, Most_Common_Type, Number_of_Unique_Cards) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    for win, deck in enumerate(decks):
        # Insert winner and loser deck into the database / for loser win = 0 and for winner win = 1
        name = ' '.join([deck['Deck'], deck['Class']])
        insert_values = [name, bool(win), deck['Deck'], deck['Class'], deck['Deck Cost'], deck['Average Card Cost'],
                         deck['Most_Common_Set'], deck['Most_Common_Type'], len(deck['Cards'])]
        con.execute(insert_command, insert_values)


def card_in_deck_update(winner_cards, loser_cards, con):
    """
    Given cards from winning and losing deck in a match - insert into card_in_deck table in the database
    :param winner_cards: a dictionary of card found in the winning deck and occurrences
    :param loser_cards: a dictionary of card found in the losing deck and occurrences
    :param con: connection object to mysql database
    """
    decks = [winner_cards, loser_cards]
    insert_command = 'INSERT INTO Card_In_Deck (Deck_ID, Card_ID, Number_of_Copies) VALUES (%s, %s, %s)'
    con.execute('SELECT MAX(Deck_ID) FROM Decks')  # find max deck_id (latest input)
    result = con.fetchall()[0][0]
    for index, deck in enumerate(decks):
        # for win/lose pair loser is inserted into decks first to decks so here winner cards gets deck_id for
        # latest insert in decks and loser cards get deck_id for deck above that which is the loser of the pair
        deck_id = result - index
        for card, duplicates in deck.items():
            con.execute(f'SELECT Card_ID FROM Cards WHERE Card_Name = "{card}"')
            card_id = con.fetchall()[0][0]
            insert_values = [deck_id, card_id, duplicates]
            con.execute(insert_command, insert_values)


def create_database(con, database_name):
    """
    Create a database with the given name including tables
    :param con: connection object to mysql database
    :param database_name: requested name for database
    """
    con.execute(f"CREATE DATABASE {database_name}")
    create_tables(con, database_name)


def create_tables(con, database_name):
    """
    Create tables in HS_stats Database
    :param database_name: requested name for database:
    :param con: connection object to mysql database
    """
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
        Mechanic_ID INT AUTO_INCREMENT,
        Mechanic_Name VARCHAR(100),
        PRIMARY KEY (Mechanic_ID))'''
    create_table_card_mechanics = '''CREATE TABLE Card_Mechanics (
        Card_Mechanic_ID INT AUTO_INCREMENT,
        Card_ID INT,
        Mechanic_ID INT,
        FOREIGN KEY(Card_ID) REFERENCES Cards(Card_ID),
        FOREIGN KEY(Mechanic_ID) REFERENCES Mechanics(Mechanic_ID),
        PRIMARY KEY (Card_Mechanic_ID))'''
    use_command = f"USE {database_name}"
    table_commands = [use_command, create_table_decks, create_table_matches, create_table_cards,
                      create_table_card_in_deck, create_table_mechanics, create_table_card_mechanics]
    for command in table_commands:
        con.execute(command)


def main():
    """Function used to test the decks_table creation and handling functions"""
    test_db_password = input('Password for MySQL: ')
    feed_results = feed_parser()
    for iterations, match in enumerate(feed_results):
        match_url, winner, loser = match[0], match[1], match[2]
        winner_rank = winner[1]
        looser_rank = loser[1]
        print('{} - winner deck {}, winner rank {}, looser deck {}, looser rank {}'.format(match_url, winner[0],
                                                                                           winner_rank, loser[0],
                                                                                           looser_rank))
        winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, False)
        with pymysql.connect(host=HOST_NAME, user=USER, passwd=test_db_password, db=DB_FILENAME) as con:
            insert_decks(winner_deck, loser_deck, con)
            insert_matches(match_url, winner, loser, con)
            for card_name, card_info in mined_cards.items():
                insert_card(card_name, card_info, con)
                insert_mechanics(card_info, con)
                insert_card_mechanics(card_name, card_info, con)
            card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'], con)
            if iterations == 1:
                break


if __name__ == '__main__':
    main()
