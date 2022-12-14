import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.getenv(key="SECRET_KEY")
    MONGODB_DEV_SETTINGS = {
        "host": os.getenv('MONGODB_URI')
    }
