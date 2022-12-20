from flask import Flask
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from flask_restful import Api
import utils
from resources.routes import initialize_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app, errors=utils.errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["BUNDLE_ERRORS"] = True
app.config["MONGODB_SETTINGS"] = {"host": os.getenv("MONGODB_URI")}
initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(host="localhost", port=6969, debug=True)
