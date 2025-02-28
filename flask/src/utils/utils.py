import functools
from flask import request, jsonify, redirect, url_for, flash
from models import User


def autenticate(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {"status": "fail", "message": "Provide a valid auth token"}

        auth_token = request.cookies.get("Authorization")
        if not auth_token:
            return jsonify(response_object), 403
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object["message"] = resp
            return jsonify(response_object), 401
        user = User.query.filter_by(id=resp).first()
        if not user:
            return jsonify(response_object), 401
        return f(resp, *args, **kwargs)

    return decorated_function


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        auth_token = request.cookies.get("Authorization")

        if not auth_token:
            flash("Please login first")
        return view(**kwargs)

    return wrapped_view


def user_level_admin(user):
    return user and user.level >= 9999


def get_user(request):

    auth_token = request.cookies.get("Authorization")

    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            return User.query.filter_by(id=resp).first()
    return None
