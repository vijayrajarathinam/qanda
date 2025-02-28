from flask import Blueprint, request, redirect, url_for, render_template, abort
from sqlalchemy import desc

from app import db
from models import Question, Answer
from utils import login_required, get_user

question_blueprint = Blueprint("question", __name__, template_folder="./templates")


@question_blueprint.route("/feed", methods=["GET"])
def feed():
    questions = Question.query.order_by(desc(Question.id)).all()
    return render_template("feed.html", questions=questions)


@question_blueprint.route("/questions/<question_id>", methods=["GET"])
def get_single_question(question_id):
    user = get_user(request)
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        abort(404)

    answers = Answer.query.filter_by(question_id=question_id).all()
    return render_template(
        "question.html", question=question, answers=answers, user=user
    )


@question_blueprint.route("/questions/<int:question_id>/reply", methods=["POST"])
@login_required
def reply(question_id):
    question = Question.query.filter_by(id=question_id).first()
    user = get_user(request)
    if user and question:
        content = request.form.get("response")
        new_answer = Answer(content, question.id, user.id)
        db.session.add(new_answer)
        db.session.commit()

    return get_single_question(question_id)


@question_blueprint.route("/questions/new", methods=["GET", "POST"])
@login_required
def new_question():
    user = get_user(request)
    if user and request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        new_question = Question(title, description, 0, user.id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("question.feed"))

    return render_template("question_new.html", user=user)
