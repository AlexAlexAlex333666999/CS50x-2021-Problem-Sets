import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT symbol, shares FROM stocks WHERE user_id = ?", session["user_id"])

    stocks = []

    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    user_total = balance

    # Fill the details for separate symbols, re-count a user's total
    for i in rows:
        stockDetails = {}
        quote = lookup(i["symbol"])

        stockDetails["symbol"] = i["symbol"]
        stockDetails["name"] = quote["name"]
        stockDetails["shares"] = i["shares"]
        stockDetails["price"] = quote["price"]
        stockDetails["total"] = i["shares"] * quote["price"]

        user_total += stockDetails["total"]

        stocks.append(stockDetails)

    return render_template("index.html", balance=balance, stocks=stocks, total=user_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Ensure that symbol and shares were submitted
        if not request.form.get("symbol"):
            return apology("please provide symbol", 400)

        elif not request.form.get("shares"):
            return apology("please provide number of shares", 400)

        # Set variables
        symbol = request.form.get("symbol")
        shares = float(request.form.get("shares"))
        quote = lookup(symbol)

        # Check that a symbol exists
        if quote == None:
            return apology("sorry, we couldn't find the stock", 400)

        shares_cost = shares * quote["price"]
        user_total = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]

        # Check if user has enough money
        if shares_cost > user_total["cash"]:
            return apology("sorry, not enough money", 400)

        # Update user's balance
        user_total["cash"] = user_total["cash"] - shares_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_total["cash"], session["user_id"])

        # Add info of buying
        rows = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        if len(rows) == 1:
            db.execute("UPDATE stocks SET shares = ? WHERE id = ?", rows[0]["shares"] + shares, rows[0]["id"])
        else:
            db.execute("INSERT INTO stocks (user_id, symbol, shares) VALUES(?, ?, ?)", session["user_id"], symbol, shares)

        db.execute("INSERT INTO history (action, user_id, symbol, shares, price) VALUES('Bought', ?, ?, ?, ?)", session["user_id"],
                   symbol, shares, shares_cost)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])

    history = []

    # Fill the details for separate actions
    for i in rows:
        stockDetails = {}

        stockDetails["action"] = i["action"]
        stockDetails["symbol"] = i["symbol"]
        stockDetails["shares"] = i["shares"]
        stockDetails["price"] = i["price"]
        stockDetails["transacted"] = i["transacted"]

        history.append(stockDetails)

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("please provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("please provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        quote = lookup(symbol)

        if quote == None:
            return apology("sorry, we couldn't find the stock", 400)
        else:
            return render_template("quote2.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("please provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("please provide password", 400)

         # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("please provide password confirmation", 400)

        # Ensure that a user isn't registered yet
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) >= 1:
            return apology("invalid username and/or password", 400)

        # Set variables for user entries
        username = request.form.get("username")
        password = request.form.get("password")
        passwordconfirm = request.form.get("confirmation")

        if len(password) < 8:
            return apology("please type at least 8 symbols into password", 400)

        # Check that password and password confirmations are the same
        if password != passwordconfirm:
            return apology("please match password with password confirmation", 400)

        else:
            # Hash passwords
            password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Put user details into a database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

        # Redirects a user to a homepage
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        # Set variables
        symbol = request.form.get("symbol")
        shares = float(request.form.get("shares"))

        # Check if a user has enough shares
        user_symbol = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        if len(user_symbol) == 0:
            return apology("seems like you don't have the symbol", 400)

        user_shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?",
                                 session["user_id"], symbol)[0]["shares"]

        if user_shares < shares:
            return apology("unfortunately, you don't have enough shares", 400)

    # Update user's balance
        quote = lookup(symbol)

        # Check that a symbol exists
        if quote == None:
            return apology("sorry, we couldn't find the stock", 403)

        shares_cost = shares * quote["price"]
        user_total = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        user_total = user_total + shares_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_total, session["user_id"])

        # Add info of selling
        rows = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        db.execute("UPDATE stocks SET shares = ? WHERE id = ?", rows[0]["shares"] - shares, rows[0]["id"])

        db.execute("INSERT INTO history (action, user_id, symbol, shares, price) VALUES('Sold', ?, ?, ?, ?)",
                   session["user_id"], symbol, shares, shares_cost)

        return redirect("/")

    else:
        rows = db.execute("SELECT symbol FROM stocks WHERE user_id = ?", session["user_id"])

        stocks = []

        for i in rows:
            stockSymbol = {}

            stockSymbol["symbol"] = i["symbol"]

            stocks.append(stockSymbol)

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
