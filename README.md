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
* The project requires the following:
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
Hearthstone is a digital turn-based card game developed and released by Blizzard Entertainment. 
Each player has a deck of 30 cards, with reducing the opponent's health points to 0 being the target. 

Each card has many attributes:
* Classes (9 in total - Warrior, Mage, Priest etc..)
* Types (Minion, Spell, Weapon etc..)
* Rarity (Common, Rare etc..)
* Cost


### What questions do we ask  ? 

* What is the most commonly used class ? 
* TBC

### Where do we go to then ?

* We used the website 'http://hsreplay.net', which serves as a statistical monitor of the game and holds many kinds of data.
    * We parsed the live game feed (updated about every second) to get the players' decks.
    * We parsed the decks to get the card names that it consists of.
    * For each card in the players' decks, we extracted its useful info.


### Challenges 

* Reproducibility in different operating systems.
* Figuring out how to extract the required data from a dynamic environment.
* Scraping data from a match where both sides have the same class.

### Insights and conclusions 

* TBC

### Additional Sources of information 
 
* https://www.itc.tech/web-scraping-with-python-a-to-z/ (Web scraping blog, by Eitan Kassuto and Shai Ardazi)
* https://selenium-python.readthedocs.io/
* Cohort Fellows : ) 


