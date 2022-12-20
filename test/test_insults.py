from unittest import TestCase
import json
import pytest

from app import app
from database.db import db
from database.models import Insult
from utils.jokester import get_cends

class InsultApiTest(TestCase):
    def test_get_censored_joke():
        