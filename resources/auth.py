
"""
These module encompass all the endpoints needed to register a user and provision a Bearer Token. It routes leverage the GateKeeper class to perform the necessary actions.
"""

import os

import pendulum
import redis
from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.exceptions import BadRequest

# from app import api
from database.db import db
from database.models import User
from utils.errors import (
    EmailAlreadyExistsError,
    UnauthorizedError,
    UserDoesNotExist,
    errors,
)
from utils.gatekeeper import GateKeeper

# Namespace Declaration
api = Namespace(
    "Authorizations & Authentication",
    description="These endpoints encompass all the endpoints needed to:\n 1. Sign-Up to contribute a joke. \n 2. Provisioning a Bearer Token require at the time of submission. <br> <sub>Note: The Bearer Token is required to submit a joke, and registration is required to receive a token.</sub>",
)
# Namespace Related Models
signup_model = api.model(
    "SignUp",
    {
        "email": fields.String(required=True),
        "password": fields.String(min_length=7, required=True),
    },
)
token_request_model = api.model(
    "Bearer Token Provision",
    {
        "email": fields.String(required=True),
        "password": fields.String(min_length=7, required=True),
    },
)
# Top-Level Vaariables/Plugins
jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv("REDIS_URI"), port=6379, db=0, decode_responses=True
)

now = pendulum.now()

@api.route("auth")
class SignupApi(Resource):
    def post(self):
        body = request.get_json()
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
