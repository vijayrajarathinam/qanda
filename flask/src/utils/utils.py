import functools
from flask import request, jsonify, redirect, url_for, flash
from models import User

def autenticate(f):
    pass

def login_required(view):
    pass

def  user_level_admin(user):
    pass

def get_user(request):
    pass