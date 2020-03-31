"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from get_driver import get_driver
from time import sleep
import pandas as pd
from sqlalchemy import create_engine

# TODO: Move these constants to the config file
RELEVANT_DATA = 2
URL_PATTERN = r'https://hsreplay.net/cards'
DATA_PATTERN = '//aside[@class="infobox"]/ul[2]'
DB_FILENAME = 'HS_Stats'
PASSWORD = 'shiralaro123'


def format_card(data):
    """Format the raw input scrapped from card web-page and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    if len(data) <= 6:  # indication of missing data
        print("Failed to get card data, attempting again")
        return False
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    if data['Set'] == 'GLOBAL_CARD_SET_BLACK_TEMPLE':
        data['Set'] = 'Ashes of Outland'
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
    card_name = url.rsplit('/', 1)[1].title()
    db_connection_str = 'mysql+pymysql://root:%s@localhost/%s' % (PASSWORD, DB_FILENAME)
    engine = create_engine(db_connection_str)
    df = pd.read_sql_query(r'SELECT * FROM Cards WHERE Card_Name = "%s"' % card_name, engine)
    if df.shape[0] == 1:  # This means the card was found in the database scraping can be skipped
        print("Card %s was pulled from database" % card_name)
        card_info = {col: df[col][0] for col in df.columns[RELEVANT_DATA:]}
        card_info['Set'] = card_info['Card_set']
    else:  # Card was not found in the database and will be scraped
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
    return card_info  # return card info either way


def main():
    """test main card_mine function"""
    card_url = 'https://hsreplay.net/cards/47222/zap'
    print(card_mine(card_url))


if __name__ == '__main__':
    main()
