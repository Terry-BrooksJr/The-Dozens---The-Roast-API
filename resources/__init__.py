from flask_restx import Api

from utils.errors import (
    BannedUserError,
    EmailAlreadyExistsError,
    InternalServerError,
    InvaildTokenError,
    UnauthorizedError,
    UserDoesNotExist,
    ValidationError,
    errors,
)

from .auth import api as AuthNS
from .insult import api as InsultNS

api = Api(
    errors=errors,
    version="1.0",
    title="Yo Mama - The Roast API",
    description="The dozens is a game of verbal combat, played mostly by African Americans on street corners, in barbershops, wherever. It is designed to teach participants to maintain control and keep cool under adverse circumstances.",
)

api.add_namespace(AuthNS, "/")
api.add_namespace(InsultNS, "/")


@api.errorhandler(Exception)
def handle_root_exception(error):
    """Return a custom message and 400 status code"""
    return {
        "Yo So Stupid": "You can't even make a vaild HTTP request. But Seriousaly, our servers don't know what the fuck to do with that request. "
    }, 400


@api.errorhandler(EmailAlreadyExistsError)
def EmailAlreadyExistsError(error):
    """Return a custom message and 409 status code"""
    return {
        "message": " Thieves never prosper!User with given email address already exists",
        "status": 409,
    }


@api.errorhandler(UserDoesNotExist)
def UserDoesNotExist(error):
    """Return a custom message and 401 status code"""
    return {
        "message": "The email provided is not registered to contriubute to the API. Please use the `/signup` endpoint, then re-attempt this request",
        "status": 401,
    }


@api.errorhandler(UnauthorizedError)
def ValidationError(error):
    """Return a custom message and 400 status code"""
    return {"message": "Please Check the Password and re-attempt that request"}


@api.errorhandler(BannedUserError)
def BannedUserError(error):
    """Return a custom message and 401 status code"""
    return {"message": "Sucks to be your! Your persona non gratia. Now, git!"}


@api.errorhandler(InternalServerError)
def InternalServerError(error):
    """Return a custom message and 400 status code"""
    return {
        "message": "We Stupid, We can't even keep the sever up and running. Sorry, Internal Sercver Error. Reload"
    }, 500


@api.errorhandler(InvaildTokenError)
def InvaildTokenError(error):
    """Return a custom message and 400 status code"""
    return {
        "message": "I know you hear this often but \"That's Not Good Enough...That token has been reovoked."
    }
