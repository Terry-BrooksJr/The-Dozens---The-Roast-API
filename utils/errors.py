
class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class BannedUserError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class ValidationError(Exception):
    pass


class InvaildTokenError(Exception):
    pass


class DBConnectionError(Exception):
    pass


class ResourceNotDFoundError(Exception):
    pass

class BannedUserError(Exception):
    pass
errors = {
    "InternalServerError": {"message": "Something went wrong", "status": 500},
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400,
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 409,
    },
    "UnauthorizedError": {"message": "Invalid password", "status": 401},
    "UserDoesNotExist": {
        "message": "The email provided is not registered to contriubute to the API. Please use the `/signup` endpoint, then re-attempt this request",
        "status": 401,
    },
}
