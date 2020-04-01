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
from config import SCHEME
import pymysql


def initialize_db(database_parameters, overwrite):
    try:  # try connecting using given database_parameters
        with pymysql.connect(host=database_parameters['Host_Name'], user='root',
                             passwd=database_parameters['Password']) as con:
            if overwrite:  # if overwrite - try to drop database
                con.execute("DROP DATABASE %s" % database_parameters['Database_Name'])
                print("Old database found and deleted")
    # except pymysql.err.InternalError as e:
    #     print(e)
    #     exit()
    except pymysql.err.OperationalError:
        print("Error - Wrong Password or Host name were provided for MySQL")
        exit()
    else:
        try:  # Try to create database, if it was dropped or did not exists it will be created otherwise except
            create_database(database_parameters)
            create_tables(database_parameters)
            print(SCHEME)
            print("Database '%s' was created" % database_parameters['Database_Name'])
        except pymysql.err.ProgrammingError:    # Database was found and will be used
            print("Database named '%s' was found and will be used (was not overwritten)" %
                  database_parameters['Database_Name'])


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
    # database_parameters holds information to connect to users MySQL Database
    database_parameters = {'Host_Name': arguments[3], 'Password': arguments[4], 'Database_Name': arguments[5]}
    # When set to True and a database with dbname is found the database will be reset
    overwrite = arguments[6]
    initialize_db(database_parameters, overwrite)
    i = 0
    if infinite:
        print("Warning! Hs_stats has been run with the infinite parameter and will collect data until interrupted "
              "by key prompt (CTRL + C) or close the driver window\n")
    try:
        while (i < number_of_iterations) or infinite:
            i += 1
            print("Now scrapping matches from HsReplay live feed")
            matches = feed_parser(quiet)
            for match in matches:
                print(match)
                match_url, winner, loser = match[0], match[1], match[2]
                winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, database_parameters, quiet)
                print("\nDatabase is updated with the Winning Deck of the match:")
                print(winner_deck)
                print("\nDatabase is updated with the Losing Deck of the match:")
                print(loser_deck)
                insert_decks(winner_deck, loser_deck, database_parameters)
                insert_matches(match_url, winner, loser, database_parameters)
                for card_name, card_info in mined_cards.items():
                    insert_card(card_name, card_info, database_parameters)
                card_in_deck_update(winner_deck['Cards'], loser_deck['Cards'], database_parameters)
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
