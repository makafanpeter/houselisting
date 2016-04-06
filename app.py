from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<string:term>')
def search(term):
    houses = House.query.filter_by(term)
    return jsonify([house.serialize for house in houses])


@app.route('/update')
def update():
    print ""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
