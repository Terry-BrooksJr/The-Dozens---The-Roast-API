import pendulum
from flask import copy_current_request_context
from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse, fields, marshal_with
from utils.parser import parse_params
from utils.arguments import Argument
from utils.gatekeeper import GateKeeper
from database.models import Insult
from utils.errors import errors, SchemaValidationError

now = pendulum.now()
parser = reqparse.RequestParser()
gatekeeper = GateKeeper()

POST_fields = {
    "content": fields.String(),
    "nsfw": fields.Boolean(),
    "catagory" : fields.String()
}

class InsultsAPI(Resource):
    def __init__(self):
        self.PARAMS = {
            "GET": {
                "nsfw": {
                    "type": bool,
                    "default": None,
                    "validators": [],
                    "locations": ["args", "headers"],
                    "required": False,
                },
                "category": {
                    "type": str,
                    "default": None,
                    "validators": [],
                    "locations": ["args", "headers"],
                    "required": False,
                },
            },
            "POST": {
                "content": {
                    "type": str,
                    "vaildators": [],
                    "locations": ["json"],
                    "required": True,
                },
                "nsfw": {
                    "type": bool,
                    "vaildators": [],
                    "locations": ["json"],
                    "required": True,
                },
                "catagory": {
                    "type": bool,
                    "vaildators": [],
                    "locations": ["json"],
                    "required": True,
                }
            },
        }
        
    def get(self):
        pipeline = [{"$sample": {"size": 1}}]
        insult = Insult.objects().aggregate(pipeline)
        non_filtered_insult = str()
        for doc in insult:
            non_filtered_insult = doc["content"]
        return {"Yo Mama So...": non_filtered_insult}, 200

    @jwt_required
    @marshal_with(POST_fields)
    def post(self):
        if "content" not in body.keys():
            return {"Error": "'content' Is A Required Key"}
        if "nsfw" not in body.keys():
            return {"Error": "'nsfw' Is A Required Key"}
        if "token" not in body.keys():
            return {"Error": "'token' Is A Required Key"}
        try:
            user_id = get_jwt_identity()
            auth_token = get_jwt()
            revoked = gatekeeper.check_if_token_is_revoked(auth_token)
            if revoked:
                return {
                    "Not Authorized": "The Token Provided has Expired or Has been Revoked!"
                }, 401
            else:
                user = User.objects.get(id=user_id)
                content = request.get("content")
                # category = request.json["category"]
                explict = request.get["nsfw"]
                date = str(now.to_datetime_string())
                Insult(
                    content=content, explict=explict, added_on=date, added_by=user
                ).save()
                insult = Insult.objects.all()
                return {"Status": "Insult Added"}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception:
            raise InternalServerError
#FIXME - Get this Parameter Parsing filteration logic to work
#    params = parse_params(self.PARAMS["GET"])
#         nsfw_setting = params["nsfw"]
#         catagory_selection = params["catagory"]
#         fields.Boolean.format(nsfw_setting)

        # # Conditiomal to Handle of Only NSFW hearder passed
        # if type(nsfw_setting) is not None:
        #     try:
        #         nsfw_set_pipeline = [
        #             {"$match": {"nsfw/explict": nsfw_setting}},
        #             {"$sample": {"size": 1}},
        #         ]
        #         insult = Insult.objects().aggregate(pipeline)
        #         nsfw_filtered_insult = str()
        #         for doc in insult:
        #             nsfw_filtered_insult = doc["content"]
        #         return {"Yo Mama So...": nsfw_filtered_insult}, 200
        #     except Exception:
        #         raise SchemaValidationError(errors["SchemaValidationError"])
        # # Conditional to Handle if Both GET Paraks Are Passed
        # elif type(nsfw_setting) is not None and type(catagory_selection) is not None:
        #     nsfw_and_cat_set_pipeline = [
        #         {
        #             "$match": {
        #                 "category": catagory_selection,
        #                 "nsfw/explict": nsfw_setting,
        #             }
        #         },
        #         {"$sample": {"size": 1}},
        #     ]
        #     insult = Insult.objects().aggregate(nsfw_and_cat_set_pipeline)
        #     filtered_by_cat_and_nsfw_insult = str()
        #     for doc in insult:
        #         filtered_by_cat_and_nsfw_insult = doc["content"]
        #     return {"Yo Mama So...": filtered_by_cat_and_nsfw_insult}, 200
        # # Conditional to Handle if only Catagory is set
        # elif type(catagory_selection) is not None:
        #     catagory_selection_only_pipeline = [
        #         {
        #             "$match": {
        #                 "category": catagory_selection,
        #             }
        #         },
        #         {"$sample": {"size": 1}},
        #     ]
        #     insult = Insult.objects().aggregate(catagory_selection_only_pipeline)
        #     catagory_selection_insult = str()
        #     for doc in insult:
        #         catagory_selection_insult = doc["content"]
        #     return {"Yo Mama So...": catagory_selection_insult}, 200
        # else: