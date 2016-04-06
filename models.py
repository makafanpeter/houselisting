from datetime import datetime
from sqlalchemy.orm import relationship
from app import db


class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    imageUrl = db.Column(db.String())
    price = db.Column(db.Float)
    address = db.Column(db.String())
    formatted = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    formattedAddress = db.Column(db.String())
    createdOn = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, address, url, price, image_url):
        self.name = name
        self.address = address
        self.url = url
        self.price = price
        self.imageUrl = image_url

    def __repr__(self):
        return '<id {0}, name {1}>'.format(self.id, self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "url": self.url,
            "price": self.price,
            "imageUrl": self.imageUrl
        }


class HouseFeature(db.Model):
    __tablename__ = 'housefeatures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    house = relationship(House)

    def __init__(self, name, house_id):
        self.name = name
        self.house_id = house_id

    def __repr__(self):
        return '<id {0}, name {1}>'.format(self.id, self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name
        }
