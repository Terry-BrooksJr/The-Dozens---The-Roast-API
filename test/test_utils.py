from unittest import TestCase

from pytest_check import check

from utils.errors import (
    BannedUserError,
    EmailAlreadyExistsError,
    InternalServerError,
    SchemaValidationError,
    UnauthorizedError,
    UserDoesNotExist,
    ValidationError,
    errors,
)
from utils.gatekeeper import GateKeeper


class TestGatekeeper(TestCase):
    def test_check_if_token_is_revoked(self):
        # Gatekeeper.check_if_token_is_revoked()
        pass


class TestErrors(TestCase):
    pass
