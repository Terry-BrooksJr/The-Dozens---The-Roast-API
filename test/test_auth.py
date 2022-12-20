from unittest import TestCase
import json
import pytest

from app import app
from database.db import db
from database.models import User


class LoginApiTest(TestCase):
    def SetUp(self):
        self.app = app.test_client()
        self.db = app.get_db()

    def test_successful_signup(self):
        test_user = User(email="Pytest_User@gmail.com", password="Butter_Baby", joined_on="1970-01-01" )
        test_user.hash_password()
        test_user.save()
        
        assert user_found = User.objects.get(email="Pytest_User@gmail.com")


        def tearDown(self):
            test_user = User.objects.get(email="Pytest_User@gmail.com")
            test_user.objects().delete()

            with pytest.raises(user.DoesNotExist):
                User.objects.get(email="Pytest_User@gmail.com")