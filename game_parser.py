"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""
from card_mine import card_mine
from get_driver import get_driver
from _collections import defaultdict
from selenium.common.exceptions import NoSuchElementException

URL_PATTERN = r'https://hsreplay.net/replay'


def get_card(link):
    """
    :param link: web-element of each card in deck
    :return: card: dictionary of card data / count: number of times a card appears in the deck
    """
    card_url = link.get_attribute("href")  # get link to card - used to with card_mine to get card info
    card_name = card_url.rsplit('/', 1)[1].title()
    card_dict = card_mine(card_url)
    try:
        count = int(link.find_element_by_class_name("card-count").get_attribute("innerHTML"))
    except NoSuchElementException:  # This means that there is only 1 of the card
        count = 1
    except ValueError:  # This happens for Legendary cards marked with * (means there is only one)
        count = 1
    cost = int(link.find_element_by_class_name("card-cost").get_attribute("innerHTML"))
    return card_name, card_dict, cost, count


def format_deck(deck, decks):
    """Format a given deck into a dictionary"""
    name, class_name = deck[0].rsplit(' ', 1)[0], deck[0].rsplit(' ', 1)[1]
    if decks[0] == class_name:
        cards = decks[len(decks) // 2 - 1]
        deck_cost = decks[1]
        deck_card_cost = decks[2]

    else:
        cards = decks[-1]
        deck_cost = decks[-3]
        deck_card_cost = decks[-2]
    return {'Deck': name, 'Class': class_name, 'Player Rank': deck[1], 'Deck Cost': deck_cost,
            'Average Card Cost': deck_card_cost / 30, 'Cards': cards}


def get_decks(driver, winner_deck, loser_deck):
    """use driver to get match info and parse it into the decks in the match
    :return: use sub-function to mine cards based on links, format decks and return them with added information
    """
    match_info = driver.find_elements_by_class_name("card-list")
    i = 0
    # define two decks per match
    decks = ['Neutral', 0, 0, defaultdict(int), 'Neutral', 0, 0, defaultdict(int)]
    for deck_in_match in match_info:  # two decks in each match
        links = deck_in_match.find_elements_by_tag_name("a")  # deck is made up of cards with links to cards
        for link in links:
            card_name, card_dict, card_cost, count = get_card(link)
            card_dict['Mana Cost'] = card_cost
            if decks[i] == 'Neutral' and card_dict['Class'] != 'Neutral':
                decks[i] = card_dict['Class']
            decks[i + 1] += (card_dict['Cost'] * count)
            print(card_name, card_dict, count)
            decks[i + 2] += card_cost
            decks[i + 3][card_name] += count
        i += len(decks) // 2
    winner_deck = format_deck(winner_deck, decks)
    loser_deck = format_deck(loser_deck, decks)
    return winner_deck, loser_deck


def game_parser(url, winner_deck, loser_deck):
    """
    :param winner_deck: deck name and rank passed in this slot belong to the winning deck
    :param loser_deck: deck name and rank passed in this slot belong to the losing deck
    :param url: input url to specific game replay in hs.replay database
    :return: mine deck data using the card_mine function and log deck win/loss state
    """
    driver = get_driver(url, URL_PATTERN)
    if driver is False:
        # right now function is set to return False and not exit() so as to not disrupt main scraping function
        return False
    # sleep(5)  # Sleep is not required but recommended by some user guides
    winner_deck, loser_deck = get_decks(driver, winner_deck, loser_deck)
    driver.quit()
    return winner_deck, loser_deck


def main():
    """Function used to test game_parser function"""
    game_url = 'https://hsreplay.net/replay/X4xfuTityKW6sYoDEGF2hD'
    winner_deck, loser_deck = game_parser(game_url, ['Highlander Warrior', '1'], ['Dragon Hunter', 'Legend 1000'])
    print("The Winning Deck of the match is:")
    print(winner_deck)
    print("The Losing Deck of the match is:")
    print(loser_deck)


if __name__ == '__main__':
    main()
