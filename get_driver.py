"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar
"""

from selenium import webdriver
from selenium import common
from platform import system
import os


def get_driver():
    """This sub-function will varify existence """
    if system() == 'Windows':
        suffix = '\\chromedriver.exe'
    else:
        suffix = '/chromedriver'
    driver_path = os.path.dirname(os.path.realpath(__file__)) + suffix
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
