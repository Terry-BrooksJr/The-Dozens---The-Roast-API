import unittest
from os import getenv
from unittest import TestCase

from mongoengine import connect
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pytest_check import check

from database.models import Insult, User

CONNECTION_STRING = getenv("MONGODB_URI")
client = MongoClient(CONNECTION_STRING)
mongoengine_connection = connect(alias="Mongo_Test_Connection", host=CONNECTION_STRING)
database = client["InsultVault"]
insult_collection = database["insults"]
user_collections = database["users"]
pipeline = {"$count": "ObjectId"}


def connection_test():
    db_heartbeat = client.admin.command("ping")
    if isinstance(db_heartbeat, dict):
        if "ok" in db_heartbeat.keys():
            return "Database is connected"
        else:  
            raise ConnectionFailure("Database is not connected")


class Test_DatabasConnection(TestCase):
    def test_database_connection(self):
        db_heartbeat = client.admin.command("ping")
        with check:
            assert "ok" in db_heartbeat.keys()
            assert isinstance(db_heartbeat, dict)

    def test_database_health(self):
        with check:
            assert isinstance(database, Database)

    def test_insult_connection(self):
        with check:
            insult = database.insults
            insult_count = Insult.objects().count()
            print(insult_count)
            assert isinstance(insult, Collection)
            assert insult_count > 0

    def test_user_connection(self):
        with check:
            user = database.users
            user_count = User.objects().count()
            assert isinstance(user, Collection)
            assert user_count >= 1


try:
    print(connection_test())
except pymongo.errors.ServerSelectionTimeoutError():
    raise ConnectionFailure("Database is not connected")
