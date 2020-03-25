"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

This function handles all driver selenium driver related setup
given a matching url (to expected url pattern) the function returns a functional driver
"""

from selenium import webdriver, common
from check_internet import test_connection
import os
import re
from platform import system
from settings import DRIVER_WINDOWS, DRIVER_LINUX, WINDOW_SIZE, CHROME_PATH_WIN_10, CHROME_PATH_WIN_7, CHROME_PATH_LINUX


def get_driver(url, url_pattern, quiet=False):
    """ This support function validates basic scraping requirements: url, internet connection and driver functionality
    :param quiet: quiet defaults to False but if set to True it will suppress chrome driver window popup
    :param url_pattern: pattern taken from main function (main page, game replay or card)
    :param url: actual url to scrap
    :return: functional driver
    """
    try:
        # validate url is a valid card url from hs.replay fitting input url_pattern
        if not re.match(url_pattern, url):
            print("Error!\nurl does not match requested url pattern")
            raise ConnectionError("url received '%s' does not match pattern for requested data '%s'" % url, url_pattern)
        driver = open_driver(quiet)
        driver.get(url)
        # Use sub-function to verify internet connection
        if not test_connection(driver):
            raise ConnectionError("Could not establish internet connection")
    except ConnectionError as err:
        print("Error!\n" + err.args[0])
        driver = False
    finally:
        return driver


def open_driver(quiet):
    """sub-function which handles all driver related setup"""
    driver_path, chrome_path = chrome_os()
    try:
        if quiet:  # if quiet variable is True - set chrome potions to operate without window popup
            chrome_options = webdriver.chrome.options.Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
            chrome_options.binary_location = chrome_path
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        else:  # if quiet is False (which is default) the window will popup
            driver = webdriver.Chrome(executable_path=driver_path)
    except (FileNotFoundError, common.exceptions.WebDriverException) as DriverError:
        print("Error in open_driver function!\n" + DriverError.args[0])
        driver = False
    finally:
        return driver


def chrome_os():
    """sub-function which handles driver and chrome executable path assignment for different operating systems"""
    if system() == 'Windows':
        driver_name = DRIVER_WINDOWS
        if os.path.exists(CHROME_PATH_WIN_10):
            chrome_path = CHROME_PATH_WIN_10
        elif os.path.exists(CHROME_PATH_WIN_7):
            chrome_path = CHROME_PATH_WIN_7
        else:
            chrome_path = input("Chrome executable (chrome.exe) could not be located, "
                                "please provide complete path to continue:\n")
    elif system() == 'Linux' and os.path.exists(CHROME_PATH_LINUX):
        driver_name = DRIVER_LINUX
        chrome_path = CHROME_PATH_LINUX
    else:
        chrome_path = input("Chrome executable (chrome.exe) could not be located, "
                            "please provide complete path to continue:\n")
    driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), driver_name)
    return driver_path, chrome_path
