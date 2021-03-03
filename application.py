import os

from cs50 import SQL
from flask import (
    Flask, abort, flash, jsonify, redirect, render_template, request, session,
    url_for,
)
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
if os.environ.get("FLASK_ENV") == "development":
    app.config["SESSION_FILE_DIR"] = "tmp"
else:
    app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

db = SQL("sqlite:///game_stats.db")


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            """SELECT
                *
            FROM
                "user"
            WHERE
                username = :username
            """,
            username = request.form.get("username"),
        )

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[0]["pw_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["user_id"]

        return redirect(url_for("home"))

    else:
        return render_template("login.html")


@app.route("/add_char", methods=["GET", "POST"])
@login_required
def add_char():

    if request.method == "POST":

            db.execute("""INSERT INTO
                characters (
                    user_id, name, alignment_lc, alignment_ge,
                    race, cha_class, level, strength, dexterity, constitution,
                    intelligence, wisdom, charisma, honour, status, height, weight,
                    handedness, eye_colour, hair_colour, sex, age, acrobatics,
                    anatomy, animal_lore, appraisal, arcana, blacksmithing, botany_forestry,
                    common, culture, dancing, dwarven, elvish, engineering, agriculture,
                    first_aid, gnomish, halfling, history, jeweler, leather_working, manual_labour,
                    masonry, mathematics, metal_working, musical_ability, observation,
                    religion, sailing, sleight, sneak, social_interaction, tailoring,
                    tracking, upkeep_maintenance, woodworking, experience, commerce
                ) VALUES (
                    :user_id, :name, :alignment_lc, :alignment_ge,
                    :race, :cha_class, :level, :strength, :dexterity, :constitution,
                    :intelligence, :wisdom, :charisma, :honour, :status, :height, :weight,
                    :handedness, :eye_colour, :hair_colour, :sex, :age, :acrobatics,
                    :anatomy, :animal_lore, :appraisal, :arcana, :blacksmithing, :botany_forestry,
                    :common, :culture, :dancing, :dwarven, :elvish, :engineering, :agriculture,
                    :first_aid, :gnomish, :halfling, :history, :jeweler, :leather_working, :manual_labour,
                    :masonry, :mathematics, :metal_working, :musical_ability, :observation,
                    :religion, :sailing, :sleight, :sneak, :social_interaction, :tailoring,
                    :tracking, :upkeep_maintenance, :woodworking, :experience, :commerce
                )
                """,
                user_id = session["user_id"],
                name = request.form.get("name"),
                alignment_lc = request.form.get("alignment_lc"),
                alignment_ge = request.form.get("alignment_ge"),
                race = request.form.get("race"),
                cha_class = request.form.get("cha_class"),
                level = request.form.get("level"),
                strength = request.form.get("strength"),
                dexterity = request.form.get("dexterity"),
                constitution = request.form.get("constitution"),
                intelligence = request.form.get("intelligence"),
                wisdom = request.form.get("wisdom"),
                charisma = request.form.get("charisma"),
                honour = request.form.get("honour"),
                status = request.form.get("status"),
                height = request.form.get("height"),
                weight = request.form.get("weight"),
                handedness = request.form.get("handedness"),
                eye_colour = request.form.get("eye_colour"),
                hair_colour = request.form.get("hair_colour"),
                sex = request.form.get("sex"),
                age = request.form.get("age"),
                acrobatics = request.form.get("acrobatics"),
                anatomy = request.form.get("anatomy"),
                animal_lore = request.form.get("animal_lore"),
                appraisal = request.form.get("appraisal"),
                arcana = request.form.get("arcana"),
                blacksmithing = request.form.get("blacksmithing"),
                botany_forestry = request.form.get("botany_forestry"),
                common = request.form.get("common"),
                culture = request.form.get("culture"),
                dancing = request.form.get("dancing"),
                dwarven = request.form.get("dwarven"),
                elvish = request.form.get("elvish"),
                engineering = request.form.get("engineering"),
                agriculture = request.form.get("agriculture"),
                first_aid = request.form.get("first_aid"),
                gnomish = request.form.get("gnomish"),
                halfling = request.form.get("halfling"),
                history = request.form.get("history"),
                jeweler = request.form.get("jeweler"),
                leather_working = request.form.get("leather_working"),
                manual_labour = request.form.get("manual_labour"),
                masonry = request.form.get("masonry"),
                mathematics = request.form.get("mathematics"),
                metal_working = request.form.get("metal_working"),
                musical_ability = request.form.get("musical_ability"),
                observation = request.form.get("observation"),
                religion = request.form.get("religion"),
                sailing = request.form.get("sailing"),
                sleight = request.form.get("sleight"),
                sneak = request.form.get("sneak"),
                social_interaction = request.form.get("social_interaction"),
                tailoring = request.form.get("tailoring"),
                tracking = request.form.get("tracking"),
                upkeep_maintenance = request.form.get("upkeep_maintenance"),
                woodworking = request.form.get("woodworking"),
                experience = request.form.get("experience"),
                commerce = request.form.get("commerce"),
            )

            return redirect(url_for("home"))

    else:
        return render_template("add_char.html")


@app.route("/view_chars")
@login_required
def view_chars():
    characters = db.execute(
        """SELECT
            characters.id,
            characters.name,
            characters.race,
            characters.cha_class,
            characters.level,
            characters.status,
            user.username
        FROM
            characters
        INNER JOIN
            user ON user.user_id = characters.user_id
        WHERE
            characters.user_id = :user_id
        """,
        user_id=session["user_id"],
    )

    if not characters:
        return redirect(url_for("add_char"))

    return render_template("view_chars.html", characters=characters)


@app.route("/<int:character_id>")
@login_required
def character_sheet(character_id):

    characters = db.execute(
        """SELECT
            *
        FROM
            characters
        WHERE
            id = :id AND
            user_id = :user_id
        """,
        id = character_id,
        user_id = session ["user_id"],
    )

    if not characters:
        return abort(404)

    return render_template("character_sheet.html", character=characters[0])


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Please confirm you password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and password confirmation must match", 400)

        # Add username and hashed password to the database
        try:
            result = db.execute(
                """
                INSERT INTO
                    "user" (username, pw_hash)
                VALUES
                    (:username, :pw_hash)
                """,
                username=request.form.get("username"),
                pw_hash=generate_password_hash(request.form.get("password")),
            )
        except ValueError as e:
            # Ensure username is not already in database
            return apology("username already exists", 400)

        # Remember which user has logged in
        print(f"register: {result}")
        if result:
            session["user_id"] = result

        return redirect(url_for("home"))

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run()
