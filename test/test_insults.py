import json
from unittest import TestCase

from pytest_check import check

from app import app
from database.db import db
from database.models import Insult
from utils.jokester import Jokester


class InsultApiTest(TestCase):
    def test_get_random_joke(self):
        with check:
            joke = Jokester.get_random_joke()

    def test_get_censored_joke(self):
        pass

    def get_categorized_joke(self):
        pass
