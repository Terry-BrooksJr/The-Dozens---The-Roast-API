from flask import request
from flask_jwt_extended import create_access_token
from database.models import User
from utils.gatekeeper import GateKeeper
from flask_restful import Resource
import pendulum
from database.db import db
import os
from utils.errors import UnauthorizedError, errors, EmailAlreadyExistsError
import redis

now = pendulum.now()
import pprint

gatekeeper = GateKeeper()
jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv("REDIS_URI"), port=6379, db=0, decode_responses=True
)


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        # Verifying the Required Keys Are In Payload
        if "email" not in body.keys():
            return {"Error": "'email' Is A Required Key"}, 406
        if "password" not in body.keys():
            return {"Error": "'password' Is A Required Key"}, 406
        # Assinging the Value Of Keys to ORM Model
        email = body["email"].lower()
        user = User(
            email=email, password=body["password"], joined_on=now.to_date_string()
        )
        # Verifying The Values of Keys Are Acceptanble and No Duplicate Submissions
        try:
            user_found = User.objects.get(email=email)
            if user_found:
                raise EmailAlreadyExistsError(EmailAlreadyExistsError)
        except user.DoesNotExist:
            pass
        except (ValidationError, Exception):
            return {"Error": "Invaild Email Address. Please Confirm Entry"}, 406
        if len(user.password) <= 6:
            return {"Error": "Passwords Must be 6 Longer Than 6  Characters"}, 412
        else:
            user.hash_password()
            user.save()
            id = user.id
            return {"id": str(id)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        if "email" not in body.keys():
            return {"Error": "'email' Is A Required Key"}
        if "password" not in body.keys():
            return {"Error": "'password' Is A Required Key"}
        email = body["email"].lower()
        user = User(email=email, password=body["password"])

        try:
            registered = User.objects.get(email=email)
        except (UnauthorizedError, DoesNotExist, Exception):
            return {"Error": "Email Not Registered"}, 401
        try:
            pipeline = [{"$match": {"email": email}}]
            users = User.objects().aggregate(pipeline)
            for doc in users:
                logged_password = doc["password"]
            gatekeeper.check_password(body["password"], logged_password)
        except (UnauthorizedError, DoesNotExist, Exception):
            return {"Error": "Password invalid"}, 401
        else:
            token = gatekeeper.issue_token(user.id)
            string_expiry = now.add(days=7)

            return {
                "Token/Key": token,
                "expires": f"{string_expiry.to_datetime_string()} UTC",
            }, 201
