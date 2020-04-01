"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

Hs_Stats.py is the main scrapping script which can be run for a number of iterations or indefinitely
(until keyboard interrupt).
Each iteration will scrape up to 10 HearthStone matches
"""

from feed_parser import feed_parser
from game_parser import game_parser
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from urllib3.exceptions import MaxRetryError
from argparse_cli import parse_args_cli
from Database import insert_card, insert_decks, insert_matches, create_database, create_tables, card_in_deck_update
from config import PASSWORD, DB_FILENAME, CREATE_NEW_DB   # TODO: get this input from user, not necessarily in CLI
import pymysql


def initializedb():
    if CREATE_NEW_DB:  # set to True to delete database if one is found and create new one
        try:
            with pymysql.connect(host='localhost', user='root', passwd=PASSWORD) as con:
                con.execute("DROP DATABASE %s" % DB_FILENAME)
                print("database found and deleted")
        except pymysql.err.InternalError as e:
            print(e)
        except pymysql.err.OperationalError:
            print("Wrong Password")
            exit()
        create_database()
        create_tables()


def main():
    """This function can be set to gather HearthStone data indefinitely (until key prompt)
     or for a set number of iterations"""
    arguments = parse_args_cli()
    # infinite - Set to True for indefinite value collection
    infinite = arguments[0]
    # number_of_iterations - Only relevant when INFINITE is set to False - determine number of scraping iterations
    number_of_iterations = arguments[1]
    # quiet - if not provided defaults to False. When set to True - suppress driver window popup
    quiet = arguments[2]
    initializedb()
    i = 0
    if infinite:
        print("Warning! Hs_stats has been run with the infinite parameter and will collect data until interrupted "
              "by key prompt (CTRL + C) or close the driver window\n")
    while (i < number_of_iterations) or infinite:
        i += 1
        try:
            print("Now scrapping matches from HsReplay live feed")
            matches = feed_parser(quiet)
            for match in matches:
                print(match)
                match_url, winner, loser = match[0], match[1], match[2]
                winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, quiet)
                print("\nDatabase is updated with the Winning Deck of the match:")
                print(winner_deck)
                print("\nDatabase is updated with the Losing Deck of the match:")
                print(loser_deck)
                insert_decks(winner_deck, loser_deck)
                insert_matches(match_url, winner, loser)
                for card_name, card_info in mined_cards.items():
                    insert_card(card_name, card_info)
                card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'])
        except (WebDriverException, NoSuchWindowException, TypeError) as err:
            print("\nError! something went wrong with the driver and the program could not continue!\nOne common cause "
                  "for this error is you might have closed the driver window\nIf that is the case please consider "
                  "running the program in quite mode (-q) to suppress driver window pop-up\n")
            print("More information on error: " + err.args[0])
        except (KeyboardInterrupt, MaxRetryError):
            print("Thank you for using Hs Stats - HearthStone matches webscrapper")
        finally:
            exit()


if __name__ == '__main__':
    main()
