"""
This Module is responsible fo the testing/status endpoint. All other endpoints are defined in their respective modules.
"""

import pendulum
from flask import jsonify, request
from flask_restx import Namespace, Resource, api

from database.db import db
from utils.administrator import Administrator

#! Namespace Declaration
api = Namespace(
    "Testing & Status",
    description="These endpoints encompass all the endpoints needed to: \n 1. Test the Current Status of the API. \n 2. If admin, get operation metrics.",
)


#!Namespace Related Models


#! Top-Level Vaariables/Plugins
now = pendulum.now()


#!Request Parameters Designations


@api.route("status")
class ApiTest(Resource):
    """Class for testing the API test Endpoints.

    Inherits from the flask_restplus Resource class.
    """

    #! GET ENDPOINT - Status

    @api.doc()
    @api.response(
        200,
        "As of <DATETIME> UTC the API Is Up and actively insulting millions of Mamas",
    )
    def get(self):
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas"
        }, 200

    def post(self):
        body = request.get_json()
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas",
            "We Hear You": body,
        }, 200

    def patch(self):
        body = request.get_json()
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas",
            "We Hear You": body,
        }, 200

    def delete(self):
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas"
        }, 200

    def put(self):
        body = request.get_json()
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas",
            "We Hear You": body,
        }, 200

    def options(self):
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas"
        }, 200

    def head(self):
        return {
            "status": f"As of {now.to_datetime_string()} UTC the API Is Up and actively insulting millions of Mamas"
        }, 200


@api.route("metrics")
class ApiMetrics(Resource):
    @api.response(200, "The Count of Insults in the Database")
    def get(self):
        jokes, users = Administrator.count_user_and_jokes()
        return jsonify(f"There are {jokes} insults and {users} in the Database")
