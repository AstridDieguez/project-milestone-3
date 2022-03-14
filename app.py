import os
import random
import secrets
import json
from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from dotenv import find_dotenv, load_dotenv
from tmdb import getMovieInfo, getMovieSearch
from models import db, Users, Comments

load_dotenv(find_dotenv())

movie_IDs = [514754, 568124, 19995, 10681, 508439, 532953, 13]
# Bao, Encanto, Avatar, Wall-E, Onward, Purl, Forrest Gump

app = Flask(__name__)
secret_key = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL_SQL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("/login")

with app.app_context():
    db.create_all()

bp = Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

@bp.route("/react", methods=["POST", "GET"])
def react():
    user = current_user
    noSearch = False
    noRating = False
    madeComment = False
    movieID = None
    if(request.method == "POST"):
        if "comment+rating" in request.form:
            print("test 1")
            userID = user.get_id()
            movieID = request.form.get("movieID")
            comment = Comments.getComment(userID, movieID)
            if not comment:
                print("test 2")
                ratings = ["1", "2", "3", "4", "5"]
                comment = request.form.get("comment")
                rating = request.form.get("rating")
                if(rating not in ratings):
                    print("test 3")
                    noRating = True
                else:
                    Comments.addComment(userID, movieID, comment, rating)
            else:
                madeComment = True
        else:
            movieName = request.form.get("query")
            if not movieName == "":
                movieID = getMovieSearch(movieName)
                if movieID == None:
                    noSearch = True
    
    if movieID == None:
        movieID = random.choice(movie_IDs)

    movieInfo = getMovieInfo(movieID)
    movieComments = Comments.getMovieComments_list(movieID)
    data = json.dumps(
        {
        "user": user.to_dict(),
        "noSearch": noSearch,
        "noRating": noRating,
        "madeComment": madeComment,
        "movieID": movieID,
        "title": movieInfo['movie_title'],
        "tagline": movieInfo['movie_tagline'],
        "genres": movieInfo['movie_genres'],
        "poster_path": movieInfo['image_url'],
        "wiki_url": movieInfo['wiki_url'],
        "movieComments": movieComments
        }
    )

    return render_template("index.html", data=data)

@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("userID")
        print("You entered: " + username)
        exists = Users.userExists(username)
        if exists:
            user = Users.getUser(username)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect("/home")
        else:
            return render_template("login.html", exists=exists)
    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect("/login")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        exists = Users.userExists(username)
        if exists:
            return render_template("signup.html", exists=exists)
        else:
            Users.addUser(username)
            return redirect("/login")
    return render_template("signup.html")

@app.route("/home", methods=["POST", "GET"])
@login_required
def home():
    return redirect("/react")
    user = current_user
    noSearch = False
    noRating = False
    madeComment = False
    movieID = None
    if(request.method == "POST"):
        if "comment+rating" in request.form:
            userID = user.get_id()
            movieID = request.form.get("movieID")
            comment = Comments.getComment(userID, movieID)
            if not comment:
                ratings = ["1", "2", "3", "4", "5"]
                comment = request.form.get("comment")
                rating = request.form.get("rating")
                if(rating not in ratings):
                    noRating = True
                else:
                    Comments.addComment(userID, movieID, comment, rating)
            else:
                madeComment = True
        else:
            movieName = request.form.get("query")
            if not movieName == "":
                movieID = getMovieSearch(movieName)
                if movieID == None:
                    noSearch = True
    
    if movieID == None:
        movieID = random.choice(movie_IDs)

    movieInfo = getMovieInfo(movieID)
    movieComments = Comments.getMovieComments(movieID)
    return render_template(
        "home.html",
        user=user,
        noSearch=noSearch,
        noRating=noRating,
        madeComment=madeComment,
        movieID = movieID,
        title=movieInfo['movie_title'],
        tagline=movieInfo['movie_tagline'],
        genres=movieInfo['movie_genres'],
        poster_path=movieInfo['image_url'],
        wiki_url=movieInfo['wiki_url'],
        movieComments=movieComments
    )

app.register_blueprint(bp)

app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)