import requests
import json
from config import STATUS_CODE_OK, INDENT, API_BASE_URL, HEADERS, QUERYSTRING


def format_response(response):
    response = response.json()
    response = json.loads(json.dumps(response, indent=INDENT))
    return response[-1]


def card_api(name):
    status_code = 0
    name = name.replace(" ", "%2520").replace("'", "%27").replace(":", "%253A").replace(",", "%252C")
    while status_code != STATUS_CODE_OK:
        response = requests.request("GET", API_BASE_URL + name, headers=HEADERS, params=QUERYSTRING)
        status_code = response.status_code
        if response.status_code != STATUS_CODE_OK:
            key = input("Could not connect to API, Please verify internet connection and press any key to continue or "
                        "'x' to exit")
            if key == 'x':
                exit()
    response = format_response(response)
    try:
        mechanics_list = [mechanic['name'] for mechanic in response['mechanics']]
    except KeyError:
        mechanics_list = ['No Mechanics']
    if response['type'] == 'Minion':
        try:
            attack, health = response['attack'], response['health']
        except KeyError:
            attack, health = 0, response['health']
    elif response['type'] == 'Weapon':
        attack, health = response['attack'], response['durability']
    else:
        attack, health = None, None
    return {'Attack': attack, 'Health': health, 'Mechanics': mechanics_list}


def main():
    """test main card_api function"""
    print(card_api('Zap!'))
    print(card_api("Hand of Gul'dan"))
    print(card_api("Big Ol' Whelp"))
    print(card_api("Shadow Word: Ruin"))
    print(card_api("Galakrond, the Unspeakable"))
    print(card_api("zilliax"))
    print(card_api("Fiery War Axe"))


if __name__ == '__main__':
    main()
