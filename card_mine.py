"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from get_driver import get_driver

URL_PATTERN = r'https://hsreplay.net/cards'
DATA_PATTERN = '//aside[@class="infobox"]/ul[2]'


def format_card(data):
    """Format the raw input scrapped from card web-page and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    try:
        data['Cost'] = int(data['Cost'].split()[0])
    except ValueError:
        data['Cost'] = 0
    except KeyError:
        data['Cost'] = int(data['GLOBAL_COST'].split()[0])
    return data


def card_mine(url):
    """
    :param url: input url to specific card in hs.replay database
    :return: mine card data and organise into dictionary
    """
    driver = get_driver(url, URL_PATTERN)
    if driver is False:
        # right now function is set to return False and not exit() so as to not disrupt main scraping function
        return False
    # sleep(5)  # Sleep is not required but recommended by some user guides
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
