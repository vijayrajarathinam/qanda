from flask import Blueprint, request, redirect, url_for, render_template, abort
from sqlalchemy import desc

from app import db
from models import Question, Answer
