from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    make_response,
    render_template,
    flash,
)
from models import User
from ...app import db, bcrypt
from sqlalchemy import exc, or_
from utils import get_user

auth_blueprints = Blueprint("auth", __name__)


@auth_blueprints("/auth/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = User.query.filter(
                or_(User.username == username, User.email == email)
            ).first()
            if not user:
                new_user = User(
                    username=username,
                    email=email,
                    password=password,
                    firstname=firstname,
                    lastname=lastname,
                )
                db.session.add(new_user)
                db.session.commit()
                auth_token = new_user.encode_auth_token(new_user.id)
                if auth_token:
                    response = make_response(redirect(url_for("questions.feed")))
                    response.set_cookie("Authorization", auth_token, httponly=True)
                    return response
                return "Sorry there was an error creating a new user"
            else:
                return "Sorry, username already exist"
        except (exc.IntegrityError, ValueError) as e:
            db.session.rollback()
            return "Signup failed", 400

    return render_template("signup.html")


@auth_blueprints.route("/auth/login", methods=["get"])
def login():
    next = request.args.get("next")
    return render_template("login.html", next=next)


@auth_blueprints.route("/auth/login", methods=["POST"])
def signin():
    email = request.form.get("email")
    password = request.form.get("password")
    next = request.args.get("next")
    try:
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                if next:
                    response = make_response(redirect(next))
                else:
                    response = make_response(redirect(url_for("questions.feed")))
                response.set_cookie("Authorization", auth_token, httponly=True)
                return response
    except Exception as e:
        print(e)

    flash("Login Failed")

    return render_template("login.html", next=next)


@auth_blueprints.route("/auth/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for("auth.login")))
    response.set_cookie("Authorization", expires=0)
    return response


@auth_blueprints.route("/auth/status", methods=["GET"])
def status():
    user = get_user(request)
    if user:
        return str(user.id)

    return "Please provide a valid token", 401
