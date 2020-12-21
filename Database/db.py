
from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

try:
    app.config['MONGO_URI'] = "mongodb+srv://Hellofresh_user:Hellofresh123@cluster0.giqdc.mongodb.net/HelloFresh"
    mongo = PyMongo(app)
    db = mongo.db
except Exception as e:
    print(e, "cannot connect to the database")


def initialize_db(app):
    db.init_app(app)
