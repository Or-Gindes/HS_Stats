"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from selenium import webdriver
from selenium import common
from check_internet import test_connection
import os
import re


def get_driver(url, url_pattern):
    """ This support function validates basic scraping requirements: url, internet connection and driver functionality
    :param url_pattern: pattern taken from main function (main page, game replay or card)
    :param url: actual url to scrap
    :return: functional driver
    """
    # validate url is a valid card url from hs.replay fitting input url_pattern
    if not re.match(url_pattern, url):
        print("Error!\nurl does not match requested url pattern")
        return False
    driver = open_driver()
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
    return driver


def open_driver():
    """sub-function which handles all driver related setup"""
    driver_name = 'chromedriver'
    driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), driver_name)
    try:
        if not os.path.exists(driver_path):
            raise FileNotFoundError("Appropriate driver not found\nPlease verify you are using Google Chrome"
                                    "and have the version specific driver in the same folder as this program")
        driver = webdriver.Chrome(driver_path)
    except FileNotFoundError as DriverError:
        print("Error!\n" + DriverError.args[0])
        return False
    except common.exceptions.WebDriverException as DriverError:
        print("Error!\n" + DriverError.args[0])
        return False
    return driver
