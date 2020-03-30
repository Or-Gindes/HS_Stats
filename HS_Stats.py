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
    i = 0
    if infinite:
        print("Warning! Hs_stats has been run with the infinite parameter and will collect data until interrupted "
              "by key prompt (CTRL + C) or close the driver window\n")
    while (i < number_of_iterations) or infinite:
        i += 1
        try:
            matches = feed_parser(quiet)
            for match in matches:
                print(match)
                match_url, winner, loser = match[0], match[1], match[2]
                winner_deck, loser_deck, mined_cards = game_parser(match_url, winner, loser, quiet)
                # TODO: input 'winner_deck' and 'loser_deck' into the decks table in the database - OR
                # TODO: input 'matches' into matches table in the database - MARIIA
                # TODO: input 'mined_cards' into cards table in the database - DOR
                print("The Winning Deck of the match is:")
                print(winner_deck)
                print("The Losing Deck of the match is:")
                print(loser_deck)
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
