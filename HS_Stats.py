"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from feed_parser import feed_parser
from game_parser import game_parser
from selenium.common.exceptions import WebDriverException
from Database import insert_card, insert_decks, insert_matches, create_database, create_tables, card_in_deck_update
from card_mine import PASSWORD, DB_FILENAME
import pymysql

INFINITE = False  # Set to True for indefinite value collection
N_ITERATIONS = 1  # Only relevant when INFINITE is set to False - determine number of scraping iterations
QUIET = False  # if not provided - defaults to False. When set to True - suppress driver window popup
CREATE_NEW_DB = True


def main():
    """This function can be set to gather HearthStone data indefinitely (until key prompt)
     or for a set number of iterations"""
    i = 0
    while (i < N_ITERATIONS) or INFINITE:
        i += 1
        matches = feed_parser()
        for match in matches:
            try:
                print(match)
                match_url, winner, loser = match[0], match[1], match[2]
                winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, QUIET)
                print("The Winning Deck of the match is:")
                print(winner_deck)
                print("The Losing Deck of the match is:")
                print(loser_deck)
                if CREATE_NEW_DB:   # set to True to delete database if one is found and create new one
                    try:
                        with pymysql.connect(host='localhost', user='root', passwd=PASSWORD) as con:
                            con.execute("DROP DATABASE %s" % DB_FILENAME)
                            print("database found and deleted")
                    except pymysql.err.InternalError as e:
                        print(e)
                    except pymysql.err.OperationalError:
                        print("Wrong Password")
                        exit()
                    create_database()  # will throw an error if already exists
                    create_tables()  # will throw an error if already exists
                insert_decks(winner_deck, loser_deck)
                insert_matches(match_url, winner, loser)
                for card_name, card_info in mined_cards.items():
                    insert_card(card_name, card_info)
                card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'])
            except WebDriverException:
                print("Error! something went wrong with the driver and the program could not continue!")
                print(WebDriverException)
                exit()


if __name__ == '__main__':
    main()
