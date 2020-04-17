"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar & Mariia Padalko

This subfunction tests for internet connection using driver from main function
and returns True for connection established or False after multiple failed attempts
 """

from time import sleep
from selenium.common.exceptions import NoSuchElementException
from config import WAIT, N_ATTEMPTS, NO_INTERNET_PATTERN, ERROR_MSG


def test_connection(driver, quiet):
    """
    This function uses a selenium driver to verify internet connection
    :param driver: a functional selenium driver from get_driver function
    :param quiet: the quiet parameter affects driver response when no internet is available
    :return: True for functional connection or raises a connection error
    """
    connection = False
    attempt = 0
    while not connection:
        try:
            attempt += 1
            # Try to find elements of the Chrome "Page not found" page - if successful that means no internet found
            driver.find_element_by_xpath(NO_INTERNET_PATTERN)
            print(f"{ERROR_MSG} - Making another attempt")
            sleep(WAIT)  # if no internet - wait WAIT seconds and attempt again
            if attempt > N_ATTEMPTS:
                raise ConnectionError(ERROR_MSG)
        except NoSuchElementException:
            if quiet and driver.page_source == '<html><head></head><body></body></html>':
                raise ConnectionError(ERROR_MSG)
            return True
