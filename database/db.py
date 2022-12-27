import os

from flask_mongoengine import MongoEngine
from mongoengine import connect

db = MongoEngine()

connect(host=os.getenv("MONGODB_URI"))


def initialize_db(app):
    db.init_app(app)
