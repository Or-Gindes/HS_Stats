# # # feed_parser

from selenium import webdriver
from check_internet import test_connection
from get_driver import get_driver

"""
This script parses the live feed of http://hsreplay.net, as part of the Data Mining Project. 
"""

try:
    driver = get_driver()
    driver.get(r'https://hsreplay.net/')
    # Use sub-function to verify internet connection
    if not test_connection(driver):
        raise ConnectionError
except ConnectionError:
    print("Error!\nCould not find internet connection")
    driver.quit()
    print("NO NO NO")

example_test = driver.find_elements_by_xpath("//a[@class='replay-feed-item']")
print([elem.get_attribute("href") for elem in example_test])
driver.close()
