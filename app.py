from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://zshah011:University-25@web0.site.uottawa.ca/zshah011'

db = SQLAlchemy(app)

print('yoo')


@app.route('/')
def index():
    return 'hello flask'

@app.route('/post_resto', methods=['POST'])
def post_resto():
    return


if __name__ == "__main__":
    app.run()
