# ITC -  Data Science and Machine Learning Cohort

## Data Mining Project by Or Gindes, Dor Sklar

### Contents 
* Requirements
* Intro
* What is the project about ?
* What questions do we want answers for ?
* Where do we go to, then ?
* Challenges
* Insights and conclusions
* Additional Sources of information


### Requirements
The project requires the following:
  * The selenium package. 
  * Google Chrome, if you aren't already using it.
  * After installing Google Chrome, install chromedriver: 
    * Firstly, check your Google Chrome version here: https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have 
    * Then, download the appropriate chromedriver.exe according to your version here: https://chromedriver.chromium.org/


### Intro 

This project is a part of the ITC Data Science and Machine Learning Cohort. 
The project revolves around Data Mining, a task that Data Scientists often have to do. 
The Data Mining technique which will be used in this project is web scraping. 
Web scraping is a Data Mining technique used to extract data from websites. 


### What is the project about ? 

This project revolves around Hearthstone. 
Hearthstone is a digital turn-based card game published in 2014 and supporting an estimated 100+ Million active players worldwide.
The game is developed and published by Blizzard Entertainment. 
Each player has a deck of 30 cards, with reducing the opponent's health points to 0 being the target. 

Each card has many attributes:
* Classes (9 in total - Warrior, Mage, Priest etc..)
* Types (Minion, Spell, Weapon etc..)
* Rarity (Common, Rare etc..)
* Crafting (buying) cost
* Playing (mana) cost
* Publishing set
* Artist


### What questions do we ask ? 

* What is the most popular class ? Is popularity influenced by streamers? 
* Is the game "Pay-To-Win" (does a more expensive deck equal greater win chance) ?
* Are newer cards (sets) more popular than older ones? (indicates power creep which affects game balance)

All of these questions are things asked by the developers in the company making and maintaining the game 
and the data gathered is used to make business and balance decisions on a daily basis.

### Where do we go to then ?

* We used the website 'http://hsreplay.net', which records an average of 700,000 matches each day and serves as a private statistical monitor of the game and holds many kinds of data.
    * We parsed the live game feed (updated about every second) to get the players' decks and match results.
    * We parsed the decks to get the card names that it consists of.
    * For each card in the players' decks, we extracted its useful info.


### Challenges 

* Compatibility with different operating systems.
* Figuring out how to extract the required data from a dynamic environment.
* Connecting and correlating separate instances of data from multiple sources.
* Inconsistencies in web-page structure in response to connection issues makes debugging difficult 
  (due to difficulties in recreating the bug) and necessitates flexible code
* Constructing multiple connected functions in an efficient way (no code reuse for example in opening a driver)

### Insights and conclusions 

* TBC

### Additional Sources of information 
 
* https://www.itc.tech/web-scraping-with-python-a-to-z/ (Web scraping blog, by Eitan Kassuto and Shai Ardazi)
* https://selenium-python.readthedocs.io/
* Cohort Fellows : ) 


