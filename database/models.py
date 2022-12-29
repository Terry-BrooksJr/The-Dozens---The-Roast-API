"""
    This is the Models that comproise the two main collections in the MongoDB Database: Users and Insults. It is powered by the ORM: Mongoengine
    
    While There are Class Methods Associated with these objects, the majaority of methods/functions have been abstracted away via a Utility Class in the `/utils` directory. 
    
    Design Choice was made to ensure sepration of cocerns and modularity:
    - Utils Classes are the Actions. 
    - Models are the Structure.
"""
import pendulum

from .db import db

now = pendulum.now()


class Insult(db.Document):
    content = db.StringField(required=True)
    category = db.StringField(required=True)
    explict = db.BooleanField(required=True)
    added_on = db.StringField(required=True)
    added_by = db.StringField(required=True)
    status = db.StringField(required=True, default="active")
    meta = {"collection": "insults"}


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    joined_on = db.StringField(required=True)
    status = db.StringField(required=True, default="active")
    meta = {"collection": "users"}
