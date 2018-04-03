
from flask import Flask, request, redirect, url_for
from flask import render_template
from models import *


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zshah011:University-25@web0.site.uottawa.ca:15432/zshah011'

db.app = app
db.init_app(app)

db.create_all()


@app.route('/')
def index():
    return render_template('post_resto.html')


@app.route('/post_resto', methods=['POST'])
def post_resto():
    restaurant = Restaurant(request.form['name'], request.form['type'], request.form['url'], request.form['rating'])
    db.session.add(restaurant)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
