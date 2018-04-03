from flask import Flask
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zshah011:University-25@web0.site.uottawa.ca:15432/zshah011'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db.app = app
db.init_app(app)

db.create_all()

@app.route('/')
def index():
    return 'hello flask'

@app.route('/post_resto', methods=['POST'])
def post_resto():
    return


if __name__ == "__main__":
    app.run()
