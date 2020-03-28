"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko
"""

import sqlite3

DB_FILENAME = 'HS_Stats.db'
SET_RELEASE_DIC = {'Basic': 2014, 'Classic': 2014, 'Ashes of Outland': 2020, 'Descent of Dragons': 2019,
                   'Saviors of Uldum': 2019, 'Rise of Shadows': 2019, 'The Witchwood': 2018, 'The Boomsday Project': 2018,
                   "Rastakhan's Rumble": 2018}


def create_cards_table():

    """
    This function creates the cards table within the Hs_stats database.
    """
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE cards (
                        Card_name VARCHAR PRIMARY KEY,
                        Class VARCHAR,
                        Type VARCHAR,
                        Rarity VARCHAR,
                        'Set' VARCHAR,
                        Release_year YEAR,
                        Cost INT,
                        Artist VARCHAR,
                        Mana_cost INT)''')
        con.commit()
        cur.close()


def cards_update(name, card_dict):

    """
    This function gets the card's name and details and inserts it into the cards database, unless it's there already.
    """
    with sqlite3.connect(DB_FILENAME) as con:
        cur = con.cursor()
        card_dict['Release Year'] = SET_RELEASE_DIC[card_dict['Set']]
        cur.execute('''INSERT OR IGNORE INTO cards (Card_name, Class, Type, Rarity, 'Set', Release_year, Cost, 
        Artist, Mana_cost) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    [name, card_dict['Class'], card_dict['Type'], card_dict['Rarity'], card_dict['Set'],
                     card_dict['Release Year'], card_dict['Cost'], card_dict['Artist'], card_dict['Mana cost']])
        con.commit()
        cur.close()


def main():

    """
    The main() function, for testing the above functions.
    """
    create_cards_table()
    # TODO: conditional creation - only if it doesn't already exist in the database (only after fusing).
    inner_name = 'Inner-Rage'
    inner_dict = {'Class': 'Warrior', 'Type': 'Spell', 'Rarity': 'Common', 'Set': 'Classic', 'Cost': 40, 'Artist': 'Slawomir Maniak', 'Mana cost': 0}
    inner_dict2 = {'Class': 'Warrior', 'Type': 'Spell', 'Rarity': 'Common', 'Set': 'Classic', 'Cost': 40, 'Artist': 'Or Gindes', 'Mana cost': 0}
    cards_update(inner_name, inner_dict)

    # Proof that the function does not overwrite existing cards
    cards_update(inner_name, inner_dict2)


if __name__ == '__main__':
    main()

