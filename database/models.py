from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Insult(db.Document):
    content = db.StringField(required=True)
    category = db.StringField(required=True)
    explict = db.BooleanField(required=True)
    added_on = db.StringField(required=True)


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)
