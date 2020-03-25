"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar

This subfunction tests for internet connection using driver from main function
and returns True for connection established or False after multiple failed attempts
 """

from time import sleep
from selenium.common.exceptions import NoSuchElementException
from settings import WAIT, N_ATTEMPTS, NO_INTERNET_PATTERN


def test_connection(driver):
    """This function uses a selenium driver to verify internet connection"""
    connection = False
    attempt = 0
    while not connection:
        try:
            attempt += 1
            # Try to find elements of the Chrome "Page not found" page - if successful that means no internet found
            driver.find_element_by_xpath(NO_INTERNET_PATTERN)
            sleep(WAIT)  # if no internet - wait WAIT seconds and attempt again
            if attempt > N_ATTEMPTS:
                return False
        except NoSuchElementException:
            return True
