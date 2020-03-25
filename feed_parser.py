"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

This function parses the live feed of Hsreplay website for HearthStone matches
and returns links to match as well as match data found only in the feed
"""

from get_driver import get_driver
from settings import FEED_URL_PATTERN, PARSING_INDEX


def feed_parser():

    """
    The very first parsing function in the chain, and so does not need any input.
    This function parses the live feed of 'http://hsreplay.net', and extracts the following data:
        * the link to the match
        * player rank
        * player deck types
        * whoever won (a list of 0's and 1's, signifying if the 'left' player had won or lost.
    The data are stored in a dictionary, which will be used for feed_matches() function.
    :return: a dictionary with the following keys:
             * game_links.
             * player_ranks
             * player_left_decks
             * player_right_decks
             * left_player_win_lose
    """

    # Opening the browser
    driver = get_driver('https://hsreplay.net/', FEED_URL_PATTERN)

    # Finding all of the needed elements in the page.
    link_elements = driver.find_elements_by_xpath("//a[@class='replay-feed-item']")
    rank_elements = driver.find_elements_by_xpath("//figure[@class='rank-icon-standalone']/img")
    left_deck_elements = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-left']/span")
    right_deck_elements = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-right']/span")
    left_win_indicator_elements = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-left']")

    # getting the list of links to the game matches (game 1 link, game 2 link etc..)
    game_links = [elem.get_attribute("href") for elem in link_elements[PARSING_INDEX:]]

    # player ranks (game left 1, game right 1, game left 2, game right 2...)
    player_ranks = [elem.get_attribute("alt") for elem in rank_elements[PARSING_INDEX:]]

    # player decks (left players)
    player_left_decks = [elem.get_attribute('innerHTML') for elem in left_deck_elements[PARSING_INDEX:]]

    # player decks (right players)
    player_right_decks = [elem.get_attribute('innerHTML') for elem in right_deck_elements[PARSING_INDEX:]]

    # finding out who won in each game.
    left_players_win_lose = []
    for elem in left_win_indicator_elements[PARSING_INDEX:]:
        elem = elem.find_elements_by_xpath(".//img[@class='winner-icon']")
        if len(elem) > 0:
            left_players_win_lose.append(1)
        else:
            left_players_win_lose.append(0)
    driver.close()

    # organizing the data to a dictionary.
    feed_dict = {'game_links': game_links, 'player_ranks': player_ranks, 'player_left_decks': player_left_decks,
                 'player_right_decks': player_right_decks, 'left_players_win_lose': left_players_win_lose}
    return feed_dict


def feed_matches(game_links, player_ranks, player_left_decks, player_right_decks, left_players_win_lose):

    """
    This function gets the extracted elements given from the feed_parser() function dictionary.
    The function returns a list of tuples.
    Each tuple is a game result, with the format being (url, (winner deck, winner rank), (loser deck, loser rank))
    :param game_links: a list of links to the games.
    :param player_ranks: a list of the player ranks
    :param player_left_decks: a list of the decks that belong to the 'left' players.
    :param player_right_decks: a list of the decks that belong to the 'right' players.
    :param left_players_win_lose: a list of 0's and 1's that describe whether the left player has won or lost.
    :return: a list of tuples, as described above.
    """

    # getting the ranks for the 'left players' and the 'right players'
    player_left_ranks = [rank for rank in player_ranks[::2]]
    player_right_ranks = [rank for rank in player_ranks[1::2]]

    # constructing the feed_summary which will be the returned expression.
    feed_summary = []

    for i in range(10):

        # if a match where the players use the same deck class occurs, we skip it because we can't analyze it.
        if player_left_decks[i].split()[-1] == player_right_decks[i].split()[-1]:
            continue

        # Appending each game summary to the list feed_summary (1 means the left player won, 0 means the right did).
        if left_players_win_lose[i] == 1:
            feed_summary.append(
                (game_links[i], (player_left_decks[i], player_left_ranks[i]), (player_right_decks[i],
                                                                               player_right_ranks[i])))
        else:
            feed_summary.append((game_links[i], (player_right_decks[i], player_right_ranks[i]),
                                 (player_left_decks[i], player_left_ranks[i])))

    return feed_summary


def main():

    """
    The main() function, used for testing the feed_parser() and feed_matches() function.
    :return: None
    """

    results = feed_parser()
    print(results)
    feed_summary = feed_matches(results['game_links'], results['player_ranks'], results['player_left_decks'],
                                results['player_right_decks'], results['left_players_win_lose'])
    print(feed_summary)


if __name__ == '__main__':
    main()


