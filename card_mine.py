"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar

This function parses the data of a single card from the cards Hsreplay page
"""

from get_driver import get_driver
from time import sleep
from config import CARD_URL_PATTERN, VALID_DATA_LENGTH, WAIT, CARD_RELEVANT_DATA
import pandas as pd
from sqlalchemy import create_engine
from argparse_cli import parse_args_cli


def from_database(card_name, database_parameters):
    db_connection_str = 'mysql+pymysql://root:%s@%s/%s' % (database_parameters['Password'],
                                                           database_parameters['Host_Name'],
                                                           database_parameters['Database_Name'])
    engine = create_engine(db_connection_str)
    card = pd.read_sql_query(r'SELECT * FROM Cards WHERE Card_Name = "%s"' % card_name, engine)
    return card


def format_card(data):
    """Format the raw input scrapped from card web-page and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    if len(data) <= VALID_DATA_LENGTH:  # indication of missing data
        print("Failed to get card data, attempting again")
        return False
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    if data['Set'] == 'GLOBAL_CARD_SET_BLACK_TEMPLE':  # this is some bad data that sometimes pops up
        data['Set'] = 'Ashes of Outland'
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
    arguments = parse_args_cli()
    database_parameters = {'Host_Name': arguments[3], 'Password': arguments[4], 'Database_Name': arguments[5]}
    card_name = url.rsplit('/', 1)[1].title()
    card = from_database(card_name, database_parameters)  # Check if card is already found in database
    if card.shape[0] == 1:  # This means the card was found in the database and scraping can be skipped
        print("Card data for '%s' was pulled from database" % card_name)
        card_info = {col: card[col][0] for col in card.columns[CARD_RELEVANT_DATA:]}
        card_info['Set'] = card_info['Card_set']
    else:  # Card was not found in the database and will be scraped
        print("Card data for '%s' is now being webscrapped" % card_name)
        driver = get_driver(url, CARD_URL_PATTERN, quiet)
        # "driver is False" is required because "not driver" can cause unexpected behaviour when get_driver succeeds
        if driver is False:
            # right now function is set to return {} and not exit() so as to not disrupt main scraping function
            print("Failed to get data on card")
            return {}
        card_info = False
        while card_info is False:
            sleep(WAIT)
            card_info = format_card(driver.find_elements_by_xpath('//aside[@class="infobox"]/ul[2]'))
        driver.quit()  # close driver when finished
    return card_info  # return card info either way


def main():
    """test main card_mine function"""
    card_url = 'https://hsreplay.net/cards/47222/zap'
    print(card_mine(card_url))


if __name__ == '__main__':
    main()
