from flask import Flask, request, redirect, url_for, jsonify
from flask import render_template
from models import *

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zshah011:University-25@web0.site.uottawa.ca:15432/zshah011'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


db.create_all()

# Home
@app.route('/')
def index():
    return render_template('index.html')


# Get all the restos
@app.route('/restaurants', methods=['GET'])
def getAllRestaurants():
    restaurants = Restaurant.query.all()
    return jsonify([i.serialize for i in restaurants])


# Get resto by key
@app.route('/restaurant/<id>', methods=['GET'])
def getRestaurantByID(id):
    restaurant = Restaurant.query.get(id)
    return jsonify(restaurant.serialize)


# Get raters
@app.route('/raters', methods=['GET'])
def getAllRaters():
    raters = Rater.query.all()
    return jsonify([i.serialize for i in raters])


# Get rater by key
@app.route('/rater/<id>', methods=['GET'])
def getRaterByID(id):
    rater = Rater.query.get(id)
    return jsonify(rater.serialize)



# Post Restaurant
@app.route('/post_resto', methods=['POST'])
def post_resto():
    restaurant = Restaurant(request.form['name'], request.form['type'], request.form['url'], request.form['rating'])
    db.session.add(restaurant)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
