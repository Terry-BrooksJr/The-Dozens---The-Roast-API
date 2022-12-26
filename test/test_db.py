import unittest
from os import getenv
from unittest import TestCase

import pytest
from mongoengine import connect
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pytest_check import check

CONNECTION_STRING = getenv("MONGO_URI")
client = MongoClient(CONNECTION_STRING)
mongoengine_connection = connect(CONNECTION_STRING)
database = client["InsultVault"]
insult_collection = database["insults"]
user_collections = database["users"]
pipeline = {"$count": "ObjectId"}


class Test_DatabasConnection(TestCase):
    def test_database_connection(self):
        with check:
            assert isinstance(database, Database)

    def test_insult_connection(self):
        with check:
            insult_count = database.insults
            assert isinstance(insult_count, Collection)
            # assert  insult_count > 0

    def test_user_connection(self):
        with check:
            user_count = database.users
            assert isinstance(user_count, Collection)
            # assert database.user_collections.count() >= 1
