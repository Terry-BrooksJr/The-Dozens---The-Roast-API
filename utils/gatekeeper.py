"""
This Module is responsible for all the actions that occur in the /auth endpoint, and the functions that are called by the /auth routes.terry

"""
import os
from datetime import timedelta

import redis
from bcrypt import checkpw, gensalt, hashpw
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request

from database.models import User
from utils.errors import BannedUserError
from test.test_db import pipeline

jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv("REDIS_URI"), port=6379, db=0, decode_responses=True
)
ACCESS_EXPIRES = timedelta(hours=1)
TOKEN_EXPIRES = timedelta(days=7)


class GateKeeper:
    @staticmethod
    def is_user_banned(email):
        email = email.lower()
        user = User.objects(email=email).first()
        if user["status"] != "active":
            raise BannedUserError("The User Associated With That Token Has Been Banned")
        else:
            return False

    @staticmethod
    def ban_user(email):
        email = email.lower()
        user = User.objects(email=email).first()
        user["status"] = "banned"

    @staticmethod
    def issue_token(email):
        email = email.lower()
        user = User.User.objects(email=email).first()
        additional_claims = {"id": user["ObjectId"]}
        if not GateKeeper.is_user_banned(email):
            access_token = create_access_token(
                identity=email,
                additional_claims=additional_claims,
                expires_delta=TOKEN_EXPIRES,
            )
            return jsonify(access_token=access_token)
        else:
            raise BannedUserError("The User Associated With That Token Has Been Banned")

    @staticmethod
    def check_password(provided_pw, logged_pw):
        salt = gensalt(rounds=8, prefix=b"2b")
        provided_pw = hashpw(provided_pw.encode("utf-8"), salt)
        # provided_pw = provided_pw.decode()
        if logged_pw == provided_pw:
            return True
        else:
            return False

    @staticmethod
    def encrypt_password(plaintext_pw):
        salt = gensalt(rounds=8, prefix=b"2b")
        hashed = hashpw(plaintext_pw.encode("utf-8"), salt)
        return hashed.decode()
    
    @staticmethod
    def is_registered(email):
        pipeline = {"$match": {"email": email}}
        user = User.objects().aggregate(pipeline)
        print(len(user))
        if len(user) > 0:
            return True
        else:
            return False

