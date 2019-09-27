import os
import logging
#logging.warn(os.environ["DUMMY"])
from flask import Flask, abort, request
from flask import Flask, render_template
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()

    return render_template('home.html', products=products)

@app.route('/products')
def read_products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/products/<int:id>')
def read_product(id):
    product = db.session.query(Product).get(id) # SQLAlchemy request => 'SELECT * FROM products'
    if product is None:
        abort(404)
    else :
        return product_schema.jsonify(product)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

@app.route('/products', methods = ['POST'])
def create_products():

    name = request.json['name']
    description = request.json['description']

    product  = product(name = name, description = description)

    db.session.add(product)
    db.session.commit()

    return product_schema.jsonify(product), 201


