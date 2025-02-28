from ...app import db

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=False, nullable=False)
    description = db.Column(db.Text)
    votes = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime(timezone=True, server_default=db.func.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    user = db.relationship('user', backref='question', lazy='joined')

    def __init__(self, title, description, votes, user_id):
        self.title = title
        self.description = description
        self.votes = votes
        self.user_id = user_id
