"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.options import Options
from check_internet import test_connection
import os
import re
from platform import system

WINDOW_SIZE = '1920,1080'
CHROME_PATH_WIN_10 = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROME_PATH_WIN_7 = r'C:\Program Files (x86)\Google\Application\chrome.exe'
CHROME_PATH_LINUX = r'/usr/bin/google-chrome'


def get_driver(url, url_pattern, quiet=False):
    """ This support function validates basic scraping requirements: url, internet connection and driver functionality
    :param quiet: quiet defaults to False but if set to True it will suppress chrome driver window popup
    :param url_pattern: pattern taken from main function (main page, game replay or card)
    :param url: actual url to scrap
    :return: functional driver
    """
    # validate url is a valid card url from hs.replay fitting input url_pattern
    if not re.match(url_pattern, url):
        print("Error!\nurl does not match requested url pattern")
        return False
    driver = open_driver(quiet)
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


def open_driver(quiet):
    """sub-function which handles all driver related setup"""
    driver_path, chrome_path = chrome_os()
    try:
        if not os.path.exists(driver_path):
            raise FileNotFoundError("Appropriate driver not found\nPlease verify you are using Google Chrome "
                                    "and have the version specific driver in the same folder as this program")
        if quiet:  # if quiet variable is True - set chrome potions to operate without window popup
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
            chrome_options.binary_location = chrome_path
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        else:  # if quiet is False (which is default) the window will popup
            driver = webdriver.Chrome(executable_path=driver_path)
    except FileNotFoundError as DriverError:
        print("Error!\n" + DriverError.args[0])
        return False
    except common.exceptions.WebDriverException as DriverError:
        print("Error!\n" + DriverError.args[0])
        return False
    return driver


def chrome_os():
    driver_name = 'chromedriver'
    if system() == 'Windows':
        driver_name += '.exe'
        if os.path.exists(CHROME_PATH_WIN_10):
            chrome_path = CHROME_PATH_WIN_10
        elif os.path.exists(CHROME_PATH_WIN_7):
            chrome_path = CHROME_PATH_WIN_7
        else:
            chrome_path = input("Chrome executable (chrome.exe) could not be located, "
                                "please provide complete path to continue:\n")
    elif system() == 'Linux' and os.path.exists(CHROME_PATH_LINUX):
        chrome_path = CHROME_PATH_LINUX
    else:
        chrome_path = input("Chrome executable (chrome.exe) could not be located, "
                            "please provide complete path to continue:\n")
    driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), driver_name)
    return driver_path, chrome_path
