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

parser = reqparse.RequestParser()
parser.add_argument("email", type=str, required=True, location="form")
parser.add_argument("password", type=str, required=True, location="form")

now = pendulum.now()

@api.route("auth")
class SignupApi(Resource):
    @api.doc(model=signup_model, body=User)
    @api.response(201, "User Created")
    @api.response(400, "Bad Request")
    @api.response(401, "Unauthroized")
    @api.doc(parser=parser)
    @api.expect(signup_model)
    
    #! POST Endpoint For User Registration
    def post(self):
        body = request.get_json()
        # TODO - Find a way to validate for Empty Post Bodies
        user = User(
            email=body["email"].lower(), password=body["password"], joined_on=now.to_date_string()
        )
        user.password = GateKeeper.encrypt_password(user.password)
        user.save()
        id = user.id
        return {"id": str(id)}, 201
   
        
        
        # else:
        #     raise EmailAlreadyExistsError(errors.EmailAlreadyExistsError)
        # except user.DoesNotExist:2
        #     pass
        # except (UserDoesNotExist):
        #     pass
        # except Exception as e:
        #     raise BadRequest(e)


@api.route("token")
class LoginApi(Resource):
    @api.doc(model=token_request_model, body=User)
    @api.response(401, "Unauthorized - Incorrect Password or Un-Registred Email")
    @api.response(201, "Token Issued")
    @api.doc(params={"email": "A Vaild Email Address", "location": "form"})
    @api.doc(params={"Password": "Any combination Of 7 or More ASCII Character."})
    @api.expect(token_request_model)
    def post(self):
        body = request.get_json()
        email = body["email"].lower()
        user = User(email=email, password=body["password"])
        try:
            registered = User.objects.get(email=email)
        except (UnauthorizedError, UserDoesNotExist, Exception):
            return {"Error": "Email Not Registered"}, 401
        try:
            pipeline = [{"$match": {"email": email}}]
            users = User.objects().aggregate(pipeline)
            for doc in users:
                logged_password = doc["password"]
            GateKeeper.check_password(body["password"], logged_password)
        except (UnauthorizedError, UserDoesNotExist, Exception):
            return {"Error": "Password invalid"}, 401
        else:
            token = GateKeeper.issue_token(user["email"])
            string_expiry = now.add(days=7)

            return {
                "Token/Key": token,
                "expires": f"{string_expiry.to_datetime_string()} UTC",
            }, 201