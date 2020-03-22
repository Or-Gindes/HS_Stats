"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko
"""

import sqlite3
import os
from game_parser import game_parser

DB_FILENAME = 'Hs_Stats.db'
DB = os.path.join(os.path.dirname(os.path.realpath(__file__)), DB_FILENAME)


def decks_update(winner_deck, loser_deck):
    """Given a winning and losing deck from a match - insert into database"""
    decks = [loser_deck, winner_deck]
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        cur.execute('SELECT MAX(Deck_ID) FROM decks')
        max_id = cur.fetchall()[0][0]
        if max_id is None:
            max_id = 0
        for win, deck in enumerate(decks):
            max_id += 1
            name = ' '.join([deck['Deck'], deck['Class']])
            cur.execute('''INSERT INTO decks (Deck_Name, Winner, Deck_Prefix, Class, Deck_Cost, 
            Average_Card_Cost, Most_Common_Set, Most_Common_Type, Number_of_Unique_Cards) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        [name, bool(win), deck['Deck'], deck['Class'], deck['Deck Cost'],
                         deck['Average Card Cost'],
                         deck['Most_Common_Set'], deck['Most_Common_Type'], len(deck['Cards'])])
            k = 1
            for card in deck['Cards'].keys():
                for i in range(deck['Cards'][card]):
                    cur.execute("UPDATE decks SET Card_%d = '%s' WHERE Deck_ID = %d" % (k, card, max_id))
                    k += 1
        con.commit()
        cur.close()


def create_decks_table():
    """Create Decks table in HS_stats Database"""
    # TODO: Decide if card related features should be in this table - Deck_cost / vAverage_Card_Cost / Most_Common_Set / Most_Common_Type
    command_string = '''CREATE TABLE decks (
        Deck_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Deck_Name VARCHAR,
        Winner BOOL,
        Deck_Prefix VARCHAR,
        Class VARCHAR,
        Deck_Cost INT,
        Average_Card_Cost INT,
        Most_Common_Set VARCHAR,
        Most_Common_Type VARCHAR,
        Number_of_Unique_Cards INT,\n'''
    for k in range(1, 31):
        command_string += ("\t\tCard_" + str(k) + " VARCHAR,\n")
    command_string = command_string[:-2] + ')'
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        cur.execute(command_string)
        con.commit()
        cur.close()


def main():
    """Function used to test the decks_table creation and handling functions"""
    # Use to reset database as needed
    # if os.path.exists(DB):
    #     os.remove(DB)
    # create_decks_table()
    game_url = 'https://hsreplay.net/replay/tHc63LLjsgnHAao2yki6DX'
    winner_deck, loser_deck = game_parser(game_url, ('Aggro Overload Shaman', 'Rank 1'),
                                          ('Quest Hunter', 'Legend 1000'),
                                          True)
    # winner_deck = {'Deck': 'Highlander', 'Class': 'Warrior', 'Player Rank': 'Rank 1', 'Deck Cost': 16380,
    #                'Average Card Cost': 3.9,
    #                'Most_Common_Set': 'The Boomsday Project', 'Most_Common_Type': 'Minion',
    #                'Cards': {'Eternium-Rover': 1, 'Shield-Slam': 1,
    #                          'Town-Crier': 1, 'Whirlwind': 1, 'Dragon-Roar': 1, 'Firetree-Witchdoctor': 1, 'Warpath': 1,
    #                          'Weapons-Project': 1,
    #                          'Zephrys-The-Great': 1, 'Bomb-Wrangler': 1, 'Evil-Quartermaster': 1, 'Livewire-Lance': 1,
    #                          'Shield-Block': 1,
    #                          'Sn1P-Sn4P': 1, 'Vulpera-Scoundrel': 1, 'Molten-Breath': 1, 'Omega-Devastator': 1,
    #                          'Restless-Mummy': 1, 'Brawl': 1,
    #                          'Cobalt-Spellkin': 1, 'Dragonmaw-Scorcher': 1, 'Dyn-O-Matic': 1, 'Harrison-Jones': 1,
    #                          'Plague-Of-Wrath': 1,
    #                          'Supercollider': 1, 'Zilliax': 1, 'Siamat': 1, 'Deathwing-Mad-Aspect': 1,
    #                          'Dr-Boom-Mad-Genius': 1, 'Dragonqueen-Alexstrasza': 1}}
    # loser_deck = {'Deck': 'Dragon', 'Class': 'Hunter', 'Player Rank': 'Legend 1000', 'Deck Cost': 5400,
    #               'Average Card Cost': 2.77, 'Most_Common_Set': 'Descent of Dragons', 'Most_Common_Type': 'Minion',
    #               'Cards':
    #                   {'Blazing-Battlemage': 2, 'Dwarven-Sharpshooter': 2, 'Tracking': 2, 'Corrosive-Breath': 2,
    #                    'Explosive-Trap': 1,
    #                    'Faerie-Dragon': 2, 'Phase-Stalker': 2, 'Snake-Trap': 1, 'Primordial-Explorer': 2,
    #                    'Scalerider': 2, 'Stormhammer': 2,
    #                    'Dragonbane': 1, 'Evasive-Feywing': 2, 'Frenzied-Felwing': 2, 'Lifedrinker': 2,
    #                    'Leeroy-Jenkins': 1, 'Rotnest-Drake': 2}}
    decks_update(winner_deck, loser_deck)
    # Testing
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        cur.execute('''
        SELECT Deck_ID, Winner, Deck_Name, Class, Deck_Cost, Average_Card_Cost, Card_2
        FROM decks
        WHERE Winner = 1''')
        result = cur.fetchall()
        print(result)
        cur.close()
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        cur.execute('''
        SELECT Deck_ID, Winner, Deck_Name, Class, Deck_Cost, Average_Card_Cost, Card_2
        FROM decks
        ''')
        result = cur.fetchall()
        print(result)
        cur.close()


if __name__ == '__main__':
    main()
