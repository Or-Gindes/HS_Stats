# # # feed_parser


from get_driver import get_driver
from time import sleep

URL_PATTERN = 'https://hsreplay.net/'


def feed_parser():

    """
    The very first parsing function in the chain, and so does not need any input.
    This function parses the live feed of 'http://hsreplay.net' to get:
        * the link to the match
        * player deck types
        * player rank
        * whoever won.
    The function returns a list, which holds up to 20 game results (it deletes games where both players use the same
    class).
    Each game result is a tuple, with the format being (url, (winner deck, winner rank), (loser deck, loser rank))
    :return: a list, as described above.
    """

    driver = get_driver('https://hsreplay.net/', URL_PATTERN)
    sleep(2)

    """
    Extracting the required data.
    """

    # getting the list of links to the game matches (game 1 link, game 2 link etc..)
    elements = driver.find_elements_by_xpath("//a[@class='replay-feed-item']")
    game_links = [elem.get_attribute("href") for elem in elements]

    # player ranks (game left 1, game right 1, game left 2, game right 2...)
    elements = driver.find_elements_by_xpath("//figure[@class='rank-icon-standalone']/img")
    player_ranks = [elem.get_attribute("alt") for elem in elements]

    # player decks (left players)
    elements = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-left']/span")
    player_left_decks = [elem.get_attribute('innerHTML') for elem in elements]

    # player decks (right players)
    elements = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-right']/span")
    player_right_decks = [elem.get_attribute('innerHTML') for elem in elements]

    # finding out who won in each game.
    elements = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-left']")
    left_players_win_lose = []
    for elem in elements:
        elem = elem.find_elements_by_xpath(".//img[@class='winner-icon']")
        if len(elem) > 0:
            left_players_win_lose.append(1)
        else:
            left_players_win_lose.append(0)

    """
    Organizing the data for the subsequent parsing functions.
    """

    # getting the ranks for the 'left players' and the 'right players'
    player_left_ranks = [rank for rank in player_ranks[::2]]
    player_right_ranks = [rank for rank in player_ranks[1::2]]

    # constructing the feed_summary which will be the returned expression.
    feed_summary = []

    for i in range(20):

        # if a match where the players use the same deck class occurs, we skip it because we can't analyze it.
        if player_left_decks[i].split()[-1] == player_right_decks[i].split()[-1]:
            continue

        # Appending each game summary to the list feed_summary
        if left_players_win_lose == 1:
            feed_summary.append((game_links[i], (player_left_decks[i], player_left_ranks[i]), (player_right_decks[i],
                                                                                               player_right_ranks[i])))
        else:
            feed_summary.append((game_links[i], (player_right_decks[i], player_right_ranks[i]),
                                 (player_left_decks[i], player_left_ranks[i])))

    driver.close()
    return feed_summary


def main():

    """
    The main() function, used for testing the feed_parser() function.
    :return: None
    """
    feed_summary = feed_parser()
    print(feed_summary)


if __name__ == '__main__':
    main()


