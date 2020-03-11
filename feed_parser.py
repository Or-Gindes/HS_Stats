# # # feed_parser


from get_driver import get_driver

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

    # Opening the browser and finding elements, extraction occurs below.
    driver = get_driver('https://hsreplay.net/', URL_PATTERN)
    elements1 = driver.find_elements_by_xpath("//a[@class='replay-feed-item']")
    elements2 = driver.find_elements_by_xpath("//figure[@class='rank-icon-standalone']/img")
    elements3 = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-left']/span")
    elements4 = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-right']/span")
    elements5 = driver.find_elements_by_xpath("//div[@class='replay-feed-player player-left']")

    """
    Extracting the required data - taking the 10 last games because of the dynamic feed. 
    """

    # getting the list of links to the game matches (game 1 link, game 2 link etc..)
    game_links = [elem.get_attribute("href") for elem in elements1[9:]]

    # player ranks (game left 1, game right 1, game left 2, game right 2...)
    player_ranks = [elem.get_attribute("alt") for elem in elements2[9:]]

    # player decks (left players)
    player_left_decks = [elem.get_attribute('innerHTML') for elem in elements3[9:]]

    # player decks (right players)
    player_right_decks = [elem.get_attribute('innerHTML') for elem in elements4[9:]]

    # finding out who won in each game.
    left_players_win_lose = []
    for elem in elements5[9:]:
        elem = elem.find_elements_by_xpath(".//img[@class='winner-icon']")
        if len(elem) > 0:
            left_players_win_lose.append(1)
        else:
            left_players_win_lose.append(0)
    driver.close()

    """
    Organizing the data for the subsequent parsing functions.
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

        # Appending each game summary to the list feed_summary
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
    The main() function, used for testing the feed_parser() function.
    :return: None
    """
    feed_summary = feed_parser()
    print(feed_summary)


if __name__ == '__main__':
    main()


