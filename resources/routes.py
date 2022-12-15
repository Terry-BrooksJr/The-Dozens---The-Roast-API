from .insult import InsultsAPI
from .auth import SignupApi, LoginApi
from flask_restful import Resource
from flask import request


class ApiTest(Resource):
    def get(self):
        return {"status": "API Is Up!"}, 200

    def post(self):
        body = request.get_json()
        return {"status": "API Is Up!", "Echo": body}, 201

    def patch(self):
        body = request.get_json()
        return {"status": "API Is Up!", "Echo": body}, 204

    def delete(self):
        return {"status": "API Is Uqp!"}, 204


def initialize_routes(api):
    api.add_resource(ApiTest, "/test")

    api.add_resource(InsultsAPI, "/insult")

    api.add_resource(SignupApi, "/auth/signup", "/auth", "/signup")
    api.add_resource(LoginApi, "/token", "/key")
    
