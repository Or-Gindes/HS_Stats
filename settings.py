"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar

This is a general settings file to define constants
"""

"""HS_Stats.py Constants - To be replaced by CLI argument parsing for checkpoint #2"""
INFINITE = False  # Set to True for indefinite value collection
N_ITERATIONS = 1  # Only relevant when INFINITE is set to False - determine number of scraping iterations
QUIET = False  # if not provided - defaults to False. When set to True - suppress driver window popup

"""Internet related Constants"""
WAIT = 5  # How long to wait between connection attempts
N_ATTEMPTS = 10  # How many connection attempts will the function make
NO_INTERNET_PATTERN = '//span[@jsselect="heading" and @jsvalues=".innerHTML:msg"]'
DRIVER_LINUX = 'chromedriver'
DRIVER_WINDOWS = 'chromedriver.exe'
WINDOW_SIZE = '1920,1080'
CHROME_PATH_WIN_10 = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROME_PATH_WIN_7 = r'C:\Program Files (x86)\Google\Application\chrome.exe'
CHROME_PATH_LINUX = r'/usr/bin/google-chrome'

"""URL Constants"""
FEED_URL_PATTERN = r'https://hsreplay.net/'
MATCH_URL_PATTERN = r'https://hsreplay.net/replay'
CARD_URL_PATTERN = r'https://hsreplay.net/cards'

"""Heartstone related constants"""
CARDS_IN_DECK = 30

"""Hsreplay website related constants"""
CARD_DATA_PATTERN = '//aside[@class="infobox"]/ul[2]'
MIN_VALID_DATA_LENGTH = 6
PARSING_INDEX = 9
