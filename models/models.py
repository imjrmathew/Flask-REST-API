# Necessary imports
from flask_sqlalchemy import SQLAlchemy
import base64, os
from io import BytesIO
import cloudinary.api


# Initializing SQLAlchemy
db = SQLAlchemy()


# Class model for User Registration
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(800), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password



# Class model for Product
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.String(800), nullable=False)

    def __init__(self, product_name, product_price, product_image):
        self.product_name = product_name
        self.product_price = product_price
        self.product_image = product_image

    def json(self):  
        image = cloudinary.api.resource(self.product_image)
        return {"product_name": self.product_name,
                "product_price": self.product_price,
                "product_image": image['secure_url']}