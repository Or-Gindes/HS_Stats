"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar

This function parses the data of a single card from the cards Hsreplay page
"""

from get_driver import get_driver
from time import sleep
from config import CARD_URL_PATTERN, CARD_DATA_PATTERN, MIN_VALID_DATA_LENGTH, WAIT


def format_card(data):
    """Format the raw input scrapped from card web-page and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    if len(data) <= MIN_VALID_DATA_LENGTH:  # indication of missing data
        print("Failed to get card data, attempting again")
        return False
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    try:
        data['Cost'] = int(data['Cost'].split()[0])
    except ValueError:
        data['Cost'] = 0
    except KeyError:
        data['Cost'] = int(data['GLOBAL_COST'].split()[0])
    finally:
        return data


def card_mine(url, quiet=False):
    """
    :param quiet: when set to True suppress chrome window popup
    :param url: input url to specific card in hs.replay database
    :return: mine card data and organise into dictionary
    """
    driver = get_driver(url, CARD_URL_PATTERN, quiet)
    # "driver is False" is required because "not driver" can cause unexpected behaviour when get_driver succeeds
    if driver is False:
        # right now function is set to return {} and not exit() so as to not disrupt main scraping function
        print("Failed to get data on card")
        return {}
    card_info = False
    while card_info is False:
        sleep(WAIT)
        card_info = format_card(driver.find_elements_by_xpath(CARD_DATA_PATTERN))
    driver.quit()  # close driver when finished
    return card_info


def main():
    """test main card_mine function"""
    card_url = 'https://hsreplay.net/cards/64/swipe#tab=recommended-decks'
    print(card_mine(card_url))


if __name__ == '__main__':
    main()
