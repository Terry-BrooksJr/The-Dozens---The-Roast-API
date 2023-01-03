"""
This Module is the central location for all the routes that are used in the /insults endpoint.
"""

import pendulum
from flask import copy_current_request_context
from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from flask_restx import Namespace, Resource, apidoc, fields, marshal_with, reqparse

from database.models import Insult, User
from utils.errors import BannedUserError, InvaildTokenError, UnauthorizedError, errors
from utils.gatekeeper import GateKeeper
from utils.jokester import Jokester

#! Namespace Declaration
api = Namespace("Insults", description="Joke operations")

#!Namespace Related Models
GET_fields = api.model(
    "Insult (Get Method)",
    {
        "explicit": fields.Boolean,
        "catagory": fields.String,
    },
)
POST_fields = api.model(
    "Insult (Post Method)",
    {
        "content": fields.String,
        "explicit": fields.Boolean,
        "catagory": fields.String,
        "bearer token": fields.String,
    },
)


#! Top-Level Vaariables/Plugins
now = pendulum.now()
parser = reqparse.RequestParser()
# joke_categories = Jokester.get_catagories()

#!Request Parameters Designations
parser.add_argument("content", type=str, required=True, location="form")
parser.add_argument("explicit", type=str, required=True, location="form")
parser.add_argument(
    "catagory",
    type=str,
    required=True,
    location="form",
    help="specify the jokes to a  category, if it doesn't fit to any choose 'snowflake'",
    # choices=joke_categsories,
)
parser.add_argument(
    "bearer token",
    type=str,
    required=True,
    location="headers",
    help="Please ensure your have registered your email and password to receive a bearer token. See endpoint `/signup` for more information.",
)

get_parsers = parser.copy()
POST_parsers = parser.copy()

get_parsers.replace_argument(
    "explicit",
    type=str,
    required=False,
    location="headers",
    help="Explicit Filter. When Set to True the default filter is turned off.",
    choices=["true", "false"],
)
get_parsers.replace_argument(
    "catagory",
    type=str,
    required=False,
    location="args",
    help="limit the jokes to a specific category",
    # choices=list(joke_categories),
)
get_parsers.remove_argument("content")
get_parsers.remove_argument("bearer token")


@api.route("insult")
class InsultsAPI(Resource):
    def get(self):
        return {"Yo Mama So...": Jokester.get_random_joke()}, 200

    # @jwt_required
    # def post(self):
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
    #             explict = request.get["nsfw"]
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
