from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Rater(db.Model):
    userid = db.Column(db.VARCHAR(50), primary_key=True)
    password = db.Column(db.VARCHAR(15), nullable=False)
    email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    name = db.Column(db.VARCHAR(50))
    join_date = db.Column(db.DATE, nullable=False)
    type = db.Column(db.VARCHAR(11), nullable=False, default='online')
    reputation = db.Column(db.Integer, default=1)
    # CheckConstraint("reputation >= 1 and reputation <= 5", name="reputationConstraint")
    # CheckConstraint("type='online' or 'blog' or 'food critic'", name="typeConstraint")

    def __init__(self, userid, password, email):
        self.userid = userid
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Rater %r>' % self.userid


class Restaurant(db.Model):
    restaurantId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50), unique=True)
    type = db.Column(db.VARCHAR(20), unique=False)
    url = db.Column(db.VARCHAR(50), unique=True)
    overallRating = db.Column(db.Integer, unique=False)
    locations = db.RelationshipProperty("Location")

    def __init__(self, restaurantId, name, type, url, overallrating):
        self.restaurantId = restaurantId
        self.name = name
        self.type = type
        self.url = url
        self.overallRating = overallrating

    def __repr__(self):
        return '<Restaurant %r>' % self.name


class Rating(db.Model):
    userId = db.Column(db.VARCHAR(50), primary_key=True)
    postDate = db.Column(db.DATE, primary_key=True)
    restaurantId = db.Column(db.Integer, primary_key=True)
    priceRating = db.Column(db.Integer, unique=False)
    foodRating = db.Column(db.Integer, unique=False)
    moodRating = db.Column(db.Integer, unique=False)
    staffRating = db.Column(db.Integer, unique=False)
    comment = db.Column(db.VARCHAR(200), unique=False)
    # CheckConstraint("1 <= priceRating <= 5", name="priceRatingConstraint")
    # CheckConstraint("1 <= foodRating <= 5", name="foodRatingConstraint")
    # CheckConstraint("1 <= moodRating <= 5", name="moodRatingConstraint")
    # CheckConstraint("1 <= staffRating <= 5", name="staffRatingConstraint")

    def __init__(self, userId, postDate, restaurantId, priceRating, foodRating, moodRating, staffRating, comment):
        self.userId = userId
        self.postDate = postDate
        self.restaurantId = restaurantId
        self.priceRating = priceRating
        self.foodRating = foodRating
        self.moodRating = moodRating
        self.staffRating = staffRating

    def __repr__(self):
        return '<Rating ID: %r>' % self.userid


class Hours(db.Model):
    hoursId = db.Column(db.Integer, primary_key=True)
    weekdayOpen = db.Column(db.Time, unique=False)
    weekdayClose = db.Column(db.Time, unique=False)
    weekendOpen = db.Column(db.Time, unique=False)
    weekendClose = db.Column(db.Time, unique=False)

    def __init__(self, hoursId, weekdayOpen, weekdayClose, weekendOpen, weekendClose):
        self.hoursId = hoursId
        self.weekdayOpen = weekdayOpen
        self.weekdayClose = weekdayClose
        self.weekendOpen = weekendOpen
        self.weekendClose = weekendClose

    def __repr__(self):
        return '<Hours ID: %r>' % self.hoursId


class MenuItem(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    restaurantId = db.Column(db.Integer, unique=False)
    name = db.Column(db.VARCHAR(50), unique=True)
    type = db.Column(db.VARCHAR(20), unique=False)
    category = db.Column(db.VARCHAR(20), unique=False)
    description = db.Column(db.VARCHAR(100), unique=True)
    price = db.Column(db.Integer, unique=False)
    # CheckConstraint("price >= 0", name="priceConstraint")

    def __init__(self, itemId, restaurantId, name, type, category, description, price):
        self.itemId = itemId
        self.restaurantId = restaurantId
        self.name = name
        self.type = type
        self.category = category
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Item Id: %r>' % self.itemId


class RatingItem(db.Model):
    userId = db.Column(db.CHAR(50), primary_key=True)
    postDate = db.Column(db.Date, primary_key=True)
    itemId = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, unique=False)
    comment = db.Column(db.CHAR(200), unique=False)
    # CheckConstraint("1 <= rating <= 5", name="ratingConstraint")

    def __init__(self, userId, postDate, itemId, rating, comment):
        self.userId = userId
        self.postDate = postDate
        self. itemId = itemId
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return '<Rating: %r>' % self.userid


class Location(db.Model):
    locationId = db.Column(db.Integer, primary_key=True)
    first_open_date = db.Column(db.DATE, nullable=False)
    manager_name = db.Column(db.VARCHAR(50), nullable=False)
    phone_number = db.Column(db.VARCHAR(14), nullable=False)
    street_address = db.Column(db.VARCHAR(100), nullable=False)
    hoursId = db.Column(db.Integer, db.ForeignKey('hours.hoursId'))
    restaurantId = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantId'))

    def __init__(self, locationId, first_open_date, manager_name, phone_number, street_address, hoursId, restaurantId):
        self.locationId = locationId
        self.first_open_date = first_open_date
        self. manager_name = manager_name
        self.phone_number = phone_number
        self.street_address = street_address
        self.hoursId = hoursId
        self.restaurantId = restaurantId

    def __repr__(self):
        return '<Location: %r>' % self.locationId
