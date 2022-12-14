from flask import request
from database.models import Insult
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import pendulum

now = pendulum.now()


class InsultsAPI(Resource):
    def get(self):
        pipeline = [{"$sample": {"size": 1}}]
        insult = Insult.objects().aggregate(pipeline)
        insult1 = ""
        for doc in insult:
            insult1 = doc["content"]
        return {"Yo Mama So...": insult1}, 200

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            content = body["content"]
            # category = request.json["category"]
            explict = body["nsfw"]
            date = str(now.to_datetime_string())
            Insult(
                content=content, explict=explict, added_on=date, added_by=user
            ).save()
            Insult.objects.all()
            return {"Status": "Insult Added"}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception:
            raise InternalServerError
