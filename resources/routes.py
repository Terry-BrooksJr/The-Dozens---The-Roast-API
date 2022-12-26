"""
This Module is responsible for routing the API requests to the correct endpoints. The only endpoints that are defined here are the testing/status endpoint. All other endpoints are defined in their respective modules.
"""

import pendulum
from flask import request
from flask_restx import Resource

from .auth import LoginApi, SignupApi
from .insult import InsultsAPI

now = pendulum.now()


class ApiTest(Resource):
    """Class for testing the API test Endpoints.

    Inherits from the flask_restplus Resource class.
    """

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


def initialize_routes(api):
    # Testinf Endpoints
    api.add_resource(ApiTest, "/test", "/status")
    # Insult Resources Endpoints
    api.add_resource(InsultsAPI, "/insult", "/")
    # Auth Endpoints
    api.add_resource(SignupApi, "/auth/signup", "/auth", "/signup")
    api.add_resource(LoginApi, "/token", "/key")
