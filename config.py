"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

This is a general settings file to define constants
"""

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
SET_RELEASE_DICT = {'Basic': 2014, 'Classic': 2014, 'Ashes of Outland': 2020, 'Descent of Dragons': 2019,
                   'Saviors of Uldum': 2019, 'Rise of Shadows': 2019, 'The Witchwood': 2018, 'Hall of Fame': 2014,
                   "Galakrond's Awakening": 2020, 'The Boomsday Project': 2018, "Rastakhan's Rumble": 2018,
                    'Demon Hunter Initiate': 2020}

"""Hsreplay website related constants"""
VALID_DATA_LENGTH = 6
MATCH_DATA_LENGTH = 2
PARSING_INDEX = 9

"""CLI constants"""
MIN_NUM_OF_ARG = 1

"""Database"""
DB_FILENAME = 'HS_Stats'
PASSWORD = 'root'
HOST_NAME = 'localhost'
CARD_RELEVANT_DATA = 2
SCHEME = 'Database scheme with the following tables will be created:\n'\
        '_________________          ____________________     ________________     ____________\n' \
        '\nMatches                    Decks                    Card_in_Deck         Cards\n' \
        '_________________          ____________________     ________________     _____________\n' \
        'Match_ID (PK)       ------ Deck_ID (PK) -----_      ID (PK)          --- Card_ID (PK)\n' \
        'Match_URL           | |    Deck_Name          L---- Deck_ID (FK)     |   Card_name\n' \
        'Winner_Deck_ID (FK) - |    Winner                   Card_ID (FK) ----    Class\n'\
        'Loser_Deck_ID (FK) ---     Deck_Prefix              Number_of_Copies     Type\n'\
        'Winner_Player_Rank         Class                                         Rarity\n'\
        'Loser_Player_Rank          Deck_Cost                                     Card_set\n'\
        '                           Average_Card_Cost                             Release_Year\n'\
        '                           Most_Common_Set                               Cost\n'\
        '                           Most_Common_Type                              Artist\n'\
        '                           Number_of_Unique_Cards                        Mana_Cost\n'

"""API"""
STATUS_CODE_OK = 200
INDENT = 2
API_BASE_URL = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/"

HEADERS = {
    'x-rapidapi-host': "omgvamp-hearthstone-v1.p.rapidapi.com",
    'x-rapidapi-key': "effab6f2dbmsh791ad27a10929b1p1b1066jsn41b50b0da5b1"  # TODO: This needs to replaced with key provided by user
} # TODO: let's create some account for a user

QUERYSTRING = {"collectible": "1"}

# "effab6f2dbmsh791ad27a10929b1p1b1066jsn41b50b0da5b1" - Mariia's api-key