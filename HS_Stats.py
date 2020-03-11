"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from feed_parser import feed_parser
from game_parser import game_parser

INFINITE = False  # Set to True for indefinite value collection
N_ITERATIONS = 1  # Only relevant when INFINITE is set to False - determine number of scraping iterations


def main():
    """This function can be set to gather HearthStone data indefinitely (until key prompt)
     or for a set number of iterations"""
    i = 0
    while (i < N_ITERATIONS) or INFINITE:
        i += 1
        matches = feed_parser()
        for match in matches:
            print(match)
            match_url, winner, loser = match[0], match[1], match[2]
            winner_deck, loser_deck = game_parser(match_url, winner, loser)
            print("The Winning Deck of the match is:")
            print(winner_deck)
            print("The Losing Deck of the match is:")
            print(loser_deck)


if __name__ == '__main__':
    main()
