from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, abort
from flask_cors import CORS
from sqlalchemy import text

from models import *
from dbFiller import *
from sqlQueries import *
import simplejson as json
import decimal, datetime

# Init app
app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Pasoon:password123@localhost:5432/restaurant_db'
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
@app.route('/restaurants', defaults={'limit': None})
@app.route('/restaurants/limit=<limit>', methods=['GET'])
def getAllRestaurants(limit):
    if(limit):
        restaurants = Restaurant.query.limit(limit).all()
    else:
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
    restaurants = Restaurant.query.filter(Restaurant.name.ilike("%" + name + "%")).all()
    if restaurants is None:
        return abort(404)
    return jsonify(items=[i.serialize for i in restaurants])


# Get resto by type
@app.route('/restaurantByType/<type>', methods=['GET'])
def getRestaurantByType(type):
    restaurants = Restaurant.query.filter(Restaurant.type.ilike("%" + type + "%")).all()
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
    menu = MenuItem.query.filter_by(restaurantId=id).order_by(MenuItem.category).all()
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
    dataReceived = request.get_json()
    print(dataReceived)
    new_restaurant = Restaurant(name=dataReceived['name'], type=dataReceived['type'], url=dataReceived['url'], pic_url=dataReceived['pic_url'], overallrating=4)
    db.session.add(new_restaurant)
    db.session.commit()
    return redirect(url_for('index'))

# Post Menu Item
@app.route('/post_menuitem', methods=['POST'])
def post_menuitem():
    dataReceived = request.get_json()
    print(dataReceived)
    new_menuitem = MenuItem(restaurantId=dataReceived['restaurantId'], name=dataReceived['name'], foodtype=dataReceived['type'], category=dataReceived['category'], description=dataReceived['description'], price=dataReceived['price'])
    db.session.add(new_menuitem)
    db.session.commit()
    return redirect(url_for('index'))

# Post Rater
@app.route('/post_rater', methods=['POST'])
def post_rater():
    dataReceived = request.get_json()
    print(dataReceived)
    joinDate = str(datetime.date.today())[:10]
    new_rater = Rater(userId=dataReceived['userId'], email=dataReceived['email'], name=dataReceived['name'], join_date=joinDate, raterType=dataReceived['type'], reputation=1)
    db.session.add(new_rater)
    db.session.commit()
    return redirect(url_for('index'))

# Delete a Menu Item
@app.route('/deleteMenuItem/<id>')
def deleteMenuItem(id):
    item = MenuItem.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

# Delete a Restaurant
@app.route('/deleteRestaurant/<id>')
def deleteRestaurant(id):
    item = Restaurant.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

# Delete a Rater Item
@app.route('/deleteRater/<id>')
def deleteRater(id):
    item = Rater.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

# Get e)
@app.route('/e', methods=['GET'])
def get_e():
    data = db.engine.execute(text(queries['e'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get f)
@app.route('/f', methods=['GET'])
def get_f():
    data = db.engine.execute(text(queries['f'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get g)
@app.route('/g', methods=['GET'])
def get_g():
    data = db.engine.execute(text(queries['g'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get h)
@app.route('/h', methods=['GET'])
def get_h():
    data = db.engine.execute(text(queries['h'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get i)
@app.route('/i', methods=['GET'])
def get_i():
    data = db.engine.execute(text(queries['i'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get j)
@app.route('/j', methods=['GET'])
def get_j():
    data = db.engine.execute(text(queries['j'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get k)
@app.route('/k', methods=['GET'])
def get_k():
    data = db.engine.execute(text(queries['k'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get l)
@app.route('/l', methods=['GET'])
def get_l():
    data = db.engine.execute(text(queries['l'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get m)
@app.route('/m', methods=['GET'])
def get_m():
    data = db.engine.execute(text(queries['m'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get n)
@app.route('/n', methods=['GET'])
def get_n():
    data = db.engine.execute(text(queries['n'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)

# Get o)
@app.route('/o', methods=['GET'])
def get_o():
    data = db.engine.execute(text(queries['o'])).fetchall()
    print(data)

    return json.dumps([dict(r) for r in data], default=alchemyencoder)


def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

if __name__ == "__main__":
    app.run(debug=True)
