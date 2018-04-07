from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, abort
from flask_cors import CORS
from models import *
from dbFiller import *

# Init app
app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Zarif:postgres@localhost:5432/munchies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# db.create_all()
# To populate table, run each populate command one at a time.
# populateRestaurantTable(db)
# populateMenuTable(db)
# populateRaterTable(db)
# populateRatingTable(db)
# populateMenuItemRatingTable(db)


# Home
@app.route('/')
def index():
    return render_template('index.html')


# Get all the restos
@app.route('/restaurants', methods=['GET'])
def getAllRestaurants():
    restaurants = Restaurant.query.all()
    if restaurants is None:
        abort(404)
    return jsonify(items=[i.serialize for i in restaurants])


# Get resto by key
@app.route('/restaurantById/<id>', methods=['GET'])
def getRestaurantByID(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return abort(404)
    return jsonify(restaurant.serialize)


# Get resto by name
@app.route('/restaurantByName/<name>', methods=['GET'])
def getRestaurantByName(name):
    restaurants = Restaurant.query.filter(Restaurant.name.ilike(name + "%")).all()
    if restaurants is None:
        return abort(404)
    return jsonify(items=[i.serialize for i in restaurants])


# Get locations of a restaurant
@app.route('/locationByRestaurantId/<id>', methods=['GET'])
def getLocationsByRestaurantId(id):
    locations = Location.query.filter_by(restaurantId=id).all()
    if locations is None:
        return abort(404)
    return jsonify(items=[i.serialize for i in locations])


# Get menus by restaurant
@app.route('/menuByRestaurantId/<id>', methods=['GET'])
def getMenuByRestaurantId(id):
    menu = MenuItem.query.filter_by(restaurantId=id).all()
    if menu is None:
        return abort(404)
    return jsonify(items=[i.serialize for i in menu])


# Get rating for menu item
@app.route('/ratingByMenuItemId/<id>')
def getRatingByMenuItemId(id):
    rating = RatingItem.query.filter_by(itemId=id).all()
    if rating is None:
        return abort(404)
    return jsonify(items=[i.serialize for i in rating])


# Get raters
@app.route('/raters', methods=['GET'])
def getAllRaters():
    raters = Rater.query.all()
    if raters is not None:
        return jsonify(items=[i.serialize for i in raters])
    return abort(404)


# Get rater by key
@app.route('/rater/<id>', methods=['GET'])
def getRaterByID(id):
    rater = Rater.query.get(id)
    if rater is None:
        return abort(404)
    return jsonify(rater.serialize)


# Post Restaurant
@app.route('/post_resto', methods=['POST'])
def post_resto():
    restaurant = Restaurant(request.form['name'], request.form['type'], request.form['url'], request.form['rating'])
    db.session.add(restaurant)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
