"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar

This function parses the data of a single card from the cards Hsreplay page
"""

from get_driver import get_driver
from time import sleep
from config import CARD_URL_PATTERN, VALID_DATA_LENGTH, WAIT, CARD_RELEVANT_DATA, USER, COST, COST_ALT, LATEST_SET, \
    LATEST_SET_ALT, SET, SET_DB
import pandas as pd
from sqlalchemy import create_engine
from argparse_cli import parse_args_cli


def from_database(card_name, db_params):
    """
    :param card_name: name of card requested
    :param db_params: database parameters for connection
    :return: card data from database
    """
    db_connection_str = f'mysql+pymysql://{USER}:{db_params.password}@{db_params.hostname}/{db_params.dbname}'
    engine = create_engine(db_connection_str)
    sql_query = f'SELECT * FROM Cards WHERE Card_Name = "{card_name}"'
    card = pd.read_sql_query(sql_query, engine)
    return card


def format_card(data):
    """Format the raw input scrapped from card web-page and return it as dictionary"""
    data = [item.text for item in data][0].split('\n')
    if len(data) <= VALID_DATA_LENGTH:  # indication of missing data
        print("Failed to get card data, attempting again")
        return False
    data = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
    if data[SET] == LATEST_SET_ALT:  # this is some bad data that sometimes pops up
        data[SET] = LATEST_SET
    try:
        data[COST] = int(data[COST].split()[0])
    except ValueError:
        data[COST] = 0
    except KeyError:
        data[COST] = int(data[COST_ALT].split()[0])
    finally:
        return data


def card_mine(url, card_name):
    """
    :param url: input url to specific card in hs.replay database
    :param card_name: name of the card mined in game_parser
    :return: mine card data and organise into dictionary
    """
    args = parse_args_cli()
    card = from_database(card_name, args)  # Check if card is already found in database
    if card.shape[0] == 1:  # This means the card was found in the database and scraping can be skipped
        print(f'Card data for "{card_name}" was pulled from database')
        card_info = {col: card[col][0] for col in card.columns[CARD_RELEVANT_DATA:]}
        card_info[SET] = card_info[SET_DB]
    else:  # Card was not found in the database and will be scraped
        print(f'Card data for "{card_name}" is now being webscrapped')
        driver = get_driver(url, CARD_URL_PATTERN, args.quiet)
        card_info = False
        while card_info is False:
            sleep(WAIT)
            card_info = format_card(driver.find_elements_by_xpath('//aside[@class="infobox"]/ul[2]'))
        driver.quit()  # close driver when finished
    return card_info  # return card info either way


def main():
    """test main card_mine function"""
    card_url = 'https://hsreplay.net/cards/57546/hand-of-adal'
    print(card_mine(card_url, "Hand of Ada'l"))


if __name__ == '__main__':
    main()
