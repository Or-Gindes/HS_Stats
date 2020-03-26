"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

This function receives a single match url and parses the game, returning the decks from it
"""
from card_mine import card_mine
from get_driver import get_driver
from _collections import defaultdict
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from config import MATCH_URL_PATTERN, CARDS_IN_DECK, WAIT


def get_card(link, quiet):
    """
    :param link: web-element of each card in deck
    :return: card: dictionary of card data / count: number of times a card appears in the deck
    """
    card_url = link.get_attribute("href")  # get link to card - used to with card_mine to get card info
    card_name = card_url.rsplit('/', 1)[1].title()
    card_dict = card_mine(card_url, quiet)
    try:
        count = int(link.find_element_by_class_name("card-count").get_attribute("innerHTML"))
    except (ValueError, NoSuchElementException):
        # ValueError: This happens for Legendary cards marked with * (means there is only one)
        # NoSuchElementException: This means that there is only 1 of the card
        count = 1
    cost = int(link.find_element_by_class_name("card-cost").get_attribute("innerHTML"))
    return card_name, card_dict, cost, count


def format_deck(win_or_lose_deck, collected_deck):
    """Format a given deck into a dictionary
     :param collected_deck: the deck built in get_decks function
     :param win_or_lose_deck: the name of the deck passed from feed_parser
    """
    name, class_name = win_or_lose_deck[0].rsplit(' ', 1)[0], win_or_lose_deck[0].rsplit(' ', 1)[1]
    return {'Deck': name, 'Class': class_name, 'Player Rank': win_or_lose_deck[1],
            'Deck Cost': collected_deck['Deck Cost'],
            'Average Card Cost': round(collected_deck['Total Mana Cost'] / CARDS_IN_DECK, 2),
            'Cards': collected_deck['Cards']}


def get_decks(driver, winner_deck, loser_deck, quiet):
    """use driver to get match info and parse it into the decks in the match
    :param quiet: indicates whether or not to suppress driver window popup
    :param loser_deck: name of losing deck passed from feed_parser
    :param winner_deck: name of winning deck passed from feed_parser
    :param driver: a functional driver
    :return: use sub-function to mine cards based on links, format decks and return them with added information
    """
    match_info = driver.find_elements_by_class_name("card-list")
    for deck_in_match in match_info:
        # define an empty deck to be filled and later format against winner/loser input
        deck = {'Class': 'Neutral', 'Deck Cost': 0, 'Total Mana Cost': 0, 'Cards': defaultdict(int)}
        links = deck_in_match.find_elements_by_tag_name("a")  # deck is made up of cards with links to cards

        for link in links:
            card_name, card_dict, card_cost, count = get_card(link, quiet)
            if card_name not in deck['Cards']:
                card_dict['Mana Cost'] = card_cost
                # This data isn't currently collected but will be used to build a card database at a later checkpoint
                print(card_name, card_dict, count)

            # input collected data into the empty deck
            if deck['Class'] == 'Neutral' and card_dict['Class'] != 'Neutral':
                deck['Class'] = card_dict['Class']
            deck['Deck Cost'] += (card_dict['Cost'] * count)
            deck['Total Mana Cost'] += (card_cost * count)
            deck['Cards'][card_name] += count

        # Check if class of collected deck matches winner or loser deck and format the match
        # There are two decks in each match - therefor this section will occur twice
        # one will match the class of the winning deck and one will match the class of losing one
        if deck['Class'] in winner_deck[0]:
            winning_deck = format_deck(winner_deck, deck)
        elif deck['Class'] in loser_deck[0]:
            losing_deck = format_deck(loser_deck, deck)
    return winning_deck, losing_deck


def game_parser(url, winner_deck, loser_deck, quiet=False):
    """
    :param quiet: quiet defaults to False but if set to True it will suppress chrome driver window popup
    :param winner_deck: deck name and rank passed in this slot belong to the winning deck
    :param loser_deck: deck name and rank passed in this slot belong to the losing deck
    :param url: input url to specific game replay in hs.replay database
    :return: mine deck data using the card_mine function and log deck win/loss state
    """
    driver = get_driver(url, MATCH_URL_PATTERN, quiet)
    if driver is False:
        # right now function is set to return False and not exit() so as to not disrupt main scraping function
        return False
    sleep(WAIT)  # Sleep is not required but useful when internet is unstable
    winner_deck, loser_deck = get_decks(driver, winner_deck, loser_deck, quiet)
    driver.quit()
    return winner_deck, loser_deck


def main():
    """Function used to test game_parser function"""
    game_url = 'https://hsreplay.net/replay/X4xfuTityKW6sYoDEGF2hD'
    winner_deck, loser_deck = game_parser(game_url, ('Highlander Warrior', '1'), ('Dragon Hunter', 'Legend 1000'))
    print("The Winning Deck of the match is:")
    print(winner_deck)
    print("The Losing Deck of the match is:")
    print(loser_deck)


if __name__ == '__main__':
    main()
