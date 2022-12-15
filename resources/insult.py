import pendulum
from flask import copy_current_request_context
from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse, fields
from utils.parser import parse_params
from utils.arguments import Argument
from utils.gatekeeper import GateKeeper
from database.models import Insult
from utils.errors import errors, SchemaValidationError

now = pendulum.now()
parser = reqparse.RequestParser()
gatekeeper = GateKeeper()

# class InsultRequest(Argument):
#     def __init__(self):
#         self.nsfw = Argument(name="nsfw",required=False, type=bool, location=['headers','values'], help="The 'nsfw/explict key denoted jokes that are not suitable for work or children",nullable=True )
#         self.category = Argument(name="category",required=False, type=str, location=['headers','values'], help="The 'category' key allows users to specifiy the type of Yo Mama joke the would like. (i.e. Fat, Stuoid, etc.)",choices=['fat','skinny,','old','short', 'tall', 'poor','stupid','ugly','hairy', 'bald', 'lazy', 'snowflake'],nullable=True )
    
#     def get_nsfw_setting(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument(self.nsfw)
#         args = parser.parse_args()
#         return args

    
#     def get_catagory_preference(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument(self.category)
#         args = parser.parse_args(strict=True)
#         return args
    
    # def get_arguments(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument(self.nsfw)
    #     parser.add_argument(self.category)
    #     args = parser.parse_args()
    #     nsfw_setting = arg['nsfw']
    #     catagory_setting = args['category']
    #     return (nsfw_setting, catagory_setting)
# response = InsultRequest()

class InsultsAPI(Resource):
    def __init__(self):
        self.PARAMS = {
                'GET': {
        'nsfw': {
            'type': bool,
            'default': None,
            'validators': [
            ],
            'locations': ['args','headers'],
            'required': False,
        },
        'category': {
            'type': str,
            'default': None,
            'validators': [
            ],
            'locations': ['args','headers'],
            'required': False,
        }
            },
            'POST': {
                'content': {
                    'type': str,
                    'vaildators': [
                    ],
                    'locations': ['json'],
                    'required': True
                }
            }
        }

    def get(self):
        params = parse_params(self.PARAMS['GET'])
        nsfw_setting = params['nsfw']
        catagory_selection = params['catagory']
        fields.Boolean.format(nsfw_setting)
        print(type(nsfw_setting))
        
        #Conditiomal to Handle of Only NSFW hearder passed
        if type(nsfw_setting) is not None:
            try:
                nsfw_set_pipeline = [{
                '$match': {
                    'nsfw/explict': nsfw_setting
                }
            }, {
                '$sample': {
                    'size': 1
                }
            }]
                insult = Insult.objects().aggregate(pipeline)
                nsfw_filtered_insult = str()
                for doc in insult:
                    nsfw_filtered_insult = doc["content"]
                return {"Yo Mama So...": nsfw_filtered_insult}, 200
            except Exception:
                raise SchemaValidationError(errors['SchemaValidationError'])
        # Conditional to Handle if Both GET Paraks Are Passed 
        elif type(nsfw_setting) is not None and type(catagory_selection) is not None:
            nsfw_and_cat_set_pipeline = [
        {
            '$match': {
                'category': catagory_selection , 
                'nsfw/explict': nsfw_setting
            }
        }, {
            '$sample': {
                'size': 1
            }
        }
    ]
            insult = Insult.objects().aggregate(nsfw_and_cat_set_pipeline)
            filtered_by_cat_and_nsfw_insult = str()
            for doc in insult:
                filtered_by_cat_and_nsfw_insult = doc['content']
            return {"Yo Mama So...": filtered_by_cat_and_nsfw_insult}, 200
        #Conditional to Handle if only Catagory is set
        if type(catagory_selection) is not None: 
            catagory_selection_only_pipeline  = [
            {
                '$match': {
                    'category': catagory_selection , 
                }
            }, {
                '$sample': {
                    'size': 1
                }
            }
        ]
            insult = Insult.objects().aggregate(catagory_selection_only_pipeline)
            catagory_selection_insult = str()
            for doc in insult:
                catagory_selection_insult = doc['content'] 
            return {"Yo Mama So...": catagory_selection_insult}, 200
        else: 
            pipeline = [{"$sample": {"size": 1}}]
            insult = Insult.objects().aggregate(pipeline)
            non_filtered_insult = str()
            for doc in insult:
                non_filtered_insult = doc["content"]
            return {"Yo Mama So...": non_filtered_insult}, 200

    @jwt_required
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
                return {'Not Authorized': "The Token Provided has Expired or Has been Revoked!"}, 401
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