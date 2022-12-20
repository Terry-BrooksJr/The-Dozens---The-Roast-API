
from flask_jwt_extended import create_access_token, get_jwt
import pendulum
from utils.gatekeeper import GateKeeper

from .db import db

gatekeeper = GateKeeper()
now = pendulum.now()


class Insult(db.Document):
    content = db.StringField(required=True)
    category = db.StringField(required=True)
    explict = db.BooleanField(required=True)
    added_on = db.StringField(required=True)
    added_by = db.StringField(required=True)

    meta = {"collection": "insults"}


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    joined_on = db.StringField(required=True)
    meta = {"collection": "users", "db": "UserCreds"}

    def hash_password(self):
        self.password = gatekeeper.encrypt_password(self.password)
