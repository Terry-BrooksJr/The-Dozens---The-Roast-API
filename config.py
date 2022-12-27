import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.getenv(key="SECRET_KEY")
    MONGODB_DEV_SETTINGS = {"host": os.getenv("MONGODB_URI"), "alias": "default"}
    BUNDLE_ERROR = True
    ENV = ("Development",)
    JWT_TOKEN_LOCATION = ("headers",)
    JWT_HEADER_NAME = ("Authorization",)
    JWT_SECRET_KEY = (os.getenv("JWT_SECRET_KEY"),)
    SECRET_KEY = os.getenv("SECRET_KEY")
