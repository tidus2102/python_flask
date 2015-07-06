import json
from flask.ext.restful import Resource
from app.utils.api import validators
from flask.ext.babelex import gettext


class ResponseStatus:
    INVALID_REQUEST = "invalid_request"
    INVALID_METHOD = "invalid_method"
    UNAUTHENTICATION = "unauthentication"
    NOT_FOUND = "not_found"
    WRONG_USERNAME_OR_PASSWORD = "wrong_username_or_password"
    VALIDATION = "validation_error"

    RESP_OK = 200
    RESP_BAD = 400


class ApiInfo:
    def __init__(self):
        pass

    VERSION = "1.0"
    URI_BASE = "/api"
    URI_V1 = "/api/v1.0"


class ApiError(Exception):
    def __init__(self, message, status=ResponseStatus.VALIDATION, data=None, httpStatus=ResponseStatus.RESP_BAD):
        Exception.__init__(self, message)
        self.message = message
        self.status = status
        self.data = data
        self.httpStatus = httpStatus


class ApiResource(Resource):
    postParser = None
    getParser = None
    putParser = None
    deleteParser = None


class ApiValidation:
    def __init__(self):
        pass

    @staticmethod
    def email(value):
        r, message = validators.email(value)
        if not r:
            raise ValueError(message)
        return value

    @staticmethod
    def datetime(value):
        r, message = validators.datetime(value)
        if not r:
            raise ValueError(message)
        return message


    @staticmethod
    def json(value, attr):
        try:
            json.loads(value)
            return value
        except Exception:
            raise ValueError(gettext("%(field)s VALIDATION_INVALID_JSON_ERROR", field=attr))


    @staticmethod
    def checkPlatformList(value, attr):
        platforms = [u"ios", u"android", u"windows"]
        if not value in platforms:
            raise ValueError(gettext("%(field)s VALIDATION_INVALID_ENUM_ERROR", field=attr))
        return value