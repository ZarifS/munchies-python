from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rater(db.Model):
    userid = db.Column(db.VARCHAR(50), primary_key=True)
    password = db.Column(db.VARCHAR(15), nullable=False)
    email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    name = db.Column(db.VARCHAR(50))
    join_date = db.Column(db.DATE, nullable=False)
    type = db.Column(db.VARCHAR(11), nullable=False, default='online')
    reputation = db.Column(db.Integer, default=1)

    def __init__(self, userid, password, email):
        self.userid = userid
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Rater %r>' % self.userid



