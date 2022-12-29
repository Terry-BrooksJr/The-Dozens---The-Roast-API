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
joke_categories = Jokester.get_catagories()
print(joke_categories)
#!Request Parameters Designations
parser.add_argument("content", type=str, required=True, location="form")
parser.add_argument("explicit", type=str, required=True, location="form")
parser.add_argument(
    "catagory",
    type=str,
    required=True,
    location="form",
    help="specify the jokes to a  category, if it doesn't fit to any choose 'snowflake'",
    choices=joke_categories,
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
    choices=list(joke_categories),
)
get_parsers.remove_argument("content")
get_parsers.remove_argument("bearer token")


@api.route("insult")
class InsultsAPI(Resource):
    #! GET ENDPOINT - Insults

    @marshal_with(GET_fields, skip_none=True)
    @api.doc(model=GET_fields, parser=get_parsers)
    @api.response(200, "Insults Found")
    @api.response(400, "Bad Request - If passing a parameter, check values and reattempt")
    @api.expect(get_parsers)
    def get(self):
        joke = Jokester.get_random_joke()
        return {"Yo Mama So...": joke['content']}, 200




#! POST ENDPOINT - Insults
    @jwt_required
    @marshal_with(POST_fields, skip_none=True)
    @api.doc(model=POST_fields, parser=POST_parsers)
    @api.expect(POST_parsers)
    @api.response(200, "Insult Added")
    @api.response(401, "Unauthorized")
    @api.response(403, "Banned User")
    @api.response(400, "Bad Request")
    def post(self):
        identity = verify_jwt_in_request(locations=["headers"])
        if identity is not None:
            claims = get_jwt()
            user = User.objects.get(id=claims["id"])
            banned = GateKeeper.is_user_banned(user["email"])
            try:
                if not banned:
                    content = request.get("content")
                    category = request.json["category"]
                    explict = request.get["explicit"]
                    date = str(now.to_datetime_string())
                    Insult(
                        content=content, explict=explict, added_on=date, added_by=user
                    ).save()
                    insult = Insult.objects.all()
                    return {"Status": "Insult Added"}, 201
            except BannedUserError:
                raise UnauthorizedError(
                    "Adding this content is not allow, the user has been banned"
                )
        else:
            raise InvaildTokenError()

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
