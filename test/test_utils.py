from unittest import TestCase
from pytest_check import check

from utils.gatekeeper import GateKeeper
from utils.errors import (
    SchemaValidationError,
    BannedUserError,
    EmailAlreadyExistsError,
    UnauthorizedError,
    UserDoesNotExist,
    ValidationError,
    EmailAlreadyExistsError,
    UserDoesNotExist,
    ValidationError,
    InternalServerError,
    errors,
)


class TestGatekeeper(TestCase):
    def test_check_if_token_is_revoked(self):
        # Gatekeeper.check_if_token_is_revoked()
        pass


class TestErrors(TestCase):
    pass

