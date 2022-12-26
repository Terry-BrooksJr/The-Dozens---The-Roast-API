from logging import FileHandler, WARNING
from flask import current_app
from flask.logging import default_handler
from config import Config

if not current_app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setLevel(WARNING)