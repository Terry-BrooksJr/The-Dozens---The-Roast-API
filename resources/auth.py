from flask import request
from flask_jwt_extended import create_access_token
from database.models import User
from flask_restful import Resource
import pendulum

now = pendulum.now()


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        # Verifying the Required Keys Are In Payload
        if "email" not in body.keys():
            return {"Error": "'email' Is A Required Key"}
        if "password" not in body.keys():
            return {"Error": "'password' Is A Required Key"}
        # Assinging the Value Of Keys to ORM Model
        user = User(**body)
        # Verifying The Values of Keys Are Acceptanble and No Duplicate Submissions
        try:
            user_found = User.objects.get(email=user.email)
            if user_found:
                return {
                    "Error": "This Email Is Already Registered. If You Need a Token Try the '/token' endpoint"
                }
        except user.DoesNotExist:
            pass
        if len(user.password) <= 6:
            return {"Error": "Passwords Must be 6 Longer Than 6  Characters"}
        else:
            user.hash_password()
            user.save()
            id = user.id
            return {"id": str(id)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get("email"))
        authorized = user.check_password(body.get("password"))
        if not authorized:
            return {"error": "Email or password invalid"}, 401

        expires = pendulum.duration(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {"token": access_token}, 200
