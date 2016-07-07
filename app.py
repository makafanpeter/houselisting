from flask import Flask, render_template, jsonify, request, abort
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
import os, re

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
    northEast = request.args.get('ne', '')
    southWest = request.args.get('sw', '')
    reg = re.compile(r'^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$')
    if not (southWest and northEast):
        abort(400)
    if not (reg.match(southWest) and reg.match(northEast)):
        abort(400)
    northEastLat = northEast.split(',')[0]
    northEastLong = northEast.split(',')[1]
    southWestLat = southWest.split(',')[0]
    southWestLong = southWest.split(',')[1]
    houses = []
    if southWestLong <= northEastLong:
        houses = House.query.filter(and_(and_(House.latitude <= southWestLat, House.latitude <= northEastLat), and_(
            House.longitude <= southWestLong, House.longitude <= northEastLong))).all()
    else:
        houses = House.query.filter(and_(and_(House.latitude <= southWestLat, House.latitude <= northEastLat), or_(
            House.longitude <= southWestLong, House.longitude <= northEastLong))).all()
    return jsonify(houses=[house.serialize for house in houses])


if __name__ == '__main__':
    app.run(host="0.0.0.0")
