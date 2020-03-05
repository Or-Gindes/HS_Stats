"""This subfunction tests for internet connection using driver from main function
 and returns True for connection establised or False after multiple failed attempts"""

from time import sleep

WAIT = 5  # How long to wait between connection attempts
N_ATTEMPTS = 10  # How many connection attempts will the function make


def test_connection(driver):
    """This function uses a selenium driver to verify internet connection"""
    connection = False
    attempt = 0
    while not connection:
        try:
            attempt += 1
            driver.find_element_by_xpath('//span[@jsselect="heading" and @jsvalues=".innerHTML:msg"]')
            sleep(WAIT)
            if attempt > N_ATTEMPTS:
                return False
        except:
            return True
