from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Rater(db.Model):
    userId = db.Column(db.VARCHAR(50), primary_key=True)
    password = db.Column(db.VARCHAR(15), nullable=False)
    email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    name = db.Column(db.VARCHAR(50))
    join_date = db.Column(db.DATE, nullable=False)
    type = db.Column(db.VARCHAR(11), nullable=False, default='online')
    reputation = db.Column(db.Integer, db.CheckConstraint('reputation<6'), db.CheckConstraint('reputation>0'), default=1)

    def __init__(self, userId, password, email):
        self.userId = userId
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Rater %r>' % self.userId

    @property
    def serialize(self):
        return {
            "userId": self.userid,
            "password": self.password,
            "email": self.email,
            "name": self.name,
            "join_date": self.join_date,
            "type": self.type,
            "reputation": self.reputation
        }


class Restaurant(db.Model):
    restaurantId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50), unique=True)
    type = db.Column(db.VARCHAR(20), unique=False)
    url = db.Column(db.VARCHAR(50), unique=True)
    overallRating = db.Column(db.Integer, unique=False)
    locations = db.Column(db.Integer, ForeignKey("location.locationId"))

    def __init__(self, restaurantId, name, type, url, overallrating):
        self.restaurantId = restaurantId
        self.name = name
        self.type = type
        self.url = url
        self.overallRating = overallrating

    def __repr__(self):
        return '<Restaurant %r>' % self.name

    @property
    def serialize(self):
        return {
            'restaurantId': self.restaurantId,
            'name': self.name,
            'type': self.type,
            'url': self.url,
            'overallRating': self.overallRating
        }


class Rating(db.Model):
    userId = db.Column(db.VARCHAR(50), ForeignKey("rater.userId"), primary_key=True)
    postDate = db.Column(db.DATE, primary_key=True)
    restaurantId = db.Column(db.Integer, ForeignKey("restaurant.restaurantId"), primary_key=True)
    price = db.Column(db.Integer, db.CheckConstraint('price<6'), db.CheckConstraint('price>0'), unique=False)
    food = db.Column(db.Integer, db.CheckConstraint('food<6'), db.CheckConstraint('food>0'), unique=False)
    mood = db.Column(db.Integer, db.CheckConstraint('mood<6'), db.CheckConstraint('mood>0'), unique=False)
    staff = db.Column(db.Integer, db.CheckConstraint('staff<6'), db.CheckConstraint('staff>0'), unique=False)
    comment = db.Column(db.VARCHAR(200), unique=False)

    def __init__(self, userId, postDate, restaurantId, priceRating, foodRating, moodRating, staffRating, comment):
        self.userId = userId
        self.postDate = postDate
        self.restaurantId = restaurantId
        self.price = priceRating
        self.food = foodRating
        self.mood = moodRating
        self.staff = staffRating
        self.comment = comment

    def __repr__(self):
        return '<Rating ID: %r>' % self.userId

    @property
    def serialize(self):
        return {
            'userId': self.userId,
            'postDate': self.postDate,
            'restaurantId': self.restaurantId,
            'price': self.price,
            'food': self.food,
            'mood': self.mood,
            'staff': self.staff,
            'comment': self.comment
        }


class MenuItem(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    restaurantId = db.Column(db.Integer, ForeignKey("restaurant.restaurantId"))
    name = db.Column(db.VARCHAR(50))
    type = db.Column(db.VARCHAR(20), unique=False)
    category = db.Column(db.VARCHAR(20), unique=False)
    description = db.Column(db.VARCHAR(100))
    price = db.Column(db.Integer, db.CheckConstraint('price >= 0'), unique=False)

    def __init__(self, itemId, restaurantId, name, foodtype, category, description, price):
        self.itemId = itemId
        self.restaurantId = restaurantId
        self.name = name
        self.type = foodtype
        self.category = category
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Item Id: %r>' % self.itemId

    @property
    def serialize(self):
        return {
            'itemId': self.itemId,
            'restaurantId': self.restaurantId,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'description': self.description,
            'price': self.price
        }


class RatingItem(db.Model):
    userId = db.Column(db.CHAR(50), ForeignKey("rater.userId"), primary_key=True)
    postDate = db.Column(db.Date, primary_key=True)
    itemId = db.Column(db.Integer, ForeignKey("menu_item.itemId"))
    rating = db.Column(db.Integer, db.CheckConstraint('rating > 0'), db.CheckConstraint('rating < 6'), unique=False)
    comment = db.Column(db.CHAR(200), unique=False)

    def __init__(self, userId, postDate, itemId, rating, comment):
        self.userId = userId
        self.postDate = postDate
        self. itemId = itemId
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return '<Rating: %r>' % self.userid

    @property
    def serialize(self):
        return {
            'userId': self.userId,
            'postDate': self.postDate,
            'itemId': self.itemId,
            'rating': self.rating,
            'comment': self.comment
        }


class Location(db.Model):
    locationId = db.Column(db.Integer, primary_key=True)
    first_open_date = db.Column(db.DATE, nullable=False)
    manager_name = db.Column(db.VARCHAR(50), nullable=False)
    phone_number = db.Column(db.VARCHAR(14), nullable=False)
    street_address = db.Column(db.VARCHAR(100), nullable=False)
    weekday_open = db.Column(db.Time, unique=False)
    weekday_close = db.Column(db.Time, unique=False)
    weekend_open = db.Column(db.Time, unique=False)
    weekend_close = db.Column(db.Time, unique=False)
    restaurantId = db.Column(db.Integer, ForeignKey("restaurant.restaurantId"))

    def __init__(self, locationid, first_open_date, manager_name, phone_number, street_address,
                 weekdayOpen, weekdayClose, weekendOpen, weekendClose, restaurantId):
        self.locationId = locationid
        self.first_open_date = first_open_date
        self. manager_name = manager_name
        self.phone_number = phone_number
        self.street_address = street_address
        self.weekend_open = weekendOpen
        self.weekend_close = weekendClose
        self.weekday_open = weekdayOpen
        self.weekday_close= weekdayClose
        self.restaurantId = restaurantId

    def __repr__(self):
        return '<Location: %r>' % self.locationId

    @property
    def serialize(self):
        return {
            'locationId': self.locationId,
            'first_open_date': self.first_open_date,
            'manager_name': self.manager_name,
            'phone_number': self.phone_number,
            'street_address': self.street_address,
            'weekday_open': self.weekday_open,
            'weekday_close': self.weekday_close,
            'weekend_open': self.weekend_open,
            'weekend_close': self.weekend_close
        }
