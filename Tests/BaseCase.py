import unittest
import pytest

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
try:
    app.config['MONGO_URI'] = "mongodb+srv://Hellofresh_user:Hellofresh123@cluster0.giqdc.mongodb.net/HelloFresh"
    mongo = PyMongo(app)
    db = mongo.db
except Exception as e:
    print(e, "cannot connect to the database")


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        # self.db = db.get_db()

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
