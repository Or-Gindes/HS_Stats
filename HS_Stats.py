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
from Database import insert_card, insert_decks, insert_matches, create_database, card_in_deck_update, \
    insert_mechanics, insert_card_mechanics
from config import SCHEME, CARDS, USER
import pymysql
import numpy as np


def initialize_db(db_params):
    """
    :param db_params: holds information to connect to users MySQL Database
    """
    try:  # try connecting using given database_parameters
        with pymysql.connect(host=db_params.hostname, user=USER, passwd=db_params.password) as con:
            if db_params.overwrite:  # if overwrite - try to drop database
                con.execute(f"DROP DATABASE {db_params.dbname}")
                print("Old database found and deleted\n")
            create_database(con, db_params.dbname)
            print(SCHEME)
            print(f"Database '{db_params.dbname}' was created\n")
    except pymysql.err.InternalError:
        print("Can't overwrite specified database because it doesn't exist.")
        exit()
    except pymysql.err.OperationalError:
        print("Error - Could not connect to database with the specified access details, please check them again.")
        exit()
    except pymysql.err.ProgrammingError:  # Database was found and will be used
        print(f"Database named '{db_params.dbname}' was found and will be used (was not overwritten)\n")


def main():
    """This function can be set to gather HearthStone data indefinitely (until key prompt)
     or for a set number of iterations"""
    args, infinity = parse_args_cli()
    if args.number_of_iterations >= 0:
        initialize_db(args)
        iteration = 0
        if infinity:
            print("Warning! Hs_stats has been run with the infinite parameter and will collect data until interrupted "
                  "by key prompt (CTRL + C) or close the driver window\n")
        else:
            print(f"The script will now run for {args.number_of_iterations} iteration" +
                  "s" * (int(args.number_of_iterations > 1)) + "\n")
        try:
            while (iteration < args.number_of_iterations) or infinity:
                iteration += 1
                print(f"Iteration {iteration} of {args.number_of_iterations}" * int(bool(args.number_of_iterations)),
                      end='')
                print(f"Iteration {iteration} of infinite number" * int(infinity))
                print("Now scrapping matches from HsReplay live feed:\n")
                matches = feed_parser(args.quiet)
                print(f"Found {len(matches)} matches to parse")
                print("---------------------------------------\n")
                for match_num, match in enumerate(matches, start=1):
                    match_url, winner, loser = match[0], match[1], match[2]
                    print(f"Now parsing match {match_num} of {len(matches)}")
                    print(f"Match URL address is: {match_url}")
                    print(f"{winner[0]} VS. {loser[0]} \n")
                    winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, args.quiet)
                    if (not winner_deck) and (not loser_deck):
                        break
                    with pymysql.connect(host=args.hostname, user=USER, passwd=args.password, db=args.dbname) as con:
                        con.execute(f'SELECT 1 FROM Matches WHERE Match_URL = "{match_url}"')
                        search_match = con.fetchall()
                        if np.shape(search_match) == (0,):
                            insert_decks(winner_deck, loser_deck, con)
                            insert_matches(match_url, winner, loser, con)
                            print("\nDatabase updates:")
                            print("---------------------------------------\n")
                            print("Database is updated with the Winning Deck of the match:")
                            print(winner_deck)
                            print("\nDatabase is updated with the Losing Deck of the match:")
                            print(loser_deck)
                            print("\n")
                            for card_name, card_info in mined_cards.items():
                                insert_card(card_name, card_info, con)
                                insert_mechanics(card_info, con)
                                insert_card_mechanics(card_name, card_info, con)
                            print(f"\nExtracted all data from match {match_num}\n")
                            card_in_deck_update(winner_deck[CARDS], loser_deck[CARDS], con)
                        else:
                            print("Duplicate match - skipping")
        except (WebDriverException, NoSuchWindowException, TypeError, IndexError) as err:
            print("\nError! something went wrong with the driver and the program could not continue!\nOne common cause "
                  "for this error is you might have closed the driver window or lost internet connection \nIf that is "
                  "the case please consider running the program in quite mode (-q) to suppress driver window pop-up\n")
            print(f"More information on error: {err.args[0]}")
            exit()
        except (KeyboardInterrupt, MaxRetryError):
            print("Thank you for using Hs Stats - HearthStone matches webscrapper")
            exit()
    else:
        print(f"Negative number of iterations {args.number_of_iterations} isn't valid - Please provide a valid input.")


if __name__ == '__main__':
    main()
