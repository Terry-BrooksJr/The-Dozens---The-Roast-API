"""
This is the main entry point of the application. It is responsible for initializing the Flask app, the database, the API, and the routes.
"""
import os
from logging import WARNING, FileHandler

from flask import Flask
from flask.logging import default_handler
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

import utils
from config import Config
from database.db import initialize_db
from resources import api
from resources.routes import initialize_routes

#!SECTION Instantaites the Flask app
app = Flask(__name__)
app.config.from_object(Config)

#!SECTION Initialize the API Endpoints and Plugins
api.init_app(app)
initialize_db(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

#!SECTION Server Error Logging
if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)


if __name__ == "__main__":
    app.run(host="localhost", port=6969, debug=True)
