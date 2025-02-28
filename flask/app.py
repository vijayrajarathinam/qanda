from flask import Flask, render_template
from flask_bcrypt import bcrypt
from flask_sqlalchemy import SQLAlchemy


def create_app(script_info=None):

    # initiate app
    app = Flask(__name__, static_url_path="", static_folder="static")

    # set configuration
    app.config.from_object("config.DevelopmentConfig")

    # register blueprints
    db.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from src.blueprints.userBlueprint import user_blueprint
    from src.blueprints.authBlueprint import auth_blueprints
    from src.blueprints.questionBlueprint import question_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprints)
    app.register_blueprint(question_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app, "db": db})

    return app


db = SQLAlchemy()
bcrypt = bcrypt()

app = create_app()


@app.errorhandler(404)
def handle404(e):
    return render_template("error.html"), 404
