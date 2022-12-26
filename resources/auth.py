import os

import pendulum
import redis
from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Resource, fields, reqparse, Namespace, fields

# from app import api
from database.db import db
from database.models import User
from utils.errors import EmailAlreadyExistsError, UnauthorizedError, errors
from utils.gatekeeper import GateKeeper
from flask_restx import Resource
import pendulum
from database.db import db
import os
from utils.errors import UnauthorizedError, errors, EmailAlreadyExistsError
import redis
from werkzeug.exceptions import BadRequest

# Namespace Declaration
api = Namespace(
    "authorizations",
    description="This Namespace is charged with the tasks of issuing, authenticating bearer tokens and registering users ",
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
gatekeeper = GateKeeper()
jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv("REDIS_URI"), port=6379, db=0, decode_responses=True
)

parser = reqparse.RequestParser()
parser.add_argument("foo", type=str, required=True, location="form")
parser.add_argument("bar", type=str, required=True, location="form")

now = pendulum.now()


@api.route("/")
class SignupApi(Resource):
    @api.doc(model=signup_model, body=User)
    @api.response(201, "User Created")
    @api.response(400, "Bad Request")
    @api.response(401, "Unauthroized")
    @api.doc(params={"email": "A Vaild Email Address", "location": "form"})
    @api.doc(params={"Password": "Any combination Of 7 or More ASCII Character."})
    @api.expect(signup_model)
    def post(self):
        body = request.get_json()
        # Verifying the Required Keys Are In Payload
        if "email" not in body.keys():
            raise BadRequest("'email' Is A Required Key")
        if "password" not in body.keys():
            raise BadRequest("'password' Is A Required Key")
        # Assinging the Value Of Keys to ORM Model
        if len(body["email"] or len(body["password"])):
            raise BadRequest("Empty Request")
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
            raise BadRequest("Invaild Email Address. Please Confirm Entry")
        if len(user.password) <= 6:
            raise BadRequest("Passwords Must be 6 Longer Than 6  Characters")
        else:
            user.hash_password()
            user.save()
            id = user.id
            return {"id": str(id)}, 200


@api.route("/token")
class LoginApi(Resource):
    @api.doc(model=token_request_model, body=User)
    @api.response(401, "Unauthorized - Incorrect Password or Un-Registred Email")
    @api.response(201, "Token Issued")
    def post(self):
        body = request.get_json()
        if "email" not in body.keys():
            raise BadRequest("'email' Is A Required Key'")
        if "password" not in body.keys():
            raise BadRequest("'passeword' Is A Required Key'")
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
