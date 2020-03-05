"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

import re
from check_internet import test_connection
from get_driver import get_driver

URL_PATTERN = r'https://hsreplay.net/cards'


def format_card(data):
    """Format the raw input scrapped from card webpage and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    try:
        data['Cost'] = int(data['Cost'].split()[0])
    except ValueError:
        data['Cost'] = 0
    return data


def card_mine(url):
    """
    :param url: input url to specific card in hs.replay database
    :return: mine card data and organise into dictionary
    """
    # validate url is a valid card url from hs.replay
    if not re.match(URL_PATTERN, url):
        print("Please provide a valid card URL")
        return False
    driver = get_driver()
    if driver is False:
        return False
    driver.get(url)
    # Use sub-function to verify internet connection
    try:
        if not test_connection(driver):
            raise ConnectionError
    except ConnectionError:
        print("Error!\nCould not find internet connection")
        driver.quit()
        return False
    # sleep(5)  # Sleep is not required but recommended by some user guides
    card_info = format_card(driver.find_elements_by_xpath('//aside[@class="infobox"]/ul[2]'))
    driver.quit()
    return card_info


def main():
    card_url = 'https://hsreplay.net/cards/64/swipe#tab=recommended-decks'
    # card_url = 'https://hsreplay.net/replay/XbWL7Ny5uimbE8G8P6TveS'
    # card_url = 'https://hsreplay.net/'
    print(card_mine(card_url))


if __name__ == '__main__':
    main()
