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


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    type = db.Column(db.String(), unique=False)
    url = db.Column(db.String(), unique=True)
    rating = db.Column(db.Integer, unique=False)

    def __init__(self, name, type, url, rating):
        self.name = name
        self.type = type
        self.url = url
        self.rating = rating

    def __repr__(self):
        return '<Restaurant %r>' % self.name


class Rating(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    postdate = db.Column(db.String(), primary_key=True)
    restaurantId = db.Column(db.Integer, primary_key=True)
    pricerating = db.Column(db.Integer, unique=False)
    foodrating = db.Column(db.Integer, unique=False)
    moodrating = db.Column(db.Integer, unique=False)
    staffrating = db.Column(db.Integer, unique=False)
    comment = db.Column(db.String(), unique=False)

    def __init__(self, userid, postdate, restaurantId, pricerating, foodrating, moodrating, staffrating, comment):
        self.userid = userid
        self.postdate = postdate
        self.restaurantId = restaurantId
        self.pricerating = pricerating
        self.foodrating = foodrating
        self.moodrating = moodrating
        self.staffrating = staffrating

    def __repr__(self):
        return '<Rating: %r>' % self.userid