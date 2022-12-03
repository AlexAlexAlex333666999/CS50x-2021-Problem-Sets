import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///nba.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/team", methods=["GET", "POST"])
def team():
    if request.method == "POST":

        # Set variables
        team = request.form.get("team")
        season = request.form.get("season")
        specific = request.form.get("specific")

        # Find games according to the specific
        if specific == 'scoring':
            pick = db.execute ("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE ((home_team_id = ? AND home_team_wins = 1) OR (visitor_team_id = ? AND home_team_wins = 0)) AND (PTS_home + PTS_away) > 240 AND season = ?", team, team, season)

        elif specific == 'ball':
            pick = db.execute ("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE ((home_team_id = ? AND home_team_wins = 1 AND AST_home >= 30) OR (visitor_team_id = ? AND home_team_wins = 0 AND AST_away >= 30)) AND season = ?", team, team, season)

        else:
            pick = db.execute ("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE ((home_team_id = ? AND home_team_wins = 1 AND (PTS_home - PTS_away) <= 3) OR (visitor_team_id = ? AND home_team_wins = 0 AND (PTS_away - PTS_home) <= 3)) AND season = ?", team, team, season)

        # Pick a game from the query
        if len(pick) == 0:
            return render_template("nothing.html")

        elif len(pick) == 1:
            game = pick
            game["home_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["CITY"]
            game["home_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["NICKNAME"]
            game["away_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["CITY"]
            game["away_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["NICKNAME"]

            return render_template("game.html", game=game)

        else:
            length = len(pick)
            i = random.randrange(0, length)
            game = pick[i]


            game["home_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["CITY"]
            game["home_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["NICKNAME"]
            game["away_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["CITY"]
            game["away_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["NICKNAME"]



            return render_template("game.html", game=game)


    else:
        # Show teams
        rows = db.execute("select DISTINCT CITY, NICKNAME, TEAM_ID from teams order by CITY ASC")
        teams = []

        for i in rows:
            teamDetails = {}

            teamDetails["CITY"] = i["CITY"]
            teamDetails["NICKNAME"] = i["NICKNAME"]
            teamDetails["TEAM_ID"] = i["TEAM_ID"]

            teams.append(teamDetails)

        # Show seasons
        years = db.execute("select distinct SEASON from games ORDER BY SEASON DESC")

        seasons = []

        for j in years:
            seasonYear = {}

            seasonYear["SEASON"] = j["SEASON"]

            seasons.append(seasonYear)

        return render_template("team.html", teams=teams, seasons=seasons)

@app.route("/player", methods=["GET", "POST"])
def player():
    if request.method == "POST":

        # Set variables
        player = request.form.get("player")
        season = request.form.get("season")
        specific = request.form.get("specific")

        # Find games according to the specific
        if specific == 'scoring':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE season = ? AND game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? AND PTS >= 40)", season, player)

        elif specific == 'assist':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE season = ? AND game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? AND AST >= 12)", season, player)

        elif specific == 'boards':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE season = ? AND game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? AND REB >= 16)", season, player)

        elif specific == 'around':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE season = ? AND game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? AND (AST + REB + STL + BLK) >= 30)", season, player)

        else:
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE season = ? AND game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? AND FG_PCT >= 0.67 AND TO <= 3)", season, player)

        # Pick a game from the query
        if len(pick) == 0:
            return render_template("nothing.html")

        elif len(pick) == 1:
            game = pick

            game["home_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["CITY"]
            game["home_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["NICKNAME"]
            game["away_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["CITY"]
            game["away_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["NICKNAME"]
            return render_template("game.html", game=game)

        else:
            length = len(pick)
            i = random.randrange(0, length)
            game = pick[i]


            game["home_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["CITY"]
            game["home_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["NICKNAME"]
            game["away_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["CITY"]
            game["away_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["NICKNAME"]

            return render_template("game.html", game=game)


    else:
        # Show seasons
        years = db.execute("select distinct SEASON from games ORDER BY SEASON DESC")

        seasons = []

        for j in years:
            seasonYear = {}

            seasonYear["SEASON"] = j["SEASON"]

            seasons.append(seasonYear)

        return render_template("player.html", seasons=seasons)

@app.route("/records", methods=["GET", "POST"])
def records():
    if request.method == "POST":
        # Set variables
        player = request.form.get("player")
        season = request.form.get("season")
        record = request.form.get("record")

        # Find games according to the record
        if record == 'Points':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? ORDER BY PTS DESC LIMIT 1)", player)

        elif record == 'Assists':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? ORDER BY AST DESC LIMIT 1)", player)

        elif record == 'Rebounds':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? ORDER BY REB DESC LIMIT 1)", player)

        elif record == 'Steals':
            pick = db.execute("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? ORDER BY STL DESC LIMIT 1)", player)

        else:
            pick = db.execute ("SELECT game_date_est, home_team_id, visitor_team_id, season FROM games WHERE game_id IN (SELECT game_ID FROM games_details WHERE player_name = ? ORDER BY BLK DESC LIMIT 1)", player)

        if len(pick) == 0:
            return render_template("nothing.html")

        game = pick[0]

        game["home_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["CITY"]
        game["home_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["HOME_TEAM_ID"])[0]["NICKNAME"]
        game["away_city"] = db.execute("SELECT city FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["CITY"]
        game["away_nickname"] = db.execute("SELECT nickname FROM teams WHERE team_id = ?", game["VISITOR_TEAM_ID"])[0]["NICKNAME"]

        return render_template("game_record.html", game=game)


    else:

        return render_template("records.html")