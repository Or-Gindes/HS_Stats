"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar

Hs_Stats.py is the main scrapping script which can be run for a number of iterations
or indefinitely (until keyboard interrupt). Each iteration will scrape about 10 HearthStone matches
"""

from feed_parser import feed_parser
from game_parser import game_parser
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from urllib3.exceptions import MaxRetryError
from settings import INFINITE, N_ITERATIONS, QUIET  # these will be replaced by cli argument parser in checkpoint #2


def main():
    """This function can be set to gather HearthStone data indefinitely (until key prompt)
     or for a set number of iterations"""
    i = 0
    if INFINITE:
        print("Warning! Hs_stats has been run with the infinite parameter and will collect data until interrupted "
              "by key prompt (CTRL + C) or close the driver window\n")
    while (i < N_ITERATIONS) or INFINITE:
        i += 1
        try:
            matches = feed_parser()
            for match in matches:
                print(match)
                match_url, winner, loser = match[0], match[1], match[2]
                winner_deck, loser_deck = game_parser(match_url, winner, loser, QUIET)
                print("The Winning Deck of the match is:")
                print(winner_deck)
                print("The Losing Deck of the match is:")
                print(loser_deck)
        except (WebDriverException, NoSuchWindowException) as err:
            print("\nError! something went wrong with the driver and the program could not continue!\nOne common cause "
                  "for this error is you might have closed the driver window\nIf that is the case please consider "
                  "running the program in quite mode (-q) to suppress driver window pop-up\n")
            print(err.args[0])
        except (KeyboardInterrupt, MaxRetryError):
            print("Thank you for using Hs Stats - Hearthstone matches webscrapper")
        finally:
            exit()


if __name__ == '__main__':
    main()
