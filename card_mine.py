"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from get_driver import get_driver
from time import sleep

URL_PATTERN = r'https://hsreplay.net/cards'
DATA_PATTERN = '//aside[@class="infobox"]/ul[2]'


def format_card(data):
    """Format the raw input scrapped from card web-page and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    if len(data) <= 6:  # indication of missing data
        print("Failed to get card data, attempting again")
        return False
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    try:
        data['Cost'] = int(data['Cost'].split()[0])
    except ValueError:
        data['Cost'] = 0
    except KeyError:
        data['Cost'] = int(data['GLOBAL_COST'].split()[0])
    return data


def card_mine(url, quiet=False):
    """
    :param quiet: when set to True suppress chrome window popup
    :param url: input url to specific card in hs.replay database
    :return: mine card data and organise into dictionary
    """
    driver = get_driver(url, URL_PATTERN, quiet)
    if driver is False:
        # right now function is set to return {} and not exit() so as to not disrupt main scraping function
        print("Failed to get data on card")
        return {}
    card_info = False
    while card_info is False:
        sleep(5)
        card_info = format_card(driver.find_elements_by_xpath(DATA_PATTERN))
    driver.quit()  # close driver when finished
    return card_info


def main():
    """test main card_mine function"""
    card_url = 'https://hsreplay.net/cards/64/swipe#tab=recommended-decks'
    # card_url = 'https://hsreplay.net/replay/XbWL7Ny5uimbE8G8P6TveS'
    # card_url = 'https://hsreplay.net/'
    print(card_mine(card_url))


if __name__ == '__main__':
    main()
