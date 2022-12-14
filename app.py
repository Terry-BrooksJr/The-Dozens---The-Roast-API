from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


initialize_db(app)
initialize_routes(api)

app.run()
