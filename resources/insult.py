from flask import Response, request
from database.models import Movie, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource


class InsultsAPI(Resource):
    def get(self):
        pipeline = [{"$sample": {"size": 1}}]
        insult = Insult.objects().aggregate(pipeline)
        insult1 = ""
        for doc in insult:
            insult1 = doc["content"]
        return jsonify(Insult=insult1), 200

    @jwt_required
    def post(self):
        content = request.json["content"]
        category = request.json["category"]
        explict = request.json["nsfw"]
        date = str(now.to_datetime_string())
        Insult(content=content, explict=explict, added_on=date).save()
        insult = Insult.objects.all()
        return jsonify(message="Added"), 201
