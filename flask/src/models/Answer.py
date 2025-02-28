from ...app import db

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", backref='answer', lazy="joined")

    def __init__(self, content, question_id, user_id):
        self.content = content
        self.question_id = question_id
        self.user_id = user_id
