from flask import Flask, render_template, jsonify, request
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


@app.route('/search', methods=['GET'])
def search():
    term = request.args.get('name', '')
    houses = House.query.filter(House.name.like("%" + term + "%")).all()
    # houses = House.query.all()
    return jsonify(houses=[house.serialize for house in houses])


@app.route('/update')
def update():
    print ("")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
