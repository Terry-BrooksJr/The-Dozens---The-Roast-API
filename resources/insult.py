import pendulum
from flask import copy_current_request_context
from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
<<<<<<< Updated upstream
from flask_restx import Resource, reqparse, fields, marshal_with
=======
from flask_restx import Resource, reqparse, fields, marshal_with, apidoc, Namespace
>>>>>>> Stashed changes
from utils.parser import parse_params
from utils.arguments import Argument
from utils.gatekeeper import GateKeeper
from database.models import Insult
from utils.errors import errors, SchemaValidationError
from utils.jokester import Jokester

# Namespace Declaration
api = Namespace("Insults", description="Joke operations")

# Namespace Related Models
GET_fields = api.model(
    "GET_fields",
    {
        "explicit": fields.Boolean,
        "catagory": fields.String,
    },
)
POST_fields = {
    "content": fields.String(),
    "explicit": fields.Boolean(),
    "catagory": fields.String(),
}
# Top-Level Vaariables/Plugins
now = pendulum.now()
parser = reqparse.RequestParser()
gatekeeper = GateKeeper()


class InsultsAPI(Resource):
    @marshal_with(GET_fields, skip_none=True)
    def get(self):
        return {"Yo Mama So...": Jokester.get_random_joke()}, 200

    # @jwt_required
    # @marshal_with(POST_fields)
    # def post(self):
    #     if "content" not in body.keys():
    #         return {"Error": "'content' Is A Required Key"}
    #     if "explicit" not in body.keys():
    #         return {"Error": "'explicit' Is A Required Key"}
    #     if "token" not in body.keys():
    #         return {"Error": "'token' Is A Required Key"}
    #     try:
    #         user_id = get_jwt_identity()
    #         auth_token = get_jwt()
    #         revoked = gatekeeper.check_if_token_is_revoked(auth_token)
    #         if revoked:
    #             return {
    #                 "Not Authorized": "The Token Provided has Expired or Has been Revoked!"
    #             }, 401
    #         else:
    #             user = User.objects.get(id=user_id)
    #             content = request.get("content")
    #             # category = request.json["category"]
    #             explict = request.get["explicit"]
    #             date = str(now.to_datetime_string())
    #             Insult(
    #                 content=content, explict=explict, added_on=date, added_by=user
    #             ).save()
    #             insult = Insult.objects.all()
    #             return {"Status": "Insult Added"}, 201
    #     except (FieldDoesNotExist, ValidationError):
    #         raise SchemaValidationError
    #     except Exception:
    #         raise InternalServerError


# FIXME - Get this Parameter Parsing filteration logic to work
#    params = parse_params(self.PARAMS["GET"])
#         explicit_setting = params["explicit"]
#         catagory_selection = params["catagory"]
#         fields.Boolean.format(explicit_setting)

# # Conditiomal to Handle of Only explicit hearder passed
# if type(explicit_setting) is not None:
#     try:
#         explicit_set_pipeline = [
#             {"$match": {"explicit/explict": explicit_setting}},
#             {"$sample": {"size": 1}},
#         ]
#         insult = Insult.objects().aggregate(pipeline)
#         explicit_filtered_insult = str()
#         for doc in insult:
#             explicit_filtered_insult = doc["content"]
#         return {"Yo Mama So...": explicit_filtered_insult}, 200
#     except Exception:
#         raise SchemaValidationError(errors["SchemaValidationError"])
# # Conditional to Handle if Both GET Paraks Are Passed
# elif type(explicit_setting) is not None and type(catagory_selection) is not None:
#     explicit_and_cat_set_pipeline = [
#         {
#             "$match": {
#                 "category": catagory_selection,
#                 "explicit/explict": explicit_setting,
#             }
#         },
#         {"$sample": {"size": 1}},
#     ]
#     insult = Insult.objects().aggregate(explicit_and_cat_set_pipeline)
#     filtered_by_cat_and_explicit_insult = str()
#     for doc in insult:
#         filtered_by_cat_and_explicit_insult = doc["content"]
#     return {"Yo Mama So...": filtered_by_cat_and_explicit_insult}, 200
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
#   def __init__(self):
#         self.PARAMS = {
#             "GET": {
#                 "explicit": {
#                     "type": bool,
#                     "default": None,
#                     "validators": [],
#                     "locations": ["args", "headers"],
#                     "required": False,
#                 },
#                 "category": {
#                     "type": str,
#                     "default": None,
#                     "validators": [],
#                     "locations": ["args", "headers"],
#                     "required": False,
#                 },
#             },
#             "POST": {
#                 "content": {
#                     "type": str,
#                     "vaildators": [],
#                     "locations": ["json"],
#                     "required": True,
#                 },
#                 "explicit": {
#                     "type": bool,
#                     "vaildators": [],
#                     "locations": ["json"],
#                     "required": True,
#                 },
#                 "catagory": {
#                     "type": bool,
#                     "vaildators": [],
#                     "locations": ["json"],
#                     "required": True,
#                 },
#             },
#         }
