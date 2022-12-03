# NBA GAME PICKER
#### Video Demo:

<https://youtu.be/n36lJ-9PEN0>

#### Description
# General
**NBA Game Picker** web app helps you find a historical NBA game by several parameters. For instance, you can find a game by a player, team, season, and specifics (clutch, high-scoring, record-breaking performances, etc.). After finding a game, a user can jump into YouTube videos about the game or just copy the data to find the game on other recourses.

The project contains several HTML pages, one style sheet, python implementation, and a database with 4 tables.

# Navigation
User can choose one of the following ways to find a desired game: 
- by a **player**
- by a **team**
- by **historical performance** 

While searching by a player, a user can specify a few additional details. For instance, it's possible to look for an all-around game, high-scored game for a player, etc. 

Game search also has additional options. In particular, a user can search for a clutch game, game with a great ball moving, etc. Every choice reflects on actual SQL queries.

On the **Personal Records** page, a user can find a game that contains personal records of a particular player. For instance, it could be a game where Rajon Rondo set a personal assist record.

# Framework and Scope

Scope of the project is quite standard. While implementing an app, I used:
- **Python**
- **SQL**
- **HTML**
- **CSS**

For Python, I used the following libraries:
- os
- random
- cs50
- flask
- werkzeug.exceptions

Apart from a CSS stylesheet, I used a **Bootstrap** stylesheet as well.

I made a web app in accordance with the **Flask** framework.

# Overall Structure

The **Static** folder contains a css stylesheet.

The **Templates** folder contains the following HTML files:
- layout with overall app layout
- index with a main page
- player with a form to find a game by a player
- team with a form to find a game by a team
- game with results of these searchings. It contains game data and a link to YouTube. The link is dynamic and contains the game data
- records with a form to find a game by a personal player record
- game_record with result of a search by the record
- nothing that is returned if no games were found

Implementation on **Python** contains a few functions that are relevant to the main form and pages. It contains a few conditions that reflect on a user's input and find the relevant game as the result. If only one game matches the search criteria, it's the game that is displayed to a user. If there are two or more games, the game that is displayed to a user is chosen randomly.

At last, an **SQL database** contains 4 tables:
- games with main game details
- games_details with player stats for particular games
- teams with a team list
- players with a list of players

# Personal Data

The app doesn't require any kind of user's details. It doesn't need no logins or passwords. It doesn't use cookies as well.
